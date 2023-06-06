#!/bin/sh
#
LOCAL_DIR=$(dirname "$0")
SCRIPTDIR=$(cd "$LOCAL_DIR" && pwd)
YUM_PKGS="python39"
APT_PKGS="python3.9"
MAC_PKGS="python@3.9"
MAJOR_REV=3
MINOR_REV=9
PYTHON_INSTALL_BIN="python3.9"
VENV_NAME=venv
YES=0
FORCE=0
INSTALL_PYTHON=0
VERBOSE=0

err_exit () {
   if [ -n "$1" ]; then
      echo "[!] Error: $1"
   fi
   exit 1
}

check_sudo () {
  if [ "$(id -u)" -ne 0 ]; then
    echo "Checking sudo access (enter account login password if prompted)"
    sudo ls > /dev/null 2>&1 || err_exit "Unable to sudo. Make sure sudo is install and you are authorized to use it."
  fi
}

set_pip_bin () {
  which pip3.9 > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    PIP_BIN=pip3.9
  else
    PIP_BIN=pip3
  fi
}

clear_log_file () {
  echo "Setup begins at $(date +%T)" > setup.log 2>&1
  echo "===========================" >> setup.log 2>&1
}

install_pkg () {
  case $PKGMGR in
  yum)
    sudo yum install -q -y "$@"
    ;;
  apt)
    sudo apt-get update
    sudo apt-get install -q -y "$@"
    ;;
  brew)
    brew install "$@"
    ;;
  *)
    err_exit "Unknown package manager $PKGMGR"
    ;;
  esac
}

check_yum () {
  for package in $YUM_PKGS
  do
    yum list installed $package >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      if [ $YES -eq 1 ]; then
        INPUT="y"
      else
        printf "Install dependency %s? (y/n) [y]:" ${package}
        read -r INPUT
      fi
      if [ "$INPUT" = "y" ] || [ -z "$INPUT" ]; then
        install_pkg $package
      else
        echo "Please install $package"
        exit 1
      fi
    fi
  done
}

check_apt () {
  for package in $APT_PKGS
  do
    dpkg -s $package >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      if [ $YES -eq 1 ]; then
        INPUT="y"
      else
        printf "Install dependency %s? (y/n) [y]:" ${package}
        read -r INPUT
      fi
      if [ "$INPUT" = "y" ] || [ -z "$INPUT" ]; then
        install_pkg $package
      else
        echo "Please install $package"
        exit 1
      fi
    fi
  done
}

check_macos () {
  PKGMGR="brew"
  which brew >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Please install Homebrew."
    exit 1
  fi
  HOMEBREW_PREFIX=$(brew --prefix)
  for package in $MAC_PKGS
  do
    brew list $package >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      if [ $YES -eq 1 ]; then
        INPUT="y"
      else
        printf "Install dependency %s? (y/n/s) [y]: " ${package}
        read -r INPUT
      fi
      if [ "$INPUT" = "s" ]; then
        continue
      fi
      if [ "$INPUT" = "y" ] || [ -z "$INPUT" ]; then
        install_pkg $package
      else
        echo "Please install $package"
        exit 1
      fi
    fi
  done
  PYTHON_BIN="${HOMEBREW_PREFIX}/bin/${PYTHON_INSTALL_BIN}"
}

check_linux_by_type () {
  . /etc/os-release
  export LINUXTYPE=$ID
  case $ID in
  centos|rhel)
    PKGMGR="yum"
    [ "$INSTALL_PYTHON" -eq 1 ] && check_yum
    ;;
  ubuntu)
    PKGMGR="apt"
    [ "$INSTALL_PYTHON" -eq 1 ] && check_apt
    if ! python3 -m ensurepip >/dev/null 2>&1
    then
      install_pkg python3-venv
    fi
    ;;
  *)
    echo "Unknown Linux distribution $ID"
    exit 1
    ;;
  esac
}

while getopts "p:yfv" opt
do
  case $opt in
    p)
      PYTHON_BIN_OPT=$OPTARG
      ;;
    y)
      YES=1
      ;;
    f)
      FORCE=1
      ;;
    v)
      VERBOSE=1
      ;;
    \?)
      echo "Invalid Argument"
      exit 1
      ;;
  esac
done

clear_log_file
check_sudo

PYTHON_BIN=${PYTHON_BIN_OPT:-python3}

if which "$PYTHON_BIN" >/dev/null 2>&1
then
  PY_MAJOR=$($PYTHON_BIN --version | awk '{print $NF}' | cut -d. -f1)
  PY_MINOR=$($PYTHON_BIN --version | awk '{print $NF}' | cut -d. -f2)
  [ "$VERBOSE" -eq 1 ] && echo "Found Python ${PY_MAJOR}.${PY_MINOR}"
else
  PY_MAJOR="0"
  PY_MINOR="0"
fi

if [ "$PY_MAJOR" -lt "$MAJOR_REV" ] || [ "$PY_MINOR" -lt "$MINOR_REV" ]; then
  INSTALL_PYTHON=1
  PYTHON_BIN=$PYTHON_INSTALL_BIN
  [ "$VERBOSE" -eq 1 ] && echo "Installing Python ${MAJOR_REV}.${MINOR_REV}"
fi

SYSTEM_UNAME=$(uname -s)
case "$SYSTEM_UNAME" in
    Linux*)
      check_linux_by_type
      ;;
    Darwin*)
      check_macos
      ;;
    CYGWIN*)
      echo "Windows Cygwin is not currently supported. Please use WSL2 instead."
      exit 1
      ;;
    *)
      echo "Unsupported system type: $SYSTEM_UNAME"
      exit 1
      ;;
esac

if ! which "$PYTHON_BIN" >/dev/null 2>&1
then
  echo "Setup failed. Python 3 not found. Please check the output and try again."
  exit 1
fi

if [ ! -f requirements.txt ]; then
  echo "Missing requirements.txt"
  exit 1
fi

if [ -d "$SCRIPTDIR/$VENV_NAME" ] && [ $FORCE -eq 0 ]; then
  echo "Virtual environment $SCRIPTDIR/$VENV_NAME already exists."
  printf "Remove the existing directory? (y/n) [y]:"
  read -r INPUT
  if [ "$INPUT" = "y" ] || [ -z "$INPUT" ]; then
    [ -n "$SCRIPTDIR" ] && [ -n "$VENV_NAME" ] && rm -rf "${SCRIPTDIR:?}/$VENV_NAME"
  else
    echo "Setup cancelled. No changes were made."
    exit 1
  fi
fi

printf "Creating virtual environment... "
$PYTHON_BIN -m venv "$SCRIPTDIR/$VENV_NAME"
if [ $? -ne 0 ]; then
  echo "Virtual environment setup failed."
  exit 1
fi
echo "Done."

printf "Activating virtual environment... "
# shellcheck disable=SC1090
. "${SCRIPTDIR:?}/${VENV_NAME:?}/bin/activate"
echo "Done."

set_pip_bin

printf "Installing dependencies... "
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel >> setup.log 2>&1
$PIP_BIN install --no-cache-dir -r requirements.txt >> setup.log 2>&1
if [ $? -ne 0 ]; then
  echo "Setup failed."
  rm -rf "${SCRIPTDIR:?}/${VENV_NAME:?}"
  exit 1
else
  echo "Done."
  echo "Setup successful."
fi

####