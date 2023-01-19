# learn Go

## install by asdf

```s
asdf help
asdf plugin add golang # MANAGE PLUGINS
asdf install golang latest # MANAGE PACKAGES
asdf local golang latest
asdf current golang
```

## Tutorial

> All tools successfully installed. You are ready to Go. :)

[Tutorial: Get started with Go - The Go Programming Language](https://go.dev/doc/tutorial/getting-started)

[How to Write Go Code - The Go Programming Language](https://go.dev/doc/code)

```s
# Generate ASCII file tree
├── go-demo
│   ├── src
│   ├── go-demo # build result
│   ├── go.mod # modules
│   ├── go.sum # for use in authenticating the module
│   ├── gort.go
│   ├── hello.go
│   └── README.md

# command to create
go mod init github.com/Steven147
vim hello.go ...
go mod tidy # add missing and remove unused modules
go run .
```

# awgo: alfred workflow with go

[deanishe/awgo: Go library for Alfred 3 + 4 workflows](https://github.com/deanishe/awgo)




# quote

- If a program is too slow, it must have a loop.
- I can eat glass and it doesn't hurt me.
- Don't communicate by sharing memory, share memory by communicating.