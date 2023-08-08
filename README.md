# red_camera

Software for isotecnic red camera control.

## Camera Connections supported 

- Version 0.1:
    - Wifi (via websockets library)

## Useful commands for the raspberry pi 

Hereby you can find a list of useful commands to test this package from raspberry.

### Select wifi network from cli with `wpa_cli`

```
wpa_cli -i wlan0 list_networks
```
Choose now your network number ID:

```
wpa_cli -i wlan0 select_network <ID>
```

You can find registered networks (with ssid and psw) in this text file:

```
/etc/wpa_supplicant/wpa_supplicant.conf
```

### Access raspberry pi via ssh

Access the raspberry pi zero w if connected to the same wifi network (password `raspberry`):
```
ssh pi@raspberrypi.local
```

## Install the `red_camera` package

### Install python's package manager

```
sudo apt install python3-pip
```
Then, clone and cd into this project and run 

```
git clone https://github.com/SystemSigma/red_camera.git
cd ~/red_camera
pip install -e .
```

# Run the FPS demo

This demo allows to increase/decrease the camera fps:
```
python scripts/test_increase_decrease.py
```


# Using `systemd` services

Copy the service to `etc/systemd/system/red_camera.service`
```
sudo cp ~/red_camera/services/red_camera.service /etc/systemd/system/red_camera.service
```

Enable it (to make it start at boot) and start it:

```
sudo systemctl enable red_camera
sudo systemctl start red_camera
```
