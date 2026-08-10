# Langauge Server Protocol

The LSP is created by Microsoft to let a file written in a specific language to be understood by any current IDEs in the system (i.e. VSCode, Nvim,Emacs, etc.), which results in richer linting, autompletion, autosuggestions, among other features.

One can see where this is useful is in debugging, where a universal debugger can do the work of multiple debuggers for each language, so long as the universal debugger understands the file.

A *Language Server* is meant to provide the language-specific smarts and communicate with development tools over a protocol that enables inter-process communication.


