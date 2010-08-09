import copy
import Base
import os
import sys
import thread 
import wx

from lib.taskmanager import * 
from lib.logger import *

from multiprocessing import Process

class mainGUI(wx.App):
    def Show(self):

        loggerName = 'mainGUI'
        if 'logger' in self.options:
            logger = self.options.get('logger')
            self.logger = logger.clone(loggerName) 
        else:
            self.logger = Logger(loggerName)

        #print "SHOW!!"

        self.frame = PIQAGUI(None, self.options)

        # This makes sure the GUI refreshes itself
        # when new items are added
        self.frame.SetAutoLayout(True)

        # Set self as 'parent' object of frame
        # This is a very dirty hack
        # TODO: Fix!
        self.frame.parent = self

        self.frame.Show()

        #self.frame.gauge.Hide()

        self.SetTopWindow(self.frame)
        
        # Disable OK button on startup
        self.frame.OkButton.Disable()

        #####################################
        #Set Selection List
        #self.tasks = [ u"testing", u"one two", u"very long name see what this does hey?", u"sfdksdfjsda", u"sdjakfsad", u"fj", u"asdf", u"sdafasdfsadf", u"sadfasdf" ]
        #self.tasks = ["dfaksfas"] 
        #self.tasks = map(os.path.basename, fileList)
        #self.tasks = fileList
        #self.tasks = []

        #print dir(self.frame.taskLabel )
        self.frame.taskLabel.SetLabel('Task')

        # Add tasks only now in order to have no default selection at startup
        for taskName, taskFile in self.tasks:

            #print  'TaskName:', taskFile
            #self.logger.info('TaskName:', taskFile)
            #self.logger.info(type(taskName))
            #print taskName
            #self.logger.info(taskName)

            self.frame.taskSelector.Append( taskName )
       
        if len(self.tasks) == 1:
            self.frame.taskSelector.SetSelection(0)
            self.frame.ProcessSelection(0)

        if not self.tasks:
            dial = wx.MessageDialog(None, 'Could not find any task!', 'Error',
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

        self.MainLoop()
           

class PIQAGUI( Base.Base ):
    def __init__( self, parent, options = {} ):
        #GUI.Base.__init__( self, parent )
        #print "PIQAGUI Options", options

        # Default options
        self.options = {
            'Title': 'PlaceLab',
            'AppWidth' : '700',
            'AppHeight' : 375,
            'EntryWidgetWidth' : 550,
            'FontFace' : 'Verdana',
            'FontSize' : 12,
            'passwordStrings': [ 'passw', 'pwd' , 'pword' ],
        }

        # Merge default options with ones provided in app INI file
        self.options.update(options)

        # Setting application specific settings from options
        self.title = self.options['Title']
        self.appWidth = int(self.options['AppWidth'])
        self.appHeight = int(self.options['AppHeight'])
        self.appSize = wx.Size( self.appWidth, self.appHeight )

        self.entryWidgetWidth = int(self.options['EntryWidgetWidth']) 
        self.entryWidgetSize = wx.Size(self.entryWidgetWidth,-1 ) 

        self.fontface = self.options['FontFace']
        self.fontsize = int(self.options['FontSize'])
        self.font = wx.Font(self.fontsize, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, self.fontface)

        # Storage for miscellaneous widgets & buttons (not the OK or Cancel ones)
        self.widgets = []
        self.buttons = []

            
        # Init Frame and set title
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = self.title, 
            pos = wx.DefaultPosition, size = self.appSize, 
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        # Set application icon

        try:
            import win32api
            exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
            self.icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        except Exception as e:
            #print "ICON file", iconFile 
            iconFile = "groundtruth.ico"
            if os.path.exists(iconFile):
                self.icon = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)

        if hasattr(self, "icon"):
            self.SetIcon(self.icon)

        # Set BG colour to white
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.SetFont(self.font) 

        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        self.fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
        self.fgSizer1.SetFlexibleDirection( wx.BOTH )
        self.fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        # Create INI file selection list
        self.taskLabel = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.taskLabel.Wrap( -1 )
        self.taskLabel.SetMinSize( wx.Size( 100,-1 ) )
        #self.taskLabel.SetLabeL('Prrrrofile!')
        
        self.fgSizer1.Add( self.taskLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        
        self.taskSelector = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.Point( -1,-1 ), wx.DefaultSize, [], wx.TAB_TRAVERSAL  )
        self.taskSelector.SetSelection( -1 )
        self.taskSelector.SetMinSize(self.entryWidgetSize)
        
        self.fgSizer1.Add( self.taskSelector, 0, wx.ALL, 5 )

        
        # Create some vertical white space
        self.fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        self.fgSizer1.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )

        self.m_scrolledWindow1.SetSizer( self.fgSizer1 )
        self.m_scrolledWindow1.Layout()
        self.fgSizer1.Fit( self.m_scrolledWindow1 )
        bSizer1.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
        

        #bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )     

        self.statusField = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statusField.Wrap( -1 )
        fgSizer2.Add( self.statusField, 0, wx.ALL|wx.EXPAND, 5 )       
        fgSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100)
        self.gauge.SetMinSize( wx.Size( 200, -1 ) )

        fgSizer2.Add(self.gauge, proportion=1, flag=wx.EXPAND)


        #bSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.OkButton = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.OkButton )
        self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
        m_sdbSizer1.SetMinSize( wx.Size( 600, 20 ) )
        m_sdbSizer1.Realize();
        #self.m_sdbSizer1Exit = wx.Button(m_sdbSizer1, wx.ID_EXIT )
        #m_sdbSizer1.AddButton( self.m_sdbSizer1Exit )
        #self.m_sdbSizer1Stop = wx.Button(m_sdbSizer1, wx.ID_STOP )
        #m_sdbSizer1.AddButton( self.m_sdbSizer1Stop )
        fgSizer2.Add( m_sdbSizer1, 1, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.EXPAND|wx.SHAPED, 5 )
        
        bSizer1.Add( fgSizer2, 0, wx.ALL|wx.EXPAND, 5 )
        """"
        fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"MyLabelkj dsfkj safkj saflk jadsfkl", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        fgSizer2.Add( self.m_staticText5, 0, wx.ALL|wx.EXPAND, 5 )
        """
        
        fgSizer2.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.taskSelector.Bind( wx.EVT_CHOICE, self.OnTaskChanged )
        self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.OnClose )
        self.OkButton.Bind( wx.EVT_BUTTON, self.OnOK )
    
        """
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.SetStatusText('You selected: %s\n' % dlg.GetPath())
        dlg.Destroy()
        """

    def OnEnableOkButton(self, evt = None):
        # Get widget from event
        self.OkButton.Enable()

    def DirectoryDialog(self, evt):

        self.OkButton.Enable()

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
        

    # Handlers for Base events.
    def OnTaskChanged( self, event ):
        #self.choices.pop(0)
        #self.choices = [ u"testing", u"one two", u"very long name see what this does hey?", u"sfdksdfjsda", u"sdjakfsad", u"fj", u"asdf", u"sdafasdfsadf", u"sadfasdf" ]
        #self.taskSelector = wx.Choice( self.m_scrolledWindow1, wx.ID_ANY, wx.Point( -1,-1 ), wx.DefaultSize, self.choices, wx.TAB_TRAVERSAL  )
        #self.taskSelector.SetSelection( -1 )
 
        #print "Change!", self, event
        selection = self.taskSelector.GetSelection()
        self.ProcessSelection(selection)
    
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
        # If we close while the app is busy, then we should ask
        # for confirmation. Otherwise, just exit
        percentage = self.gauge.GetValue()
        if 0 < percentage < 100:
            dlg = wx.MessageDialog(self, 
                "Do you really want to close this application?",
                "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.task.stop()
                self.Destroy()
                #self.task.join()
        else:
            self.Destroy()
    
    def OnOK( self, event ):

        #self.SetStatus('Running...')

        self.OkButton.Disable()

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
            containsPassword = any( [ x in key.lower() for x in self.options.get('passwordStrings')])

            # Encrypt password
            if containsPassword:
                value = Crypt().Encrypt(value)

            self.task.config.set(self.section,key, value)

        p = self.task

        #print "*" * 60
        #print p
        #print "*" * 60
        #p.SubstituteVariablesFromItems(items)

        #p = p.Clone(False)
        #print p, p.GetSectionItems('PIQA Parcel Extract') 
        
        useThread = True


        if useThread:
            p.readyCallback = self.onLongRunDone
            p.progressCallback = self.onUpdateProgress
            p.errorCallback = self.OnTaskError

            try:
               p.start()
            except Exception as e:
                errorString = "ERROR: The task failed with the following error:\n%s" % (str(e))

            """
            try:

                p.readyCallback = self.onLongRunDone
                p.progressCallback = self.onUpdateProgress

                p.start()
                #p.Execute()

            except Exception as e:
                errorString = "ERROR: The task failed with the following error:\n%s" % (str(e))
                self.OnError(errorString, 'Task failed')
                raise
                """
        else:
            try:
                p.Execute(self.onLongRunDone, self.onUpdateProgress)
            except Exception as e:
                errorString = "ERROR: The task failed with the following error:\n%s" % (str(e))
                self.OnError(errorString, 'Task failed')
                raise

        #print self.task
    def DisableAllFields(self):
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROWWAIT))
        self.taskLabel.Disable()
        self.taskSelector.Disable()
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                labelWidget.Disable()
                entryWidget.Disable()
        self.OkButton.Disable()

    def EnableAllFields(self):
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.taskLabel.Enable()
        self.taskSelector.Enable()
        if hasattr(self, "widgets"):
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                labelWidget.Enable()
                entryWidget.Enable()

    def OnTaskError(self, e):
        message = "ERROR: The task failed with the following message:\n\n" + str(e)
        title = "Task Failed"
        wx.CallAfter(self.OnError, message, title)

    def onUpdateProgress(self, percentage, status = ''):
        wx.CallAfter(self.gauge.SetValue, int(percentage))
        self.SetStatus(status)
        #self.gauge.SetValue(percentage)

    def SetStatus(self, text = ''):
        self.statusField.SetLabel(text)

    def onLongRunDone(self, status = ''):
        wx.CallAfter(self.gauge.SetValue, 100)
        #self.labelWidget.SetlabelWidget("Done")
        wx.CallAfter(self.EnableAllFields)
        self.OkButton.Disable()
        #print "\n*** All DONE! ***"

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
                map(self.fgSizer1.Hide, (labelWidget, entryWidget))

            self.widgets = []

        if hasattr(self, "buttons"):
            for button in self.buttons:
                button.Hide()
            self.buttons = []

        self.SetStatus()
        self.gauge.SetValue(0)

        # Repaint the window
        self.fgSizer1.Layout()

    def GetItems(self):
        items = {}
        if hasattr(self, "widgets"):
            # Take the itemKey as the key and not the label of the labelWidget
            # Since the label could have had nice string formatting options
            for labelWidget, entryWidget, itemKey, defaultValue in self.widgets:
                value = entryWidget.GetValue()
                items[itemKey] = value
        return items

    def ProcessSelection(self, id):
        self.OkButton.Enable()
        #print "Selected processing:", id

        # Get file name from 'parent' object.
        taskName, taskFile = self.parent.tasks[id]

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

        items = self.task.GetSectionItems('User Settings')
        #print "ITEMS", type(items), items

        for itemKey, defaultValue in items:

            # Replace all underscores with spaces
            labelText = itemKey.replace('_',' ') 

            labelWidget = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, labelText, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.fgSizer1.Add( labelWidget, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
            

            entryWidget = None

            # Fancy function to find out if any of the password strings are 
            # in the itemKey name. If so, this will return true.
            containsPassword = any( [ x in itemKey.lower() for x in self.options.get('passwordStrings')])

            entryWidgetStyle = 0
            if containsPassword:
                entryWidgetStyle = wx.TE_PASSWORD
                defaultValue = Crypt().Decrypt(defaultValue)

            entryWidgetStyle =  wx.TE_PASSWORD if containsPassword else 0
            entryWidget = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, defaultValue , wx.DefaultPosition, wx.DefaultSize, entryWidgetStyle)
                


            entryWidget.SetMinSize( self.entryWidgetSize )
            self.fgSizer1.Add( entryWidget , 0, wx.ALL, 5 )

            entryWidget.Bind( wx.EVT_SET_FOCUS, self.OnEnableOkButton)

            # Check if the entry field is a folder field
            # If so, we open a directory selection dialog upon clicking
            # in the field
            folderStrings = ['dir', 'directory', 'folder', 'fldr']
            containsFolder = any( [ itemKey.lower().endswith(x) for x in folderStrings])
            if containsFolder:
                entryWidget.Bind( wx.EVT_SET_FOCUS, self.DirectoryDialog)
                entryWidget.SetEditable(False)

            # Keep track of widgets. We need to remove them
            # when another task gets selected
            # We store them as tuples in a list
            self.widgets.append((labelWidget, entryWidget, itemKey, defaultValue))
        
        """
        buttonSections = self.task.GetButtonSections()
        for buttonSection in buttonSections:
            buttonItems = self.task.GetSectionItems(buttonSection, 'dict')
            print buttonSection, buttonItems

            button = wx.Button(self.m_scrolledWindow1, wx.ID_ANY, buttonItems['ButtonName'] )
            button.items = buttonItems # dirty hack to pass the items into the event object

            def tmpFunction(evt):
                button = evt.GetEventObject()
                items = button.items
                command = items.get('Command')
                if command:
                    self.task.ExecuteCommand(command)

            button.Bind( wx.EVT_BUTTON, tmpFunction)
            self.buttons.append(button)
            self.fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
            self.fgSizer1.Add( button, 0, wx.ALL, 5 )
        """

        #for x in dir(self.fgSizer1):
            #print x

        #######
        # Refresh of window (needed)
        self.fgSizer1.Layout()
        self.Layout()


if __name__ == "__main__":
    #print "PIQA GUI: this can only be run as an import"

    app = mainGUI(0)

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

    app.MainLoop()
    print "END"
    sys.exit()

