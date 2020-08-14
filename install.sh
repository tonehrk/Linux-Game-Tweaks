#!/bin/bash
lib_dir="/usr/lib/loverlay"
DIR=$(cd `dirname $0` && pwd)
if [ -z $1 ]; then
set "x"
fi

if [[ $EUID > 0 ]]; then
	echo "Please run as root/sudo"
	exit 1
else
	if [ $1 = "--install" ]; then
		if test -f "/usr/bin/loverlay"; then
			echo "LOverlay it's already installed. If you are updating, please remove and reinstall."
		else
			echo "Installing"
			echo "copying files"
			mkdir $lib_dir
			cp $DIR/src/*.ui $lib_dir
			cp $DIR/src/*.py $lib_dir
			cp -r $DIR/src/res $lib_dir
			cp $DIR/bin/loverlay /usr/bin
			chmod +x /usr/bin/loverlay
			echo "... OK"
			echo "finalizing"
			cp $DIR/bin/loverlay.desktop /usr/share/applications
			cp $DIR/icons/loverlay.svg /usr/share/icons/hicolor/scalable/apps
			cp $DIR/icons/loverlay.png /usr/share/pixmaps
			echo "LOverlay successfully installed."
		fi
	elif [ $1 = "--uninstall" ]; then
		echo "Are you sure? (y/n)"
		read YES_NO
		if [ $YES_NO = "y" ] || [ $YES_NO = "yes" ] || [ $YES_NO = "YES" ] || [ $YES_NO = "NO" ];
		then
			echo "removing"
			echo "removing lib/bin"
			rm -r $lib_dir
			rm /usr/bin/loverlay
			echo "... OK"
			echo "removing icons"
			rm /usr/share/applications/loverlay.desktop
			rm /usr/share/icons/hicolor/scalable/apps/loverlay.svg
			rm /usr/share/pixmaps/loverlay.png
			echo "... OK"
			echo "Uninstalled"
		else
			echo "Aborted"
		fi
	else
	echo "Please run with --install or --uninstall."
	fi
fi
