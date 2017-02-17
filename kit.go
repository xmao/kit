package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"os/user"
	"path"
	"strings"
)

func main() {
	if len(os.Args) <= 1 {
		Usage()
	}

	switch os.Args[1] {
	case "help":
		CmdHelp(os.Args[2:]...)
	case "cat":
		CmdCat(os.Args[2:]...)
	case "add":
		CmdAdd(os.Args[2:]...)
	case "edit":
		CmdEdit(os.Args[2:]...)
	case "run":
		CmdRun(os.Args[2:]...)
	default:
		if _, err := os.Stat(GetCmdPath(os.Args[1:2])); err == nil {
			CmdRun(os.Args[1:]...)
		} else {
			fmt.Printf("Wrong command: %s\n", os.Args[1])
		}
	}
}

func CmdAdd(opts ...string) {
	KIT_TYPES := map[string]string{
		"awk":         "#!/usr/bin/env awk",
		"mathematica": "#!/usr/bin/env MathematicaScript -script",
		"perl":        "#!/usr/bin/env perl",
		"python":      "#!/usr/bin/env python",
		"R":           "#!/usr/bin/env Rscript",
		"ruby":        "#!/usr/bin/env ruby",
		"sed":         "#!/usr/bin/env sed",
		"shell":       "#!/usr/bin/env sh",
	}

	cmdStrs, _ := GetCmdAndArgs(opts)

	cmdDirPath := GetCmdPath(cmdStrs[:len(cmdStrs)-1])
	if os.MkdirAll(cmdDirPath, 0777) != nil {
		log.Fatal(fmt.Sprintf("Can't create directory %s", cmdDirPath))
	}

	cmdPath := GetCmdPath(cmdStrs)
	f, _ := os.Create(cmdPath)
	f.WriteString(fmt.Sprintf("%s\\n", KIT_TYPES["python"]))
	f.Sync()
	f.Close()

	CmdEdit(opts...)
}

func CmdCat(opts ...string) {
	cmdstrs, _ := GetCmdAndArgs(opts)
	file, err := os.Open(GetCmdPath(cmdstrs))
	if err != nil {
		panic("Command not exists")
	}
	defer file.Close()

	out, _ := ioutil.ReadAll(file)
	fmt.Printf("%s", out)
}

func CmdRun(opts ...string) {
	cmdStrs, args := GetCmdAndArgs(opts)
	cmdPath := GetCmdPath(cmdStrs)

	cmd := exec.Command(cmdPath, args...)
	cmd.Stdin = os.Stdin
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout

	if err := cmd.Run(); err != nil {
		panic(fmt.Sprintf("\n\nRun error: %s", cmdPath))
	}
}

func CmdEdit(opts ...string) {
	cmdstrs, _ := GetCmdAndArgs(opts)
	content, err := ioutil.ReadFile(GetCmdPath(cmdstrs))
	if err != nil {
		panic("Can't find command file")
	}

	tmpfile, err := ioutil.TempFile("", "kit")
	if err != nil {
		panic("Can't create a temp file for command")
	}
	defer os.Remove(tmpfile.Name())

	if ioutil.WriteFile(tmpfile.Name(), content, 0755) == nil {
		cmd := exec.Command("vim", tmpfile.Name())
		cmd.Stdin = os.Stdin
		cmd.Stderr = os.Stderr
		cmd.Stdout = os.Stdout

		if cmd.Run() == nil {
			new_content, err := ioutil.ReadFile(tmpfile.Name())
			if err == nil {
				ioutil.WriteFile(GetCmdPath(cmdstrs), new_content, 0755)
			}
		} else {
			log.Fatal(err)
		}
	}
}

func CmdHelp(opts ...string) {
	cmdstrs, _ := GetCmdAndArgs(opts)
	file, err := os.Open(GetCmdPath(cmdstrs))
	if err != nil {
		panic("Command not exists")
	}
	defer file.Close()

	reader := bufio.NewScanner(file)
	for reader.Scan() {
		line := reader.Text()

		if strings.HasPrefix(line, "#!") {
			continue
		} else if strings.HasPrefix(line, "#") {
			fmt.Println(strings.TrimLeft(line, "# "))
		} else {
			break
		}
	}
}

func Usage() {
	fmt.Printf(
		"Usage: %s [run|cat|add|edit|help] Command\n",
		path.Base(os.Args[0]))
	os.Exit(1)
}

func GetCmdPath(names []string) string {
	return path.Join(GetCmdRootPath(), path.Join(names...))
}

func GetCmdAndArgs(opts []string) ([]string, []string) {
	for i, _ := range opts {
		fileInfo, err := os.Stat(GetCmdPath(opts[:(i + 1)]))
		if err == nil && fileInfo.Mode().IsRegular() {
			return opts[:(i + 1)], opts[(i + 1):]
		}
	}
	return opts[:], opts[:0]
}

func GetCmdRootPath() string {
	root := os.Getenv("KITROOT")

	if root == "" {
		usr, _ := user.Current()
		return path.Join(usr.HomeDir, ".kit", "scripts")
	} else {
		return root
	}
}
