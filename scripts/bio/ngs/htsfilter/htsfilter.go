package main

import (
	"code.google.com/p/biogo.boom"
	"github.com/deckarep/golang-set"
	"os"
)

func main() {
	
	set1 := mapset.NewSet()

	reader1, _ := boom.OpenBAM(os.Args[1])
	for r, _, e := reader1.Read(); e == nil; r, _, e = reader1.Read() {
		set1.Add(r.Name())
	}
	reader1.Close()

	reader2, _ := boom.OpenBAM(os.Args[2])
	writer, _ := boom.CreateBAM(os.Args[3], reader2.Header(), true)
	for r, _, e := reader2.Read(); e == nil; r, _, e = reader2.Read() {
		if ! set1.Contains(r.Name()) {
			writer.Write(r)
		}
	}
	reader2.Close()
	writer.Close()
}
