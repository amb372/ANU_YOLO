# ANU_YOLO
YOLO scripts and env setups on Raspberry Pi OS

## Instructions

```bash
echo "1) Update & upgrade system…"
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

echo "2) Repair broken packages (if any)…"
sudo apt-get install -f -y -qq
sudo dpkg --configure -a

echo "3) Install core prerequisites: curl, unzip, compilers, media libs…"
sudo apt-get install -y -qq \
    curl unzip wget bzip2 build-essential cmake \
    libjpeg-dev libpng-dev libtiff-dev \
    libavcodec-dev libavformat-dev libswscale-dev ffmpeg \
    git ca-certificates
```
