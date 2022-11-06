#!/bin/sh

[ -f "$DOTFILES/funcs/py_venv.sh" ] && . "$DOTFILES/funcs/py_venv.sh"

clean() {
  # python_project_clean || return 1
  python_clean || return 1
  rm -rf .pytest_cache || return 1
}

build() {
  python_clean || return 1
  python_build || return 1
  python_deploy || return 1
}

gen() {
  python_tools_gen || return 1
  python_venv_gen || return 1
}

run() {
  lsf ext
}

up() {
  COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose up
}

