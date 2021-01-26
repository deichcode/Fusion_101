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

extrudeCount = 0


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
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            # msg = "An event has been fired from the html to Fusion with the following data:\n"
            # msg += '    Command: {}\n    arg1: {}\n    arg2: {}'.format(htmlArgs.action, data['arg1'], data['arg2'])
            if data['command'] == 'close':
                palette = _ui.palettes.itemById(PALLET_ID)
                if palette:
                    palette.isVisible = False

            chaptersToBeSkipped
            if data['command'] == 'skipChapter1':
                chaptersToBeSkipped = 1
            if data['command'] == 'skipChapter2':
                chaptersToBeSkipped = 2
            if data['command'] == 'skipChapter3':
                chaptersToBeSkipped = 3
            if data['command'] == 'skipChapter4':
                chaptersToBeSkipped = 4
            if data['command'] == 'skipChapter5':
                chaptersToBeSkipped = 5
            if data['command'] == 'skipChapter6':
                chaptersToBeSkipped = 6
            if data['command'] == 'skipChapter7':
                chaptersToBeSkipped = 7
            if data['command'] == 'skipChapter8':
                chaptersToBeSkipped = 8
            if data['command'] == 'skipChapter9':
                chaptersToBeSkipped = 9

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
                isDontShowAgain = True
            else:

                isDontShowAgain = False

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

#class UserInterfaceGeneralEventHandlerImpl(adsk.core.UserInterfaceGeneralEvent):
    #def __init__(self):
         #super().__init__()
    #def notify(self, args):
        #print(args, 'General')

# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-EBB6C82A-A256-4AB7-9A86-0F7A9653A7E9
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)

        print(eventArgs.commandId, 'Starting')
        # Code to react to the event.
        # _ui.messageBox(str(eventArgs))
        #print(eventArgs.commandId)



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

        if (sketches.count == 2):
            sketch = sketches.item(1)

            #Check if the frontal plane of the cube has been selected as a sketch base
            if (sketch.profiles.count != 0):
                frontalCentroidModel = point.create(-1.1368683772161603e-16, -5.0, 6.333333333333333)
                frontalCentroid = point.create(-1.1368683772161603e-16, 6.333333333333333, 0.0)
                centroid = sketch.modelToSketchSpace(frontalCentroidModel)
                if ((frontalCentroid.x == centroid.x) and (frontalCentroid.y == centroid.y) and (frontalCentroid.z == centroid.z)):
                    self.palette.sendInfoToHTML('send', 'selectCubeFrontPlaneRoof')


                #Check the right points and order of the triangle lines to create the triangle sketch
                if (sketch.sketchPoints.count >= 6):
                    #create the right points as points
                    actualFirstPoint = point.create(-5,10,0)
                    actualSecondPoint = point.create(0,15,0)
                    actualThirdPoint = point.create(5,10,0)
                    #check if the right points are equivalent to the selected points as soon as one point has been created
                    firstPoint = sketch.sketchPoints.item(5).geometry
                    if ((actualFirstPoint.x == firstPoint.x) and (actualFirstPoint.y == firstPoint.y) and (actualFirstPoint.z == firstPoint.z)):
                        self.palette.sendInfoToHTML('send', 'clickedFirstTriangleLine')
                    if (sketch.sketchPoints.count >= 7):
                        secondPoint = sketch.sketchPoints.item(6).geometry
                        if ((actualSecondPoint.x == secondPoint.x) and (actualSecondPoint.y == secondPoint.y) and (actualSecondPoint.z == secondPoint.z)):
                            self.palette.sendInfoToHTML('send', 'clickedSecondTriangleLine')
                        if (sketch.sketchPoints.count >= 8):
                            thirdPoint = sketch.sketchPoints.item(7).geometry
                            if ((actualThirdPoint.x == thirdPoint.x) and (actualThirdPoint.y == thirdPoint.y) and (actualThirdPoint.z == thirdPoint.z)):
                                self.palette.sendInfoToHTML('send', 'clickedThirdTriangleLine')
                            #Check if the roof has been extruded in the right size by checking the volume
                            if (rootComp.features.extrudeFeatures.count == 2):
                                roof = rootComp.features.extrudeFeatures.item(1)
                                roofVolume = roof.bodies.item(0).volume
                                if ((roofVolume <= 1250.01) and (roofVolume >= 124.99)):
                                    self.palette.sendInfoToHTML('send', 'extrudeRoof')
                                    self.palette.sendInfoToHTML('send', 'confirmExtrudeRoof')

                                    #Check if the right size for the shell has been used by checking the remaining volume of the roof
                                    if ((roofVolume <= 508.509668) and (roofVolume >= 508.509666)):
                                        self.palette.sendInfoToHTML('send', 'draggedShell')
                                        self.palette.sendInfoToHTML('send', 'confirmShell')




        #Check if an additonal sketch has been created.
        if sketches.count == 3:
            sketch = sketches.item(2)

            #Check if the frontal plane of the cube has been selected as a sketch base
            if (sketch.profiles.count != 0):
                frontalCentroidModel = point.create(-1.1368683772161603e-16, -5.0, 6.333333333333333)
                frontalCentroid = point.create(-1.1368683772161603e-16, 6.333333333333333, 0.0)
                centroid = sketch.modelToSketchSpace(frontalCentroidModel)
                if ((frontalCentroid.x == centroid.x) and (frontalCentroid.y == centroid.y) and (frontalCentroid.z == centroid.z)):
                    self.palette.sendInfoToHTML('send', 'selectCubeFrontPlane')

                    #Check if the next profile of the sketch has been created. If so, check if it has the right size by area and centroid
                    if sketch.profiles.count == 2:
                        profile = sketch.profiles.item(1)
                        areaProps = sketch.profiles.item(0).areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                        centroid = areaProps.centroid
                        area = areaProps.area
                        if ((area == 105.0)):
                            if  ((centroid.y == 7.063492063492063) and (centroid.z == 0.0)):
                                self.palette.sendInfoToHTML('send', 'created2PointRectangle')

                                #Check if an additional Extrude has been created. If so, check if the volume is right and confirm afterwards.
                                if (rootComp.features.extrudeFeatures.count == 3):
                                    entrance = rootComp.features.extrudeFeatures.item(2)
                                    entranceVolume = entrance.bodies.item(0).volume
                                    if ((entranceVolume <= 488.5097) and (entranceVolume >= 488.5095)):
                                        self.palette.sendInfoToHTML('send', 'createdEntrance')
                                        self.palette.sendInfoToHTML('send', 'confirmExtrudeEntrance')

                                        #Check if the constructionPlane has been created
                                        if (rootComp.constructionPlanes.count != 0):
                                            offsetPlane = rootComp.constructionPlanes.item(0)
                                            xyPlane = rootComp.xYConstructionPlane
                                            #Check if the construction plane is parallel to the xyPlane
                                            if (offsetPlane.geometry.isParallelToPlane(xyPlane.geometry)):
                                                self.palette.sendInfoToHTML('send', 'selectXYPlane')
                                                self.palette.sendInfoToHTML('send', 'confirmOffsetPlane')
                                                origin = point.create(0,0,16)
                                                #Check if the offset Plane has a height of 160mm
                                                if (offsetPlane.geometry.origin.z == origin.z):
                                                    self.palette.sendInfoToHTML('send', 'draggedOffsetPlane')

                                                    #Check if a box has been created. If so, check if it has the right volume. Confirm if true
                                                    if (rootComp.features.boxFeatures.count != 0):
                                                        box = rootComp.features.boxFeatures.item(0).bodies.item(0)
                                                        boxVolume = box.volume
                                                        if((boxVolume <= 2.001) and (boxVolume >= 1.999)):
                                                            self.palette.sendInfoToHTML('send', 'createdBox')
                                                            self.palette.sendInfoToHTML('send', 'confirmBox')

        #Check if the cylinder has the right volume. Confirm if true.
        if (rootComp.features.cylinderFeatures.count != 0):
            cylinder = rootComp.features.cylinderFeatures.item(0)
            cylinderVolume = cylinder.bodies.item(0).volume
            if ((cylinderVolume >= 1.5706) and (cylinderVolume <= 1.5708)):
                self.palette.sendInfoToHTML('send', 'selectedCylinderDiameter')
                self.palette.sendInfoToHTML('send', 'confirmCylinder')

                #Check if there has been an additional sketch created
                if sketches.count == 4:
                    sketch = sketches.item(3)

                    #Check if the right roof has been selected as a sketch base
                    if (sketch.profiles.count != 0):
                        rightCentroidModel = point.create(2.5,0.0, 12.5)
                        rightCentroid = point.create(0, 7.071067811865474, 1.7763568394002505)
                        centroid = sketch.modelToSketchSpace(rightCentroidModel)
                        if ((rightCentroid.x == centroid.x) and (rightCentroid.y == centroid.y)):
                            self.palette.sendInfoToHTML('send', 'selectedRightSideofRoof')

                            #Check if the center diameter circle has the right area. Confirm if so.
                            if sketch.profiles.count == 2:
                                profile = sketch.profiles.item(1)
                                areaProps = sketch.profiles.item(0).areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                                area = areaProps.area
                                print(area)
                                if ((area == 58.14430750429558)):
                                    self.palette.sendInfoToHTML('send', 'draggedCircleDiameter')


        if (rootComp.features.loftFeatures.count != 0):
            self.palette.sendInfoToHTML('send', 'draggedCircleDiameter')
            self.palette.sendInfoToHTML('send', 'confirmLoft')

        #Check if the offset plane is visible. Confirm if true.
        if (rootComp.constructionPlanes.count != 0):
            offsetPlane = rootComp.constructionPlanes.item(0)
            if (offsetPlane.isLightBulbOn):
                self.palette.sendInfoToHTML('send', 'offsetPlaneVisible')


        #Check for the extrusion of the Box. If it has the right volume, confirm
        if(rootComp.features.extrudeFeatures.count ==4 ):
            boxExtrusion = rootComp.features.extrudeFeatures.item(3)
            extend = boxExtrusion.extentOne
            if (extend.classType == adsk.fusion.ToEntityExtentDefinition.classType):
                self.palette.sendInfoToHTML('send', 'clickedToObject')
                self.palette.sendInfoToHTML('send', 'confirmExtrudeChimney')

                #Check for the timeline. Confirm, if the markerposition is right
                timeline = design.timeline
                if timeline.markerPosition == 8:
                    self.palette.sendInfoToHTML('send', 'wentBackInTime')


        #Check for the extrusion of the cube. If it has the right volume, confirm.
        if (rootComp.features.extrudeFeatures.count != 0):
            cube = rootComp.features.extrudeFeatures.item(0)
            cubeVolume = cube.bodies.item(0).volume
            if ((cubeVolume <= 1000.01) and (cubeVolume >= 999.99)):
                self.palette.sendInfoToHTML('send', 'extrudeSquare')
                self.palette.sendInfoToHTML('send', 'confirmExtrudeCube')

        print('ActiveSelectionCount', _ui.activeSelections.count)

        if not self.palette:
            return
        print('Goes into If')
        if eventArgs.commandId == 'SketchCreate':
                self.palette.sendInfoToHTML('send', 'clickedCreateSketch')
                #Checks if in the current sketch xy plane has been used as reference plane
        elif eventArgs.commandId == 'ShapeRectangleCenter':
                self.palette.sendInfoToHTML('send', 'clickedCenterRectangle')
        elif eventArgs.commandId == 'CommitCommand':
            if (sketches.count != 0):
                sketch = sketches.item(0)
                #Das wird leider verspätet aufgerufen. Es wäre gut, wenn man hier ein Event findet was gleichzeitig geworfen wird
                if (sketch.referencePlane == rootComp.xYConstructionPlane):
                        self.palette.sendInfoToHTML('send', 'selectXYPlane')
        elif eventArgs.commandId == 'SketchStop':
            #ValidateBaseSquare here
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
        elif eventArgs.commandId == 'PrimitiveCylinder':
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
        
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #Get current design
        design = adsk.fusion.Design.cast(app.activeProduct)
        #If there is no active design, send error message
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        #Get root of active design
        rootComp = design.rootComponent

        #Create new sketch on xy plane
        sketches = rootComp.sketches

        if eventArgs.commandId == 'ShapeRectangleCenter':
            if (sketches.count != 0):
                sketch = sketches.item(0)
                self.validateBaseSquare(sketch)

        print(eventArgs.commandId, 'Terminating')
        # Code to react to the event.
        # _ui.messageBox(str(eventArgs))

    def validateBaseSquare(self, sketch):
        sketchHasLeastOneProfile = sketch.profiles.count != 0
        if sketchHasLeastOneProfile:
            areaProps = sketch.profiles.item(0).areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
            centroid1 = areaProps.centroid

            # Rectangle
            rectangleLine1 = sketch.sketchCurves.sketchLines.item(0).length
            rectangleLine2 = sketch.sketchCurves.sketchLines.item(1).length
            # Check if rectangle is 100x100 does not always work
            squareIsOfSize10by10cm = (rectangleLine1 >= 9.999) and (rectangleLine2 >= 9.999) and (rectangleLine1 <= 10.001) and (
                        rectangleLine2 <= 10.001)
            if squareIsOfSize10by10cm:
                self.palette.sendInfoToHTML('send', 'specify100100square')
            rectangleCenterIsInX0Y0 = (centroid1.x == 0.0) and (centroid1.y == 0.0) and (centroid1.z == 0.0)
            if rectangleCenterIsInX0Y0:
                self.palette.sendInfoToHTML('send', 'setCenterRectangleCenter')

# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-7D12B291-979B-4620-870F-D4C10E72DE1E
class MyCameraChangedHandler(adsk.core.CameraEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CameraEventArgs.cast(args)
        args = eventArgs
        # print(eventArgs.commandId, 'CameraChange')
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

        sketches = rootComp.sketches

        print(eventArgs.currentSelection, 'Selection changed')

        if(_ui.activeSelections.count < 0):
            firstActiveSelection = _ui.activeSelections.item(0).entity

            if (firstActiveSelection.classType == adsk.fusion.Profile.classType):
                print('si')
                profile = firstActiveSelection
                parentSketch = profile.parentSketch
                if (parentSketch == sketches.item(1)):
                    self.palette.sendInfoToHTML('send', 'clickedTrianglePlane')






        # Code to react to the event.
        #ui.messageBox('In MyActiveSelectionChangedHandler event handler.')


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