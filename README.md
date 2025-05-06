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

## Clone this repo and prepare env

```bash
git clone https://www.github.com/1ssb/ANU_YOLO
cd YOLO
# Installing the environment
chmod +x install_env.sh
./install_env.sh
```
