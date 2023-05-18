# PathPicker

[![tests](https://github.com/facebook/PathPicker/workflows/tests/badge.svg)](https://github.com/facebook/PathPicker/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Facebook PathPicker is a simple command line tool that solves the perpetual
problem of selecting files out of bash output. PathPicker will:
* Parse all incoming lines for entries that look like files
* Present the piped input in a convenient selector UI
* Allow you to either:
    * Edit the selected files in your favorite `$EDITOR`
    * Execute an arbitrary command with them

It is easiest to understand by watching a simple demo:

<a href="https://asciinema.org/a/19519" target="_blank"><img src="https://asciinema.org/a/19519.png" width="597"/></a>

## Examples

After installing PathPicker, using it is as easy as piping into `fpp`. It takes
a wide variety of input -- try it with all the options below:

* `git status | fpp`
* `hg status | fpp`
* `git grep "FooBar" | fpp`
* `grep -r "FooBar" . | fpp`
* `git diff HEAD~1 --stat | fpp`
* `find . -iname "*.js" | fpp`
* `arc inlines | fpp`

and anything else you can dream up!

## Requirements

PathPicker requires Python 3.

### Supported Shells

* Bash is fully supported and works the best.
* ZSH is supported as well, but won't have a few features like alias expansion in command line mode.
* csh/fish/rc are supported in the latest version, but might have quirks or issues in older versions of PathPicker. Note: if your default shell and current shell is not in the same family (bash/zsh... v.s. fish/rc), you need to manually export environment variable `$SHELL` to your current shell.

## Installing PathPicker

The recommended way to install Jasha's fork of PathPicker is with [pipx](https://pypa.github.io/pipx/).

### Pipx

```
pipx install git+https://github.com/jasha10/PathPicker@jasha-dev
# OR
git clone https://github.com/jasha10/PathPicker ~/opt/PathPicker --branch jasha-dev
pipx install --editable ~/opt/PathPicker
```

### Add-ons

For tmux users, you can additionally install `tmux-fpp` which adds a key combination to run PathPicker on the last received `stdout`.
This makes jumping into file selection mode even easier. ([Check it out here!](https://github.com/tmux-plugins/tmux-fpp))

#### $FPP_EDITOR_ENTRY_POINT plugins

Jasha's fork of fpp supports editor plugins via an [entry point](https://packaging.python.org/en/latest/specifications/entry-points/)
named `pathpicker.editor`.

See ./src/pathpicker/output.py for the interface.

## Advanced Functionality

As mentioned above, PathPicker allows you to also execute arbitrary commands using the specified files.
Here is an example showing a `git checkout` command executed against the selected files:

<a href="https://asciinema.org/a/19520" target="_blank"><img src="https://asciinema.org/a/19520.png" width="597"/></a>

The selected files are appended to the command prefix to form the final command. If you need the files
in the middle of your command, you can use the `$F` token instead, like:

`cat $F | wc -l`

Another important note is that PathPicker, by default, only selects files that exist on the filesystem. If you
want to skip this (perhaps to selected deleted files in `git status`), just run PathPicker with the `--no-file-checks` (or `-nfc`, for short) flag.

## How PathPicker works

PathPicker is a combination of a bash script and some small Python modules.
It essentially has three steps:

* Firstly, the bash script redirects all standards out into a python module that
parses and extracts out filename candidates. These candidates are extracted with a series of
regular expressions, since the input to PathPicker can be any `stdout` from another program. Rather
than make specialized parsers for each program, we treat everything as noisy input, and select candidates via
regexes. To limit the number of calls to the filesystem (to check existence), we are fairly restrictive on the
candidates we extract.

The downside to this is that files that are single words, with no extension (like `test`), that are not prepended by
a directory will fail to match. This is a known limitation to PathPicker, and means that it will sometimes fail to find valid files in the input.

* Next, a selector UI built with `curses` is presented to the user. At this point you can select a few files to edit, or input a command
to execute.

* Lastly, the python script outputs a command to a bash file that is later
executed by the original bash script.

It's not the most elegant architecture in the world but, in our opinion, it provides a lot of utility.

## Documentation & Configuration

For all documentation and configuration options, see the output of `fpp --help`.

## Join the PathPicker community

See the [CONTRIBUTING.md](https://github.com/facebook/PathPicker/blob/master/CONTRIBUTING.md) file for how to help out.

## License

PathPicker is MIT licensed.
