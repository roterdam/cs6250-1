#!/bin/bash

pushd ~/pyretic/pyretic/pyresonance/
for ((i=1;i<7;i++)) ; do
    python json_sender.py --flow="{srcip=10.0.0.${i}}" -e auth -s authenticated -a 127.0.0.1 -p 5000${i}
    python json_sender.py --flow="{srcip=10.0.0.${i}}" -e ids -s clean -a 127.0.0.1 -p 5000${i}
done
popd
