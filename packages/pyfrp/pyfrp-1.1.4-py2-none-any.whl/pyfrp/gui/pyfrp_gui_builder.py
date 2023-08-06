#=====================================================================================================================================
#Copyright
#=====================================================================================================================================

#Copyright (C) 2014 Alexander Blaessle, Patrick Mueller and the Friedrich Miescher Laboratory of the Max Planck Society
#This software is distributed under the terms of the GNU General Public License.

#This file is part of PyFRAP.

#PyFRAP is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#===========================================================================================================================================================================
#Module Description
#===========================================================================================================================================================================

#Basic module used for gui construction. Contains simple functions that help to easily construct commonly used small widgets and aligments.

#===========================================================================================================================================================================
#Importing necessary modules
#===========================================================================================================================================================================

#Misc
import sys
import time
import os, os.path

#PyFRAP modules
from pyfrp.modules.pyfrp_term_module import *

#PyQT
from PyQt4 import QtGui, QtCore

#===========================================================================================================================================================================
#Module function
#===========================================================================================================================================================================

def genSettingQLE(parent,lblText,qleText,callback=None,validator=None):
	
	"""Generates ``QLabel`` and ``QLineEdit`` with given label and connects 
	to correct callback.
	
	.. note:: ``QLineEdit`` is conncect with ``editingFinished`` slot.
	
	Args:
		parent (QtGui.QWidget): Some parenting widget.
		lblText (str): Text displayed in label.
		qleText (str): Text displayed initially in qle.
	
	Keyword Args:
		callback (function): Some callback function.
		validator (QtGui.QValidator): Some validator.
		
	Returns:
		tuple: Tuple containing:
		
			* lbl (QtGui.QLabel): Label.
			* qle (QtGui.QLineEdit): Lineedit.
			
	"""
	
	lbl = QtGui.QLabel(lblText, parent)
	qle = QtGui.QLineEdit(str(qleText),parent=parent)
	
	if validator!=None:
		qle.setValidator(validator)
	
	if callback!=None:
		qle.editingFinished.connect(callback)
	
	return lbl,qle

def genSettingCB(parent,lblText,cbVal,callback=None):
	
	"""Generates ``QLabel`` and ``QCheckbox`` with given label and connects 
	to correct callback.
	
	.. note:: ``QCheckBox`` is conncect with ``stateChanged`` slot.
	
	Args:
		parent (QtGui.QWidget): Some parenting widget.
		lblText (str): Text displayed in label.
		cbVal (bool): Checked or not.
	
	Keyword Args:
		callback (function): Some callback function.
	
	Returns:
		tuple: Tuple containing:
		
			* lbl (QtGui.QLabel): Label.
			* cb (QtGui.QCheckBox): Checkbox.
			
	"""
	
	lbl = QtGui.QLabel(lblText, parent)
	cb = QtGui.QCheckBox('', parent)
	cb.setCheckState(2*int(cbVal))
	
	if callback!=None:
		parent.connect(cb, QtCore.SIGNAL('stateChanged(int)'), callback)
	
	return lbl,cb

def genSettingBtn(parent,lblText,btnText,callback=None):
	
	"""Generates ``QLabel`` and ``QPushButton`` with given label and connects 
	to correct callback.
	
	.. note:: ``QPushButton`` is conncect with ``clicked`` slot.
	
	Args:
		parent (QtGui.QWidget): Some parenting widget.
		lblText (str): Text displayed in label.
		btnText (str): Text displayed on button.
	
	Keyword Args:
		callback (function): Some callback function.
		
	Returns:
		tuple: Tuple containing:
		
			* lbl (QtGui.QLabel): Label.
			* btn (QtGui.QPushButton): Push button.
			
	"""
	
	lbl = QtGui.QLabel(lblText, parent)
	btn=QtGui.QPushButton(btnText)
		
	if callback!=None:
		btn.connect(btn, QtCore.SIGNAL('clicked()'), callback)
	
	return lbl,btn

def genSettingCombo(parent,lblText,comboList,callback=None,idx=0):
	
	"""Generates ``QLabel`` and ``QPushButton`` with given label and connects 
	to correct callback.
	
	.. note:: ``QPushButton`` is conncect with ``clicked`` slot.
	
	Args:
		parent (QtGui.QWidget): Some parenting widget.
		lblText (str): Text displayed in label.
		comboList (list): List of strings that are added to QComboBox.
	
	Keyword Args:
		callback (function): Some callback function.
		idx (int): Starting index of combo.
		
	Returns:
		tuple: Tuple containing:
		
			* lbl (QtGui.QLabel): Label.
			* combo (QtGui.QComboBox): Combobox.
			
	"""
	
	lbl = QtGui.QLabel(lblText, parent)
	combo=QtGui.QComboBox(parent)
	
	for x in comboList:
		combo.addItem(x)
	
	if callback!=None:
		combo.activated[str].connect(callback)   
	
	combo.setCurrentIndex(idx)
	
	return lbl,combo





		
