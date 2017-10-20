"""
This file is the heart of the GUI for PlaceLab
It loads and extends the GUI files* created by
the excellent wxFormBuilder

Note: don't edit the generated files by hand
but use PlaceLab.fbp in wxFormBuilder

* GUI_Template and GUI_TemplateMain
(actually, GUI_TemplateMain is not used)
"""

# Make app dir available to the sys path
import sys
sys.path.extend(['.', '..', 'lib','../..'])

import copy
import os
import thread
import wx
from base64 import b64encode, b64decode

import agw.hyperlink
import urllib
from PoziConnect.taskmanager import *
from PoziConnect.logger import *

# Get version information
from PoziConnect.version import version

# Needed for non-blocking threads
from multiprocessing import Process

# wxFormBuilder generated code
from GUI_Template import *

# Some globals
FILE_SUFFIXES = ['file'] # + ['filmename']
FOLDER_SUFFIXES = ['dir', 'directory', 'folder', 'fldr']
WIDGET_BORDER = 5


class GUI(wx.App):
    """
    PlaceLab GUI class.
    """

    def __init__(self, options = {}):
        """
        Constructor
        """
        console = options.get('console', 0)
        wx.App.__init__(self, console)

        # Disable any possible error message coming
        # from wxPython (like missing icon files, etc)
        wx.Log.Suspend()

        self.options = {
            'Title': 'Pozi Connect',
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
            self.logger.warn('Could not create GUI. Not sure what do do now.', e)

        # This makes sure the GUI refreshes itself
        # when new items are added
        frame.SetAutoLayout(True)

        #####################################################
        # Icon:
        # Get Icon from executable or, if that fails from template
        # Actually, it doesn't get the icon from the template atm
        # but it should!
        try:
            import win32api
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            self.icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        except Exception as e:
            self.logger.debug('Could not get icon from exe. Will use template one')

            # Get icon from the one provided in the template
            self.icon = wx.Icon('icon',wx.BITMAP_TYPE_ICO )

            # Hardcoded file reference. TODO: Fix!
            iconBitmap = wx.Bitmap("app/PoziConnect/gui/PlaceLabIcon.ico", wx.BITMAP_TYPE_ANY)
            self.icon.CopyFromBitmap(iconBitmap)
        finally:
            self.frame.SetIcon(self.icon)


        #####################################################
        # Logo:
        #
        # We import gui_logo_png which has a base64 encoded
        # version of PlaceLab.png. We do this to work around in
        # issue where we cannot include the image in the PlaceLab
        # executable
        #
        #####################################################
        import gui_logo_png
        imageStream = gui_logo_png.imageStream
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
        """
        Loops through the provided tasks and adds them to the
        task selector.
        """
        if taskList:
            for taskName, taskFile in taskList:
                self.frame.taskSelect.Append( taskName )

            if len(taskList) == 1:
                self.frame.taskSelect.SetSelection(0)
                self.frame.OnTaskSelect()
        else:
            dial = wx.MessageDialog(None, 'Could not find any task!', 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

    def Show(self):
        """
        Starts the GUI
        """
        self.logger.info('Starting GUI...')
        self.frame.Show()
        self.MainLoop()


#####################################################
# Class GUI Main
#####################################################
class GUI_Main(Main ):
    """
    This is the place where the nitty gritty of the GUI is
    stored.
    It extends and overwrites parts of the class Main that
    was generated by wxPython in the file GUI_Template.py
    """

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
        self.buttons = []
        self.widgets = []   # some widgets get hidden (and some widgets contain text_fields)

        # Storage for the actual items
        self.text_fields = {}     # each key maps to a text_field widget with a GetValue() method.

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

        # Set dimensions
        appWidth = int(self.options['AppWidth'])
        appHeight = int(self.options['AppHeight'])
        appSize = wx.Size( appWidth, appHeight )
        self.SetSize(appSize)

        entryWidgetWidth = int(self.options['EntryWidgetWidth'])
        entryWidgetSize = wx.Size(entryWidgetWidth,-1 )
        self.options['EntryWidgetSize'] = entryWidgetSize

        fontface = self.options['FontFace']
        fontsize = int(self.options['FontSize'])
        font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, fontface)
        self.SetFont(font)
    # __init__()

    def _is_a_password(self, itemKey):
        """
        Fancy function to find out if any of the password strings are
        in the itemKey name. If so, this will return true.
        This is used for turning a plain text field into a password field.
        """
        return any( [ x in itemKey.lower() for x in self.options.get('PasswordStrings')])
    # _is_a_password()

    def _contains_suffix(self, itemKey, suffixes):
        """
        Check the suffix of the field and returns true/false whether
        the string ends with any of the provided suffixes
        """
        return any( [ itemKey.lower().endswith(x) for x in suffixes])
    # _contains_suffix()

    def _is_a_folder(self, itemKey):
        """
        Check if the entry field is a folder field
        If so, we open a directory selection dialog upon clicking
        in the field
        """
        return self._contains_suffix(itemKey, FOLDER_SUFFIXES)
    # _is_a_folder()

    def _is_a_file(self, itemKey):
        """
        Check if the entry field is a file field
        If so, we open a file selection dialog upon clicking
        in the field
        """
        return self._contains_suffix(itemKey, FILE_SUFFIXES)
    # _is_a_file()

    #########################################################
    # Handlers for Main events.
    def OnTaskSelect( self, event = None ):
        """
        Loads a selected task, but does not start it yet.
        """
        # Enable Start button
        self.buttonStart.SetLabel('&Start')
        self.buttonStart.Enable()

        selection = self.taskSelect.GetSelection()
        self.LoadTask(selection)
    # OnTaskSelect()

    def OnUpdateClick( self, event = None ):
        """
        Process the task update.
        """
        # dlg = wx.MessageDialog(self,
            # "Pressing OK will download the latest tasks.\nThis might take a few seconds.",
            # "", wx.OK|wx.ICON_INFORMATION)
        # result = dlg.ShowModal()
        # dlg.Destroy()
        # if result == wx.ID_OK:
            # url = "https://github.com/groundtruth/PoziConnectConfig/archive/master.zip"
            # urllib.urlretrieve(url, "PoziConnectConfig-master.zip")

    def _show_dialog(self, evt, dialog_cb, title):
        """
        Helper method for showing any kind of dialog
        """

        self.buttonStart.Enable()

        # Get widget from event
        widget = evt.GetEventObject()
        widget = widget.text_field     # get the text input field

        # Get folder path from widget and turn
        # it into an absolute path
        path = widget.GetValue()
        abspath = os.path.abspath(path)

        dialog = None
        if   dialog_cb == wx.FileDialog:
            defaultDir = os.path.dirname(abspath)
            defaultFile = os.path.basename(abspath)
            dialog = dialog_cb(self, title, defaultDir, defaultFile)
        elif dialog_cb == wx.DirDialog:
            dialog = dialog_cb(self, title, abspath, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        else:
            raise Exception("Unknown dialog callback:", dialog_cb)

        # Show dialog and set the new path as a value of the widget
        if dialog.ShowModal() == wx.ID_OK:
            newpath = dialog.GetPath()
            widget.SetValue(newpath)

        widget.Enable()
    # _show_dialog()


    def _show_directory_dialog(self, evt):
        """
        Shows a directory dialog
        """
        self._show_dialog(evt, wx.DirDialog, "Choose a directory:")
    # _show_directory_dialog()


    def _show_file_dialog(self, evt):
        """
        Shows a file dialog
        """
        self._show_dialog(evt, wx.FileDialog, "Choose a file:")
    # _show_directory_dialog()


    def _new_text_field(self, defaultValue, style = 0):
        """
        Creates a new text field and returns it
        """
        text_field = wx.TextCtrl( self.scrolledWindow, wx.ID_ANY, defaultValue , wx.DefaultPosition, wx.DefaultSize, style)
        text_field.Bind( wx.EVT_TEXT, self.OnEnableButtonStart)   ### - do we need this for *every* text_field?
        return text_field
    # _new_text_field()


    def _new_password_widget(self, defaultValue):
        """
        Creates a new password field and returns it
        """
        entryWidgetStyle = wx.TE_PASSWORD
        defaultValue = Crypt().Decrypt(defaultValue)
        return self._new_text_field(defaultValue, entryWidgetStyle)
    # _new_password_widget()


    def _new_buttoned_widget(self, itemKey, defaultValue, buttonCallback):
        """
        Creates a new buttoned widget and returns it
        """
        # Buttoned widget is a grid (BoxSizer) containing a text_field (TextCtrl) & a button (Button)
        text_field = self._new_text_field(defaultValue)
        button = wx.Button(self.scrolledWindow, wx.ID_ANY, '...')
        button.text_field = text_field   # create a link to the text_ctrl widget for the dialog to use
        button.Bind( wx.EVT_BUTTON, buttonCallback)
        grid = wx.BoxSizer()
        grid.Add(text_field, 1)
        grid.Add(button    , 0)

        # Change value to a file path value
        absolutePath = os.path.abspath(defaultValue)
        text_field.SetValue(absolutePath)
        self.text_fields[itemKey] = text_field

        return grid
    # _new_buttoned_widget()()


    def _add_item(self, itemKey, defaultValue):
        """
        Creates a widget (either a text field or a button) and
        adds it to the GUI
        """
        # Replace all underscores with spaces
        labelText = itemKey.replace('_',' ')

        labelWidget = wx.StaticText( self.scrolledWindow, wx.ID_ANY, labelText, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.widgets += [labelWidget]
        self.flexGridSizer.Add( labelWidget, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, WIDGET_BORDER )

        entryWidget = None
        if   self._is_a_password(itemKey):
            entryWidget = self._new_password_widget(defaultValue)
            self.text_fields[itemKey] = entryWidget
        elif self._is_a_folder(  itemKey):
            entryWidget = self._new_buttoned_widget(itemKey, defaultValue, self._show_directory_dialog)
        elif self._is_a_file(    itemKey):
            entryWidget = self._new_buttoned_widget(itemKey, defaultValue, self._show_file_dialog)
        else:
            entryWidget = self._new_text_field(defaultValue)
            self.text_fields[itemKey] = entryWidget

        self.widgets += [entryWidget]
        self.flexGridSizer.Add( entryWidget , 0, wx.ALL|wx.EXPAND, WIDGET_BORDER )
    # _add_item()


    def LoadTask(self, id):
        """
        Loads a provided task, clears the GUI and rebuilds
        the GUI with the fields from that task
        """
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

        self.fieldsSizer = self.exampleLabel.GetParent()
        self.flexGridSizer = self.fieldsSizer.GetSizer()

        for itemKey, defaultValue in self.task.GetSectionItems('User Settings'):
            self._add_item(itemKey, defaultValue)

        #######
        # Refresh of window (needed)
        self.flexGridSizer.Layout()
        self.Layout()
    # LoadTask()


    def SetStatus(self, text = ''):
        """
        Updates the text in the status bar
        """
        self.statusText.SetLabel(text)
    # SetStatus()

    def DisableAllFields(self):
        """
        Disables all fields and Start button
        """
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROWWAIT))
        self.taskLabel.Disable()
        self.taskSelect.Disable()
        #if hasattr(self, "fields"):
        #    for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
        #        labelWidget.Disable()
        #        entryWidget.Disable()
        for field in self.text_fields.values(): field.Disable()

        self.buttonStart.Disable()
    # DisableAllFields()

    def EnableAllFields(self):
        """
        Enables all fields
        """
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.taskLabel.Enable()
        self.taskSelect.Enable()
        #if hasattr(self, "fields"):
        ###   for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
        ###        labelWidget.Enable()
        ###        entryWidget.Enable()
        for field in self.text_fields.values(): field.Enable()
    # EnableAllFields()


#    def GetItems(self):
#        items = {}
#        if hasattr(self, "widgets"):
#            # Take the itemKey as the key and not the label of the labelWidget
#            # Since the label could have had nice string formatting options
#            for entryWidget, itemKey in self.widgets:
#                value = entryWidget.GetValue()
#                items[itemKey] = value
#        return items
#   # GetItems()


    def OnTaskError(self, e):
        """
        Displays a modal window with the message when an error occurs
        """
        message = "ERROR: The task failed with the following message:\n\n" + str(e)
        title = "Task Failed"
        wx.CallAfter(self.OnError, message, title)
    # OnTaskError()

    def onUpdateProgress(self, percentage, status = ''):
        """
        Gets called throughout the process and provides
        an update on the progress of the app
        """
        wx.CallAfter(self.gauge.SetValue, int(percentage))
        self.SetStatus(status)
    # OnUpdateProgress()


    def onLongRunDone(self, status = ''):
        """
        Gets called after the whole task is finished. It
        sets the gauge to 100%, enables all fields
        and transforms the Cancel button into a Close button.
        """
        wx.CallAfter(self.gauge.SetValue, 100)
        #self.labelWidget.SetlabelWidget("Done")
        wx.CallAfter(self.EnableAllFields)

        # Rename button to 'Close' (was Cancel)
        self.buttonClose.SetLabel('&Close')

        self.buttonStart.SetLabel('&Start')
        self.buttonStart.Enable()

        self.SetStatus(status)

        #######################################################
        # Show a dialog when task is finished
        #dlg = wx.MessageDialog(self,
            #"You can find the files in the output folder",
            #"All Done!", wx.OK|wx.ICON_INFORMATION)
        #wx.CallAfter(dlg.ShowModal)
    # onLongRunDone()


    def ClearGuiItems(self):
        """
        Clears all task related GUI items. Gets called when a (new)
        task gets loaded.
        """
        if hasattr(self, "widgets"):
            ###for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
            ###    # Hide both the labelWidget and the entryWidget
            ###    # in one go
            ###    map(self.flexGridSizer.Hide, (labelWidget, entryWidget))
            #[self.flexGridSizer.Hide(widget) for widget in self.widgets]  # memory leak?
            for widget in self.widgets: self.flexGridSizer.Hide(widget)
            self.widgets = []

        if hasattr(self, "buttons"):
            for button in self.buttons:
                button.Hide()
            self.buttons = []

        self.SetStatus()
        self.gauge.SetValue(0)

        # Repaint the window
        #self.flexGridSizer.Layout()
    # ClearGuiItems()


    def OnEnableButtonStart(self, evt = None):
        """
        Helper function that responds to an event
        telling the appliation that the Start button
        can be enabled (again).
        """
        # Get widget from event
        self.buttonStart.Enable()
    # OnEnableButtonStart()

    def OnStart( self, event ):
        """
        Gets called when the Start button gets pressed. This
        method calls the script that runs the task.
        """

        self.buttonStart.Disable()
        self.buttonClose.SetLabel('&Cancel')

        self.gauge.Show()
        self.DisableAllFields()

        # Refresh task
        # TODO: find a better way to do this.
        self.task = TaskManager(self.task.options)

        self.section = 'User Settings'

        for key in self.text_fields.keys():

            value = self.text_fields[key].GetValue()

            # Encrypt password
            if self._is_a_password(key):
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
    # OnStart()

    def OnError(self, message, title):
        """
        This method will display an error dialog when a fatal error
        has occurred. After clicking OK it will re-enable the buttons
        """
        dlg = wx.MessageDialog(self,
            message,
            title, wx.OK|wx.ICON_ERROR)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.gauge.SetValue, 0)
            wx.CallAfter(self.EnableAllFields)
    # OnError()

    def OnClose(self, event):
        """
        If the app is busy, the action is a 'Cancel' action:
        we will stop the task, but not close the app.

        When the app is not busy, the action is a 'Close' action:
        we will close the application
        """
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
    # OnClose()

# GUI_Main
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
