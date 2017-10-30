#!/bin/bash

n="$(pwd)"
cd ~/models/research

# From the models/ directory
python object_detection/train.py \
  --logtostderr \
  --pipeline_config_path="$n/models/model/ssd_mobilenet_v1.config" \
  --train_dir="$n/models/train"
