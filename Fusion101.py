# Author-Julia & Sören
# Description-Fusion101 provides you a gentle introduction into the basics of Fusion360 by providing step-by-step tutorials to multiple topics.

import adsk.core
import adsk.fusion
import adsk.cam
import traceback

from .PopUpCommandHandler import PopUpCommandCreatedEventHandler
from .TutorialButtonHandler import CommandCreatedEventHandlerQATRight
from .ShowPalletEventHandler import ShowPaletteCommandCreatedHandler
from .constants import PALLET_ID

# global set of event handlers to keep them referenced for the duration of the command
handlers = []
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
num = 0
isDontShowAgain = False

extrudeCount = 0

def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Add a command that displays the panel.
        showPaletteCmdDef = _ui.commandDefinitions.itemById('showPalette')
        if not showPaletteCmdDef:
            showPaletteCmdDef = _ui.commandDefinitions.addButtonDefinition('showPalette', 'Show Fusion 101',
                                                                           'Show the custom palette', '')

            # Connect to Command Created event.
            onCommandCreated = ShowPaletteCommandCreatedHandler(handlers)
            showPaletteCmdDef.commandCreated.add(onCommandCreated)
            handlers.append(onCommandCreated)

        # AddInSAMPLE
        cmdDef = _ui.commandDefinitions

        # add a button command on Quick Access Toolbar
        if not _ui.toolbars.itemById('QATRight').controls.itemById('TutorialButtonOnQATRight'):
            btnCmdDefinitionQATRight_ = cmdDef.itemById('TutorialButtonOnQATRight')
            if not btnCmdDefinitionQATRight_:
                btnCmdDefinitionQATRight_ = cmdDef.addButtonDefinition('TutorialButtonOnQATRight', 'Tutorial Command',
                                                                       'Tutorial Command', './resources')
            onButtonCommandCreated = CommandCreatedEventHandlerQATRight(handlers)
            btnCmdDefinitionQATRight_.commandCreated.add(onButtonCommandCreated)

            # keep the handler referenced beyond this function
            handlers.append(onButtonCommandCreated)

            # Connect to Command Created event.
            handlers.append(onCommandCreated)
            _ui.toolbars.itemById('QATRight').controls.addCommand(btnCmdDefinitionQATRight_).isVisible = True

        # Create the popUpButton command definition
        popUpButton = cmdDef.addButtonDefinition(
            'popUpButton01PYTHON',
            'Tutorial PopUp',
            'Imaginary tutorial PopUp Button that is not visible anywhere in the UI',
            ''
        )

        # Connect to the command created event
        popUpCommandCreated = PopUpCommandCreatedEventHandler(handlers)
        popUpButton.commandCreated.add(popUpCommandCreated)
        handlers.append(popUpCommandCreated)

        cmd = cmdDef.itemById('popUpButton01PYTHON')

        cmd.execute()

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        ############addinsample######
        objArrayQATRight = []

        if _ui.toolbars.itemById('QATRight').controls.itemById('TutorialButtonOnQATRight'):
            objArrayQATRight.append(_ui.toolbars.itemById('QATRight').controls.itemById('TutorialButtonOnQATRight'))

        btnCmdDefinitionQATRight_ = _ui.commandDefinitions.itemById('TutorialButtonOnQATRight')
        if btnCmdDefinitionQATRight_:
            objArrayQATRight.append(btnCmdDefinitionQATRight_)

        for obj in objArrayQATRight:
            if _ui and obj:
                if obj.isValid:
                    obj.deleteMe()
                else:
                    _ui.messageBox('obj is not a valid object')

        #############addinsample######

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

        popUp = _ui.commandDefinitions.itemById('popUpButton01PYTHON')
        if popUp:
            popUp.deleteMe()

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
