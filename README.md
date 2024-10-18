$$
\begin{pmatrix}
x' \\
y' \\
1
\end{pmatrix}
=
\begin{pmatrix}
a & b & t_x \\
c & d & t_y \\
0 & 0 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
x \\
y \\
1
\end{pmatrix}

$$



```go
package main

import (
	"image/color"
	"log"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth  = 320
	screenHeight = 640
	tileSize     = 32
	boardWidth   = 10
	boardHeight  = 20
	moveDelay    = 5  // Задержка для перемещения
	rotateDelay  = 15 // Задержка для вращения
)

var tetrominoes = [][][]int{
	{
		{1, 1, 1, 1}, // I
	},
	{
		{1, 1, 1},
		{0, 1, 0}, // T
	},
	{
		{1, 1},
		{1, 1}, // O
	},
	{
		{1, 1, 0},
		{0, 1, 1}, // Z
	},
	{
		{0, 1, 1},
		{1, 1, 0}, // S
	},
	{
		{1, 1, 1},
		{1, 0, 0}, // L
	},
	{
		{1, 1, 1},
		{0, 0, 1}, // J
	},
}

// Цвета для каждого типа тетромино
var tetrominoColors = []color.RGBA{
	{0, 255, 255, 255}, // I - голубой
	{255, 0, 255, 255}, // T - пурпурный
	{255, 255, 0, 255}, // O - желтый
	{255, 0, 0, 255},   // Z - красный
	{0, 255, 0, 255},   // S - зеленый
	{255, 165, 0, 255}, // L - оранжевый
	{0, 0, 255, 255},   // J - синий
}

type Game struct {
	board                  [][]int
	currentTetromino       [][]int
	currentColor           color.RGBA
	tetrominoX, tetrominoY int
	frameCount             int
	moveTimer              int
	rotateTimer            int
	movePressed            bool // Отслеживание состояния клавиш перемещения
	rotatePressed          bool // Отслеживание состояния клавиш вращения
	score                  int  // Счет игрока
	linesCleared           int  // Количество убранных линий
}

func (g *Game) Init() {
	g.board = make([][]int, boardHeight)
	for i := range g.board {
		g.board[i] = make([]int, boardWidth)
	}
	g.spawnTetromino()
}

func (g *Game) spawnTetromino() {
	rand.Seed(time.Now().UnixNano())
	index := rand.Intn(len(tetrominoes))
	g.currentTetromino = tetrominoes[index]
	g.currentColor = tetrominoColors[index] // Установка цвета тетромино
	g.tetrominoX = boardWidth/2 - len(g.currentTetromino[0])/2
	g.tetrominoY = 0

	// Проверка на проигрыш
	if !g.canMove(g.tetrominoX, g.tetrominoY, g.currentTetromino) {
		g.gameOver()
	}
}

func (g *Game) gameOver() {
	log.Println("Game Over! Final Score:", g.score)
	ebiten.SetCursorMode(ebiten.CursorModeHidden) // Показываем курсор при проигрыше
	ebiten.SetWindowTitle("Game Over")
}

func (g *Game) Update() error {
	g.frameCount++
	g.moveTimer++
	g.rotateTimer++

	if g.frameCount%30 == 0 { // Замедление падения
		if !g.moveTetromino(0, 1) {
			g.mergeTetromino()
			linesCleared := g.clearLines()
			g.updateScore(linesCleared)
			g.spawnTetromino()
		}
	}

	// Управление перемещением
	if !g.movePressed {
		if ebiten.IsKeyPressed(ebiten.KeyLeft) && g.moveTimer >= moveDelay {
			g.moveTetromino(-1, 0)
			g.moveTimer = 0
			g.movePressed = true
		}
		if ebiten.IsKeyPressed(ebiten.KeyRight) && g.moveTimer >= moveDelay {
			g.moveTetromino(1, 0)
			g.moveTimer = 0
			g.movePressed = true
		}
	}
	if ebiten.IsKeyPressed(ebiten.KeyDown) && g.moveTimer >= moveDelay {
		g.moveTetromino(0, 1)
		g.moveTimer = 0
	}

	if !g.rotatePressed {
		if ebiten.IsKeyPressed(ebiten.KeySpace) && g.rotateTimer >= rotateDelay {
			g.rotateTetromino()
			g.rotateTimer = 0
			g.rotatePressed = true
		}
	}

	// Обработка отпускания клавиш для одиночных действий
	if !ebiten.IsKeyPressed(ebiten.KeyLeft) && !ebiten.IsKeyPressed(ebiten.KeyRight) {
		g.movePressed = false
	}
	if !ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.rotatePressed = false
	}

	return nil
}

func (g *Game) moveTetromino(dx, dy int) bool {
	newX, newY := g.tetrominoX+dx, g.tetrominoY+dy
	if g.canMove(newX, newY, g.currentTetromino) {
		g.tetrominoX = newX
		g.tetrominoY = newY
		return true
	}
	return false
}

func (g *Game) canMove(x, y int, tetromino [][]int) bool {
	for i, row := range tetromino {
		for j, cell := range row {
			if cell == 1 {
				if x+j < 0 || x+j >= boardWidth || y+i >= boardHeight || (y+i >= 0 && g.board[y+i][x+j] == 1) {
					return false
				}
			}
		}
	}
	return true
}

func (g *Game) mergeTetromino() {
	for i, row := range g.currentTetromino {
		for j, cell := range row {
			if cell == 1 && g.tetrominoY+i >= 0 {
				g.board[g.tetrominoY+i][g.tetrominoX+j] = 1
			}
		}
	}
}

func (g *Game) clearLines() int {
	linesCleared := 0
	for i := 0; i < boardHeight; i++ {
		full := true
		for j := 0; j < boardWidth; j++ {
			if g.board[i][j] == 0 {
				full = false
				break
			}
		}
		if full {
			linesCleared++
			g.board = append(g.board[:i], g.board[i+1:]...)
			newLine := make([]int, boardWidth)
			g.board = append([][]int{newLine}, g.board...)
		}
	}
	return linesCleared
}

func (g *Game) updateScore(linesCleared int) {
	if linesCleared > 0 {
		g.linesCleared += linesCleared
		g.score += linesCleared * linesCleared * 100 // Множитель очков
	}
}

func (g *Game) rotateTetromino() {
	newTetromino := rotateMatrix(g.currentTetromino)
	if g.canMove(g.tetrominoX, g.tetrominoY, newTetromino) {
		g.currentTetromino = newTetromino
	}
}

func rotateMatrix(matrix [][]int) [][]int {
	n := len(matrix)
	m := len(matrix[0])
	newMatrix := make([][]int, m)
	for i := range newMatrix {
		newMatrix[i] = make([]int, n)
		for j := range newMatrix[i] {
			newMatrix[i][j] = matrix[n-j-1][i]
		}
	}
	return newMatrix
}

func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(color.RGBA{0, 0, 0, 255})

	// Рисуем сетку между блоками
	for i := 0; i <= boardWidth; i++ {
		ebitenutil.DrawLine(screen, float64(i*tileSize), 0, float64(i*tileSize), float64(screenHeight), color.RGBA{27, 27, 27, 65}) // Вертикальные линии
	}
	for i := 0; i <= boardHeight; i++ {
		ebitenutil.DrawLine(screen, 0, float64(i*tileSize), float64(screenWidth), float64(i*tileSize), color.RGBA{27, 27, 27, 65}) // Горизонтальные линии
	}

	// Рисуем игровое поле
	for i, row := range g.board {
		for j, cell := range row {
			if cell == 1 {
				ebitenutil.DrawRect(screen, float64(j*tileSize), float64(i*tileSize), float64(tileSize), float64(tileSize), g.currentColor)
			}
		}
	}

	// Рисуем текущий тетромино
	for i, row := range g.currentTetromino {
		for j, cell := range row {
			if cell == 1 {
				ebitenutil.DrawRect(screen, float64((g.tetrominoX+j)*tileSize), float64((g.tetrominoY+i)*tileSize), float64(tileSize), float64(tileSize), g.currentColor)
			}
		}
	}

	// Рисуем счет
	ebitenutil.DebugPrint(screen, "Score: "+string(g.score))
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func main() {
	game := &Game{}
	game.Init()

	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Tetris")

	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}


```