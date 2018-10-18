package main

import (
	"image"
	"image/color"
	"image/png"
	"math/rand"
	"os"
)

func draw() {
	width := 512
	height := 512

	upLeft := image.Point{0, 0}
	lowRight := image.Point{width, height}

	img := image.NewRGBA(image.Rectangle{upLeft, lowRight})

	// Set color for each pixel.
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			img.Set(x, y, color.RGBA{
				uint8(rand.Intn(255)), //R
				uint8(rand.Intn(255)), //G
				uint8(rand.Intn(255)), //B
				0xff})                 //Alpha
		}
	}

	// Encode as PNG.
	f, _ := os.Create("image.png")
	png.Encode(f, img)
}
