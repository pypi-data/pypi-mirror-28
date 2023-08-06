# mc-tools [![Build Status](https://travis-ci.org/max-lobur/mc-tools.svg?branch=master)](https://travis-ci.org/max-lobur/mc-tools)

#### Installation

1. Install brew
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update; brew upgrade; brew cleanup;
```
2. Install python
```bash
brew install python3
```
3. Install mc-tools
```bash
pip3 install --upgrade --no-cache mc-tools
```
4. Fill-up the config
```bash
mv /tmp/mua-config.yml.sample ~/mua-config.yml
open ~/mua-config.yml
```