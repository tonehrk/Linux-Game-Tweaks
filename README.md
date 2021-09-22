
# Linux Game-Tweaks

![](src/res/cake-piece.png) Linux Overlay configurations (OpenGL and Vulkan).

![](assets/ksnip_20200824-154156.png)

For: MangoHUD

## Dependences 

- Qt5
- python-setproctitle

#### Optional

- [mangohud](https://github.com/flightlessmango/MangoHud)
- mesa-demos
- vulkan-tools



## Install/Uninstall

```
git clone https://github.com/tonehrk/LOverlay.git
cd LOverlay
```

& run install.sh via terminal with "--install" or "--uninstall" option as sudo

Install:
```
sudo sh install.sh --install
```
Uninstall:
```
sudo sh install.sh --uninstall
```

## Run without installing
After git clone, run via terminal: 
```
cd src
python loverlay.py
```
