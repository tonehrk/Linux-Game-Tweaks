#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LOverlay.py
#  
#  Copyright 2020 Tony San Agustin <hormone@live.com.mx>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import os
import subprocess
import res
from _parser import parser
try: from setproctitle import setproctitle 
except ImportError:
	pass

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QColorDialog, QDialog, QMessageBox, QInputDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSettings, QPoint, QSize


MH_PATH=os.environ['HOME']+"/.config/MangoHud/"
OWN_PATH=os.path.dirname(os.path.abspath(__file__))



#VKB_PATH="$HOME/.config/vkBasalt"

class MainControl(QMainWindow):
		
	def __init__(self):
		super(MainControl, self).__init__()
		uic.loadUi(OWN_PATH+"/loverlay.ui", self)

		self.setWindowIcon(QtGui.QIcon(":/icons/cake-piece.svg"))
		self.runButton.clicked.connect(self.run_test)
		self.setWindowTitle("LOverlay - "+self.tabWidget.tabText(self.tabWidget.currentIndex()))
		QtGui.QFontDatabase.addApplicationFont(":/fonts/unispace_bd.ttf")
		self.settings = QSettings( 'Linux', 'LOverlay') 
		self.resize(self.settings.value("size", QSize(996, 763)))
		self.move(self.settings.value("pos", QPoint(50, 50)))
		self.aboutButton.clicked.connect(lambda: AboutDialog(self).show())

		# MANGU HUD -------
		
		self.loadConf("MangoHud") 
		self.HUD_rectangle.setStyleSheet("QWidget {background-color: #7F000000;font-family:Unispace;font-weight:Bold;border-radius: 10px;}")
		self.preview_u("load")
		self.saveButton.clicked.connect(lambda:self.saveConf(self.conf_comBox.currentText()))
		self.fpsCombox.currentIndexChanged.connect(self.fps_limit)
		self.logButton.clicked.connect(self.selectFile)
		self.conf_comBox.currentIndexChanged.connect(lambda:self.loadConf(self.conf_comBox.currentText()))
		self.conf_comBox.currentIndexChanged.connect(lambda: self.preview_u("load"))
		files = os.listdir(MH_PATH)
		
		for i in range (len(files)):
			if files [i][-5:] != ".conf": pass
			elif files[i] == "MangoHud.conf" or files[i] == "glxgears.conf" or files[i] == "vkcube.conf": pass
			else:self.conf_comBox.addItem(files[i][:-5])
		
		self.remove_profButton.clicked.connect(lambda:self.remove_config(self.conf_comBox.currentText()))
		self.add_profButton.clicked.connect(lambda:self.add_config())
		
		cpu_color_labels = self.hud_cpu,self.hud_cpu2
		engine_color_labels = self.hud_engine, self.hud_engine_verL, self.hud_modelL, self.hud_vulkan_driverL, self.hud_archL, self.hud_ftimeL
		text_color_labels = self.hud_hud_versionL, self.hud_gpu_usageL, self.hud_cpu_tempL, self.hud_gpu_clockL, self.hud_gpu_wattsL, self.hud_gpu_tempL, self.hud_cpu_usageL, self.hud_cpu_tempL, self.hud_cpu_usage2, self.hud_cpu_clockL, self.hud_io_readL,  self.hud_io_writeL, self.hud_vram_useL, self.hud_vram_clockL, self.hud_ram_useL, self.hud_engine_fpsL, self.hud_engine_msL
			
		
		# gpu init
		self.gpunameLine.editingFinished.connect(lambda:self._unblank(self.gpunameLine, "GPU"))
		self.gpucolorButton.clicked.connect(lambda:self.colorButtonU(self.gpucolorButton, self.hud_GPU))
		self.gpu_vram_colorButton.clicked.connect(lambda:self.colorButtonU(self.gpu_vram_colorButton, self.hud_vram))


		# cpu init
		
		self.cpu_Line.editingFinished.connect(lambda:self._unblank(self.cpu_Line, "CPU"))
		self.cpu_colorButton.clicked.connect(lambda:self.colorButtonU(self.cpu_colorButton, *cpu_color_labels))
		
		# other init
		self.other_diskcolorButton.clicked.connect(lambda:self.colorButtonU(self.other_diskcolorButton, self.hud_ioL))
		self.other_ramcolorButton.clicked.connect(lambda:self.colorButtonU(self.other_ramcolorButton, self.hud_ramL))
		self.o_winecolorButton.clicked.connect(lambda:self.colorButtonU(self.o_winecolorButton, self.hud_wineL))
		self.other_enginecolorButton.clicked.connect(lambda:self.colorButtonU(self.other_enginecolorButton, *engine_color_labels))
		self.other_frame_tcolorButton.clicked.connect(lambda:self.colorButtonU(self.other_frame_tcolorButton, self.hud_frame_gL))
		self.o_backg_colorButton.clicked.connect(lambda:self.colorButtonU(self.o_backg_colorButton, self.HUD_rectangle))
		self.o_mediacolorButton.clicked.connect(lambda:self.colorButtonU(self.o_mediacolorButton, self.hud_mediaL))
		self.o_font_colorButton.clicked.connect(lambda:self.colorButtonU(self.o_font_colorButton, *text_color_labels))
		
		# set colors

		
		# HUD rectangle
		a=self.preview_u

		self.posCombox.currentIndexChanged.connect(lambda:a("position"))
		self.o_bg_hSlider.sliderReleased.connect(lambda:a("hud_bg_slider"))
		# gpu
		self.gpunameLine.textChanged.connect(lambda:a("gpu_text"))
		self.gpu_av_loadCBox.stateChanged.connect(lambda:a("gpu_av_load"))
		self.gpu_tempCBox.stateChanged.connect(lambda:a("gpu_temp"))
		self.gpu_mem_fqCBox.stateChanged.connect(lambda:a("vram_clock"))
		self.gpu_vramCBox.stateChanged.connect(lambda:a("vram"))
		self.gpu_core_fqCBox.stateChanged.connect(lambda:a("gpu_core"))
		self.gpu_powerCBox.stateChanged.connect(lambda:a("gpu_watts"))
		self.gpu_modelCBox.stateChanged.connect(lambda:a("gpu_model"))
		self.gpu_driverCBox.stateChanged.connect(lambda:a("vulkan_driver"))
		
		# cpu
		self.cpu_Line.textChanged.connect(lambda:a("cpu_text"))
		self.cpu_av_loadCBox.stateChanged.connect(lambda:a("cpu_load"))
		self.cpu_by_coreCBox.stateChanged.connect(lambda:a("cpu_by_core"))
		self.cpu_tempCBox.stateChanged.connect(lambda:a("cpu_temp"))
		
		# other/misc
		self.o_ioCBox.stateChanged.connect(lambda:a("io_read"))
		self.o_iowCBox.stateChanged.connect(lambda:a("io_write"))
		self.other_ramCBox.stateChanged.connect(lambda:a("ram"))
		self.other_fpsCBox.stateChanged.connect(lambda:a("fps"))
		self.other_timeCBox.stateChanged.connect(lambda:a("time"))
		self.o_wineCBox.stateChanged.connect(lambda:a("wine"))
		self.other_engineCBox.stateChanged.connect(lambda:a("engine_version"))
		self.other_archCBox.stateChanged.connect(lambda:a("arch"))
		self.other_hud_verCBox.stateChanged.connect(lambda:a("hud_version"))
		self.other_frame_tCBox.stateChanged.connect(lambda:a("frametime"))
		self.other_graph_rButton.toggled.connect(lambda:a("frametime"))
		self.other_histogram_rButton.toggled.connect(lambda:a("frametime"))
		self.other_mediaCBox.stateChanged.connect(lambda:a("music"))
		# VK BASALT (uninplemented yet)
	def run_test(self):
		
		if self.tabWidget.currentIndex() == 0: 
			self.saveConf(self.test_useCBox.currentText())
			subprocess.Popen(["mangohud "+self.test_useCBox.currentText()], shell=True)
			
	def loadConf(self, file):
		

		if file == "General": file = "MangoHud"

		if os.path.isfile(MH_PATH+file+".conf") == 0: # NO PATH 
			mangoFile = open(MH_PATH+file+".conf", "w")
			mangoFile.close()
		
		with open (MH_PATH+file+".conf","r") as f:
			mangoFile = "\n"+f.read()+"\n"

		#---- configs ------------ (add if None to avoid blankfiles and no configured options
		
		# FPS LIMIT
		(a) = parser.get(mangoFile, "fps_limit")
		if a == "0": self.fpsCombox.setCurrentIndex(0) # 0 Index = No fps limit
		elif a=="30" or a=="60" or a=="75" or a=="144" or a=="240":
			self.fpsCombox.setCurrentIndex(self.fpsCombox.findText(a))
		else:
			self.fpsCombox.setCurrentIndex(self.fpsCombox.count()-1)
			self.fpsSpinbox.setEnabled(True)
			self.fpsSpinbox.setValue(int(a))
			
		# FPS VSync
		
		(a) = parser.get(mangoFile, "gl_vsync")
		if a == "-1": self.GLVsyncCombox.setCurrentIndex(0)
		elif a == "0": self.GLVsyncCombox.setCurrentIndex(1)
		elif a == "1": self.GLVsyncCombox.setCurrentIndex(2)
		elif a == "n": self.GLVsyncCombox.setCurrentIndex(3)
		
		(a)=parser.get(mangoFile, "vsync")
		self.VVSyncCombox.setCurrentIndex(int (a))
			
		# HUD & LOG TOGGLE... pos.
		self.hudscCombox.setCurrentText(parser.get(mangoFile, "toggle_hud"))
		self.logCombox.setCurrentText(parser.get(mangoFile, "toggle_logging"))
		if parser.get(mangoFile, "output_folder") == "0": self.logLine.setText(os.environ['HOME'])
		else: self.logLine.setText(parser.get(mangoFile, "output_folder"))
		self.posCombox.setCurrentText(parser.get(mangoFile, "position"))

		
		# GPU box ------------------------
		if parser.get(mangoFile, "gpu_text") == "0": self.gpunameLine.setText("GPU")
		else: self.gpunameLine.setText(parser.get(mangoFile, "gpu_text"))
		self.s_color(self.gpucolorButton, parser.get(mangoFile, "gpu_color"), "2e9762") # se pone el botón a colorear de argumento al inicio + default
		self.gpu_vramCBox.setChecked(int(parser.get(mangoFile, "vram")))
		self.s_color(self.gpu_vram_colorButton, parser.get(mangoFile, "vram_color"), "ad64c1")
		self.other_fpsCBox.setChecked(int(parser.get(mangoFile, "fps")))
		self.gpu_av_loadCBox.setChecked(int(parser.get(mangoFile, "gpu_stats")))
		self.gpu_powerCBox.setChecked(int(parser.get(mangoFile, "gpu_power")))
		self.gpu_tempCBox.setChecked(int(parser.get(mangoFile, "gpu_temp")))
		self.gpu_core_fqCBox.setChecked(int(parser.get(mangoFile, "gpu_core_clock")))
		self.gpu_mem_fqCBox.setChecked(int(parser.get(mangoFile, "gpu_mem_clock")))	
		self.gpu_modelCBox.setChecked(int(parser.get(mangoFile, "gpu_name")))
		self.gpu_driverCBox.setChecked(int(parser.get(mangoFile, "vulkan_driver")))
		
		# CPU box
		if parser.get(mangoFile, "cpu_text") == "0": self.cpu_Line.setText("CPU")
		else: self.cpu_Line.setText(parser.get(mangoFile, "cpu_text"))
		self.s_color(self.cpu_colorButton, parser.get(mangoFile, "cpu_color"), "2e97cb")
		self.cpu_av_loadCBox.setChecked(int(parser.get(mangoFile, "cpu_stats")))
		self.cpu_by_coreCBox.setChecked(int(parser.get(mangoFile, "core_load")))
		self.cpu_tempCBox.setChecked(int(parser.get(mangoFile, "cpu_temp")))
		
		# Other/others
		self.o_ioCBox.setChecked(int(parser.get(mangoFile, "io_read")))
		self.o_iowCBox.setChecked(int(parser.get(mangoFile, "io_write")))
		self.s_color(self.other_diskcolorButton, parser.get(mangoFile, "io_color"), "a491d3")
		self.other_ramCBox.setChecked(int(parser.get(mangoFile, "ram\n")))
		self.s_color(self.other_ramcolorButton, parser.get(mangoFile, "ram_color"),"c26693")
		# "fps" ya hecho arriba
		self.s_color(self.other_enginecolorButton, parser.get(mangoFile, "engine_color"), "eb5b5b")
		self.other_timeCBox.setChecked(int(parser.get(mangoFile, "time\n")))
		self.o_wineCBox.setChecked(int(parser.get(mangoFile, "wine")))
		self.s_color(self.o_winecolorButton, parser.get(mangoFile, "wine_color"), "eb5b5b")
		self.other_engineCBox.setChecked(int(parser.get(mangoFile, "engine_version")))
		self.other_archCBox.setChecked(int(parser.get(mangoFile, "arch")))
		self.other_hud_verCBox.setChecked(int(parser.get(mangoFile, "version")))
		self.other_mediaCBox.setChecked(int(parser.get(mangoFile, "media_player")))
		self.other_mediacomBox.setCurrentText(parser.get(mangoFile, "media_player_name"))
		self.s_color(self.o_mediacolorButton, parser.get(mangoFile, "media_player_color"), "ffffff")
		self.other_frame_tCBox.setChecked(int(parser.get(mangoFile, "frame_timing")))
		self.s_color(self.other_frame_tcolorButton, parser.get(mangoFile, "frametime_color"), "00ff00")
		self.other_histogram_rButton.setChecked(int(parser.get(mangoFile, "histogram")))

		a = parser.get(mangoFile, "font_size")
		if a == "0" or a == "24": self.o_font_sBox.setValue(24)
		else: self.o_font_sBox.setValue(int(a))
		self.s_color(self.o_font_colorButton, parser.get(mangoFile, "text_color"), "ffffff")
		if parser.get(mangoFile, "alpha") == "0": self.o_font_hSlider.setValue(100)
		else: 
			a = int(float(parser.get(mangoFile, "alpha"))*100) # <-- value 0.1 to 1.0... #.#*100 = ###.#... to int = ###
			if a=="100": self.o_font_hLider.setValue(100)
			else: self.o_font_hSlider.setValue(a)
		a = parser.get(mangoFile, "background_color")
		if a == "0": self.s_color(self.o_backg_colorButton, a, "000000")
		else: self.s_color(self.o_backg_colorButton, a, "000000")
		if parser.get(mangoFile, "background_alpha") == "0": self.o_bg_hSlider.setValue(50)
		else:
			a = int(float(parser.get(mangoFile, "background_alpha"))*100)
			if a == 50: pass
			else: self.o_bg_hSlider.setValue(a)
		
		# finishing
		del a

	def remove_config(self, index):
		
		if index == "General": 
			m_Box = QMessageBox()
			m_Box.setIcon(QMessageBox.Information)
			ret=m_Box.information(self, "Remove Prefile", "General profiles can't be removed")
		else :
			m_Box = QMessageBox()
			m_Box.setIcon(QMessageBox.Warning)
			ret = m_Box.question(self,'Remove Profile', 'Are you sure to remove "'+index+'" config?\nAction cannot be reversed.', m_Box.Yes | m_Box.No)
			if ret == m_Box.Yes:
				subprocess.run(["rm "+MH_PATH+index+".conf"], shell=True)
				self.conf_comBox.removeItem(self.conf_comBox.currentIndex())
				self.conf_comBox.setCurrentIndex(0)
			else: pass
			
	def add_config(self):
		i_d = QInputDialog()
		texto = i_d.getText(self, "Add New Profile", 'Insert name of app (process title)\nfor wine app use: wine-"nameapp" (no ".exe"): ')
		if texto[1] == True: 
			if self.conf_comBox.findText(texto[0]) != -1 or texto[0] == "MangoHud":
				QMessageBox().information(self, "Add New Profile", "Can't insert"+texto[0]+"\nDuplicate or General/MangoHud problem (are the same file)")

			else: self.conf_comBox.addItem(texto[0]), self.conf_comBox.setCurrentText(texto[0])
		
			
	def fps_limit(self):
		if self.fpsCombox.currentText() == "Custom":
			self.fpsSpinbox.setEnabled(True)
		else: self.fpsSpinbox.setEnabled(False)
		
	def selectFile(self):
		a=self.logLine.text()
		self.logLine.setText(QFileDialog.getExistingDirectory(self, "Select directory", os.environ['HOME']))
		if self.logLine.text() == "": self.logLine.setText(a)
		
	def _unblank(self, line, text):
		if line.text() == "": line.setText(text)
	
	def colorButtonU(self, button, *args):

		gpu_color = QColorDialog().getColor(QColor(button.palette().color(QtGui.QPalette.Base)))
		if (gpu_color.isValid()):
			button.setStyleSheet('QPushButton {background-color: '+gpu_color.name()+'; color: black;}')

			for i in range (len(args)):
				
				a=args[i].styleSheet()
				b=a.rfind("#")
				if a[b+9:b+10] == ";":
					args[i].setStyleSheet(a.replace(a[b+3:b+9], gpu_color.name()[1:]))
				else:
					args[i].setStyleSheet(a.replace(a[b:b+8], gpu_color.name()))
		
	def s_color (self, button, color, d_color):
		
		if color != "0" and color != "1":	button.setStyleSheet('QPushButton {background-color: #'+color+'; color: black;}')
		else:	button.setStyleSheet('QPushButton {background-color: #'+d_color+'; color: black;}')
		
	def hud_colors (self, color1, *color2):
		
		a=color1.styleSheet()
		b=a.rfind("#")
		color1 = a[b:b+8]

		for i in range (len(color2)):
			a=color2[i].styleSheet()
			b=a.rfind("#")
			if a[b+9:b+10] == ";": color2[i].setStyleSheet(a.replace(a[b+3:b+10], color1[1:]))
			else:color2[i].setStyleSheet(a.replace(a[b:b+8], color1))
			
####################### hud preview $#####################

	def preview_u(self, string):
			
		if string == "load": #ONLY ON LOAD
			# coloreable labels (+1) again -_-

			cpu_color_labels = self.hud_cpu,self.hud_cpu2 
			engine_color_labels = self.hud_engine, self.hud_engine_verL, self.hud_modelL, self.hud_vulkan_driverL, self.hud_archL, self.hud_ftimeL
			text_color_labels = self.hud_hud_versionL, self.hud_gpu_usageL, self.hud_cpu_tempL, self.hud_gpu_clockL, self.hud_gpu_wattsL, self.hud_gpu_tempL, self.hud_cpu_usageL, self.hud_cpu_tempL, self.hud_cpu_usage2, self.hud_cpu_clockL, self.hud_io_readL,  self.hud_io_writeL, self.hud_vram_useL, self.hud_vram_clockL, self.hud_ram_useL, self.hud_engine_fpsL, self.hud_engine_msL
			self.hud_colors(self.gpu_vram_colorButton, self.hud_vram)
			self.hud_colors(self.other_diskcolorButton, self.hud_ioL)
			self.hud_colors(self.other_ramcolorButton, self.hud_ramL)
			self.hud_colors(self.o_font_colorButton, *text_color_labels)
			self.hud_colors(self.other_enginecolorButton, *engine_color_labels)
			self.hud_colors(self.o_backg_colorButton, self.HUD_rectangle)
			self.hud_colors(self.gpucolorButton, self.hud_GPU)
			self.hud_colors(self.other_frame_tcolorButton, self.hud_frame_gL)
			self.hud_colors(self.cpu_colorButton, *cpu_color_labels)
			self.hud_colors(self.o_winecolorButton, self.hud_wineL)
			
		if string == "load" or string == "position":
			
			a=self.posCombox.currentText()
			tl=self.hud_wtop, self.hud_wleft
			tr=self.hud_wtop, self.hud_wright
			bl=self.hud_wbuttom, self.hud_wleft
			br=self.hud_wbuttom, self.hud_wright
			if a == "top-left": self.hide_all(tl), self.show_all(br)
			if a == "top-right": self.hide_all(tr), self.show_all(bl)
			if a == "buttom-left": self.hide_all(bl), self.show_all(tr)
			if a == "buttom-right": self.hide_all(br), self.show_all(tl)
			
					
		if string == "hud_version" or string == "load": self.hud_hud_versionL.setVisible(self.other_hud_verCBox.isChecked())
		if string == "time" or string == "load": self.hud_timeL.setVisible(self.other_timeCBox.isChecked())

		# gpu
		
		if string == "gpu_text" or string == "load": self.hud_GPU.setText(self.gpunameLine.text())
			
		if string == "gpu_av_load" or string =="load":
			a = self.hud_GPU, self.hud_gpu_usageL, self.hud_gpu_tempL, self.hud_gpu_wattsL, self.hud_gpu_clockL
			if self.gpu_av_loadCBox.isChecked() == False: self.hide_all(a)
			else: 
				self.show_all(a)
				self.hud_gpu_wattsL.setVisible(self.gpu_powerCBox.isChecked())
				self.hud_gpu_clockL.setVisible(self.gpu_core_fqCBox.isChecked())
				
		
		if string == "gpu_temp" or string == "load": self.hud_gpu_tempL.setVisible(self.gpu_tempCBox.isChecked())
			
		if string == "gpu_core" or string == "load":
			if self.gpu_core_fqCBox.isChecked() == False: 
				self.hud_gpu_clockL.hide()
				if self.gpu_powerCBox.isChecked() == True:
					self.hud_gpu_clockL.setText("75<sup>w"), self.hud_gpu_clockL.show(), self.hud_gpu_wattsL.hide()
			else:
				self.hud_gpu_clockL.setText("1200<sup>Mhz"), self.hud_gpu_clockL.show()
				if self.gpu_powerCBox.isChecked()==True: self.hud_gpu_wattsL.show()

		if string == "gpu_watts" or string == "load":
			if self.gpu_powerCBox.isChecked() == False: 
				self.hud_gpu_wattsL.hide()
				if self.gpu_core_fqCBox.isChecked() == False: self.hud_gpu_clockL.hide()
			else:
				self.hud_gpu_wattsL.show()
				if self.gpu_core_fqCBox.isChecked() == False:
					self.hud_gpu_wattsL.hide(), self.hud_gpu_clockL.setText("75<sup>w"), self.hud_gpu_clockL.show()
		
		if string == "vram" or string == "load":
			a=self.gpu_vramCBox.isChecked()
			self.hud_vram.setVisible(a), self.hud_vram_useL.setVisible(a)
			if self.gpu_mem_fqCBox.isEnabled() == True: self.hud_vram_clockL.setVisible(self.gpu_mem_fqCBox.isChecked())
			else: self.hud_vram_clockL.setVisible(self.gpu_mem_fqCBox.isEnabled())
			
		if string == "vram_clock" or string == "load":
			a=self.gpu_vramCBox.isChecked()
			if a == False:  self.hud_vram_clockL.setVisible(a)
			else:self.hud_vram_clockL.setVisible(self.gpu_mem_fqCBox.isChecked())
			
		# cpu 
		if string == "cpu_text" or string == "load": self.hud_cpu.setText(self.cpu_Line.text()) 
		if string == "cpu_load" or string == "cpu_temp" or string == "cpu_by_core" or string == "load" :
			a = self.hud_cpu, self.hud_cpu_usageL, self.hud_cpu_tempL
			for i in range (len(a)):
				a[i].setVisible(self.cpu_av_loadCBox.isChecked())
			a=self.hud_cpu2,self.hud_cpu_usage2,self.hud_cpu_clockL
			for i in range (len(a)):
				a[i].setVisible(self.cpu_by_coreCBox.isChecked() and self.cpu_by_coreCBox.isEnabled())
			self.hud_cpu_tempL.setVisible(self.cpu_tempCBox.isChecked() and self.cpu_tempCBox.isEnabled())

		# other/misc
		if string == "io_read" or string == "io_write" or string == "load":
			a=self.o_ioCBox.isChecked()
			b=self.o_iowCBox.isChecked()
			self.hud_io_readL.setVisible(a)
			self.hud_io_writeL.setVisible(b)
			if a == False and b == False: self.hud_ioL.hide()
			if a == True or b == True: self.hud_ioL.setText("IO RW"),self.hud_ioL.show()
			if a == True and b == False: self.hud_ioL.setText("IO RD")
			if a == False and b == True: self.hud_ioL.setText("IO WR")
		
		if string == "ram" or string == "load":
			self.hud_ramL.setVisible(self.other_ramCBox.isChecked()), self.hud_ram_useL.setVisible(self.other_ramCBox.isChecked())
			
		if string == "fps" or string == "load":
			a=self.hud_engine, self.hud_engine_fpsL, self.hud_engine_msL
			if self.other_fpsCBox.isChecked() == False: 
				self.hide_all(a)
				if self.other_engineCBox.isChecked() == True: self.hud_engine.show()
			else: self.show_all(a)
		if string == "wine" or string == "load": self.hud_wineL.setVisible(self.o_wineCBox.isChecked())
			
		if string == "engine_version" or string == "load": 
			self.hud_engine_verL.setVisible(self.other_engineCBox.isChecked())
			if self.other_fpsCBox.isChecked() == False: self.hud_engine.setVisible(self.other_engineCBox.isChecked())
			
		if string == "gpu_model" or string == "load": self.hud_modelL.setVisible(self.gpu_modelCBox.isChecked())
		if string == "vulkan_driver" or string == "load": self.hud_vulkan_driverL.setVisible(self.gpu_driverCBox.isChecked())
		if string == "arch" or string == "load": self.hud_archL.setVisible(self.other_archCBox.isChecked())
		if string == "frametime" or string == "load":
			a=self.hud_ftimeL, self.hud_ftime_msL, self.hud_frame_gL
			if self.other_frame_tCBox.isChecked() == False: self.hide_all(a)
			else: 
				self.show_all(a)
				if self.other_histogram_rButton.isChecked() == True: self.hud_frame_gL.setText("█▄█▄▄██▄▄▄█▄█ ██▄█▄")
				else: self.hud_frame_gL.setText("------------------------------")
		if string == "music" or string == "load": self.hud_mediaL.setVisible(self.other_mediaCBox.isChecked())
		
		if string == "load" or string == "hud_bg_slider":

			alpha=str(hex(int(self.o_bg_hSlider.value()/100*255)))[2:]
			if len(alpha) < 2: alpha="0"+alpha
			a=self.HUD_rectangle.styleSheet()
			b=a.find("#")
			c=a[b:b+3]
			self.HUD_rectangle.setStyleSheet(a.replace(c, "#"+alpha))
		
		a=0
		b=0
		del a, b
			
	def hide_all(self, a):
		for i in range (len(a)):
			a[i].hide()
	
	def show_all(self, a):
		for i in range (len(a)):
			a[i].show()
			

	def saveConf(self, file):
		
		if file == "General": file="MangoHud"
		mangoFile = open(MH_PATH+"."+file+".conf", "w")

		# FPS ------
		
		if self.fpsCombox.currentText() == "Custom":
			mangoFile.write("\nfps_limit="+str(self.fpsSpinbox.value()))
		elif self.fpsCombox.currentText() == "No":
			pass
		else:
			mangoFile.write("\nfps_limit="+self.fpsCombox.currentText())
		# VSync ----
		mangoFile.write("\n"+"gl_vsync=")
		if self.GLVsyncCombox.currentText() == "Adaptive":mangoFile.write("-1")
		if self.GLVsyncCombox.currentText() == "Off":mangoFile.write("0")
		if self.GLVsyncCombox.currentText() == "On":mangoFile.write("1")
		if self.GLVsyncCombox.currentText() == "R/Rate":mangoFile.write("n")
		
		mangoFile.write("\n"+"vsync="+str(self.VVSyncCombox.currentIndex()))
			
		# HUD & log accels
		mangoFile.write("\n"+"toggle_hud="+self.hudscCombox.currentText())
		mangoFile.write("\n"+"toggle_logging="+self.logCombox.currentText())
		mangoFile.write("\n"+"output_folder="+self.logLine.text())
		mangoFile.write("\n"+"position="+self.posCombox.currentText())
		if self.hiddencBox.isChecked() == True: mangoFile.write("\nno_display")
		
		# GPU box 
		if self.other_fpsCBox.isChecked() == False: mangoFile.write("\n"+"fps=0")

		if self.gpunameLine.text() == "": mangoFile.write("\n"+"gpu_text=GPU")
		else:mangoFile.write("\n"+"gpu_text="+self.gpunameLine.text())
		mangoFile.write("\n"+"gpu_color="+self.gpucolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		
		if self.gpu_vramCBox.isChecked() == True:
			mangoFile.write("\n"+"vram")
			mangoFile.write("\n"+"vram_color="+self.gpu_vram_colorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.gpu_av_loadCBox.isChecked() == False: mangoFile.write("\n"+"gpu_stats=0")
		if self.gpu_powerCBox.isChecked() == True: mangoFile.write("\n"+"gpu_power")
		if self.gpu_tempCBox.isChecked() == True: mangoFile.write("\n"+"gpu_temp")
		if self.gpu_core_fqCBox.isChecked() == True: mangoFile.write("\n"+"gpu_core_clock")
		if self.gpu_mem_fqCBox.isChecked() == True: mangoFile.write("\n"+"gpu_mem_clock")
		if self.gpu_modelCBox.isChecked() == True: mangoFile.write("\n"+"gpu_name")
		if self.gpu_driverCBox.isChecked() == True: mangoFile.write("\n"+"vulkan_driver")
		
		# CPU box
		if self.cpu_Line.text() == "": mangoFile.write("\ncpu_text=CPU")
		else: mangoFile.write("\n"+"cpu_text="+self.cpu_Line.text())
		mangoFile.write("\n"+"cpu_color="+self.cpu_colorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.cpu_av_loadCBox.isChecked() == False: mangoFile.write("\n"+"cpu_stats=0")
		if self.cpu_by_coreCBox.isEnabled() == False: pass
		elif self.cpu_by_coreCBox.isChecked() == True: mangoFile.write("\n"+"core_load")
		if self.cpu_tempCBox.isChecked() == True: mangoFile.write("\n"+"cpu_temp")
		
		# Other Box
		a=self.o_ioCBox.isChecked()
		b=self.o_iowCBox.isChecked()
		
		if a == True or b == True: 
			
			if a == True: mangoFile.write("\nio_read")
			if b == True: mangoFile.write("\nio_write")	
			mangoFile.write("\nio_color="+self.other_diskcolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
			
			
		if self.other_ramCBox.isChecked() == True: mangoFile.write("\nram"), mangoFile.write("\nram_color="+self.other_ramcolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		# fps ya está arriba v:
		if self.other_timeCBox.isChecked() == True: mangoFile.write("\ntime")
		
		if self.o_wineCBox.isChecked() == True: mangoFile.write("\nwine"), mangoFile.write("\nwine_color="+self.o_winecolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.other_engineCBox.isChecked() == True: mangoFile.write("\nengine_version")
		mangoFile.write("\nengine_color="+self.other_enginecolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.other_archCBox.isChecked() == True: mangoFile.write("\narch")
		if self.other_hud_verCBox.isChecked() == True: mangoFile.write("\nversion")
		if self.other_mediaCBox.isChecked() == True: mangoFile.write("\nmedia_player\nmedia_player_name="+self.other_mediacomBox.currentText()+"\nmedia_player_color="+self.o_mediacolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.other_frame_tCBox.isChecked() == False: mangoFile.write("\nframe_timing=0")
		else:
			mangoFile.write("\nframe_timing\nframetime_color="+self.other_frame_tcolorButton.palette().color(QtGui.QPalette.Base).name()[1:])
			if self.other_histogram_rButton.isChecked() == True: mangoFile.write("\nhistogram")
		# HUD config.
		if self.o_font_sBox.value() != 24: mangoFile.write("\nfont_size="+str(self.o_font_sBox.value()))
		mangoFile.write("\ntext_color="+self.o_font_colorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		mangoFile.write("\nbackground_color="+self.o_backg_colorButton.palette().color(QtGui.QPalette.Base).name()[1:])
		if self.o_bg_hSlider.value() != 50: mangoFile.write("\nbackground_alpha="+str(self.o_bg_hSlider.value()/100))
		if self.o_font_hSlider.value() != 100: mangoFile.write("\nalpha="+str(self.o_font_hSlider.value()/100))
		# END
		
		mangoFile.write("\n")
		mangoFile.close()
		subprocess.run(["mv "+MH_PATH+"."+file+".conf "+MH_PATH+file+".conf"], shell=True)
	
	def closeEvent(self, e):
			
		# Write window size and position to config file
		self.settings.setValue("size", self.size())
		self.settings.setValue("pos", self.pos())
		e.accept()
			
	
class AboutDialog (QDialog):
	
	def __init__(self,*args):
		super(AboutDialog, self).__init__(*args)
		uic.loadUi(OWN_PATH+"/about.ui", self)
		self.label.setOpenExternalLinks(True)

if __name__=='__main__':
	app = QApplication(sys.argv)
	try: setproctitle ("loverlay")
	except: pass
	GUI = MainControl()

	GUI.show()
	sys.exit(app.exec_())
