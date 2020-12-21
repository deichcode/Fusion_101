# Author-Julia & Sören
# Description-Fusion101 provides you a gentle introduction into the basics of Fusion360 by providing step-by-step tutorials to multiple topics.

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
from .constants import PALLET_ID, PALLET_NAME, PALLET_URL
import json

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
num = 0


# Event handler for the commandExecuted event.
class ShowPaletteCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Create and display the palette.
            palette = _ui.palettes.itemById(PALLET_ID)
            if not palette:
                palette = initializePalette()
    
                # Add handler to HTMLEvent of the palette.
                onHTMLEvent = MyHTMLEventHandler()
                palette.incomingFromHTML.add(onHTMLEvent)   
                handlers.append(onHTMLEvent)
    
                # Add handler to CloseEvent of the palette.
                onClosed = MyCloseEventHandler()
                palette.closed.add(onClosed)
                handlers.append(onClosed)   
            else:
                palette.isVisible = True                               
        except:
            _ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()              
    def notify(self, args):
        try:
            command = args.command
            onExecute = ShowPaletteCommandExecuteHandler()
            command.execute.add(onExecute)
            handlers.append(onExecute)                                     
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))     


# Event handler for the commandExecuted event.
class SendInfoCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Send information to the palette. This will trigger an event in the javascript
            # within the html so that it can be handled.
            palette = _ui.palettes.itemById('myPalette')
            if palette:
                global num
                num += 1
                palette.sendInfoToHTML('send', 'This is a message sent to the palette from Fusion. It has been sent {} times.'.format(num))                        
        except:
            _ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class SendInfoCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()              
    def notify(self, args):
        try:
            command = args.command
            onExecute = SendInfoCommandExecuteHandler()
            command.execute.add(onExecute)
            handlers.append(onExecute)                                     
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))     


# Event handler for the palette close event.
class MyCloseEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            _ui.messageBox('Close button is clicked.') 
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the palette HTML event.                
class MyHTMLEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
            # data = json.loads(htmlArgs.data)
            # msg = "An event has been fired from the html to Fusion with the following data:\n"
            # msg += '    Command: {}\n    arg1: {}\n    arg2: {}'.format(htmlArgs.action, data['arg1'], data['arg2'])
            _ui.palettes.itemById(PALLET_ID).deleteMe()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))           

                
def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui  = _app.userInterface
        
        # Add a command that displays the panel.
        showPaletteCmdDef = _ui.commandDefinitions.itemById('showPalette')
        if not showPaletteCmdDef:
            showPaletteCmdDef = _ui.commandDefinitions.addButtonDefinition('showPalette', 'Show Fusion 101', 'Show the custom palette', '')

            # Connect to Command Created event.
            onCommandCreated = ShowPaletteCommandCreatedHandler()
            showPaletteCmdDef.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)
        
         
        # Add a command under ADD-INS panel which sends information from Fusion to the palette's HTML.
        sendInfoCmdDef = _ui.commandDefinitions.itemById('sendInfoToHTML')
        if not sendInfoCmdDef:
            sendInfoCmdDef = _ui.commandDefinitions.addButtonDefinition('sendInfoToHTML', 'Send info to Palette', 'Send Info to Palette HTML', '')

            # Connect to Command Created event.
            onCommandCreated = SendInfoCommandCreatedHandler()
            sendInfoCmdDef.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)

        # Add the command to the toolbar.
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = panel.controls.itemById('showPalette')
        if not cntrl:
            panel.controls.addCommand(showPaletteCmdDef)

        cntrl = panel.controls.itemById('sendInfoToHTML')
        if not cntrl:
            panel.controls.addCommand(sendInfoCmdDef)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:        
        # Delete the palette created by this add-in.
        palette = _ui.palettes.itemById(PALLET_ID)
        if palette:
            palette.deleteMe()
            
        # Delete controls and associated command definitions created by this add-ins
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cmd = panel.controls.itemById('showPalette')
        if cmd:
            cmd.deleteMe()
        cmdDef = _ui.commandDefinitions.itemById('showPalette')
        if cmdDef:
            cmdDef.deleteMe() 

        cmd = panel.controls.itemById('sendInfoToHTML')
        if cmd:
            cmd.deleteMe()
        cmdDef = _ui.commandDefinitions.itemById('sendInfoToHTML')
        if cmdDef:
            cmdDef.deleteMe() 
            
        _ui.messageBox('Stop addin')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def initializePalette():
    fusion101Palette = _ui.palettes.add(
        PALLET_ID,
        PALLET_NAME,
        PALLET_URL,
        isVisible=True,
        showCloseButton=True,
        isResizable=False,
        width=400,
        height=800)
    fusion101Palette.dockingOption = adsk.core.PaletteDockingOptions.PaletteDockOptionsToVerticalOnly
    fusion101Palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateLeft
    fusion101Palette.setMaximumSize = 400
    fusion101Palette.setMinimumSize = 300
    return fusion101Palette