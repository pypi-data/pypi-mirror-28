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

#PyQT Editor for gmsh geo files used in PyFRAP
#(1) gmshEditor
#(2) gmshHighlighter


#===========================================================================================================================================================================
#Importing necessary modules
#===========================================================================================================================================================================

#QT
from PyQt4 import QtGui, QtCore

#PyFRAP modules
from pyfrp.modules.pyfrp_term_module import *

#===================================================================================================================================
#Dialog for editing embryo datasets
#===================================================================================================================================



class gmshFileEditor(QtGui.QDialog):
	
	def __init__(self,geometry,parent):
		
		super(gmshFileEditor,self).__init__(parent)
	
		self.geometry=geometry
	
		#Bookkeeping
		self.currFn=None
		
		#Buttons
		self.btnDone=QtGui.QPushButton('Done')	
		self.btnDone.connect(self.btnDone, QtCore.SIGNAL('clicked()'), self.donePressed)
		
		self.btnNew=QtGui.QPushButton('New')	
		self.btnNew.connect(self.btnNew, QtCore.SIGNAL('clicked()'), self.newFile)
		
		self.btnOpen=QtGui.QPushButton('Open')	
		self.btnOpen.connect(self.btnOpen, QtCore.SIGNAL('clicked()'), self.openFile)
		
		self.btnSave=QtGui.QPushButton('Save')	
		self.btnSave.connect(self.btnSave, QtCore.SIGNAL('clicked()'), self.saveFile)
		
		self.btnSaveAs=QtGui.QPushButton('Save As')	
		self.btnSaveAs.connect(self.btnSaveAs, QtCore.SIGNAL('clicked()'), self.saveFileAs)
		
		self.btnUse=QtGui.QPushButton('Use for geometry')	
		self.btnUse.connect(self.btnUse, QtCore.SIGNAL('clicked()'), self.useForGeometry)
		
		
		#QTextEdit
		self.editor = QtGui.QTextEdit()
		
		#QHighLight
		self.highlighter=gmshHighlighter(self.editor,'Classic')
		
		#Layout
		self.hbox = QtGui.QHBoxLayout()
		self.hbox.addWidget(self.btnNew)
		self.hbox.addWidget(self.btnOpen)
		self.hbox.addWidget(self.btnSave)
		self.hbox.addWidget(self.btnSaveAs)
		self.hbox.addWidget(self.btnSaveAs)
		self.hbox.addWidget(self.btnUse)
		self.hbox.addWidget(self.btnDone)
		
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.editor)
		self.vbox.addLayout(self.hbox)
		
		self.setLayout(self.vbox)
		
		self.setWindowTitle('Edit Geometry File ')  
		
		self.loadGeoFile()
		
		self.resize(700,500)
	
		self.show()
	
	def openFile(self):
		mdir=pyfrp_misc_module.getMeshfilesDir()
		fn = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', mdir,"*.geo",))
		if fn=='':
			return
		
		self.loadFile(fn)
				
		return fn
		
	def saveFile(self):
		
		if self.currFn!=None:
			self.writeFile(self.currFn)
		else:
			self.saveFileAs()
			
		
	def saveFileAs(self):
		mdir=pyfrp_misc_module.getMeshfilesDir()
		fn=str(QtGui.QFileDialog.getSaveFileName(self, 'Save file', mdir+"newGeo.geo","*.geo",))
		
		self.writeFile(fn)
		
		return
		
	def writeFile(self,fn):
		
		if fn=='':
			printError("Invalid filename, won't save.")
			return
		
		mdir=pyfrp_misc_module.getMeshfilesDir()
		if fn==mdir+"emptyTemplate.geo":
			printError("Cannot overwrite emptyTemplate.geo! Choose a different file name.")
			return
		
		text=str(self.editor.toPlainText())
		
		with open(fn,'wb') as f:	
			f.write(text)
			
		self.currFn=fn
			
		return	
	
		
	def newFile(self):
		mdir=pyfrp_misc_module.getMeshfilesDir()
		try:
			self.loadFile(mdir+'emptyTemplate.geo')
		except:
			printWarning('Cannot load file '+ mdir+'emptyTemplate.geo')
		
		return
		
	def loadGeoFile(self):
		self.loadFile(self.geometry.fnGeo)
		
	def loadFile(self,fn):	
		f=open(fn,'r')
		self.currFn=fn
		text=f.read()
		f.close()
		
		self.editor.setPlainText(text)
		
		self.setWindowTitle('Edit Geometry File ' + fn)  
	
	def useForGeometry(self):
		if self.currFn==None:
			self.saveFileAs()
			
		self.geometry.fnGeo=self.currFn
		
		return
		
	def donePressed(self):
		self.done(1)
		return 

class gmshHighlighter( QtGui.QSyntaxHighlighter ):
	
	#Taken from http://carsonfarmer.com/2009/07/syntax-highlighting-with-pyqt/
	
	def __init__( self, parent, theme ):
		
		#QtGui.QSyntaxHighlighter.__init__( self, parent )
		
		super(gmshHighlighter,self).__init__(parent)
		self.parent = parent
		
		mathExpr = QtGui.QTextCharFormat()
		geomObj = QtGui.QTextCharFormat()
		delimiter = QtGui.QTextCharFormat()
		number = QtGui.QTextCharFormat()
		comment = QtGui.QTextCharFormat()
		string = QtGui.QTextCharFormat()
		singleQuotedString = QtGui.QTextCharFormat()

		self.highlightingRules = []
		
		# Math Expr
		brush = QtGui.QBrush( QtCore.Qt.darkBlue, QtCore.Qt.SolidPattern )
		mathExpr.setForeground( brush )
		mathExpr.setFontWeight( QtGui.QFont.Bold )
		keywords = QtCore.QStringList( [ "Sqrt","Cos","Sin","Arcos","Arsin","Abs"] )
		for word in keywords:
			pattern = QtCore.QRegExp("\\b" + word + "\\b")
			rule = HighlightingRule( pattern, mathExpr )
			self.highlightingRules.append( rule )
			
		# GeomObjects
		brush = QtGui.QBrush( QtCore.Qt.green, QtCore.Qt.SolidPattern )
		geomObj.setForeground( brush )
		geomObj.setFontWeight( QtGui.QFont.Bold )
		keywords = QtCore.QStringList( [ "Point","Circle","Line","Surface","Volume","Line Loop","Surface Loop","Ruled Surface"] )
		for word in keywords:
			pattern = QtCore.QRegExp("\\b" + word + "\\b")
			rule = HighlightingRule( pattern, geomObj )
			self.highlightingRules.append( rule )	
		
		# delimiter
		brush = QtGui.QBrush( QtCore.Qt.gray, QtCore.Qt.SolidPattern )
		pattern = QtCore.QRegExp( "[\)\(]+|[\{\}]+|[][]+" )
		delimiter.setForeground( brush )
		delimiter.setFontWeight( QtGui.QFont.Bold )
		rule = HighlightingRule( pattern, delimiter )
		self.highlightingRules.append( rule )

		# number
		brush = QtGui.QBrush( QtCore.Qt.magenta, QtCore.Qt.SolidPattern )
		pattern = QtCore.QRegExp( "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?" )
		pattern.setMinimal( True )
		number.setForeground( brush )
		rule = HighlightingRule( pattern, number )
		self.highlightingRules.append( rule )

		# comment
		brush = QtGui.QBrush( QtCore.Qt.blue, QtCore.Qt.SolidPattern )
		pattern = QtCore.QRegExp( "//[^\n]*" )
		comment.setForeground( brush )
		rule = HighlightingRule( pattern, comment )
		self.highlightingRules.append( rule )

		# string
		brush = QtGui.QBrush( QtCore.Qt.red, QtCore.Qt.SolidPattern )
		pattern = QtCore.QRegExp( "\".*\"" )
		pattern.setMinimal( True )
		string.setForeground( brush )
		rule = HighlightingRule( pattern, string )
		self.highlightingRules.append( rule )

		# singleQuotedString
		pattern = QtCore.QRegExp( "\'.*\'" )
		pattern.setMinimal( True )
		singleQuotedString.setForeground( brush )
		rule = HighlightingRule( pattern, singleQuotedString )
		self.highlightingRules.append( rule )

	def highlightBlock( self, text ):
		for rule in self.highlightingRules:
			expression = QtCore.QRegExp( rule.pattern )
			index = expression.indexIn( text )
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat( index, length, rule.format )
				index = text.indexOf( expression, index + length )
		self.setCurrentBlockState( 0 )

class HighlightingRule():
	def __init__( self, pattern, format ):
		self.pattern = pattern
		self.format = format




