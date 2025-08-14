#!/bin/bash

eval "$(conda shell.bash hook)"

source  /home/mos/drive_0/miniconda/etc/profile.d/conda.sh
conda activate web || { echo "Failed to activate Conda environment"; exit 1; }