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

var KIT_TYPES = map[string]string{
	"awk":         "#!/usr/bin/env awk",
	"mathematica": "#!/usr/bin/env MathematicaScript -script",
	"perl":        "#!/usr/bin/env perl",
	"python":      "#!/usr/bin/env python",
	"R":           "#!/usr/bin/env Rscript",
	"ruby":        "#!/usr/bin/env ruby",
	"sed":         "#!/usr/bin/env sed",
	"shell":       "#!/usr/bin/env sh",
}

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
	case "delete":
		CmdDelete(os.Args[2:]...)
	case "edit":
		CmdEdit(os.Args[2:]...)
	case "run":
		CmdRun(os.Args[2:]...)
	case "path":
		CmdPath(os.Args[2:]...)
	default:
		if _, err := os.Stat(GetCmdPath(os.Args[1:2])); err == nil {
			CmdRun(os.Args[1:]...)
		} else {
			fmt.Printf("Wrong command: %s\n", os.Args[1])
		}
	}
}

func CmdAdd(opts ...string) {
	cmdStrs, _ := GetCmdAndArgs(opts)
	cmdDir := GetCmdPath(cmdStrs[:(len(cmdStrs) - 1)])
	cmdPath := GetCmdPath(cmdStrs)

	if _, err := os.Stat(cmdDir); os.IsNotExist(err) {
		os.MkdirAll(GetCmdPath(cmdStrs[:(len(cmdStrs)-1)]), 0755)
	}

	if _, err := os.Stat(cmdPath); os.IsNotExist(err) {
		fmt.Printf("Command not exist at %s\nPlease select one type to create:\n", cmdPath)
		i := 0
		for k, v := range KIT_TYPES {
			i++
			fmt.Printf("%d: %s (%s)\n", i, k, v)
		}

		answer := GetInput("Type of script you will create: ")

		ioutil.WriteFile(cmdPath, []byte(KIT_TYPES[strings.Trim(answer, "\n")]+"\n"), 0755)

		CmdEdit(opts...)
	} else {
		log.Fatal("Command file already exists!")
	}
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
		fmt.Printf("\n-----------------------------------------------------------------\n")
		panic(fmt.Sprintf("Run error: %s", cmdPath))
	}
}

func CmdDelete(opts ...string) {
	cmdStrs, _ := GetCmdAndArgs(opts)
	cmdPath := GetCmdPath(cmdStrs)

	if err := os.Remove(cmdPath); err == nil {
		fmt.Println("Command deleted!")
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
		editor, args := GetEditor()
		args = append(args, tmpfile.Name())

		cmd := exec.Command(editor, args...)
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

func CmdPath(opts ...string) {
	cmdstrs, _ := GetCmdAndArgs(opts)
	fmt.Printf("%s\n", GetCmdPath(cmdstrs))
	os.Exit(0)
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
		"Usage: %s [run|cat|add|delete|edit|help] Command\n",
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

func GetEditor() (string, []string) {
	editor, ok := os.LookupEnv("EDITOR")

	if ok {
		editor_opts := strings.Split(editor, " ")
		return editor_opts[0], editor_opts[1:]
	} else {
		return "vim", []string{}
	}
}

func GetInput(prompt string) string {
	fmt.Print(prompt)
	answer, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	return answer
}
