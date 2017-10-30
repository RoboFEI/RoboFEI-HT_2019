n="$(pwd)"
mkdir ./models/rede

cd ./models/train

var=$(ls model.ckpt-*.index | sort -V | tail -n 1)
var=${var%.index}

cd ~/models/research

python object_detection/export_inference_graph.py \
  --input_type image_tensor \
  --pipeline_config_path="$n/models/model/ssd_mobilenet_v1.config" \
  --trained_checkpoint_prefix "$n/models/train/$var" \
  --output_directory "$n/models/rede/"

cd "$n"
tar -zcvf ../Data/newRede.tar.gz ./models/rede/frozen_inference_graph.pb ./data/object-detection.pbtxt
