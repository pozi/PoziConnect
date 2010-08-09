# Make app dir available to the sys path
import sys
sys.path.extend(['.', '..', 'lib','../..'])

import copy
import os
import thread 
import wx
from base64 import b64encode, b64decode

import agw.hyperlink
from lib.taskmanager import * 
from lib.logger import *

# Get version information
from version import version

from multiprocessing import Process

from GUI_Template import *

class GUI(wx.App):
    def __init__(self, options = {}):
        console = options.get('console', 0)
        wx.App.__init__(self, console)

        # Disable any possible error message coming
        # from wxPython (like missing icon files, etc)
        wx.Log.Suspend()

        self.options = {
            'Title': 'PlaceLab',
            'AppWidth' : '700',
            'AppHeight' : 375,
            'EntryWidgetWidth' : 550,
            'FontFace' : 'Verdana',
            'FontSize' : 12,
            'PasswordStrings': [ 'passw', 'pwd' , 'pword' ],
        }

        # Merge default options with ones provided in app INI file
        self.options.update(options)

        # Initialise logger
        loggerName = 'GUI'
        if 'logger' in self.options:
            logger = self.options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

        #####################################################
        # Create Frame (window)
        try:
            frame = GUI_Main(None, self.options)
            self.frame = frame
        except Exception as e:
            self.logger.warn('OJASFDKSFK', e)

        # This makes sure the GUI refreshes itself
        # when new items are added
        frame.SetAutoLayout(True)
        
        #for i in sorted (dir(self.frame)):
            #print i

        #####################################################
        # Icon:
        # Get Icon from executable or, if that fails from template
        try:
            import win32api
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            self.icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        except Exception as e:
            self.logger.debug('Could not get icon from exe. Will use template one')

            # Get icon from the one provided in the template
            self.icon = wx.Icon('icon',wx.BITMAP_TYPE_ICO )

            # Hardcoded file reference. TODO: Fix!
            iconBitmap = wx.Bitmap("app/lib/gui/PlaceLabIcon.ico", wx.BITMAP_TYPE_ANY)
            self.icon.CopyFromBitmap(iconBitmap)
        finally:
            self.frame.SetIcon(self.icon)
        

        #####################################################
        # Logo:
        #####################################################
        import PlaceLabBanner_png
        imageStream = PlaceLabBanner_png.imageStream
        logoBitmap = wx.BitmapFromImage( wx.ImageFromStream( imageStream ))
        frame.logoBitmap.SetBitmap(logoBitmap)

        #####################################################
        # Fill task selector 
        #####################################################
        self.taskList = self.options.get('taskList')
        self.AddTasks(self.taskList) 

        #####################################################
        # Set Version 
        #####################################################
        self.frame.versionText.SetLabel('Version: %s' % version) 


    def AddTasks(self, taskList):
        for taskName, taskFile in taskList:
            self.frame.taskSelect.Append( taskName )
       
        if len(taskList) == 1:
            self.frame.taskSelect.SetSelection(0)
            self.frame.OnTaskSelect()

        if not taskList:
            dial = wx.MessageDialog(None, 'Could not find any task!', 'Error',
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

    def Show(self):
        self.logger.info('Starting GUI...')

        self.frame.Show()

        self.MainLoop()

#####################################################
# Class GUI Main     
#####################################################
class GUI_Main(Main ):
    def __init__( self, parent, options = {} ):
        Main.__init__( self, parent)

        self.options = options

        loggerName = 'GUI Main'
        if 'logger' in self.options:
            logger = self.options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

        # Storage for miscellaneous widgets & buttons (not the OK or Cancel ones)
        self.widgets = []
        self.buttons = []

        #####################################################
        # Clean up template 
        #####################################################
        self.descriptionText.Hide()
        self.exampleLabel.Hide()
        self.exampleField.Hide()
        self.SetStatus()

        # Disable Start button
        self.buttonStart.Disable()

        # Set some values
        # Setting application specific settings from options
        title = self.options['Title']
        self.SetTitle(title)

        appWidth = int(self.options['AppWidth'])
        appHeight = int(self.options['AppHeight'])
        appSize = wx.Size( appWidth, appHeight )
        self.SetSize(appSize)

        entryWidgetWidth = int(self.options['EntryWidgetWidth']) 
        entryWidgetSize = wx.Size(entryWidgetWidth,-1 ) 
        self.options['EntryWidgetSize'] = entryWidgetSize

        fontface = self.options['FontFace']
        fontsize = int(self.options['FontSize'])
        font = wx.Font(fontsize, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, fontface)
        self.SetFont(font)

        
    # Handlers for Main events.
    def OnTaskSelect( self, event = None ):

        # Enable Start button
        self.buttonStart.Enable()

        selection = self.taskSelect.GetSelection()
        self.LoadTask(selection)
        pass
    
    def DirectoryDialog(self, evt):

        self.buttonStart.Enable()

        # Get widget from event
        widget = evt.GetEventObject()

        # Prevent other dialogs while we're busy 
        widget.Disable() 

        # Get folder path from widget and turn
        # it into an absolute path
        path = widget.GetValue()
        abspath = os.path.abspath(path)

        #print path
        #print abspath

        dirDialog = wx.DirDialog(self, "Choose a directory:", abspath, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        # Show dialog and set the new path as a value of the widget
        if dirDialog.ShowModal() == wx.ID_OK:
            newpath = dirDialog.GetPath()
            widget.SetValue(newpath)

        widget.Enable()
        
    def FileDialog(self, evt):

        self.buttonStart.Enable()

        # Get widget from event
        widget = evt.GetEventObject()

        # Prevent other dialogs while we're busy 
        widget.Disable() 

        # Get folder path from widget and turn
        # it into an absolute path
        path = widget.GetValue()
        abspath = os.path.abspath(path)

        defaultDir = os.path.dirname(abspath)
        defaultFile = os.path.basename(abspath)

        dialog = wx.FileDialog(self, "Choose a file:", defaultDir, defaultFile)

        # Show dialog and set the new path as a value of the widget
        if dialog.ShowModal() == wx.ID_OK:
            newpath = dialog.GetPath()
            widget.SetValue(newpath)

        widget.Enable()
        
    def LoadTask(self, id):
        self.logger.debug( "Load task:", id)

        # Get file name from 'parent' object.
        taskList = self.options.get('taskList')

        taskName, taskFile = taskList[id]

        options = {
            'lowerKeys': False,
            'itemsAsDict': False,
            'taskName': taskName,
            'configFile': taskFile,
        }

        try:
            self.task = TaskManager(options)
        except Exception as e:
            print "Can't create task '%s' from file '%s'" % (taskName, taskFile)
      
        # Remove any existing fields from the GUI
        self.ClearGuiItems()

        ##############################################################
        # Task Description
        self.descriptionText.Hide()

        generalSettings = dict(self.task.GetSectionItems('General Settings'))
        taskDescription = generalSettings.get('Description', '').strip()
        if taskDescription:
            self.descriptionText.SetLabel(taskDescription)
            self.descriptionText.Show()

        items = self.task.GetSectionItems('User Settings')
        #print "ITEMS", type(items), items

        #print "EXAMPLE", self.exampleLabel, dir(self.exampleLabel)

        self.fieldsSizer = self.exampleLabel.GetParent()
        self.flexGridSizer = self.fieldsSizer.GetSizer()

        #print "FIELD", self.fieldsSizer
        #print "SIZER", self.flexGridSizer

        for itemKey, defaultValue in items:

            # Replace all underscores with spaces
            labelText = itemKey.replace('_',' ') 

            labelWidget = wx.StaticText( self.scrolledWindow, wx.ID_ANY, labelText, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.flexGridSizer.Add( labelWidget, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
            

            entryWidget = None

            # Fancy function to find out if any of the password strings are 
            # in the itemKey name. If so, this will return true.
            containsPassword = any( [ x in itemKey.lower() for x in self.options.get('PasswordStrings')])

            entryWidgetStyle = 0
            if containsPassword:
                entryWidgetStyle = wx.TE_PASSWORD
                defaultValue = Crypt().Decrypt(defaultValue)

            entryWidgetStyle =  wx.TE_PASSWORD if containsPassword else 0
            entryWidget = wx.TextCtrl( self.scrolledWindow, wx.ID_ANY, defaultValue , wx.DefaultPosition, wx.DefaultSize, entryWidgetStyle)
                
            #entryWidget.SetMinSize( self.entryWidgetSize )
            self.flexGridSizer.Add( entryWidget , 0, wx.ALL|wx.EXPAND, 5 )

            entryWidget.Bind( wx.EVT_SET_FOCUS, self.OnEnableButtonStart)

            # Check if the entry field is a folder field
            # If so, we open a directory selection dialog upon clicking
            # in the field
            folderStrings = ['dir', 'directory', 'folder', 'fldr']
            containsFolder = any( [ itemKey.lower().endswith(x) for x in folderStrings])
            if containsFolder:
                entryWidget.Bind( wx.EVT_SET_FOCUS, self.DirectoryDialog)
                entryWidget.SetEditable(False)

                # Change value to a file path value
                absolutePath = os.path.abspath(defaultValue)
                entryWidget.SetValue(absolutePath)

            # Check if the entry field is a file field
            # If so, we open a file selection dialog upon clicking
            # in the field
            fileStrings = ['file']
            containsFile = any( [ itemKey.lower().endswith(x) for x in fileStrings])
            if containsFile:
                entryWidget.Bind( wx.EVT_SET_FOCUS, self.FileDialog)
                entryWidget.SetEditable(False)

                # Change value to a file path value
                absolutePath = os.path.abspath(defaultValue)
                entryWidget.SetValue(absolutePath)

            # Keep track of widgets. We need to remove them
            # when another task gets selected
            # We store them as tuples in a list
            self.widgets.append((labelWidget, entryWidget, itemKey, defaultValue))

        #######
        # Refresh of window (needed)
        self.flexGridSizer.Layout()
        self.Layout()
            

    def ClearGuiItems(self):
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                # Hide both the labelWidget and the entryWidget
                # in one go
                map(self.flexGridSizer.Hide, (labelWidget, entryWidget))

            self.widgets = []

        if hasattr(self, "buttons"):
            for button in self.buttons:
                button.Hide()
            self.buttons = []

        self.SetStatus()
        self.gauge.SetValue(0)

        # Repaint the window
        self.flexGridSizer.Layout()

    def SetStatus(self, text = ''):
        self.statusText.SetLabel(text)

    def DisableAllFields(self):
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROWWAIT))
        self.taskLabel.Disable()
        self.taskSelect.Disable()
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                labelWidget.Disable()
                entryWidget.Disable()
        self.buttonStart.Disable()

    def EnableAllFields(self):
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.taskLabel.Enable()
        self.taskSelect.Enable()
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                labelWidget.Enable()
                entryWidget.Enable()

    def GetItems(self):
        items = {}
        if hasattr(self, "widgets"):
            # Take the itemKey as the key and not the label of the labelWidget
            # Since the label could have had nice string formatting options
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                value = entryWidget.GetValue()
                items[itemKey] = value
        return items

    def OnTaskError(self, e):
        message = "ERROR: The task failed with the following message:\n\n" + str(e)
        title = "Task Failed"
        wx.CallAfter(self.OnError, message, title)

    def onUpdateProgress(self, percentage, status = ''):
        wx.CallAfter(self.gauge.SetValue, int(percentage))
        self.SetStatus(status)
        #self.gauge.SetValue(percentage)

    def onLongRunDone(self, status = ''):
        wx.CallAfter(self.gauge.SetValue, 100)
        #self.labelWidget.SetlabelWidget("Done")
        wx.CallAfter(self.EnableAllFields)

        # Rename button to 'Close' (was Cancel)
        self.buttonClose.SetLabel('&Close')

        self.buttonStart.Disable()

        self.SetStatus(status)

        dlg = wx.MessageDialog(self, 
            "You can find the files in the output folder",
            "All Done!", wx.OK|wx.ICON_INFORMATION)
        #wx.CallAfter(dlg.ShowModal)
        #dlg.Destroy()
 
    def ClearGuiItems(self):
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                # Hide both the labelWidget and the entryWidget
                # in one go
                map(self.flexGridSizer.Hide, (labelWidget, entryWidget))

            self.widgets = []

        if hasattr(self, "buttons"):
            for button in self.buttons:
                button.Hide()
            self.buttons = []

        self.SetStatus()
        self.gauge.SetValue(0)

        # Repaint the window
        #self.flexGridSizer.Layout()

    def OnEnableButtonStart(self, evt = None):
        # Get widget from event
        self.buttonStart.Enable()

    def OnStart( self, event ):

        self.buttonStart.Disable()
        self.buttonClose.SetLabel('&Cancel')

        self.gauge.Show()
        self.DisableAllFields()

        # Refresh task
        # TODO: find a better way to do this.
        self.task = TaskManager(self.task.options)

        items = self.GetItems()

        self.section = 'User Settings'

        for key in items.keys():

            value = items.get(key)
            
            # Fancy function to find out if any of the password strings are 
            # in the itemKey name. If so, this will return true.
            containsPassword = any( [ x in key.lower() for x in self.options.get('PasswordStrings')])

            # Encrypt password
            if containsPassword:
                value = Crypt().Encrypt(value)

            self.task.config.set(self.section,key, value)

        p = self.task
        
        useThread = True
        if useThread:
            p.readyCallback = self.onLongRunDone
            p.progressCallback = self.onUpdateProgress
            p.errorCallback = self.OnTaskError

            try:
               p.start()
            except Exception as e:
                errorString = "ERROR: The task failed with the following error:\n%s" % (str(e))
        else:
            try:
                p.Execute(self.onLongRunDone, self.onUpdateProgress)
            except Exception as e:
                errorString = "ERROR: The task failed with the following error:\n%s" % (str(e))
                self.OnError(errorString, 'Task failed')
                raise

    def OnError(self, message, title):
        print "on error"
        dlg = wx.MessageDialog(self, 
            message,
            title, wx.OK|wx.ICON_ERROR)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.gauge.SetValue, 0)
            wx.CallAfter(self.EnableAllFields)
    
    def OnClose(self, event):
        # If the app is busy, the action is a 'Cancel' action:
        # we will stop the task, but not close the app.
        #
        # When the app is not busy, the action is a 'Close' action:
        # we will close the application
        percentage = self.gauge.GetValue()
        if 0 < percentage < 100:
            dlg = wx.MessageDialog(self, 
                "Do you really want to cancel this task?",
                "Confirm Cancel", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.SetStatus('Cancelling task. Please wait...')
                self.task.stop()
        else:
            self.Destroy()
    
if __name__ == "__main__":
    #print "PIQA GUI: this can only be run as an import"

    #app = mainGUI(0)

    #print dir(app)

    """
    w = app.frame.m_scrolledWindow1
    s = app.frame
    sizer = w.GetSizer()
    m_staticText9 = wx.StaticText( s.m_scrolledWindow1, wx.ID_ANY, u"RREKAJASLKFKDS", wx.DefaultPosition, wx.DefaultSize, 0 )
    sizer.Add( m_staticText9, 0, wx.ALL, 5 )
    w.Refresh()
    #print dir (w)
    """

    #app.MainLoop()

    options = {
        'foo': 'bar'
    }
    app = GUI(options)
    app.Show()

    print "END"
    sys.exit()

