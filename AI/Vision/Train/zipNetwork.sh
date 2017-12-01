n="$(pwd)"
rm -R ./models/rede
mkdir ./models/rede

cd ./models/train

var=$(ls model.ckpt-*.index | sort -V | tail -n 1)
var=${var%.index}
echo "Checkpoint "$var

cd ~/models/research

python object_detection/export_inference_graph.py \
  --input_type image_tensor \
  --pipeline_config_path="$n/models/model/ssd_mobilenet_v1.config" \
  --trained_checkpoint_prefix "$n/models/train/$var" \
  --output_directory "$n/models/rede/"

cd "$n"
mkdir newRede
cp ./models/rede/frozen_inference_graph.pb ./newRede/frozen_inference_graph.pb
cp ./data/object-detection.pbtxt ./newRede/object-detection.pbtxt
cd newRede
rm ../../Data/newRede.tar.gz
tar -czf ../../Data/newRede.tar.gz *
cd ..
rm -R newRede
