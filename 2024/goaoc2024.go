package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
)


func day01Part01(puzzleInput string) int {
	lines := puzzleInput.Split("\n")
}


func main() {
	if len(os.Args) != 4 {
		fmt.Println("Usage: goac2024 day part input_filename")
		os.exit(1)
	}
	day, err := strconv.ParseInt(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	part, err := strconv.ParseInt(os.Args[2])
	if err != nil {
		log.Fatal(err)
	}
	filename := os.Args[3]
	data, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	puzzleInput := string(data)
}
