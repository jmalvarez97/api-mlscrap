#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
  unzip -d ./ chromedriver_linux64.zip
  rm ./chromedriver_linux64.zip
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

# add your own build commands...