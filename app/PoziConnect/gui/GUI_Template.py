# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 14 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import agw.hyperlink

ID_VERSION = 1000
ID_SCROLLED_WINDOW = 1001
ID_TASK_SELECT = 1002
ID_TASK_DESC = 1003
ID_EXAMPLE_LABEL = 1004
ID_EXAMPLE_FIELD = 1005
ID_STATUS_TEXT = 1006
ID_GAUGE = 1007

###########################################################################
## Class Main
###########################################################################

class Main ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlaceLab", pos = wx.DefaultPosition, size = wx.Size( 694,424 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 10, 70, 90, 90, False, "Verdana" ) )
		self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		headerSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.logoBitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"PlaceLabBanner.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		headerSizer.Add( self.logoBitmap, 0, wx.ALL, 5 )
		
		self.iconBitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"PlaceLabIcon.ico", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.iconBitmap.Hide()
		
		headerSizer.Add( self.iconBitmap, 0, wx.ALL, 5 )
		
		headerSizerRight = wx.BoxSizer( wx.VERTICAL )
		
		self.headerSizerSpacerText = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,5 ), 0 )
		self.headerSizerSpacerText.Wrap( -1 )
		headerSizerRight.Add( self.headerSizerSpacerText, 0, wx.ALL, 5 )
		
		self.helpLink = agw.hyperlink.HyperLinkCtrl(parent=self, pos=(225, 60))
		self.helpLink.SetURL(URL='http://www.groundtruth.com.au/pozi-connect-admin-guide/')
		self.helpLink.SetLabel(label='Help')
		self.helpLink.SetToolTipString(tip='Visit website for help')
		headerSizerRight.Add( self.helpLink, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.aboutLink = agw.hyperlink.HyperLinkCtrl(parent=self, pos=(225, 60))
		self.aboutLink.SetURL(URL='http://www.groundtruth.com.au/pozi-connect/')
		self.aboutLink.SetLabel(label='About')
		self.aboutLink.SetToolTipString(tip='Visit website for more info')
		headerSizerRight.Add( self.aboutLink, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		headerSizerRight.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.versionText = wx.StaticText( self, ID_VERSION, u"Version 0.99.x", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.versionText.Wrap( -1 )
		headerSizerRight.Add( self.versionText, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		headerSizer.Add( headerSizerRight, 1, wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		
		mainSizer.Add( headerSizer, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.scrolledWindow = wx.ScrolledWindow( self, ID_SCROLLED_WINDOW, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.scrolledWindow.SetScrollRate( 5, 5 )
		fieldsSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		fieldsSizer.AddGrowableCol( 1 )
		fieldsSizer.SetFlexibleDirection( wx.BOTH )
		fieldsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		self.taskLabel = wx.StaticText( self.scrolledWindow, wx.ID_ANY, u"Task", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.taskLabel.Wrap( -1 )
		fieldsSizer.Add( self.taskLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		taskSelectChoices = []
		self.taskSelect = wx.Choice( self.scrolledWindow, ID_TASK_SELECT, wx.DefaultPosition, wx.DefaultSize, taskSelectChoices, 0 )
		self.taskSelect.SetSelection( 0 )
		fieldsSizer.Add( self.taskSelect, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fieldsSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.descriptionText = wx.StaticText( self.scrolledWindow, ID_TASK_DESC, u"Example Description", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.descriptionText.Wrap( -1 )
		fieldsSizer.Add( self.descriptionText, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.exampleLabel = wx.StaticText( self.scrolledWindow, ID_EXAMPLE_LABEL, u"Example Label", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.exampleLabel.Wrap( -1 )
		fieldsSizer.Add( self.exampleLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.exampleField = wx.TextCtrl( self.scrolledWindow, ID_EXAMPLE_FIELD, u"Example Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.exampleField.SetMaxLength( 0 ) 
		fieldsSizer.Add( self.exampleField, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.scrolledWindow.SetSizer( fieldsSizer )
		self.scrolledWindow.Layout()
		fieldsSizer.Fit( self.scrolledWindow )
		mainSizer.Add( self.scrolledWindow, 1, wx.ALL|wx.EXPAND, 5 )
		
		footerSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.horizontalLine = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		footerSizer.Add( self.horizontalLine, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.statusText = wx.StaticText( self, ID_STATUS_TEXT, u"Processing Items...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.statusText.Wrap( -1 )
		footerSizer.Add( self.statusText, 0, wx.ALL, 5 )
		
		controlSizer = wx.FlexGridSizer( 2, 3, 0, 0 )
		controlSizer.AddGrowableCol( 0 )
		controlSizer.SetFlexibleDirection( wx.HORIZONTAL )
		controlSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.gauge = wx.Gauge( self, ID_GAUGE, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		controlSizer.Add( self.gauge, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		controlSizer.AddSpacer( ( 100, 0), 1, wx.EXPAND, 5 )
		
		buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.buttonStart = wx.Button( self, wx.ID_OK, u"&Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		buttonSizer.Add( self.buttonStart, 0, wx.ALL, 5 )
		
		self.buttonClose = wx.Button( self, wx.ID_CLOSE, u"&Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		buttonSizer.Add( self.buttonClose, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		controlSizer.Add( buttonSizer, 1, wx.ALIGN_RIGHT, 5 )
		
		
		footerSizer.Add( controlSizer, 1, wx.EXPAND, 5 )
		
		
		mainSizer.Add( footerSizer, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( mainSizer )
		self.Layout()
		
		self.Centre( wx.HORIZONTAL )
		
		# Connect Events
		self.taskSelect.Bind( wx.EVT_CHOICE, self.OnTaskSelect )
		self.buttonStart.Bind( wx.EVT_BUTTON, self.OnStart )
		self.buttonClose.Bind( wx.EVT_BUTTON, self.OnClose )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnTaskSelect( self, event ):
		event.Skip()
	
	def OnStart( self, event ):
		event.Skip()
	
	def OnClose( self, event ):
		event.Skip()
	

