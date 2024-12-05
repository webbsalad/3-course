package main

import (
	"bytes"
	"embed"
	"encoding/json"
	"image/color"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/go-mp3"

	"github.com/hajimehoshi/oto"
)

const (
	screenWidth  = 800
	screenHeight = 600
)

var (
	colorYellow = color.RGBA{R: 255, G: 255, B: 0, A: 255}
	colorGreen  = color.RGBA{R: 0, G: 255, B: 0, A: 255}
)

//go:embed static/sounds/*
var sounds embed.FS

type Game struct {
	shipX          float64
	bullets        []bullet
	aliens         []alien
	alienDirX      float64
	gameOver       bool
	lastShotTime   time.Time
	shootCooldown  time.Duration
	alienSpawnTime time.Time
	alienSpawnRate time.Duration
	audioContext   *oto.Context
	level          int
	score          int
	lives          int
}

type bullet struct {
	x, y float64
}

type alien struct {
	x, y float64
}

type gameData struct {
	Level int `json:"level"`
	Score int `json:"score"`
	Lives int `json:"lives"`
}

func (g *Game) playSound(fileName string) {
	data, err := sounds.ReadFile(fileName)
	if err != nil {
		log.Printf("Error reading sound: %v\n", err)
		return
	}

	decoder, err := mp3.NewDecoder(bytes.NewReader(data))
	if err != nil {
		log.Printf("Error decoding MP3: %v\n", err)
		return
	}

	player := g.audioContext.NewPlayer()
	defer player.Close()

	buf := make([]byte, 4096)
	for {
		n, err := decoder.Read(buf)
		if err != nil {
			break
		}
		player.Write(buf[:n])
	}
}

func (g *Game) saveGame() {
	data := gameData{
		Level: g.level,
		Score: g.score,
		Lives: g.lives,
	}
	file, err := os.Create("savegame.json")
	if err != nil {
		log.Printf("Error saving game: %v\n", err)
		return
	}
	defer file.Close()

	jsonData, err := json.Marshal(data)
	if err != nil {
		log.Printf("Error serializing game data: %v\n", err)
		return
	}

	file.Write(jsonData)
	log.Println("Game saved!")
}

func (g *Game) loadGame() {
	file, err := os.Open("savegame.json")
	if err != nil {
		log.Printf("Error loading game: %v\n", err)
		return
	}
	defer file.Close()

	data, err := ioutil.ReadAll(file)
	if err != nil {
		log.Printf("Error reading game data: %v\n", err)
		return
	}

	var loadedData gameData
	err = json.Unmarshal(data, &loadedData)
	if err != nil {
		log.Printf("Error deserializing game data: %v\n", err)
		return
	}

	g.level = loadedData.Level
	g.score = loadedData.Score
	g.lives = loadedData.Lives
	log.Println("Game loaded!")
}

func (g *Game) Update() error {
	if g.gameOver {
		return nil
	}

	if ebiten.IsKeyPressed(ebiten.KeyLeft) && g.shipX > 0 {
		g.shipX -= 5
	}
	if ebiten.IsKeyPressed(ebiten.KeyRight) && g.shipX < screenWidth-20 {
		g.shipX += 5
	}

	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		if time.Since(g.lastShotTime) >= g.shootCooldown {
			g.bullets = append(g.bullets, bullet{x: g.shipX + 10, y: screenHeight - 40})
			g.lastShotTime = time.Now()
			go g.playSound("static/sounds/shot.mp3")
		}
	}

	if ebiten.IsKeyPressed(ebiten.KeyS) {
		g.saveGame()
	}
	if ebiten.IsKeyPressed(ebiten.KeyL) {
		g.loadGame()
	}

	for i := 0; i < len(g.bullets); i++ {
		g.bullets[i].y -= 5
		if g.bullets[i].y < 0 {
			g.bullets = append(g.bullets[:i], g.bullets[i+1:]...)
			i--
		}
	}

	edgeReached := false
	for i := 0; i < len(g.aliens); i++ {
		g.aliens[i].x += g.alienDirX
		if g.aliens[i].x > screenWidth-20 || g.aliens[i].x < 0 {
			edgeReached = true
		}

		if g.aliens[i].y > screenHeight-60 && g.aliens[i].x >= g.shipX && g.aliens[i].x <= g.shipX+20 {
			g.gameOver = true
			go g.playSound("static/sounds/dead.mp3")
		}

		if g.aliens[i].y > screenHeight-20 {
			g.gameOver = true
			go g.playSound("static/sounds/dead.mp3")
		}
	}

	if edgeReached {
		g.alienDirX *= -1
		for i := 0; i < len(g.aliens); i++ {
			g.aliens[i].y += 20
		}
	}

	for i := 0; i < len(g.bullets); i++ {
		hit := false
		for j := 0; j < len(g.aliens); j++ {
			if g.bullets[i].x >= g.aliens[j].x && g.bullets[i].x <= g.aliens[j].x+20 &&
				g.bullets[i].y >= g.aliens[j].y && g.bullets[i].y <= g.aliens[j].y+20 {
				g.aliens = append(g.aliens[:j], g.aliens[j+1:]...)
				hit = true
				g.score += 10
				break
			}
		}
		if hit {
			g.bullets = append(g.bullets[:i], g.bullets[i+1:]...)
			i--
		}
	}

	if len(g.aliens) == 0 {
		g.level++
		g.alienDirX *= 1.1
		g.spawnAliens()
		g.bullets = nil
	}

	if time.Since(g.alienSpawnTime) >= g.alienSpawnRate {
		g.spawnAliens()
		g.alienSpawnTime = time.Now()
	}

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	if g.gameOver {
		ebitenutil.DebugPrint(screen, "Игра окончена!")
		return
	}

	ebitenutil.DebugPrint(screen, "Уровень: "+strconv.Itoa(g.level)+"\nОчки: "+strconv.Itoa(g.score)+"\nЖизни: "+strconv.Itoa(g.lives))
	ebitenutil.DrawRect(screen, g.shipX, screenHeight-40, 20, 20, color.White)

	for _, b := range g.bullets {
		ebitenutil.DrawRect(screen, b.x, b.y, 5, 10, colorYellow)
	}

	for _, a := range g.aliens {
		ebitenutil.DrawRect(screen, a.x, a.y, 20, 20, colorGreen)
	}
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func (g *Game) spawnAliens() {
	for j := 0; j < 11; j++ {
		g.aliens = append(g.aliens, alien{
			x: float64(50 + j*50),
			y: 0,
		})
	}
}

func main() {
	audioCtx, err := oto.NewContext(44100, 2, 2, 4096)
	if err != nil {
		log.Fatal(err)
	}

	game := &Game{
		shipX:          screenWidth / 2,
		alienDirX:      2,
		shootCooldown:  500 * time.Millisecond,
		alienSpawnRate: 5 * time.Second,
		audioContext:   audioCtx,
		level:          1,
		score:          0,
		lives:          3,
	}
	game.spawnAliens()
	game.alienSpawnTime = time.Now()

	go game.playSound("static/sounds/start.mp3")

	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Вторжение инопланетян")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
