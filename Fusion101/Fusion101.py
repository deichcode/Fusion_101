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
isDontShowAgain = False


# Event handler for the commandExecuted event.
class ShowPaletteCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            #Open new document
            _app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)



            # Create and display the palette.
            palette = _ui.palettes.itemById(PALLET_ID)
            if not palette:
                palette = initializePalette()
                palette.isVisible = True

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

            # Add handler to react in palette on startedCommands
            onCommandStarting = MyCommandStartingHandler(palette)
            _ui.commandStarting.add(onCommandStarting)
            handlers.append(onCommandStarting)
            
            
            # Add handler to react in palette on terminatedCommands
            onCommandTerminated = MyCommandTerminatedHandler(palette)
            _ui.commandTerminated.add(onCommandTerminated)
            handlers.append(onCommandTerminated)    

            # Add handler to react in palette on changes of the camera
            onCameraChanged = MyCameraChangedHandler(palette)
            _app.cameraChanged.add(onCameraChanged)
            handlers.append(onCameraChanged)     

            # Add handler to react in palette on changes of the active selection
            onActiveSelectionChanged = MyActiveSelectionChangedHandler(palette)
            _ui.activeSelectionChanged.add(onActiveSelectionChanged)
            handlers.append(onActiveSelectionChanged)


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
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)            
            data = json.loads(htmlArgs.data)
            # msg = "An event has been fired from the html to Fusion with the following data:\n"
            # msg += '    Command: {}\n    arg1: {}\n    arg2: {}'.format(htmlArgs.action, data['arg1'], data['arg2'])
            if data['command'] == 'close':
                palette = _ui.palettes.itemById(PALLET_ID)
                if palette:
                    palette.isVisible = False
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))           



###########AddInSample#################################


#CommandExecuteHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.firingEvent.sender
                    _ui.messageBox('command: {} executed successfully').format(command.parentCommandDefinition.id)
                except:
                    if _ui:
                        _ui.messageBox('command executed failed: {}').format(traceback.format_exc())

#CommandCreatedHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class CommandCreatedEventHandlerQATRight(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.command
                    #onExecute = CommandExecuteHandler()
                    onExecute = ShowPaletteCommandExecuteHandler()
                    command.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    #_ui.messageBox('Right QAT command created successfully')
                except:
                    _ui.messageBox(' Right QAT command created failed: {}').format(traceback.format_exc())               
###########AddinSample#################

#Event handler for the commandCreated event
class popUpCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        
        #Get the command
        command = eventArgs.command

        #Get the CommandInputs collection for new inputs
        inputs = command.commandInputs


        command.cancelButtonText = 'Close'
        command.okButtonText = 'Start Fusion 101'

        #Create a "textBox" with the welcoming text
        welcomeText = inputs.addTextBoxCommandInput(
            'welcomeText', 
            '',
            '<div align="center"><b>Welcome to Fusion 101!</b></div>',
            3,
            True
        )

        #Create a "textBox" with the description of the tutorial
        introductionText = inputs.addTextBoxCommandInput(
            'introductionText', 
            '',
            '<div align="center">This interactive tutorial will guide you through'+
            ' your first steps in Fusion 360. You will get to know the most important'+
            ' tools, workflows and concepts to kickstart your own ideas</div>.',
            6,
            True
        )

        #Create a "textBox" with the second description of the tutorial
        introductionText2 = inputs.addTextBoxCommandInput(
            'introductionText2', 
            '',
            '<div align="center">To start Fusion 101 later just click on the HAT symbol'+
            ' next to your profile picture or initials in the upper right Quick Access Bar of your screen</div>.',
            6,
            True
        )

        #Create a check box asking for random or explicit number of rings
        dontShowAgain = inputs.addBoolValueInput('dontShowAgain', 'Don\'t show again', True, '', False)



        #Connect to the execute event
        onExecute = popUpCommandExecuteHandler()
        command.execute.add(onExecute)
        handlers.append(onExecute)

        #Connect to the inputChanged event
        onInputChanged = popUpCommandInputChangedHandler()
        command.inputChanged.add(onInputChanged)
        handlers.append(onInputChanged)

#Event handler for the inputChanged event
class popUpCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)

        #Check the value of dont show again
        changedInput = eventArgs.input
        if changedInput.id == 'dontShowAgain':
            
        

            if changedInput.value == True:
                #inputs = eventArgs.firingEvent.sender.commandInputs
                #sliderInput = inputs.itemById('explicitAmountOfRings')
                #command = adsk.core.CommandCreatedEventArgs.cast(args)
                #commands = command.firingEvent.sender.command
                #commands = "Remind me next time"
               # command.cancelButtonText = 'Remind me next time'
                print(eventArgs.objectType)
                isDontShowAgain = True
                print(isDontShowAgain)
            else:

                isDontShowAgain = False
                print(isDontShowAgain)

#Event handler for the execute event
class popUpCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        #Code to react to the event
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Tutorial will start now')

        #Get values from command inputs
        inputs = eventArgs.command.commandInputs

        cmd = ui.commandDefinitions.itemById('TutorialButtonOnQATRight')
        cmd.execute()

class UserInterfaceGeneralEventHandlerImpl(adsk.core.UserInterfaceGeneralEvent):
    # def __init__(self):
    #     super().__init__()
    def notify(self, args):
        print(args)         

# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-EBB6C82A-A256-4AB7-9A86-0F7A9653A7E9
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        # Code to react to the event.
        # _ui.messageBox(str(eventArgs))
        #print(eventArgs.commandId)

        #print(_ui.activeSelections.count)


        app = adsk.core.Application.get()
        ui  = app.userInterface
        #Get the collection: CommandDefinitions
        commandDefinitions = ui.commandDefinitions

        #Get current design
        design = adsk.fusion.Design.cast(app.activeProduct)
        #If there is no active design, send error message
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        #Get root of active design
        rootComp = design.rootComponent

        #3D Points
        point = adsk.core.Point3D

        #Create new sketch on xy plane
        sketches = rootComp.sketches
        sketch = sketches.item(0)

        print(sketch.referencePlane == rootComp.xYConstructionPlane)
        if not self.palette:
            return
        if eventArgs.commandId == 'SketchCreate':
                self.palette.sendInfoToHTML('send', 'clickedCreateSketch')
        #Das mag noch geändert werden wenn wir es in real Time schaffen
        elif (sketch.referencePlane == rootComp.xYConstructionPlane):
                self.palette.sendInfoToHTML('send', 'selectXYPlane')
        elif eventArgs.commandId == 'ShapeRectangleCenter':
                self.palette.sendInfoToHTML('send', 'clickedCenterRectangle')
        elif eventArgs.commandId == 'SketchStop':
                self.palette.sendInfoToHTML('send', 'clickedFinishSketch')
        elif eventArgs.commandId == 'Extrude':
                self.palette.sendInfoToHTML('send', 'clickedExtrudeFeauture')
        elif eventArgs.commandId == 'DrawPolyline':
                self.palette.sendInfoToHTML('send', 'clickedLine')
        elif eventArgs.commandId == 'FusionShellBodyCommand':
                self.palette.sendInfoToHTML('send', 'clickedOnShell')
        elif eventArgs.commandId == 'ShapeRectangleTwoPoint':
                self.palette.sendInfoToHTML('send', 'clicked2PointRectangle')
        elif eventArgs.commandId == 'WorkPlaneOffsetFromPlaneCommand':
                self.palette.sendInfoToHTML('send', 'clickedOffsetPlane')
        elif eventArgs.commandId == 'PrimitiveBox':
                self.palette.sendInfoToHTML('send', 'clickedBox')
        #Confirm == Box?
        elif eventArgs.commandId == 'Cylinder':
                self.palette.sendInfoToHTML('send', 'clickedCylinder')
        elif eventArgs.commandId == 'CircleCenterRadius':
                self.palette.sendInfoToHTML('send', 'clickedCircle')
        elif eventArgs.commandId == 'SolidLoft':
                self.palette.sendInfoToHTML('send', 'clickedLoft')
    




class MyCommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        args = eventArgs

        # Code to react to the event.
        # _ui.messageBox(str(eventArgs))

# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-7D12B291-979B-4620-870F-D4C10E72DE1E
class MyCameraChangedHandler(adsk.core.CameraEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CameraEventArgs.cast(args)
        args = eventArgs
        # Code to react to the event.
        # _ui.messageBox(eventArgs.commandId)

#https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-19D8AC9F-E4F7-4E8A-8B3C-9D128EF932F3
# Event handler for the activeSelectionChanged event.
class MyActiveSelectionChangedHandler(adsk.core.ActiveSelectionEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.ActiveSelectionEventArgs.cast(args)


        for selection in eventArgs.currentSelection:
            print(selection)
        #print(eventArgs.currentSelection.entity.classType == adsk.fusion.BRepBody.classType)

        # Code to react to the event.
        ui.messageBox('In MyActiveSelectionChangedHandler event handler.')


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


                #######AddInSAMPLE######

        cmdDef = _ui.commandDefinitions

        # add a button command on Quick Access Toolbar
        if not _ui.toolbars.itemById('QATRight').controls.itemById('TutorialButtonOnQATRight'):
            btnCmdDefinitionQATRight_ = cmdDef.itemById('TutorialButtonOnQATRight')
            if not btnCmdDefinitionQATRight_:
                btnCmdDefinitionQATRight_ = cmdDef.addButtonDefinition('TutorialButtonOnQATRight', 'Tutorial Command', 'Tutorial Command', './resources')
            onButtonCommandCreated = CommandCreatedEventHandlerQATRight()
            btnCmdDefinitionQATRight_.commandCreated.add(onButtonCommandCreated)

            # keep the handler referenced beyond this function
            handlers.append(onButtonCommandCreated)


            # Connect to Command Created event.
            handlers.append(onCommandCreated)
            _ui.toolbars.itemById('QATRight').controls.addCommand(btnCmdDefinitionQATRight_).isVisible = True
            _ui.messageBox('A Tutorial button command is successfully added to the right Quick Access Toolbar')
            

        ###### AddInSample ############

        #Create the popUpButton command definition
        popUpButton = cmdDef.addButtonDefinition(
            'popUpButton01PYTHON', 
            'Tutorial PopUp', 
            'Imaginary tutorial PopUp Button that is not visible anywhere in the UI',
            ''
        )

        #Connect to the command created event
        popUpCommandCreated = popUpCommandCreatedEventHandler()
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
                    _ui.messageBox(_('obj is not a valid object'))


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
        #popUp = _ui.commandDefinitions.itemById('popUpButton01PYTHON')
        if popUp:
            popUp.deleteMe()
            
        _ui.messageBox('Stop addin')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def initializePalette():
    fusion101Palette = _ui.palettes.add(
        PALLET_ID,
        PALLET_NAME,
        PALLET_URL,
        isVisible=False,
        showCloseButton=True,
        isResizable=True,
        width=400,
        height=800,
        useNewWebBrowser=False)
    fusion101Palette.dockingOption = adsk.core.PaletteDockingOptions.PaletteDockOptionsToVerticalOnly
    fusion101Palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateLeft
    fusion101Palette.setMaximumSize = 400
    fusion101Palette.setMinimumSize = 300
    return fusion101Palette