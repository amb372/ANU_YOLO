# ANU_YOLO
YOLO scripts and env setups on Raspberry Pi OS....

## Instructions

Open a terminal and copy and execute the following command sets. Be careful to not change the order!

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

echo "4) Clean up unused packages & caches…"
sudo apt-get autoremove -y -qq
sudo apt-get autoclean -y -qq

echo "5) Ensure no broken dpkg state remains…"
sudo dpkg --configure -a
sudo apt-get install -f -y -qq

echo "6) Switch keyboard layout to US…"
# Update the default keyboard configuration
sudo sed -i 's/^XKBLAYOUT=.*/XKBLAYOUT="us"/' /etc/default/keyboard
# Reconfigure keyboard without interactive prompts
sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure keyboard-configuration
# Apply immediately
sudo udevadm trigger --subsystem-match=input --action=change
sudo reboot
```
After rebooting, if your Raspberry Pi survives ......

## Clone this repo and prepare env

```bash
git clone https://www.github.com/1ssb/ANU_YOLO
cd YOLO
# Installing the environment
chmod +x install_env.sh
./install_env.sh
```
This should automatically downlaod and set everything up!

Now let's download the YOLO system and install necessary libraries
```bash
conda create -n yolo python-3.10
conda activate yolo
pip install opencv-python ultralytics face-recognition
```

## Task

Count the number apples falling in the video: apples.mp4

Credits: https://www.istockphoto.com/video/gala-apple-falling-gm472985251-20196243?utm_source=pixabay&utm_medium=affiliate&utm_campaign=sponsored_video&utm_content=srp_topbanner_media&utm_term=apple+fall
