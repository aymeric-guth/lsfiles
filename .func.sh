#!/bin/sh

[ -f "$DOTFILES/funcs/py_venv.sh" ] && . "$DOTFILES/funcs/py_venv.sh"

clean() {
  python_clean || return 1
}

build() {
  python_deploy|| return 1
}

gen() {
  python_venv_gen || return 1
}


