#!/bin/bash
conda create -n flask python=3.9
conda env update --file environment.yml  --prune
python init.py
