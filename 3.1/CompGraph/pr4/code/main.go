package main

import (
	"fmt"
	"image/color"
	"log"
	"math"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth        = 640
	screenHeight       = 480
	tileSize           = 32
	playerSpeed        = 2
	enemySpeed         = 1
	attackCooldown     = 180 // 3 seconds
	attackSize         = tileSize * 2.5
	damageCooldown     = 180 // 3 seconds
	bulletSpeed        = 3
	shootCooldown      = 60  // 1 second for shooting enemies
	healRoomChance     = 1   // 10% chance for a healing cell room
	healMessageRadius  = 48  // Radius to display the healing message
	maxRoomsGeneration = 100 // Prevent infinite room generation
)

// Player represents the player entity.
type Player struct {
	X, Y          float64
	Width, Height float64
	Lives         int
	Score         int
	AttackCD      int // Cooldown for attacking
	Attacking     int
	DamageCD      int // Cooldown after taking damage
}

// Enemy represents an enemy entity.
type Enemy struct {
	X, Y          float64
	Width, Height float64
	MoveCD        int
	Shoots        bool // Can the enemy shoot
	ShootCD       int  // Cooldown for shooting
}

// Bullet represents a bullet entity.
type Bullet struct {
	X, Y   float64
	VX, VY float64
}

// Room represents a single room in the game.
type Room struct {
	X, Y         int // Coordinates of the room on the map grid
	Enemies      []*Enemy
	Bullets      []*Bullet
	Walls        map[string]bool
	HealPresent  bool    // Is there a healing cell
	HealX, HealY float64 // Coordinates of the healing cell
	Doors        map[string]bool
}

// Game represents the overall game state.
type Game struct {
	player        *Player
	currentRoom   *Room
	rooms         map[string]*Room
	gameOver      bool
	roomWidth     int
	roomHeight    int
	doorPositions map[string][2]int // Predefined door positions
}

// NewGame initializes and returns a new Game instance.
func NewGame() *Game {
	rand.Seed(time.Now().UnixNano())
	game := &Game{
		player: &Player{
			X:      screenWidth / 2,
			Y:      screenHeight / 2,
			Width:  tileSize,
			Height: tileSize,
			Lives:  3,
			Score:  0,
		},
		rooms:         make(map[string]*Room),
		roomWidth:     screenWidth,
		roomHeight:    screenHeight,
		doorPositions: predefinedDoors(),
	}

	// Create the starting room at (0,0).
	game.currentRoom = game.generateRoom(0, 0)
	return game
}

// predefinedDoors defines the door positions on each room's edges.
func predefinedDoors() map[string][2]int {
	return map[string][2]int{
		"top":    {screenWidth/2 - tileSize/2, 0},
		"bottom": {screenWidth/2 - tileSize/2, screenHeight - tileSize},
		"left":   {0, screenHeight/2 - tileSize/2},
		"right":  {screenWidth - tileSize, screenHeight/2 - tileSize/2},
	}
}

// Layout defines the screen layout.
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

// Update handles the game state updates each frame.
func (g *Game) Update() error {
	if g.gameOver {
		// Restart the game if 'R' is pressed.
		if ebiten.IsKeyPressed(ebiten.KeyR) {
			*g = *NewGame()
		}
		return nil
	}

	// Handle player movement.
	var dx, dy float64
	if ebiten.IsKeyPressed(ebiten.KeyW) {
		dy -= playerSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyS) {
		dy += playerSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyA) {
		dx -= playerSpeed
	}
	if ebiten.IsKeyPressed(ebiten.KeyD) {
		dx += playerSpeed
	}

	// Check collision before moving.
	if g.canMove(g.player.X+dx, g.player.Y+dy, g.player.Width, g.player.Height) {
		g.player.X += dx
		g.player.Y += dy
	}

	// Check room boundaries and switch rooms if necessary.
	roomChanged := false
	var switchDX, switchDY int

	if g.player.X < 0 {
		switchDX = -1
		g.player.X = screenWidth - g.player.Width
		roomChanged = true
	} else if g.player.X+g.player.Width > screenWidth {
		switchDX = 1
		g.player.X = 0
		roomChanged = true
	}
	if g.player.Y < 0 {
		switchDY = -1
		g.player.Y = screenHeight - g.player.Height
		roomChanged = true
	} else if g.player.Y+g.player.Height > screenHeight {
		switchDY = 1
		g.player.Y = 0
		roomChanged = true
	}

	if roomChanged {
		g.switchRoom(switchDX, switchDY)
	}

	// Interaction with healing cell.
	if g.currentRoom.HealPresent &&
		g.isColliding(g.player.X, g.player.Y, g.player.Width, g.player.Height, g.currentRoom.HealX, g.currentRoom.HealY, tileSize, tileSize) {
		g.player.Lives++
		g.currentRoom.HealPresent = false // Remove the healing cell after use
	}

	// Update attack cooldown.
	if g.player.AttackCD > 0 {
		g.player.AttackCD--
	}

	// Handle player attacking.
	if ebiten.IsKeyPressed(ebiten.KeySpace) && g.player.AttackCD == 0 {
		g.player.AttackCD = attackCooldown
		g.player.Attacking = 15 // Attack lasts 15 frames.
	}
	if g.player.Attacking > 0 {
		g.player.Attacking--
	}

	// Reduce damage cooldown.
	if g.player.DamageCD > 0 {
		g.player.DamageCD--
	}

	// Update enemies.
	for _, enemy := range g.currentRoom.Enemies {
		if enemy.MoveCD > 0 {
			enemy.MoveCD--
			continue
		}

		edx, edy := g.calculateEnemyMovement(enemy)
		if g.canMove(enemy.X+edx, enemy.Y+edy, enemy.Width, enemy.Height) {
			enemy.X += edx
			enemy.Y += edy
		}

		enemy.MoveCD = 10 // Enemy moves every 10 frames.

		// Check collision with player.
		if g.isColliding(g.player.X, g.player.Y, g.player.Width, g.player.Height, enemy.X, enemy.Y, enemy.Width, enemy.Height) && g.player.DamageCD == 0 {
			g.player.Lives--
			g.player.DamageCD = damageCooldown
			if g.player.Lives <= 0 {
				g.gameOver = true
			}
		}

		// Enemy shooting logic.
		if enemy.Shoots && enemy.ShootCD == 0 {
			bullet := g.createBullet(enemy)
			g.currentRoom.Bullets = append(g.currentRoom.Bullets, bullet)
			enemy.ShootCD = shootCooldown
		} else if enemy.ShootCD > 0 {
			enemy.ShootCD--
		}
	}

	// Update bullets.
	g.updateBullets()

	// Destroy enemies in attack range.
	if g.player.Attacking > 0 {
		g.destroyEnemiesInAttackRange()
	}

	return nil
}

// calculateEnemyMovement determines the movement direction for an enemy towards the player.
func (g *Game) calculateEnemyMovement(enemy *Enemy) (float64, float64) {
	var edx, edy float64
	if enemy.X < g.player.X {
		edx += enemySpeed
	} else if enemy.X > g.player.X {
		edx -= enemySpeed
	}
	if enemy.Y < g.player.Y {
		edy += enemySpeed
	} else if enemy.Y > g.player.Y {
		edy -= enemySpeed
	}
	return edx, edy
}

// createBullet initializes a new bullet directed towards the player.
func (g *Game) createBullet(enemy *Enemy) *Bullet {
	dx := g.player.X - enemy.X
	dy := g.player.Y - enemy.Y
	dist := math.Hypot(dx, dy)
	if dist == 0 {
		dist = 1
	}
	return &Bullet{
		X:  enemy.X + enemy.Width/2,
		Y:  enemy.Y + enemy.Height/2,
		VX: (dx / dist) * bulletSpeed,
		VY: (dy / dist) * bulletSpeed,
	}
}

// updateBullets updates the positions of all bullets and handles collisions.
func (g *Game) updateBullets() {
	for i := len(g.currentRoom.Bullets) - 1; i >= 0; i-- {
		bullet := g.currentRoom.Bullets[i]
		bullet.X += bullet.VX
		bullet.Y += bullet.VY

		// Remove bullet if it goes out of bounds.
		if bullet.X < 0 || bullet.Y < 0 || bullet.X > screenWidth || bullet.Y > screenHeight {
			g.currentRoom.Bullets = append(g.currentRoom.Bullets[:i], g.currentRoom.Bullets[i+1:]...)
			continue
		}

		// Check collision with player.
		if g.isColliding(g.player.X, g.player.Y, g.player.Width, g.player.Height, bullet.X, bullet.Y, 4, 4) && g.player.DamageCD == 0 {
			g.player.Lives--
			g.player.DamageCD = damageCooldown
			g.currentRoom.Bullets = append(g.currentRoom.Bullets[:i], g.currentRoom.Bullets[i+1:]...)
			if g.player.Lives <= 0 {
				g.gameOver = true
			}
		}
	}
}

// destroyEnemiesInAttackRange removes enemies within the attack range of the player.
func (g *Game) destroyEnemiesInAttackRange() {
	for i := len(g.currentRoom.Enemies) - 1; i >= 0; i-- {
		enemy := g.currentRoom.Enemies[i]
		if g.isColliding(
			g.player.X+(g.player.Width-attackSize)/2,
			g.player.Y+(g.player.Height-attackSize)/2,
			attackSize, attackSize,
			enemy.X, enemy.Y,
			enemy.Width, enemy.Height,
		) {
			g.currentRoom.Enemies = append(g.currentRoom.Enemies[:i], g.currentRoom.Enemies[i+1:]...)
			g.player.Score++
		}
	}
}

// Draw renders the game screen.
func (g *Game) Draw(screen *ebiten.Image) {
	if g.gameOver {
		ebitenutil.DebugPrint(screen, "Game Over! Press R to restart.")
		return
	}

	// Draw room floor.
	ebitenutil.DrawRect(screen, 0, 0, screenWidth, screenHeight, color.RGBA{50, 50, 50, 255})

	// Draw doors.
	for direction, pos := range g.currentRoomDoors() {
		if g.currentRoom.Doors[direction] {
			ebitenutil.DrawRect(screen,
				float64(pos[0]),
				float64(pos[1]),
				tileSize, tileSize,
				color.RGBA{200, 200, 0, 255}, // Yellow doors
			)
		}
	}

	// Draw walls.
	for wallKey := range g.currentRoom.Walls {
		coords := parseKey(wallKey)
		ebitenutil.DrawRect(screen,
			float64(coords[0]*tileSize),
			float64(coords[1]*tileSize),
			tileSize, tileSize,
			color.RGBA{100, 100, 100, 255},
		)
	}

	// Draw healing cell.
	if g.currentRoom.HealPresent {
		ebitenutil.DrawRect(screen,
			g.currentRoom.HealX,
			g.currentRoom.HealY,
			tileSize, tileSize,
			color.RGBA{0, 100, 100, 255}, // Blue healing cell
		)

		// Display healing message if player is nearby.
		if math.Hypot(g.player.X-g.currentRoom.HealX, g.player.Y-g.currentRoom.HealY) < healMessageRadius {
			ebitenutil.DebugPrintAt(screen, "Press E to heal (+1 Life)", int(g.currentRoom.HealX)+tileSize, int(g.currentRoom.HealY)-20)
		}
	}

	// Draw player.
	playerColor := color.RGBA{0, 255, 0, 255} // Green player
	if g.player.DamageCD > 0 {
		playerColor = color.RGBA{255, 255, 0, 255} // Yellow when invulnerable
	}
	ebitenutil.DrawRect(screen,
		g.player.X,
		g.player.Y,
		g.player.Width, g.player.Height,
		playerColor,
	)

	// Visualize attack.
	if g.player.Attacking > 0 {
		ebitenutil.DrawRect(screen,
			g.player.X+(g.player.Width-attackSize)/2,
			g.player.Y+(g.player.Height-attackSize)/2,
			attackSize, attackSize,
			color.RGBA{255, 255, 0, 100}, // Semi-transparent yellow
		)
	}

	// Draw enemies.
	for _, enemy := range g.currentRoom.Enemies {
		enemyColor := color.RGBA{255, 0, 0, 255} // Red for normal enemies
		if enemy.Shoots {
			enemyColor = color.RGBA{0, 0, 255, 255} // Blue for shooting enemies
		}
		ebitenutil.DrawRect(screen,
			enemy.X,
			enemy.Y,
			enemy.Width, enemy.Height,
			enemyColor,
		)
	}

	// Draw bullets.
	for _, bullet := range g.currentRoom.Bullets {
		ebitenutil.DrawRect(screen,
			bullet.X,
			bullet.Y,
			4, 4,
			color.RGBA{255, 255, 0, 255}, // Yellow bullets
		)
	}

	// Display score and lives.
	ebitenutil.DebugPrintAt(screen, fmt.Sprintf("Score: %d  Lives: %d", g.player.Score, g.player.Lives), 10, 10)

	// Optional: Display instructions
	ebitenutil.DebugPrintAt(screen, "W/A/S/D to move, SPACE to attack, R to restart", 10, screenHeight-20)
}

// currentRoomDoors returns the positions of doors based on room coordinates.
func (g *Game) currentRoomDoors() map[string][2]int {
	return g.doorPositions
}

// switchRoom handles transitioning to a new room based on direction.
func (g *Game) switchRoom(dx, dy int) {
	newX := g.currentRoom.X + dx
	newY := g.currentRoom.Y + dy
	roomKey := roomKey(newX, newY)

	if len(g.rooms) >= maxRoomsGeneration {
		log.Println("Maximum number of rooms generated. Cannot create more.")
		return
	}

	if _, exists := g.rooms[roomKey]; !exists {
		g.rooms[roomKey] = g.generateRoom(newX, newY)
	}

	g.currentRoom = g.rooms[roomKey]

	// Position the player at the corresponding door.
	switch {
	case dx == -1: // Entered from the right
		g.player.X = screenWidth - g.player.Width - tileSize
		g.player.Y = float64(screenHeight / 2)
	case dx == 1: // Entered from the left
		g.player.X = tileSize
		g.player.Y = float64(screenHeight / 2)
	case dy == -1: // Entered from the bottom
		g.player.Y = screenHeight - g.player.Height - tileSize
		g.player.X = float64(screenWidth / 2)
	case dy == 1: // Entered from the top
		g.player.Y = tileSize
		g.player.X = float64(screenWidth / 2)
	}
}

// generateRoom creates a new room with random walls, enemies, and possibly a healing cell.
func (g *Game) generateRoom(x, y int) *Room {
	room := &Room{
		X:           x,
		Y:           y,
		Enemies:     []*Enemy{},
		Bullets:     []*Bullet{},
		Walls:       make(map[string]bool),
		Doors:       make(map[string]bool),
		HealPresent: false,
	}

	// Define doors based on room position (optional: connect to existing rooms)
	// For simplicity, doors are always present on all sides.
	for direction := range g.doorPositions {
		room.Doors[direction] = true
	}

	// Add random walls, avoiding door positions.
	numWalls := rand.Intn(20) + 10
	for i := 0; i < numWalls; i++ {
		wallX := rand.Intn(screenWidth / tileSize)
		wallY := rand.Intn(screenHeight / tileSize)
		// Prevent walls where doors are
		if g.isDoorPosition(wallX, wallY, room) {
			continue
		}
		room.Walls[wallKey(wallX, wallY)] = true
	}

	// Add random enemies.
	numEnemies := rand.Intn(5) + 1
	for i := 0; i < numEnemies; i++ {
		enemyX, enemyY := g.getRandomFreePosition(room)
		if enemyX == -1 && enemyY == -1 {
			continue // No free position found
		}
		room.Enemies = append(room.Enemies, &Enemy{
			X:      float64(enemyX),
			Y:      float64(enemyY),
			Width:  tileSize,
			Height: tileSize,
			Shoots: rand.Float64() < 0.5, // 50% chance to shoot
		})
	}

	// Add a healing cell with a certain chance.
	if rand.Float64() < healRoomChance {
		healX, healY := g.getRandomFreePosition(room)
		if healX != -1 && healY != -1 {
			room.HealPresent = true
			room.HealX = float64(healX)
			room.HealY = float64(healY)
		}
	}

	return room
}

// isDoorPosition checks if the given tile coordinates correspond to a door.
func (g *Game) isDoorPosition(wallX, wallY int, room *Room) bool {
	for direction, pos := range g.doorPositions {
		if direction == "top" && wallX*tileSize == pos[0] && wallY*tileSize == pos[1] {
			return true
		}
		if direction == "bottom" && wallX*tileSize == pos[0] && wallY*tileSize == pos[1] {
			return true
		}
		if direction == "left" && wallX*tileSize == pos[0] && wallY*tileSize == pos[1] {
			return true
		}
		if direction == "right" && wallX*tileSize == pos[0] && wallY*tileSize == pos[1] {
			return true
		}
	}
	return false
}

// getRandomFreePosition finds a random position in the room that is not a wall or door.
func (g *Game) getRandomFreePosition(room *Room) (int, int) {
	maxAttempts := 100
	for attempts := 0; attempts < maxAttempts; attempts++ {
		x := rand.Intn(screenWidth/tileSize) * tileSize
		y := rand.Intn(screenHeight/tileSize) * tileSize

		// Check if the position is not a wall or a door.
		tileKey := wallKey(x/tileSize, y/tileSize)
		if room.Walls[tileKey] {
			continue
		}
		isDoor := false
		for _, pos := range g.currentRoomDoors() {
			if int(x) == pos[0] && int(y) == pos[1] {
				isDoor = true
				break
			}
		}
		if isDoor {
			continue
		}
		return x, y
	}
	return -1, -1 // No free position found
}

// canMove checks if the entity can move to the specified position without colliding with walls or room boundaries.
func (g *Game) canMove(x, y, width, height float64) bool {
	tx1, ty1 := int(x/tileSize), int(y/tileSize)
	tx2, ty2 := int((x+width)/tileSize), int((y+height)/tileSize)

	for tx := tx1; tx <= tx2; tx++ {
		for ty := ty1; ty <= ty2; ty++ {
			wallKey := wallKey(tx, ty)
			if _, isWall := g.currentRoom.Walls[wallKey]; isWall {
				return false
			}
		}
	}
	return x >= 0 && y >= 0 && x+width <= screenWidth && y+height <= screenHeight
}

// isColliding checks if two rectangles are colliding.
func (g *Game) isColliding(x1, y1, w1, h1, x2, y2, w2, h2 float64) bool {
	return x1 < x2+w2 && x1+w1 > x2 && y1 < y2+h2 && y1+h1 > y2
}

// roomKey generates a unique key for each room based on its coordinates.
func roomKey(x, y int) string {
	return fmt.Sprintf("%d,%d", x, y)
}

// wallKey generates a unique key for each wall tile based on its grid coordinates.
func wallKey(x, y int) string {
	return fmt.Sprintf("%d,%d", x, y)
}

// parseKey converts a wall or room key back to grid coordinates.
func parseKey(key string) [2]int {
	var x, y int
	fmt.Sscanf(key, "%d,%d", &x, &y)
	return [2]int{x, y}
}

// main initializes and runs the game.
func main() {
	game := NewGame()
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Rogue-Like with Shooting Enemies and Healing Rooms")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
