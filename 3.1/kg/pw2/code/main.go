package main

import (
	"fmt"
	"math"
)

// Векторная структура
type Vector struct {
	x, y, z float64
}

// Скалярное произведение двух векторов
func dotProduct(v1, v2 Vector) float64 {
	return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
}

// Нормализация вектора
func normalize(v Vector) Vector {
	magnitude := math.Sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
	return Vector{v.x / magnitude, v.y / magnitude, v.z / magnitude}
}

// Построение вектора отражения
func reflect(L, n Vector) Vector {
	scale := 2 * dotProduct(L, n)
	return Vector{
		x: scale*n.x - L.x,
		y: scale*n.y - L.y,
		z: scale*n.z - L.z,
	}
}

func main() {
	// Входные данные
	n := Vector{0, 1, 0}                             // Нормаль
	L := Vector{-1, 2, -1}                           // Вектор света
	S := Vector{1, 1.5, 0.5}                         // Вектор наблюдателя
	ka, kd, ks, Ia, Il := 0.15, 0.15, 0.8, 1.0, 10.0 // Коэффициенты и интенсивности
	K, d, nShine := 1.0, 0.0, 5.0                    // Параметры сцены

	// Нормализация векторов
	L = normalize(L)
	S = normalize(S)
	n = normalize(n)

	// Углы и их косинусы
	cosTheta := dotProduct(n, L)
	if cosTheta < 0 {
		cosTheta = 0 // Свет позади объекта
	}

	R := reflect(L, n) // Вектор отражения
	cosAlpha := dotProduct(R, S)
	if cosAlpha < 0 {
		cosAlpha = 0 // Углы больше 90° не учитываются
	}

	// Вычисление интенсивности
	I := Ia*ka + (Il/(d+K))*(kd*cosTheta+ks*math.Pow(cosAlpha, nShine))

	// Вывод результата
	fmt.Printf("Интенсивность света в точке: %.2f\n", I)
}
