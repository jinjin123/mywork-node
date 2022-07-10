package main

import (
	"fmt"
	"github.com/vova616/screenshot"
	"image/png"
	"os"
	"time"
)

func main() {
	img, err := screenshot.CaptureScreen()
	if err != nil {
		panic(err)
	}
	//f, err := os.Create("./ss.png")
	//strtime, _ := fmt.Println(fmt.Sprintf("%s.png", time.Now().Format("20060102-150405")))
	fname := fmt.Sprintf("%s.png", time.Now().Format("20060102-150405"))
	f, err := os.Create(fname)
	if err != nil {
		panic(err)
	}
	err = png.Encode(f, img)
	if err != nil {
		panic(err)
	}
	f.Close()
}
