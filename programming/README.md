# Development Environment Setup

## 1. Languages

supported and to be supported:

1. Assembly
2. Bash
3. C/C++  clang/gcc
5. C#
6. Go
7. Groovy
8. HTML/CSS
9. Java
10. JavaScript
11. Matlab
12. Perl
13. PHP
14. PowerShell
15. Python
16. R
17. Ruby
18. Rust
19. Scala
20. SQL (ANSI SQL, T-SQL, PL/SQL)
21. Swift
22. TypeScript

## 2. Editors

1. VIM
2. Emacs
3. Atom
4. Code
5. Sublime

## 3. Installation

For each case, please exit current terminal after installation and re-open a new one to activate profile settings!

### 3.1. Linux/macOS/FreeBSD

install all languages and tools:

```bash
curl https://raw.githubusercontent.com/conke/witbox/master/programming/setup.sh | bash
```

or only install the specified languages:

```bash
curl https://raw.githubusercontent.com/conke/witbox/master/programming/setup.sh | bash -s -- -l go,python
```

### 3.2. Windows

PowerShell:

```bash
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/conke/witbox/master/programming/setup.ps1'))
```

CMD:

```bash
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/conke/witbox/master/programming/setup.ps1'))"
```
