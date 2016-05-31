#!/bin/bash
#!/RoboFEI-HT/build/bin

echo "control"

cd ..
echo 123456 | sudo -S ./build/Control/control
