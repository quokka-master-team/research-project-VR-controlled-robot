#!/bin/bash
rm -r build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
make --directory=build -j$(nproc) -s
