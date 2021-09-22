#!/bin/sh

if [ -d build ]; then
  rm -dr build
fi
if [ -d dist ]; then
  rm -dr dist
fi
if [ -d test/tweezer ]; then
  rm -dr test/tweezer
fi
if [ -d tweezer.egg-info ]; then
  rm -dr tweezer.egg-info
fi
