#!/usr/bin/env python
# -*- coding: utf-8  -*-

###############################################################################
# This file is part of gLapse.                                                #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# any later version.                                                          #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
# Copyright (C) 2011, David Saltares Márquez, <david.saltares@gmail.com>      #
###############################################################################

import os
import gtk
from gettext import gettext as _

from glapse import glapseMain

class GlapseMainGUI:
    
    def __init__(self):
	
	# Version
	self.version = 0.1
	
	print ''
	print 'gLapse v0.1 - Take screenshots, glue them together'
	print '=================================================='
	print ''
	
	print 'Initialising GUI...'
	
	# Get Builder
        builder = gtk.Builder()
        
        # Set path to find Glade file
        path = os.path.dirname(__file__) + '/../data/glade/glapseGUI.glade'
		
        # Build file from Glade file
        builder.add_from_file(path)
		
        # Get objects
	self.window = builder.get_object('wndGlapse')
	self.imgLogo = builder.get_object('imgLogo')
	self.lblStatus = builder.get_object('lblStatus')
        self.btnScrOutput = builder.get_object('btnScrOutput')
	self.txtScrOutput = builder.get_object('txtScrOutput')
        self.spinScrQuality = builder.get_object('spinScrQuality')
        self.spinScrInterval = builder.get_object('spinScrInterval')
        self.btnScrStart = builder.get_object('btnScrStart')
        self.btnScrStop = builder.get_object('btnScrStop')
        self.btnVideoInput = builder.get_object('btnVideoInput')
	self.txtVideoInput = builder.get_object('txtVideoInput')
        self.btnVideoOutput = builder.get_object('btnVideoOutput')
	self.txtVideoOutput = builder.get_object('txtVideoOutput')
        self.spinVideoFPS = builder.get_object('spinVideoFPS')
        self.btnMakeVideo = builder.get_object('btnMakeVideo')
	
	
	self.dlgError = builder.get_object('dlgError')
	self.msgOverwrite = builder.get_object('msgOverwrite')
	self.aboutDlg = builder.get_object('aboutDlg')
		
        # Connect signals
	builder.connect_signals(self)
	
	# Get controller class
	self.controller = glapseMain.GlapseMain()
	
	# Load logo and icon
	self.imgLogo.set_from_file(os.path.dirname(__file__) + '/../data/img/glapse-icon-small.png')
	self.window.set_icon_from_file(os.path.dirname(__file__) + '/../data/img/glapse-icon-small.png')
	#self.aboutDlg.set_logo_icon_name(os.path.dirname(__file__) + '/../data/img/glapse-icon-small.png')
	
	# Default spin buttons value
	self.spinScrInterval.set_value(5);
	self.spinScrQuality.set_value(80);
	self.spinVideoFPS.set_value(10);
	
	# Default path
	self.txtScrOutput.set_text(os.getenv('HOME'))
	self.txtVideoInput.set_text(os.getenv('HOME'))
	self.txtVideoOutput.set_text(os.getenv('HOME') + os.sep + 'timelapse.mp4')
	
	# Disable stop screenshots
	self.btnScrStop.set_sensitive(False)
	
	print 'GUI Loaded.'
	
    
    def onDestroy(self, widget):
	
	print 'Closing gLapse...'
	
	gtk.main_quit()
		
    def onBtnScrOutputClicked(self, widget):
	action =  gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
	title = _('Screenshots output folder')

        chooser = gtk.FileChooserDialog(title = title, parent = None, action = action, buttons = buttons, backend = None)
        chooser.set_current_folder(os.getenv('HOME'))
	
	if chooser.run() == gtk.RESPONSE_OK:
            self.txtScrOutput.set_text(chooser.get_filename())
	
	chooser.destroy()
	
    def onBtnVideoInputClicked(self, widget):
	action =  gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
	title = _('Video input folder')

        chooser = gtk.FileChooserDialog(title = title, parent = None, action = action, buttons = buttons, backend = None)
	chooser.set_current_folder(os.getenv('HOME'))
        
	if chooser.run() == gtk.RESPONSE_OK:
            self.txtVideoInput.set_text(chooser.get_filename())
	
	chooser.destroy()
	
    def onBtnVideoOutputClicked(self, widget):
	action =  gtk.FILE_CHOOSER_ACTION_SAVE
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK)
	title = _('Video output file')

        chooser = gtk.FileChooserDialog(title = title, parent = None, action = action, buttons = buttons, backend = None)
        chooser.set_current_folder(os.getenv('HOME'))
	chooser.set_current_name('timelapse.mp4')
	
	fileFilter = gtk.FileFilter()
	fileFilter.add_pattern('*.mp4')
	fileFilter.set_name(_('MP4 files'))
	
	chooser.add_filter(fileFilter)
	
	if chooser.run() == gtk.RESPONSE_OK:
            self.txtVideoOutput.set_text(chooser.get_filename())
	
	chooser.destroy()
	
    def onBtnScrStartClicked(self, widget):
	# Get options
	output = self.txtScrOutput.get_text()
	quality = self.spinScrQuality.get_value()
	interval = self.spinScrInterval.get_value()
	
	checkList = True
	
	# Check folder existence
	if not os.path.exists(output):
	    checkList = False
	    self.dlgError.set_title(_('Folder not found'))
	    self.dlgError.set_markup(_('<b>%s does not exist</b>') % (output))
	    self.dlgError.format_secondary_text(_('Please, select a valid output folder'))
	    self.dlgError.run()
	    self.dlgError.hide()
	    
	
	# Search folder for possible file overwrite
	if checkList and self.controller.getPossibleOverwrite(output):
	    if self.msgOverwrite.run() == gtk.RESPONSE_NO:
		checkList = False
	    
	    self.msgOverwrite.hide()
	    
	
	# If everything is correct
	if checkList:
	    # Disable start, enable stop
	    self.btnScrStart.set_sensitive(False)
	    self.btnScrStop.set_sensitive(True)
	    
	    # Set status
	    self.lblStatus.set_text(_('Taking screenshots...'))
	    
	    # Call controller
	    self.controller.startScreenshots(output, quality, interval)
	
    def onBtnScrStopClicked(self, widget):
	# Disable stop, enable start
	self.btnScrStop.set_sensitive(False)
	self.btnScrStart.set_sensitive(True)
	
	# Set status
	self.lblStatus.set_text(_('Idle'))
	
	# Call controller
	self.controller.stopScreenshots()
	
    def onBtnAboutClicked(self, widget):
	#Show about dialog
	self.aboutDlg.run()
	self.aboutDlg.hide()
	
    def onBtnMakeVideoClicked(self, widget):
	# Get options
	videoInput = self.txtVideoInput.get_text()
	videoOutput = self.txtVideoOutput.get_text()
	videoFPS = self.spinVideoFPS.get_value()
	
	checkList = True
	
	# Check if input folder exists
	if not os.path.exists(videoInput):
	    checkList = False
	    self.dlgError.set_title(_('Folder not found'))
	    self.dlgError.set_markup(_('<b>%s does not exist</b>') % (output))
	    self.dlgError.format_secondary_text(_('Please, select a valid input folder'))
	    self.dlgError.run()
	    self.dlgError.hide()
	
	# Check if output folder exists
	(outputPath, outputFile) = os.path.split(videoOutput)
	if not os.path.exists(outputPath):
	    checkList = False
	    self.dlgError.set_title(_('Folder not found'))
	    self.dlgError.set_markup(_('<b>%s does not exist</b>') % (output))
	    self.dlgError.format_secondary_text(_('Please, select a valid input folder'))
	    self.dlgError.run()
	    self.dlgError.hide()
	    
	# Check video overwrite
	
	# If everything is right
	if checkList:
	    # Chanche status bar
	    self.lblStatus.set_text(_('Creating video...'))
	    # Call controller
	    self.controller.makeVideo(self, videoInput,videoOutput, videoFPS)
	
    def onMakeVideoFinished(self):
	# Chanche status bar
	self.lblStatus.set_text(_('Idle'))
    
    def _isExecutable(self, filePath):
	return os.path.exists(filePath) and os.access(filePath, os.X_OK)
	
    def _which(self, program):
	filePath, fileName = os.path.split(program)
	
	if filePath and self._isExecutable(program):
	    return True
	else:
	    for path in os.environ['PATH'].split(os.pathsep):
		exeFile = os.path.join(path, program)
		if self._isExecutable(exeFile):
		    return True
	
	return False
    
    def checkDependencies(self):
	# Check wether all dependencies are installed or not
	dependencies = ('ffmpeg', 'scrot')
	
	for dependence in dependencies:
	    if not self._which(dependence):
		self.dlgError.set_title(_('Dependencies error'))
		self.dlgError.set_markup(_('<b>%s was not found</b>') % (dependence))
		self.dlgError.format_secondary_text(_('Please, install the package and launch gLapse again'))
		self.dlgError.run()
		self.dlgError.destroy()
		return False
	
	return True
