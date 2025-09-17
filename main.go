package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

var (
	speed    int
	running  bool
	stopChan chan bool
)

var rootCmd = &cobra.Command{
	Use:   "fan",
	Short: "CLI приложение с анимированным вентилятором",
	Long:  "Интерактивное CLI приложение с анимированным вентилятором в терминале",
}

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Запустить вентилятор",
	Run: func(cmd *cobra.Command, args []string) {
		startFan()
	},
}

var stopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Остановить вентилятор",
	Run: func(cmd *cobra.Command, args []string) {
		stopFan()
	},
}

var speedCmd = &cobra.Command{
	Use:   "speed [1-10]",
	Short: "Установить скорость вентилятора (1-10)",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		setSpeed(args[0])
	},
}

func main() {
	rootCmd.AddCommand(startCmd, stopCmd, speedCmd)

	startCmd.Flags().IntVarP(&speed, "speed", "s", 8, "Скорость вентилятора (1-10)")

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func startFan() {
	if running {
		fmt.Println("Вентилятор уже запущен!")
		return
	}

	running = true
	stopChan = make(chan bool)

	fmt.Println("🌀 Вентилятор запущен! Нажмите Ctrl+C для остановки")

	go animateFan()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	select {
	case <-c:
		stopFan()
	case <-stopChan:
	}
}

func stopFan() {
	if !running {
		fmt.Println("Вентилятор уже остановлен!")
		return
	}

	running = false
	if stopChan != nil {
		close(stopChan)
	}

	fmt.Println("\n🛑 Вентилятор остановлен!")
}

func setSpeed(speedStr string) {
	var newSpeed int
	if _, err := fmt.Sscanf(speedStr, "%d", &newSpeed); err != nil {
		fmt.Println("Ошибка: скорость должна быть числом от 1 до 10")
		return
	}

	if newSpeed < 1 || newSpeed > 10 {
		fmt.Println("Ошибка: скорость должна быть от 1 до 10")
		return
	}

	speed = newSpeed
	fmt.Printf("Скорость установлена: %d/10\n", speed)
}

func animateFan() {
	frames := []string{
		`    ╭─────╮
    │ ╱ ╲  │
    │╱   ╲ │
    │     ╲│
    ╰─────╯`,
		`    ╭─────╮
    │  ╱ ╲ │
    │ ╱   ╲│
    │╱     │
    ╰─────╯`,
		`    ╭─────╮
    │   ╱ ╲│
    │  ╱   │
    │ ╱    │
    ╰─────╯`,
		`    ╭─────╮
    │    ╱ │
    │   ╱  │
    │  ╱   │
    ╰─────╯`,
		`    ╭─────╮
    │     │╱
    │    ╱ │
    │   ╱  │
    ╰─────╯`,
		`    ╭─────╮
    │╲     │
    │ ╲    │
    │  ╲   │
    ╰─────╯`,
		`    ╭─────╮
    │ ╲    │
    │  ╲   │
    │   ╲  │
    ╰─────╯`,
		`    ╭─────╮
    │  ╲   │
    │   ╲  │
    │    ╲ │
    ╰─────╯`,
		`    ╭─────╮
    │   ╲  │
    │    ╲ │
    │     ╲│
    ╰─────╯`,
		`    ╭─────╮
    │    ╲ │
    │     │╲
    │     │ ╲
    ╰─────╯`,
		`    ╭─────╮
    │     │
    │     │
    │     │
    ╰─────╯`,
		`    ╭─────╮
    │     │
    │     │
    │     │
    ╰─────╯`,
	}

	frameIndex := 0
	delay := time.Duration(200-speed*15) * time.Millisecond

	for running {
		select {
		case <-stopChan:
			return
		default:
			clearScreen()

			cyan := color.New(color.FgCyan).SprintFunc()
			yellow := color.New(color.FgYellow).SprintFunc()

			fmt.Println(cyan("╔══════════════════════════════════════╗"))
			fmt.Println(cyan("║") + yellow("           ВЕНТИЛЯТОР CLI           ") + cyan("║"))
			fmt.Println(cyan("╚══════════════════════════════════════╝"))
			fmt.Println()

			fmt.Println(frames[frameIndex])
			fmt.Println()

			green := color.New(color.FgGreen).SprintFunc()
			fmt.Printf("Скорость: %s/10\n", green(speed))

			red := color.New(color.FgRed).SprintFunc()
			fmt.Printf("Статус: %s\n", red("ВРАЩАЕТСЯ"))
			fmt.Println()
			fmt.Println("Нажмите Ctrl+C для остановки")

			frameIndex = (frameIndex + 1) % len(frames)
			time.Sleep(delay)
		}
	}
}

func clearScreen() {
	fmt.Print("\033[2J\033[H")
}
