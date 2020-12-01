#Author-
#Description-


import adsk.core, adsk.fusion, adsk.cam, traceback, random, math
handlers = []

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #Get the collection: CommandDefinitions
        commandDefinitions = ui.commandDefinitions

        #Create the RingButton command definition
        ringButton = commandDefinitions.addButtonDefinition('ringButton01PYTHON', 
        'Ring', 
        'Creates a single ring or a set on the xy plane. Choose if you want to create a random number of rings or an explicite number.')

        #Connect to the command created event
        ringButtonCommandCreated = ringButtonCommandCreatedEventHandler()
        ringButton.commandCreated.add(ringButtonCommandCreated)
        handlers.append(ringButtonCommandCreated)

        #Get the Create SolidCreatePanel in the model workspace
        solidCreatePanel = ui.allToolbarPanels.itemById('SolidCreatePanel')


        #Add the button to the panel
        ringButtonControl = solidCreatePanel.controls.addCommand(ringButton, 'PrimitivePipe', False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

#Event handler for the commandCreated event
class ringButtonCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        
        #Get the command
        command = eventArgs.command

        #Get the CommandInputs collection for new inputs
        inputs = command.commandInputs

        #Create a check box asking for random or explicit number of rings
        checkRingsRandom = inputs.addBoolValueInput('checkRingsRandom', 'Random amount of rings', True, '', False)

        #Create a slider to get the explicit amount of rings to be created
        explicitAmountOfRings = inputs.addIntegerSliderCommandInput('explicitAmountOfRings', 'Amount of rings', 1, 10, False)

        #Create a slider to vary the radius of the circle
        ringdistance = inputs.addIntegerSliderCommandInput('ringDistance', 'Distance between Rings in cm', 1, 15, False)

        #Connetct to the execute event
        onExecute = ringButtonCommandExecuteHandler()
        command.execute.add(onExecute)
        handlers.append(onExecute)

        #Connect to the inputChanged event
        onInputChanged = ringButtonCommandInputChangedHandler()
        command.inputChanged.add(onInputChanged)
        handlers.append(onInputChanged)

#Event handler for the inputChanged event
class ringButtonCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)

        #Check the value of randomRingCheck
        changedInput = eventArgs.input
        if changedInput.id == 'checkRingsRandom':
            inputs = eventArgs.firingEvent.sender.commandInputs
            sliderInput = inputs.itemById('explicitAmountOfRings')

            #Change the visibility of the slider
            if changedInput.value == True:
                sliderInput.isVisible = False
            else:
                sliderInput.isVisible = True

#Event handler for the execute event
class ringButtonCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        #Code to react to the event
        app = adsk.core.Application.get()
        ui = app.userInterface
        #ui.messageBox('In command execute event handler')

        #Get values from command inputs
        inputs = eventArgs.command.commandInputs

        #Get current design
        design = adsk.fusion.Design.cast(app.activeProduct)
        #If there is no active design, send error message
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        #Get root of active design
        rootComp = design.rootComponent

        #Check the radius of the rings (input)
        ringDistance = inputs.itemById('ringDistance').valueOne

        #Check if user decided to use random or explicit number
        if inputs.itemById('checkRingsRandom').value == True:
            r = random.randint(5,10)
        else:
            r = inputs.itemById('explicitAmountOfRings').valueOne

        #Range r-1, because range starts with 0
        for x in range(r):
            #Create new sketch on xy plane
            sketches = rootComp.sketches
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)

            # Get the SketchCircles collection from an existing sketch (circle)
            circles = sketch.sketchCurves.sketchCircles

            # Create a new circle by adding to the collection
            circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(x*ringDistance,0,0), 2)

            # Get the SketchLines collection from an existing sketch (line)
            lines = sketch.sketchCurves.sketchLines

            # Create a new line by adding to collection
            axis = lines.addByTwoPoints(adsk.core.Point3D.create(-1,-4,0), adsk.core.Point3D.create(1,-4,0))

            # Get the first profile from the sketch (profile of the circle)
            prof = sketch.profiles.item(0)

            # For using revolves, you have to get the revolveFeatures Collection first
            revolves = rootComp.features.revolveFeatures

            # Create a revolve input object that will be edited later
            revInput = revolves.createInput(prof, axis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)


            # Define a revolve by specifying 360° with math and multiplicating it with x+1/r 
            # for growing angle with every body .
            angle = adsk.core.ValueInput.createByReal(((x+1) / r)*(math.pi * 2))
            revInput.setAngleExtent(False, angle)
		
            # Create a revolve by adding it with the input
            rev = revolves.add(revInput)
            #Get the current body
            body = rootComp.bRepBodies.item(x)

            #Get the material Libraries
            libraries = app.materialLibraries
            #Get the appearance library
            library = libraries.itemByName("Fusion 360 Appearance Library")
            #Select a random appearance between 86 and 100 and exclude ugly colors like black, dark grey...
            color = random.choice([i for i in range(86,100) if i in [87,89,91,93,95]])
            
            libApp = library.appearances.item(color)
            
            #Set the appearance of the body
            body.appearance = libApp


def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #Clean up the user interface
        commandDefinition = ui.commandDefinitions.itemById('ringButton01PYTHON')
        if commandDefinition:
            commandDefinition.deleteMe()

        solidCreatePanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        control = solidCreatePanel.controls.itemById('ringButton01PYTHON')
        if control:
            control.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
