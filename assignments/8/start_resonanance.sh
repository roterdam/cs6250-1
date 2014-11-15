#!/bin/bash

pushd ${HOME}/pyretic
pyretic.py pyretic.pyresonance.main --config=./pyretic/pyresonance/global.config --mode=manual
popd
