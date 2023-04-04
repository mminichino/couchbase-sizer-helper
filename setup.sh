#!/bin/sh
#
SCRIPTDIR=$(cd $(dirname $0) && pwd)
YUM_PKGS="python39"
APT_PKGS="python3.9"
MAC_PKGS="python@3.9"
LEGACY_YUM_PKGS=""
MAJOR_REV=3
MINOR_REV=9
VENV_NAME=venv
YES=0
FORCE=0
BUILD_PYTHON=0

err_exit () {
   if [ -n "$1" ]; then
      echo "[!] Error: $1"
   fi
   exit 1
}

check_sudo () {
  sudo ls > /dev/null 2>&1
  [ $? -ne 0 ] && err_exit "Unable to sudo. Make sure sudo is install and you are authorized to use it."
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
        echo -n "Install dependency ${package}? (y/n) [y]:"
        read INPUT
      fi
      if [ "$INPUT" = "y" ] || [ -z "$INPUT" ]; then
        install_pkg $package
      else
        echo "Please install $package"
        exit 1
      fi
    fi
  done
  if [ $BUILD_PYTHON -eq 1 ]; then
    which python3.9 >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      printf "Building and installing Python 3.9 ... "
      sudo $SCRIPTDIR/install_python.sh >> setup.log 2>&1
      [ $? -ne 0 ] && err_exit "Python build failed. See setup.log for more details."
      echo "Done."
    else
      echo "Python 3.9 already installed."
    fi
  fi
}

check_apt () {
  for package in $APT_PKGS
  do
    dpkg -s $package >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      if [ $YES -eq 1 ]; then
        INPUT="y"
      else
        echo -n "Install dependency ${package}? (y/n) [y]:"
        read INPUT
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
  for package in $MAC_PKGS
  do
    brew list $package >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      if [ $YES -eq 1 ]; then
        INPUT="y"
      else
        printf "Install dependency ${package}? (y/n/s) [y]: "
        read INPUT
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
}

check_linux_by_type () {
  . /etc/os-release
  export LINUXTYPE=$ID
  case $ID in
  centos|rhel)
    PKGMGR="yum"
    if [ "$VERSION_ID" = "7" ]; then
      YUM_PKGS=$LEGACY_YUM_PKGS
      BUILD_PYTHON=1
    fi
    check_yum
    ;;
  ubuntu)
    PKGMGR="apt"
    check_apt
    ;;
  *)
    echo "Unknown Linux distribution $ID"
    exit 1
    ;;
  esac
}

while getopts "p:yf" opt
do
  case $opt in
    p)
      PYTHON_BIN=$OPTARG
      ;;
    y)
      YES=1
      ;;
    f)
      FORCE=1
      ;;
    \?)
      echo "Invalid Argument"
      exit 1
      ;;
  esac
done

clear_log_file

SYSTEM_UNAME=$(uname -s)
case "$SYSTEM_UNAME" in
    Linux*)
      machine=Linux
      PYTHON_BIN=${PYTHON_BIN:-python3.9}
      check_linux_by_type
      ;;
    Darwin*)
      machine=MacOS
      check_macos
      BREW_PREFIX=$(brew --prefix)
      PYTHON_BIN=${PYTHON_BIN:-python3.9}
      ;;
    CYGWIN*)
      machine=Cygwin
      echo "Windows is not currently supported."
      exit 1
      ;;
    *)
      echo "Unsupported system type: $SYSTEM_UNAME"
      exit 1
      ;;
esac

check_sudo

which $PYTHON_BIN >/dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Python 3 is required and $PYTHON_BIN should be in the execution search PATH."
  exit 1
fi

if [ ! -f requirements.txt ]; then
  echo "Missing requirements.txt"
  exit 1
fi

PY_MAJOR=$($PYTHON_BIN --version | awk '{print $NF}' | cut -d. -f1)
PY_MINOR=$($PYTHON_BIN --version | awk '{print $NF}' | cut -d. -f2)

if [ "$PY_MAJOR" -lt "$MAJOR_REV" ] || [ "$PY_MINOR" -lt "$MINOR_REV" ]; then
  echo "Python ${MAJOR_REV}.${MINOR_REV} or higher is required."
  exit 1
fi

if [ -d $SCRIPTDIR/$VENV_NAME -a $FORCE -eq 0 ]; then
  echo "Virtual environment $SCRIPTDIR/$VENV_NAME already exists."
  printf "Remove the existing directory? (y/n) [y]:"
  read INPUT
  if [ "$INPUT" == "y" -o -z "$INPUT" ]; then
    [ -n "$SCRIPTDIR" ] && [ -n "$VENV_NAME" ] && rm -rf $SCRIPTDIR/$VENV_NAME
  else
    echo "Setup cancelled. No changes were made."
    exit 1
  fi
fi

printf "Creating virtual environment... "
$PYTHON_BIN -m venv $SCRIPTDIR/$VENV_NAME
if [ $? -ne 0 ]; then
  echo "Virtual environment setup failed."
  exit 1
fi
echo "Done."

printf "Activating virtual environment... "
. ${SCRIPTDIR:?}/${VENV_NAME:?}/bin/activate
echo "Done."

set_pip_bin

printf "Installing dependencies... "
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel >> setup.log 2>&1
$PIP_BIN install --no-cache-dir -r requirements.txt >> setup.log 2>&1
if [ $? -ne 0 ]; then
  echo "Setup failed."
  rm -rf ${SCRIPTDIR:?}/${VENV_NAME:?}
  exit 1
else
  echo "Done."
  echo "Setup successful."
fi

####