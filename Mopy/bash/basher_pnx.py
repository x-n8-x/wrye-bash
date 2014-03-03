#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrye Bash Phoenix Advanced User Interface.

"""

#--------------------
# TODO
# 1. Finish Installers Tab Skeleton
# 2. Finish Saves Tab Skeleton
# 3. Figure out a better GUI for INIEdits Tab sash thingy if easy enough.
# 4. Not every Game has or works with INIs so figure out what would work best
#       universally or just make this tab disappear when not using a game that
#       would utilize a tab like this.
#    Tho some games might use INI's this tab may need to be pluggable as
#       the GUI layout would change. Ex: need switched out for a better
#       layed out game-specific one.
#    Only Beth games are supported ATM, but this will change eventually, so
#       we need to discuss how the INIEdits code/gui stuff should be cut up...
# 5. OUTWARDS THINKING! In general, what other tabs would the ultimate file manager type app have by default???
#       Ex: If I(bash the app) was a font installation tool,
#           I would install fonts(BAIN),
#           have a list of installed fonts(MODS),
#           and saved font configurations(SAVES)
#
# 6. When done with all the skeleton mockup stuff, consider cutting grouped classes
#       into their own blablaTabModule.py for easier working with specific code.
#
# 7. Convert standard wx.widgets calls to wxPython library licensed wxrap oneliners.
#       Scrap balt related similar stuff.
#
#--------------------

#-Imports----------------------------------------------------------------------

#--Python Imports.
import os
import sys
from sys import _getframe # Debug Def

if sys.version_info[0] == 2:
    PY2 = True
    PY3 = False
elif sys.version_info[0] == 3:
    PY2 = False
    PY3 = True

#--wxPython Imports.
import wxversion
wxversion.select('3.0.1-phoenix')
import wx # wxPython GUI library.
print(u'wx.VERSION = %s' % (str(wx.VERSION)))
if 'phoenix' in wx.version():
    PHOENIX = True
else:
    PHOENIX = False

import wx.lib.agw.aui as aui
# TODO make a fancy switcher dialog for the notebook tabs(Ctrl+Tab)
## from wx.lib.agw.aui import aui_switcherdialog as ASD
import wx.lib.scrolledpanel as scrolled
import wx.lib.resizewidget as RW

import wx.py as py # Interactive Python Shell

# import wx.lib.six as six # Six is a Python 2 and 3 compatibility library.


#--Local wxPython Imports.
## import wx.lib.mcow.shapedbitmapbutton as SBB # Fancy Game Intro/Mode Panel, About dialog.
import wx.lib.mcow.threewaysplitter as TWS
import wx.lib.mcow.picture as PIC
## import wx.lib.mcow.wxrap import button, menuItem, staticText, textCtrl


#-Globals----------------------------------------------------------------------

# Define a translation function.
_ = wx.GetTranslation

# global opt/less dots
defId = wx.ID_ANY
defPos = wx.DefaultPosition
defSize = wx.DefaultSize

#--IDs.
# There will be many of these eventually, so best stick them in a
# allIDs.py module when IDs get too big to handle
# Then they would be imported as...
# from allIDs import *
# or just the ones needed depending on the module.
ID_DROPDOWNTOOLBARITEM = wx.NewId()
ID_CHANGETOOLBARICONSIZE16 = wx.NewId()
ID_CHANGETOOLBARICONSIZE24 = wx.NewId()
ID_CHANGETOOLBARICONSIZE32 = wx.NewId()
ID_CUSTOMIZETOOLBAR = wx.NewId()

ID_TOGGLEPANE_PICTUREALBUM = wx.NewId()
ID_TOGGLEPANE_PMARCHIVE = wx.NewId()
ID_TOGGLEPANE_PEOPLE = wx.NewId()
ID_TOGGLEPANE_WRYESHELL = wx.NewId()
ID_TOGGLEPANE_WIZBAIN = wx.NewId()

auiNBArts = (
    aui.AuiDefaultTabArt,
    aui.AuiSimpleTabArt,
    aui.VC71TabArt,
    aui.FF2TabArt,
    aui.VC8TabArt,
    aui.ChromeTabArt
    )

# Debug Def
def funcname(funcClass=None):
    """
    print the function name of a def.

    Example Usage:
    --------------
    from printFunc import funcname

    def TestingPrintFuncName()
        # your code...
        # ...
        # then at the end...
        print(funcname())

    @return: Should print "TestingPrintFuncName"/*The actual calling def's name*
    @param: Optionally print the classname also.
        print(funcname(funcClass=self)) or print(funcname(self))

    """
    if funcClass:
        cn = funcClass.__class__.__name__
        return _getframe(1).f_code.co_name, cn
        # return sys._getframe(1).f_code.co_name, cn
    else:
        return _getframe(1).f_code.co_name
        # return sys._getframe(1).f_code.co_name


class MainAuiManager(aui.AuiManager):

    def __init__(self, managed_window=None, agwFlags=
                 aui.AUI_MGR_ALLOW_FLOATING
                 ## | aui.AUI_MGR_ALLOW_ACTIVE_PANE
                 ## | aui.AUI_MGR_TRANSPARENT_DRAG
                 | aui.AUI_MGR_TRANSPARENT_HINT
                 | aui.AUI_MGR_VENETIAN_BLINDS_HINT
                 ## | aui.AUI_MGR_RECTANGLE_HINT
                 | aui.AUI_MGR_HINT_FADE
                 ## | aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
                 ## | aui.AUI_MGR_LIVE_RESIZE
                 | aui.AUI_MGR_ANIMATE_FRAMES
                 | aui.AUI_MGR_PREVIEW_MINIMIZED_PANES
                 ## | aui.AUI_MGR_AERO_DOCKING_GUIDES
                 | aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
                 | aui.AUI_MGR_SMOOTH_DOCKING
                 ## | aui.AUI_MGR_USE_NATIVE_MINIFRAMES # Redocking of toolbar panes seems impossible(cause there are so many items in the toollauncher toolbar) if use this.
                 ## | aui.AUI_MGR_AUTONB_NO_CAPTION
                 | 0):
        aui.AuiManager.__init__(self, managed_window, agwFlags)

        # ... Tell AuiManager to manage this frame.
        self.SetManagedWindow(managed_window)

        self.SetAutoNotebookStyle(
            agwStyle=
            aui.AUI_NB_DRAW_DND_TAB
            ## | aui.AUI_NB_TOP
            ## | aui.AUI_NB_LEFT
            ## | aui.AUI_NB_RIGHT
            | aui.AUI_NB_BOTTOM
            | aui.AUI_NB_TAB_SPLIT
            | aui.AUI_NB_TAB_MOVE
            ## | aui.AUI_NB_TAB_EXTERNAL_MOVE
            ## | aui.AUI_NB_TAB_FIXED_WIDTH
            | aui.AUI_NB_SCROLL_BUTTONS
            | aui.AUI_NB_WINDOWLIST_BUTTON
            ## | aui.AUI_NB_CLOSE_BUTTON
            ## | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
            ## | aui.AUI_NB_CLOSE_ON_ALL_TABS
            ## | aui.AUI_NB_MIDDLE_CLICK_CLOSE
            | aui.AUI_NB_SUB_NOTEBOOK
            ## | aui.AUI_NB_HIDE_ON_SINGLE_TAB
            | aui.AUI_NB_SMART_TABS
            ## | aui.AUI_NB_USE_IMAGES_DROPDOWN
            ## | aui.AUI_NB_CLOSE_ON_TAB_LEFT
            | aui.AUI_NB_TAB_FLOAT
            | 0)

        self._notebook_theme = 0
        self.SetAutoNotebookTabArt(auiNBArts[self._notebook_theme]())
        self.SetAnimationStep(40.0) # 30.0 is default

    def DoInitializePaneIfNot(self, pane):
        if hasattr(pane.window, '_isInitialized'):
            if not pane.window._isInitialized:
                pane.window.Initialize()
        else:
            pass
            #DEBUG# wx.Bell()
            #DEBUG# print('TODO: %s is missing _isInitialized Attribute' % pane.name)

    def DoShowPaneIfPaneIsNotShown(self, paneName):
        """
        Show a Pane if it is not currently shown.
        """
        pane = self.GetPane(paneName)
        self.DoInitializePaneIfNot(pane)
        if not pane.IsShown():
            pane.Show()
            self.Update()

    def BindEvents_AuiManager(self):
        # self.Bind(aui.EVT_AUI_PANE_BUTTON, self.OnAUIPaneButton)
        self.Bind(aui.EVT_AUI_PANE_MAXIMIZE, self.OnAUIPaneMaximize)
        self.Bind(aui.EVT_AUI_PANE_RESTORE, self.OnAUIPaneRestore)

        self.Bind(aui.EVT_AUI_PANE_ACTIVATED, self.OnAUIPaneActivated)
        # self.Bind(aui.EVT_AUI_PANE_MIN_RESTORE, self.OnAUIPaneMinRestore)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnAuiPaneClose)
        self.Bind(aui.EVT_AUI_PERSPECTIVE_CHANGED, self.OnAUIPerspectiveChanged)
        #
        ### self.Bind(aui.EVT_AUI_RENDER, self.OnAUIRender)
        ### self.Bind(aui.EVT_AUI_FIND_MANAGER, self.OnAUIFindManager)

        # self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        # self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        # self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        # self.Bind(wx.EVT_MOTION, self.OnMotion)

    # def OnLeftDClick(self, event):
    #     """
    #     Handle the wx.EVT_LEFT_DCLICK event for :class:`MainAuiManager`.
    #     """
    #     # event.Skip()
    #     print(funcname(self))
    #
    # def OnLeftDown(self, event):
    #     """
    #     Handle the wx.EVT_LEFT_DOWN event for :class:`MainAuiManager`.
    #     """
    #     event.Skip()
    #     print(funcname(self))
    #
    # def OnLeftUp(self, event):
    #     """
    #     Handle the wx.EVT_LEFT_UP event for :class:`MainAuiManager`.
    #     """
    #     event.Skip()
    #     print(funcname(self))
    def OnMiddleDown(self, event):
        """
        Handle the wx.EVT_MIDDLE_DOWN event for :class:`MainAuiManager`.
        """
        event.Skip()
        print(funcname(self))

    def OnMiddleUp(self, event):
        """
        Handle the wx.EVT_MIDDLE_UP event for :class:`MainAuiManager`.
        """
        event.Skip()
        print(funcname(self))

    # def OnMotion(self, event):
    #     """
    #     Handle the wx.EVT_MOTION event for :class:`MainAuiManager`.
    #     """
    #     event.Skip()
    #     print(funcname(self))

    def OnRightDown(self, event):
        event.Skip()
        print(funcname(self))

    def OnRightUp(self, event):
        event.Skip()
        print(funcname(self))

    def OnAuiPaneClose(self, event):
        if event.pane.IsToolbar():
            self.GetPane(u'%s' % event.pane.name).Hide()
            # event.Veto()
            print(u'%s Hidden' % event.pane.name)
            # return

        # Show how to veto closing a pane.
        if event.pane.name.startswith('Plugin:'):
            msg = 'Are you sure you want to '
            if event.GetEventType() == aui.wxEVT_AUI_PANE_MINIMIZE:
                msg += 'minimize '
            else:
                msg += 'close/hide '

            wx.Bell()
            res = wx.MessageBox(event.pane.name + '\n' + msg + 'this pane?', u'AUI Pane Close', wx.YES_NO, self)
            if res != wx.YES:
                event.Veto()

            self.ClosePane(event.pane)

        print(funcname(self))

    def DoSaveFramePerspective(self, event):
        auiFramePersp = self.SavePerspective()
        gGlobalsDict['FramePerspective'] = auiFramePersp
        gConfig.set('Startup', 'FramePerspective', auiFramePersp)

    def OnAUIPerspectiveChanged(self, event):
        print(funcname(self))

    def OnAUIFindManager(self, event):
        print(funcname(self))

    def OnAUIPaneMinRestore(self, event):
        print(funcname(self))

    def OnAUIPaneActivated(self, event):
        print(funcname(self))

    def OnAUIPaneButton(self, event):
        print(funcname(self))

    def OnAUIPaneMaximize(self, event):
        print(funcname(self))

    def OnAUIPaneRestore(self, event):
        print(funcname(self))

    def OnAUIRender(self, event):
        print(funcname(self))


class BashFrame(wx.Frame):
    """Main Window Frame For The Application."""
    def __init__(self, parent=None, id=wx.ID_ANY, title=_(u'Wrye Bash'),
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER,
                 name='frame', log=None):
        """Default class constructor."""
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        #--Singleton
        ## global bashFrame
        ## bashFrame = self
        global gMainWin
        gMainWin = self

        #--AuiManager
        self._mgr = MainAuiManager(self)
        self._mgr.SetManagedWindow(self)

        #--Panes
        self.BuildPanes()

        #--StatusBar
        self.statusbar = BashStatusBar(self)
        self.SetStatusBar(self.statusbar)
        self.statusbar.SetStatusText(u'wxPython %s' % wx.version())

        gMainAuiNB.AddPage(InstallersPanel(gMainAuiNB, mainWin=self), _(u'Installers'), False)
        gMainAuiNB.AddPage(ModsPanel(gMainAuiNB, mainWin=self), _(u'Mods'), True)
        gMainAuiNB.AddPage(SavesPanel(gMainAuiNB, mainWin=self), _(u'Saves'), False)

        #--Events
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        ##TODO/HOOKIN## self.Bind(wx.EVT_ACTIVATE, self.RefreshData)
        self.BindEvents()

        self._mgr.Update()

        # Yep the monkey God of Modding himself.
        ## self.SetIcon(wx.Icon('images/bash_16.png'))
        self.SetIcon(wx.Icon('images/wryemonkey32.png'))

        self.Bind(wx.EVT_MOVE_END, self.OnMoveEnd)

    def OnMoveEnd(self, event):
        event.Skip()
        self.Refresh()

    def OnCloseWindow(self, event):
        """Handle Close event. Save application data."""
        ##TODO## try:
        ##TODO##     self.SaveSettings()
        ##TODO## except:
        ##TODO##     deprint(u'An error occurred while trying to save settings:', traceback=True)
        ##TODO##     pass
        ##TODO## if self.updater.pool:
        ##TODO##     self.updater.pool.terminate()
        self.Destroy()

    def TogglePane(self, event):
        # print(event.GetEventObject())
        # print(event.GetId())

        # print(event.GetEventObject().GetToolLabel(event.GetId()))#Tool

        evtId = event.GetId()
        print(evtId)

        try: # Called from Menu.
            menulabel = self.GetMenuBar().FindItemById(evtId).GetLabel().lower().replace(' ', '')
            pane = self._mgr.GetPane(u'%s' % (menulabel))
            self._mgr.DoInitializePaneIfNot(pane)
            ## print('menulabel:', menulabel)
        except AttributeError as exc: # Called from Tool.
            label = event.GetEventObject().GetToolLabel(evtId)
            pane = self._mgr.GetPane(u'%s' % label)
            self._mgr.DoInitializePaneIfNot(pane)
            ## print('label', label)
        except Exception as exc:
            raise exc
        if pane.IsShown():
            pane.Hide()
        elif pane.IsToolbar(): # TODO(priority=7) ~Attempt to keep gripper shown.~ Seems use native wx.miniframes works for this...
        #     # pane.Gripper(visible=False)
        #     # pane.Gripper(visible=True)
            pane.ToolbarPane()
            # pane.GripperTop()
        #     # pane.Dock()
            pane.Show()
        else:
            pane.Show()
        self._mgr.Update()
        print(funcname())

    def BuildPanes(self):

        # local opt/less dots
        nb = wx.NullBitmap
        auiITEM_NORMAL = aui.ITEM_NORMAL

        # prepare a few custom overflow elements for the toolbars' overflow buttons
        prepend_items, append_items = [], []
        item = aui.AuiToolBarItem()

        item.SetKind(wx.ITEM_SEPARATOR)
        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CHANGETOOLBARICONSIZE16)
        item.SetLabel(_(u'Change Icon Size to 16'))
        item.SetBitmap(wx.Bitmap('images/bash_16.png'))

        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CHANGETOOLBARICONSIZE24)
        item.SetLabel(_(u'Change Icon Size to 24'))
        item.SetBitmap(wx.Bitmap('images/bash_24.png'))

        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CHANGETOOLBARICONSIZE32)
        item.SetLabel(_(u'Change Icon Size to 32'))
        item.SetBitmap(wx.Bitmap('images/bash_32.png'))

        append_items.append(item)

        item = aui.AuiToolBarItem()
        item.SetKind(wx.ITEM_NORMAL)
        item.SetId(ID_CUSTOMIZETOOLBAR)
        item.SetLabel(_(u'Customize...'))
        item.SetBitmap(wx.Bitmap('images/settingsbutton24.png'))

        append_items.append(item)

        self.toolbar1 = tb1 = aui.AuiToolBar(self, -1, defPos, defSize,
            agwStyle=aui.AUI_TB_DEFAULT_STYLE
                   | aui.AUI_TB_OVERFLOW
                   # | aui.AUI_TB_TEXT
                   # | aui.AUI_TB_HORZ_TEXT
                   )
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/checkbox_red_off_32.png'), nb, auiITEM_NORMAL, _(u'Auto-Quit Enabled/Disabled'), _(u'Auto-Quit Enabled/Disabled'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/checkbox_red_off_32.png'), nb, auiITEM_NORMAL, _(u'OBSE'), _(u'OBSE'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/checkbox_red_off_32.png'), nb, auiITEM_NORMAL, _(u'LAA'), _(u'LAA'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/wryemonkey32.png'), nb, auiITEM_NORMAL, _(u'Launch Game'), _(u'Launch Game'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/docbrowser32.png'), nb, auiITEM_NORMAL, _(u'Doc Browser'), _(u'Doc Browser'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/modchecker32.png'), nb, auiITEM_NORMAL, _(u'Mod Checker'), _(u'Mod Checker'), None)
        tb1.AddSeparator()
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/settingsbutton32.png'), nb, auiITEM_NORMAL, _(u'Settings'), _(u'Settings'), None)
        tb1.AddTool(wx.ID_ANY, _(u''), wx.Bitmap('images/help32.png'), nb, auiITEM_NORMAL, _(u'Help File'), _(u'Help File'), None)
        tb1.SetToolDropDown(ID_DROPDOWNTOOLBARITEM, True)
        tb1.SetCustomOverflowItems(prepend_items, append_items)
        tb1.Realize()

        self.toolbar2 = tb2 = aui.AuiToolBar(self, -1, defPos, defSize,
            agwStyle=aui.AUI_TB_DEFAULT_STYLE
                   | aui.AUI_TB_OVERFLOW
                   | aui.AUI_TB_VERTICAL
                   # | aui.AUI_TB_TEXT
                   # | aui.AUI_TB_HORZ_TEXT
                   )
        tb2.SetToolBitmapSize(wx.Size(16, 16))
        tb2.AddTool(ID_TOGGLEPANE_PICTUREALBUM, 'picturealbum', wx.Bitmap('images/database_connect16.png'), nb, auiITEM_NORMAL, _(u'Picture Album'), _(u'Picture Album'), None)
        tb2.AddTool(ID_TOGGLEPANE_PMARCHIVE, 'pmarchive', wx.Bitmap('images/database_connect16.png'), nb, auiITEM_NORMAL, _(u'PM Archive'), _(u'PM Archive'), None)
        tb2.AddTool(ID_TOGGLEPANE_PEOPLE, 'people', wx.Bitmap('images/database_connect16.png'), nb, auiITEM_NORMAL, _(u'People'), _(u'People'), None)
        tb2.AddTool(ID_TOGGLEPANE_WIZBAIN, 'wizbain', wx.Bitmap('images/wizard.png'), nb, auiITEM_NORMAL, _(u'WizBAIN'), _(u'WizBAIN'), None)
        tb2.AddTool(ID_TOGGLEPANE_WRYESHELL, 'pythonshell', wx.Bitmap('images/wryemonkey16.png'), nb, auiITEM_NORMAL, _(u'Wrye Shell'), _(u'Wrye Shell'), None)
        tb2.SetToolDropDown(ID_DROPDOWNTOOLBARITEM, True)
        tb2.SetCustomOverflowItems(prepend_items, append_items)
        tb2.Realize()

        # Testing external tool laucher toolbar concept.
        self.toolbar3 = tb3 = aui.AuiToolBar(self, -1, defPos, defSize,
            agwStyle=aui.AUI_TB_DEFAULT_STYLE
                   | aui.AUI_TB_OVERFLOW
                   | aui.AUI_TB_VERTICAL
                   # | aui.AUI_TB_TEXT
                   # | aui.AUI_TB_HORZ_TEXT
                   )
        tb3.SetToolBitmapSize(wx.Size(16, 16))
        for toolImg in os.listdir('images/tools'):
            if toolImg.endswith('32.png'):
                tb3.AddTool(wx.ID_ANY, 'tool', wx.Bitmap('images/tools/%s' % toolImg), nb, auiITEM_NORMAL, _(u'%s' % toolImg), _(u'%s' % toolImg), None)
        tb3.SetToolDropDown(ID_DROPDOWNTOOLBARITEM, True)
        tb3.SetCustomOverflowItems(prepend_items, append_items)
        tb3.Realize()

        # local opt
        lMgrAddPane = self._mgr.AddPane
        auiAuiPaneInfo = aui.AuiPaneInfo

        # Add the panes to the manager.
        lMgrAddPane(self.CreateMainAuiNotebook(), auiAuiPaneInfo().
                    Name("main_aui_notebook").
                    CenterPane().Show().PaneBorder(False))

        lMgrAddPane(self.CreatePictureAlbumCtrl(), auiAuiPaneInfo().
                    Name('picturealbum').Caption(_(u'Picture Album')).
                    MinimizeButton(True).MaximizeButton(True).CloseButton(True).
                    FloatingSize((300, 300)). #MinSize((64, 24)).
                    BestSize((200, 100)).Icon(wx.Bitmap('images/database_connect16.png')))

        lMgrAddPane(self.CreatePMArchiveCtrl(), auiAuiPaneInfo().
                    Name('pmarchive').Caption(_(u'PM Archive')).
                    MinimizeButton(True).MaximizeButton(True).CloseButton(True).
                    FloatingSize((300, 300)). #MinSize((64, 24)).
                    BestSize((200, 100)).Icon(wx.Bitmap('images/database_connect16.png')))

        lMgrAddPane(self.CreatePeopleCtrl(), auiAuiPaneInfo().
                    Name('people').Caption(_(u'People')).
                    MinimizeButton(True).MaximizeButton(True).CloseButton(True).
                    FloatingSize((300, 300)). #MinSize((64, 24)).
                    BestSize((200, 100)).Icon(wx.Bitmap('images/database_connect16.png')))

        lMgrAddPane(self.CreateWizBAINCtrl(), auiAuiPaneInfo().
                    Name('wizbain').Caption(_(u'WizBAIN')).
                    MinimizeButton(True).MaximizeButton(True).CloseButton(True).
                    FloatingSize((300, 300)). #MinSize((64, 24)).
                    BestSize((200, 100)).Icon(wx.Bitmap('images/wizard.png'))) # TODO Where did the hat icon go?

        lMgrAddPane(self.CreatePyShell(), auiAuiPaneInfo().
                    Name('pythonshell').Caption(_(u'Wrye Shell')).
                    MinimizeButton(True).MaximizeButton(True).CloseButton(True).PinButton(True).
                    BestSize((600, 100)).Icon(wx.Bitmap('images/wryemonkey16.png')))

        # Add the toolbars to the manager.
        lMgrAddPane(tb1, auiAuiPaneInfo().
                    Name('maintoolbar').Caption(_(u'Main Toolbar')).
                    ToolbarPane().Gripper().Bottom().Row(0).Position(0).Floatable())

        lMgrAddPane(tb2, auiAuiPaneInfo().
                    Name('pluginstoolbar').Caption(_(u'Plugins Toolbar')).
                    ToolbarPane().Gripper().Left().Row(0).Position(0).Floatable())

        lMgrAddPane(tb3, auiAuiPaneInfo().
                    Name('externaltoolstoolbar').Caption(_(u'External Tools Toolbar')).
                    ToolbarPane().Gripper().Right().Row(0).Position(0).Floatable())

        # setup the initial perspective
        lMgrGetPane = self._mgr.GetPane
        lMgrGetPane('pythonshell').Show().Bottom().Dock().Layer(0).Row(1).Position(0)
        lMgrGetPane('picturealbum').Show().Left().Dock().Layer(1).Row(2).Position(0)
        lMgrGetPane('pmarchive').Show().Left().Dock().Layer(1).Row(2).Position(0)
        lMgrGetPane('people').Show().Left().Dock().Layer(1).Row(2).Position(0)
        lMgrGetPane('wizbain').Show().Left().Dock().Layer(1).Row(2).Position(0)

        lMgrGetPane('pythonshell').Hide()
        lMgrGetPane('picturealbum').Hide()
        lMgrGetPane('pmarchive').Hide()
        lMgrGetPane('people').Hide()
        lMgrGetPane('wizbain').Hide()

    def BindEvents(self):
        """
        Binds all the major main events for the application.
        """
        wxEVT_TOOL = wx.EVT_TOOL
        wxEVT_MENU = wx.EVT_MENU

        self.Bind(wxEVT_TOOL, self.TogglePane, id=ID_TOGGLEPANE_PICTUREALBUM)
        self.Bind(wxEVT_TOOL, self.TogglePane, id=ID_TOGGLEPANE_PMARCHIVE)
        self.Bind(wxEVT_TOOL, self.TogglePane, id=ID_TOGGLEPANE_PEOPLE)
        self.Bind(wxEVT_TOOL, self.TogglePane, id=ID_TOGGLEPANE_WRYESHELL)
        self.Bind(wxEVT_TOOL, self.TogglePane, id=ID_TOGGLEPANE_WIZBAIN)

    def CreateMainAuiNotebook(self):
        """Create the main AUI Notebook for the application."""

        self.gNBPanel = wx.Panel(self, -1)
        self.gNBPanel.parent = self

        global gNBPanel
        gNBPanel = self.gNBPanel

        self.gMainAuiNB = MainAuiNotebook(self.gNBPanel) # BashNotebook

        global gMainAuiNB
        gMainAuiNB = self.gMainAuiNB

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.gMainAuiNB, 1, wx.EXPAND | wx.ALL, 1)
        self.gNBPanel.SetSizer(vbSizer)

        return self.gNBPanel

    def CreatePeopleCtrl(self):
        try:
            self.gPeoplePanel = PeoplePanel(self, mainWin=self)
        except Exception:
            self.gPeoplePanel = ExceptionPanel(self)
        return self.gPeoplePanel

    def CreatePMArchiveCtrl(self):
        try:
            self.gPMArchivePanel = PMArchivePanel(self, mainWin=self)
        except Exception:
            self.gPMArchivePanel = ExceptionPanel(self)
        return self.gPMArchivePanel

    def CreatePictureAlbumCtrl(self):
        try:
            self.gPictureAlbumPanel = PictureAlbumPanel(self, mainWin=self)
        except Exception:
            self.gPictureAlbumPanel = ExceptionPanel(self)
        return self.gPictureAlbumPanel

    def CreateWizBAINCtrl(self):
        try:
            self.gWizBAINPanel = WizBAINPanel(self, mainWin=self)
        except Exception:
            self.gWizBAINPanel = ExceptionPanel(self)
        return self.gWizBAINPanel

    def CreatePyShell(self):
        USEPYCRUST = True

        if USEPYCRUST: # Use pycrust
            self.pythoncrust = py.crust.Crust(self, id=wx.ID_ANY,
                pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
                style=4194304,
                # intro='Welcome To PyCrust %s - The Flakiest Python Shell' % (py.version.VERSION),
                intro='Welcome To WryeShell %s - The Zookeepers Warning' % (py.version.VERSION),
                locals=None, InterpClass=None,
                startupScript=None, execStartupScript=True)
            self.pythonshell = self.pythoncrust.shell

        else: # Use pyshell
            self.pythonshell = py.shell.Shell(self, id=wx.ID_ANY,
                pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
                # intro='Welcome To PyCrust %s - The Flakiest Python Shell' % (py.version.VERSION),
                intro='Welcome To WryeShell %s - The Zookeepers Warning' % (py.version.VERSION),
                locals=None, InterpClass=None,
                startupScript=None, execStartupScript=True)

        global gPyShell
        gPyShell = self.gPyShell = self.pythonshell

        self.gPyShell.SetHelpText(_(u'PyShell is an interactive Python shell.'))
        try:
            return self.pythoncrust
        except Exception as exc:
            return self.pythonshell


class PictureAlbumPanel(wx.Panel):
    """
    Picture Album panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self._isInitialized = False

    def Initialize(self):
        self.dirCtrl = wx.DirPickerCtrl(self, defId, path=os.getcwd(), message=_(u'Choose a directory...'))

        self.counter = 0
        self.albumDir = 'images'

        self.gImageWildcard = wx.Image.GetImageExtWildcard()
        self.listofimages = self.GetListOfImages(self.albumDir)
        ## print(self.listofimages)

        self.bitmap = None
        self.bitmapPath = None

        self.gPicture = pic = PIC.Picture(self, style=wx.BORDER_NONE)
        # self.gPicture.SetPicture(wx.Bitmap('images/wryesplash.png'))
        self.gPicture.SetPicture(wx.Bitmap(self.listofimages[0]))

        self.pictureAlbumOptions = {
            'RandomOrder' : False,
            'IncludeSubDir' : False,
            'ChangePictureInterval(Sec)' : 5,
            'Background' : wx.BLACK_BRUSH,
            }

        # pic.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnMouseAux1DClick)
        pic.Bind(wx.EVT_MOUSE_AUX1_DOWN,   self.OnMouseAux1Down)
        # pic.Bind(wx.EVT_MOUSE_AUX1_UP,     self.OnMouseAux1Up)
        # pic.Bind(wx.EVT_MOUSE_AUX2_DCLICK, self.OnMouseAux2DClick)
        pic.Bind(wx.EVT_MOUSE_AUX2_DOWN,   self.OnMouseAux2Down)
        # pic.Bind(wx.EVT_MOUSE_AUX2_UP,     self.OnMouseAux2Up)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.dirCtrl, 0, wx.EXPAND | wx.ALL, 1)
        vbSizer.Add(pic, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

        self._isInitialized = True

    def OnMouseAux1Down(self, event):
        event.Skip()
        self.OnPrevImage(self)

    def OnMouseAux2Down(self, event):
        event.Skip()
        self.OnNextImage(self)

    def OnSetImage(self, bmp, bmpPath=None):
        self.bitmap = bmp
        self.bitmapPath = bmpPath
        gMainWin._mgr.GetPane('picturealbum').Caption('Picture Album')
        gMainWin._mgr.Update()

        self.Refresh()

    def OnPrevImage(self, event):
        if self.pictureAlbumOptions['RandomOrder']:
            self.counter = gRandInt(0, len(self.listofimages)-1)
        else:
            if self.counter == 0:
                self.counter = len(self.listofimages) - 1
            else:
                self.counter -= 1

        self.bitmap = wx.Bitmap(self.listofimages[self.counter], wx.BITMAP_TYPE_ANY)
        self.bitmapPath = self.listofimages[self.counter]

        self.gPicture.SetPicture(self.bitmap)
        print('Picture %s of %s\n%s' %(self.counter, len(self.listofimages), self.listofimages[self.counter]))
        baseName = os.path.basename(self.listofimages[self.counter])
        gMainWin._mgr.GetPane('picturealbum').Caption('Picture Album - %s' % baseName)
        gMainWin._mgr.Update()

        self.Refresh()

    def OnNextImage(self, event):
        if self.pictureAlbumOptions['RandomOrder']:
            self.counter = gRandInt(0, len(self.listofimages)-1)
        else:
            self.counter += 1
            if self.counter == len(self.listofimages):
                self.counter = 0

        self.bitmap = wx.Bitmap(self.listofimages[self.counter], wx.BITMAP_TYPE_ANY)
        self.bitmapPath = self.listofimages[self.counter]

        self.gPicture.SetPicture(self.bitmap)
        print('Picture %s of %s\n%s' %(self.counter, len(self.listofimages), self.listofimages[self.counter]))
        baseName = os.path.basename(self.listofimages[self.counter])
        gMainWin._mgr.GetPane('picturealbum').Caption('Picture Album - %s' % baseName)
        gMainWin._mgr.Update()

        # self.HideWithEffect(wx.SHOW_EFFECT_ROLL_TO_LEFT)
        # wx.CallAfter(self.ShowWithEffect, wx.SHOW_EFFECT_ROLL_TO_LEFT)

        self.Refresh()

    def GetListOfImages(self, path):
        self.listofimages = []
        lOsSep = os.sep # local optimization.
        for (path, dirs, files) in os.walk(path): # Recursive walk dir down.
            for filename in files:
                ## print(filename)
                ## print(path)
                ext = filename[filename.rfind('.'):]
                ## print(ext)
                if ext in self.gImageWildcard:
                    ## print(filename)
                    ## print(path)
                    # filepath = path + lOsSep + filename
                    # self.listofimages.append(filepath)
                    self.listofimages.append(path + lOsSep + filename)
        ## print('self.listofimages = ', self.listofimages)
        # if not self.listofimages: # Set a default image. TODO: make no images found image.
        #     # Need at least 2 images for random.
        #     self.listofimages.append('missingimage.png')
        #     self.listofimages.append('missingimage.png')

        return self.listofimages


class PMArchivePanel(wx.Panel):
    """
    PM Archive panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self._isInitialized = False

    def Initialize(self):
        self.textCtrl = wx.TextCtrl(self, -1, 'TODO PMArchivePanel', style=wx.TE_MULTILINE)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

        self._isInitialized = True

class PeoplePanel(wx.Panel):
    """
    People panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self._isInitialized = False

    def Initialize(self):
        self.textCtrl = wx.TextCtrl(self, -1, 'TODO PeoplePanel', style=wx.TE_MULTILINE)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

        self._isInitialized = True

class WizBAINPanel(wx.Panel):
    """
    WizBAIN panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self._isInitialized = False

    def Initialize(self):
        self.textCtrl = wx.TextCtrl(self, -1, 'TODO WizBAIN', style=wx.TE_MULTILINE)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

        self._isInitialized = True


class BashStatusBar(wx.StatusBar):
    #--Class Data
    ##buttons = Links()

    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, wx.ID_ANY)
        global statusBar
        statusBar = self
        self.SetFieldsCount(3)
        self.SetStatusWidths([-1, 100, 100])
        ##self.UpdateIconSizes()
        #--Bind events
        ##self.Bind(wx.EVT_SIZE, self.OnSize)
        #--Clear text notice
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        #--Setup Drag-n-Drop reordering
        self.dragging = wx.NOT_FOUND
        self.dragStart = 0
        self.moved = False

    def OnSize(self, event=None):
        """
        Handles the `wx.EVT_SIZE` event for :class:`BashStatusBar`.

        :param `event`: a `wx.EVT_SIZE` event to be processed.
        :type `event`: wx.SizeEvent
        """
        rect = self.GetFieldRect(0)
        (xPos, yPos) = (rect.x + 4, rect.y + 2)
        for button in self.buttons:
            button.SetPosition((xPos, yPos))
            xPos += self.size
        if event:
            event.Skip()

    def SetText(self, text=u'', timeout=5, statusField=1):
        """
        Set's display text as specified. Empty string clears the field.

        :param `text`: The status message to show.
        :type `text`: str
        :param `timeout`: Number of seconds fro the status message to show.
        :type `timeout`: int
        :param `statusField`: Status field to show the status message text in.
        :type `statusField`: int
        """
        self.SetStatusText(text, statusField)
        if timeout > 0:
            wx.Timer(self).Start(timeout * 1000, wx.TIMER_ONE_SHOT)

    def OnTimer(self, event):
        """
        Clears display text as specified. Empty string clears the field.

        :param `event`: a `wx.EVT_TIMER` event to be processed.
        :type `event`: wx.TimerEvent
        """
        self.SetStatusText(u'', 1)


class MainAuiNotebook(aui.AuiNotebook):
    def __init__(self, parent, id=defId, pos=defPos, size=defSize,
                 style=wx.SUNKEN_BORDER,
                 agwStyle=## aui.AUI_NB_DEFAULT_STYLE |         #AUI_NB_DEFAULT_STYLE = AUI_NB_TOP | AUI_NB_TAB_SPLIT | AUI_NB_TAB_MOVE | AUI_NB_SCROLL_BUTTONS | AUI_NB_CLOSE_ON_ACTIVE_TAB | AUI_NB_MIDDLE_CLICK_CLOSE | AUI_NB_DRAW_DND_TAB
                          aui.AUI_NB_TOP |                 #With this style, tabs are drawn along the top of the notebook
                          ## aui.AUI_NB_BOTTOM |              #With this style, tabs are drawn along the bottom of the notebook
                          ## aui.AUI_NB_LEFT |               #With this style, tabs are drawn along the left of the notebook. Not implemented yet.
                          ## aui.AUI_NB_RIGHT |              #With this style, tabs are drawn along the right of the notebook. Not implemented yet.
                          ## aui.AUI_NB_CLOSE_BUTTON |        #With this style, a close button is available on the tab bar
                          ## aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | #With this style, a close button is available on the active tab
                          ## aui.AUI_NB_CLOSE_ON_ALL_TABS |   #With this style, a close button is available on all tabs
                          aui.AUI_NB_SCROLL_BUTTONS |      #With this style, left and right scroll buttons are displayed
                          ## aui.AUI_NB_TAB_EXTERNAL_MOVE |     #Allows a tab to be moved to another tab control
                          ## aui.AUI_NB_TAB_FIXED_WIDTH |     #With this style, all tabs have the same width
                          aui.AUI_NB_TAB_MOVE |            #Allows a tab to be moved horizontally by dragging
                          aui.AUI_NB_TAB_SPLIT |           #Allows the tab control to be split by dragging a tab
                          ## aui.AUI_NB_HIDE_ON_SINGLE_TAB |  #Hides the tab window if only one tab is present
                          ## aui.AUI_NB_SUB_NOTEBOOK |        #This style is used by AuiManager to create automatic AuiNotebooks
                          ## aui.AUI_NB_MIDDLE_CLICK_CLOSE |  #Allows to close AuiNotebook tabs by mouse middle button click
                          ## aui.AUI_NB_SMART_TABS |          #Use Smart Tabbing, like Alt + Tab on Windows
                          ## aui.AUI_NB_USE_IMAGES_DROPDOWN | #Uses images on dropdown window list menu instead of check items
                          ## aui.AUI_NB_CLOSE_ON_TAB_LEFT |   #Draws the tab close button on the left instead of on the right (a la Camino browser)
                          ## aui.AUI_NB_TAB_FLOAT |           #Allows the floating of single tabs. Known limitation: when the notebook is more or less full screen, tabs cannot be dragged far enough outside of the notebook to become floating pages
                          aui.AUI_NB_DRAW_DND_TAB |        #Draws an image representation of a tab while dragging (on by default)
                          ## aui.AUI_NB_ORDER_BY_ACCESS |     #Tab navigation order by last access time for the tabs
                          ## aui.AUI_NB_NO_TAB_FOCUS |        #Don’t draw tab focus rectangle
                          aui.AUI_NB_WINDOWLIST_BUTTON       #With this style, a drop-down list of windows is available
                          , name='auinotebook'):
        aui.AuiNotebook.__init__(self, parent, id, pos, size, agwStyle, name)

        self._notebook_style = agwStyle
        self._notebook_theme = 0

        art = auiNBArts[self._notebook_theme]()
        self.SetArtProvider(art)

        self.SetAGWWindowStyleFlag(agwStyle)

        self.gTabContainer = self.GetTabContainer()

        wx.CallAfter(self.BindTabCtrlMouseEvents) # TODO(priority=7) ~Better to move this after Tabs are loaded~

    def BindTabCtrlMouseEvents(self):

        self.gTabCtrl = self.GetTabCtrlFromPoint((10, 10))
        self.gTabCtrl.Bind(wx.EVT_MOUSE_EVENTS, self.OnTabCtrlMouseEvents) # wx.EVT_MOUSEWHEEL doesn't work 4 this???
        return

        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnMouseAux1DClick)
        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX1_DOWN, self.OnMouseAux1Down)
        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX1_UP, self.OnMouseAux1Up)
        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX2_DCLICK, self.OnMouseAux2DClick)
        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX2_DOWN, self.OnMouseAux2Down)
        self.gTabCtrl.Bind(wx.EVT_MOUSE_AUX2_UP, self.OnMouseAux2Up)

    def OnTabCtrlMouseEvents(self, event):
        event.Skip()
        evtType = event.GetEventType()
        if evtType in wx.EVT_ENTER_WINDOW.evtType:
            self.gTabCtrl.SetFocus() # For mousewheel tab switching.
        elif evtType in wx.EVT_LEAVE_WINDOW.evtType:
            # The only way to remove focus from a widget is to set focus to
            # some other widget that accepts focus.
            self.GetCurrentPage().SetFocus()
        elif evtType in wx.EVT_MOUSEWHEEL.evtType:
            wr = event.GetWheelRotation()
            ## ctrlDown = event.ControlDown()
            ## shiftDown = event.ShiftDown()
            ## altDown = event.AltDown()
            ## print('GetWheelRotation: ', wr)
            ## print('GetWheelDelta: ', event.GetWheelDelta())
            if wr < 0:#negative/down Ex: -120
                self.AdvanceSelection(True)
                ## print('WheelDown')
            elif wr > 0:#positive/up Ex: 120
                self.AdvanceSelection(False)
                ## print('WheelUp')
            print('OnTabCtrlMouseEvents')

#------------------------------------------------------------------------------

class InstallersList(wx.ListCtrl):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                     | wx.LC_REPORT
                     | wx.LC_EDIT_LABELS
                     | wx.LC_SORT_ASCENDING,
                 validator=wx.DefaultValidator,
                 name='listctrl'):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)

        for i, label in enumerate((_(u'Package'),
                                  _(u'Order'),
                                  _(u'Modified'),
                                  _(u'Size'),
                                  _(u'Files'))
                                  ):
            self.InsertColumn(i, label)
            self.SetColumnWidth(i, 100)
        for i in range(301):
            self.InsertItem(sys.maxint, 'TestArchive%s.7z' % i)

class InstallersDetails(wx.Panel):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.SetBackgroundColour(wx.GREEN)

class InstallersPanel(wx.Panel):
    """
    Installers panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self.threeWaySplitter = tws = TWS.ThreeWaySplitter(self, -1, agwStyle=wx.SP_LIVE_UPDATE)
        tws.SetWindowsPopupLabels(
            window0PopupLabel=_(u'Installers List'),
            window1PopupLabel=_(u'Installers Details'),
            window2PopupLabel=_(u'Installers Other'))

        self.gInstallersListCtrl = InstallersList(tws, mainWin=self)
        tws.AppendWindow(self.gInstallersListCtrl)

        self.gInstallersDetails = InstallersDetails(tws, mainWin=self)
        tws.AppendWindow(self.gInstallersDetails)

        self.gInstallersScreenshot = PIC.Picture(tws, style=wx.BORDER_SUNKEN)
        self.gInstallersScreenshot.SetPicture(wx.Bitmap('images/wryesplash.png'))
        tws.AppendWindow(self.gInstallersScreenshot)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.threeWaySplitter, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

#------------------------------------------------------------------------------

class ModsList(wx.ListCtrl):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                     | wx.LC_REPORT
                     | wx.LC_EDIT_LABELS
                     | wx.LC_SORT_ASCENDING,
                 validator=wx.DefaultValidator,
                 name='listctrl'):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)

        for i, label in enumerate((_(u'File'),
                                  _(u'Load Order'),
                                  _(u'Rating'),
                                  _(u'Group'),
                                  _(u'Installer'),
                                  _(u'Modified'),
                                  _(u'Size'),
                                  _(u'Author'),
                                  _(u'CRC'),
                                  _(u'Mod Status'))
                                  ):
            self.InsertColumn(i, label)
            self.SetColumnWidth(i, 100)
        for i in range(301):
            self.InsertItem(sys.maxint, 'TestMod%s.esp' % i)

class MasterList(wx.ListCtrl):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                     | wx.LC_REPORT
                     | wx.LC_EDIT_LABELS
                     | wx.LC_SORT_ASCENDING,
                 validator=wx.DefaultValidator,
                 name='listctrl'):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)

        for i, label in enumerate((_(u'File'),
                                  _(u'MI'),
                                  _(u'Current LO'))
                                  ):
            self.InsertColumn(i, label)
            self.SetColumnWidth(i, 100)
        for i in range(301):
            self.InsertItem(sys.maxint, 'TestMod%s.esp' % i)

class ModsDetails(scrolled.ScrolledPanel):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.BORDER_SUNKEN, name='panel'):
        scrolled.ScrolledPanel.__init__(self, parent, id, pos, size, style, name)

        if True:
            self.file_versionPanel = wx.Panel(self, -1)
            self.save_cancelPanel = wx.Panel(self, -1)
            #--Version
            self.version = wx.StaticText(self.file_versionPanel, -1, u'v0.00')
            Id_file = self.fileId = wx.NewId()
            #--File Name
            self.file = wx.TextCtrl(self, Id_file)#,size=(textWidth,-1))
            self.file.SetMaxLength(200)
            #TODO/HOOKIN# self.file.Bind(wx.EVT_KILL_FOCUS, self.OnEditFile)
            #TODO/HOOKIN# self.file.Bind(wx.EVT_TEXT, self.OnTextEdit)
            #--Author
            Id_author = self.authorId = wx.NewId()
            self.author = wx.TextCtrl(self, Id_author)
            self.author.SetMaxLength(512)
            #TODO/HOOKIN# self.author.Bind(wx.EVT_KILL_FOCUS, self.OnEditAuthor)
            #TODO/HOOKIN# self.author.Bind(wx.EVT_TEXT, self.OnTextEdit)
            #--Modified
            Id_modified = self.modifiedId = wx.NewId()
            self.modified = wx.TextCtrl(self, Id_modified, u'') # size=(textWidth,-1)
            self.modified.SetMaxLength(32)
            #TODO/HOOKIN# self.modified.Bind(wx.EVT_KILL_FOCUS, self.OnEditModified)
            #TODO/HOOKIN# self.modified.Bind(wx.EVT_TEXT, self.OnTextEdit)
            #--Description
            Id_description = self.descriptionId = wx.NewId()
            self.descriptionResizeWidget = RW.ResizeWidget(self)
            self.description = (
                wx.TextCtrl(self, Id_description, u'', size=(-1, 150), style=wx.TE_MULTILINE)) # , size=(textWidth, 150)
            self.description.SetMaxLength(512) # NOTE: Not all games will enforce this limit. Beth esp/m format has this limit tho.
            self.descriptionResizeWidget.SetManagedChild(self.description)
            #TODO/HOOKIN# self.description.Bind(wx.EVT_KILL_FOCUS, self.OnEditDescription)
            #TODO/HOOKIN# self.description.Bind(wx.EVT_TEXT, self.OnTextEdit)
            #--Masters
            Id_masters = self.mastersId = wx.NewId()
            #TODO/HOOKIN# self.masters = MasterList(masterPanel, None, self.SetEdited)
            self.masters = MasterList(self, Id_masters)
            #--Save/Cancel
            self.save = wx.Button(self.save_cancelPanel, wx.ID_SAVE, _(u'Save')) # ,onClick=self.DoSave,
            self.cancel = wx.Button(self.save_cancelPanel, wx.ID_CANCEL, _(u'Cancel')) # ,onClick=self.DoCancel,
            self.save.Disable()
            self.cancel.Disable()
            #--Bash tags
            #TODO/HOOKIN# self.allTags = bosh.allTags
            self.bashTagsResizeWidget = RW.ResizeWidget(self)
            Id_tags = self.tagsId = wx.NewId()
            self.gTags = (
                wx.TextCtrl(self, Id_tags, u'', size=(-1, 100), style=wx.TE_MULTILINE | wx.TE_READONLY))
            self.bashTagsResizeWidget.SetManagedChild(self.gTags)

        #--Events
        #TODO/HOOKIN# self.gTags.Bind(wx.EVT_CONTEXT_MENU, self.ShowBashTagsMenu)
        #TODO/HOOKIN# self.Bind(wx.EVT_MENU, self.DoAutoBashTags, id=ID_TAGS.AUTO)
        #TODO/HOOKIN# self.Bind(wx.EVT_MENU, self.DoCopyBashTags, id=ID_TAGS.COPY)
        #TODO/HOOKIN# self.Bind(wx.EVT_MENU_RANGE, self.ToggleBashTag, id=ID_TAGS.BASE, id2=ID_TAGS.MAX)

        self.Bind(RW.EVT_RW_LAYOUT_NEEDED, self.OnResizeWidgetLayoutNeeded)

        #--Sizers/Layout
        vbSizer = wx.BoxSizer(wx.VERTICAL)

        hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer1.Add(wx.StaticText(self.file_versionPanel, -1, _(u"File:")), 1, wx.EXPAND | wx.ALIGN_LEFT, 0)
        hbSizer1.AddStretchSpacer()
        hbSizer1.Add(self.version, 0, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        self.file_versionPanel.SetSizer(hbSizer1)
        vbSizer.Add(self.file_versionPanel, 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)

        vbSizer.Add(self.file, 0, wx.EXPAND | wx.ALL, 3)
        vbSizer.Add(wx.StaticText(self, -1, _(u"Author:")), 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)
        vbSizer.Add(self.author, 0, wx.EXPAND | wx.ALL, 3)
        vbSizer.Add(wx.StaticText(self, -1, _(u"Modified:")), 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)
        vbSizer.Add(self.modified, 0, wx.EXPAND | wx.ALL, 3)
        vbSizer.Add(wx.StaticText(self, -1, _(u"Description:")), 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)
        vbSizer.Add(self.descriptionResizeWidget, 0, wx.EXPAND | wx.ALL, 3)
        vbSizer.Add(wx.StaticText(self, -1, _(u"Masters:")), 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)
        vbSizer.Add(self.masters, 0, wx.EXPAND | wx.ALL, 3)

        hbSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer2.Add(self.save, 1, wx.EXPAND | wx.RIGHT | wx.ALIGN_LEFT, 3)
        hbSizer2.AddSpacer(3)
        hbSizer2.Add(self.cancel, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        self.save_cancelPanel.SetSizer(hbSizer2)
        vbSizer.Add(self.save_cancelPanel, 0, wx.EXPAND | wx.ALL, 3)

        vbSizer.Add(wx.StaticText(self, -1, _(u"Bash Tags:")), 0, wx.EXPAND | wx.LEFT | wx.TOP, 3)
        vbSizer.Add(self.bashTagsResizeWidget, 0, wx.EXPAND | wx.ALL, 3)

        #PENDING_PHOENIX_PR# self.bashTagsResizeWidget.SetDimensions(6, 32)
        #PENDING_PHOENIX_PR# self.bashTagsResizeWidget.SetColors(wx.BLACK, wx.BLUE, wx.GREEN)

        self.SetSizer(vbSizer)
        self.SetupScrolling(False, True) # Only show vert scrollbar.

        self.Bind(wx.EVT_SIZE, self.OnSize)
        sb = wx.ScrollBar(self, size=(-1, 100), style=wx.SB_VERTICAL)
        self.defScrollBarWidth = sb.GetSize()[0]
        sb.Hide()
        wx.CallAfter(self.RemoveChild, sb)

        ## self.SetDoubleBuffered(True) # Overkill switch

    def OnResizeWidgetLayoutNeeded(self, event):
        self.OnSize()
        self.PostSizeEvent()

    def OnSize(self, event=None):
        """
        Handle the wx.SIZE event for :class:`ModsDetails`.

        :param `event`: A `wx.SizeEvent` to be processed.
        :type `event`: A `wx.SizeEvent`
        """
        # What is happening here is we are trying to control the width of
        # all the widgets in the scrolled panel while only having the vertical
        # scrollbar showing, so that automatic layout acts as wanted.
        # This is achieved by all the items in the VERTICAL BoxSizer being in-line
        # per-say or just one item with children(why the buttons are in a hbSizer panel as children)
        # A bit strange approach, but it works. sorta like a autoadjusting wrapsizer,
        # but for a scrolled panel.

        evtSizeW = self.GetSize()[0] - 10
        if self.GetScrollThumb(wx.VERTICAL): # Not 0; The vert scrollbar is showing.
            localOptW = self.defScrollBarWidth
            [wx.CallAfter(w.SetSize, evtSizeW - localOptW, -1)
                for w in self.GetChildren()]
        else:
            [wx.CallAfter(w.SetSize, evtSizeW, -1)
                for w in self.GetChildren()]
        self.Layout()
        self.Refresh()
        ## print('OnSize = %s' % self.GetSize())
        ## print('GetScrollThumb', self.GetScrollThumb(wx.VERTICAL))

class ModsPanel(wx.Panel):
    """
    Mods panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self.threeWaySplitter = tws = TWS.ThreeWaySplitter(self, -1, agwStyle=wx.SP_LIVE_UPDATE)
        tws.SetWindowsPopupLabels(
            window0PopupLabel=_(u'Mods List'),
            window1PopupLabel=_(u'Mods Details'),
            window2PopupLabel=_(u'Mods Screenshot'))

        self.gModsListCtrl = ModsList(tws, mainWin=self)
        tws.AppendWindow(self.gModsListCtrl)

        self.gModsDetails = ModsDetails(tws, mainWin=self)
        tws.AppendWindow(self.gModsDetails)

        self.gModsScreenshot = PIC.Picture(tws, style=wx.BORDER_SUNKEN)
        self.gModsScreenshot.SetPicture(wx.Bitmap('images/wryesplash.png'))
        tws.AppendWindow(self.gModsScreenshot)

        ## tws.SetSplitterMinSize(50, 50)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.threeWaySplitter, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

#------------------------------------------------------------------------------

class SavesList(wx.ListCtrl):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN
                     | wx.LC_REPORT
                     | wx.LC_EDIT_LABELS
                     | wx.LC_SORT_ASCENDING,
                 validator=wx.DefaultValidator,
                 name='listctrl'):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)

        for i, label in enumerate((_(u'File'),
                                  _(u'Modified'),
                                  _(u'Size'),
                                  _(u'Hours'),
                                  _(u'Player'),
                                  _(u'Cell'))
                                  ):
            self.InsertColumn(i, label)
            self.SetColumnWidth(i, 100)
        for i in range(301):
            self.InsertItem(sys.maxint, 'TestSave%s.ess' % i)

class SavesDetails(wx.Panel):
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.SetBackgroundColour(wx.BLUE)

class SavesPanel(wx.Panel):
    """
    Saves panel.
    """
    def __init__(self, parent, mainWin, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # global gMainWin
        # gMainWin = mainWin

        self.threeWaySplitter = tws = TWS.ThreeWaySplitter(self, -1, agwStyle=wx.SP_LIVE_UPDATE)
        tws.SetWindowsPopupLabels(
            window0PopupLabel=_(u'Saves List'),
            window1PopupLabel=_(u'Saves Details'),
            window2PopupLabel=_(u'Saves Screenshot'))

        self.gSavesListCtrl = SavesList(tws, mainWin=self)
        tws.AppendWindow(self.gSavesListCtrl)

        self.gSavesDetails = SavesDetails(tws, mainWin=self)
        tws.AppendWindow(self.gSavesDetails)

        self.gSavesScreenshot = PIC.Picture(tws, style=wx.BORDER_SUNKEN)
        self.gSavesScreenshot.SetPicture(wx.Bitmap('images/help32.png'))
        tws.AppendWindow(self.gSavesScreenshot)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(tws, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(vbSizer)

#------------------------------------------------------------------------------

class WryeBashApp(wx.App):
    """Bash Application class."""
    def Init(self): # not OnInit(), we need to initialize _after_ the app has been instanced
        global appRestart
        appRestart = False
        """wxWindows: Initialization handler."""

        # frame = BashFrame(pos=settings['bash.framePos'], size=settings['bash.frameSize'])
        frame = BashFrame(size=(800, 600))

        self.SetTopWindow(frame)
        frame.Show()

    def OnInit(self):
        self.Init()

        return True


if __name__ == '__main__':

    gApp = WryeBashApp(redirect=False, # stdio will stay at the console...
                       filename=None, # Will redirect stdout to 'filespec'.
                       useBestVisual=False,
                       clearSigInt=True)

    gApp.MainLoop()

