#!/bin/bash
lib_dir="/usr/lib/linux-game-tweaks"
DIR=$(cd `dirname $0` && pwd)
if [ -z $1 ]; then
set "x"
fi

if [[ $EUID > 0 ]]; then
	echo "Please run as root/sudo"
	exit 1
else
	if [ $1 = "--install" ]; then
		if test -f "/usr/bin/linux-game-tweaks"; then
			echo "Linux Game-Tweaks it's already installed. If you are updating, please remove and reinstall."
		else
			echo "Installing"
			echo "copying files"
			mkdir $lib_dir
			mkdir $lib_dir/src
			/usr/bin/install -vm644 -D $DIR/src/*.ui $lib_dir
			/usr/bin/install -vm644 -D $DIR/src/*.py $lib_dir
			/usr/bin/install -vm644 -D $DIR/src/res/* $lib_dir/src
			/usr/bin/install -vm644 -D $DIR/icons/loverlay.svg /usr/share/icons/hicolor/scalable/apps
			/usr/bin/install -vm644 -D $DIR/icons/loverlay.png /usr/share/pixmaps
			
			/usr/bin/install -vm755 $DIR/bin/linux-game-tweaks /usr/bin
			/usr/bin/install -vm644 -D $DIR/bin/linux-game-tweaks.desktop /usr/share/applications
			/usr/bin/install -vm644 -D $DIR/bin/linux-game-tweaks.metainfo.xml /usr/share/metainfo
			echo "L Game-Tweaks successfully installed."
		fi
	elif [ $1 = "--uninstall" ]; then
		echo "Are you sure? (y/n)"
		read YES_NO
		if [ $YES_NO = "y" ] || [ $YES_NO = "yes" ] || [ $YES_NO = "YES" ] || [ $YES_NO = "NO" ];
		then
			echo "removing"
			rm -r $lib_dir
			rm /usr/bin/linux-game-tweaks
			rm /usr/share/applications/linux-game-tweaks.desktop
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
