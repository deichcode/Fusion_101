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

        #circles = sketch.sketchCurves.sketchCircles

        #Chapter1
        #Create the base square sketch of the house
        lines = sketch.sketchCurves.sketchLines
        baseRectangle = lines.addCenterPointRectangle(point.create(0,0,0), point.create(5,5,0))

        #Chapter2
        #Extrude the sketch and create a cube

        #Get profile defined by baseRectangle
        baseRectangleProfile = sketch.profiles.item(0)
        #Define Distance of Extrusion
        distance = adsk.core.ValueInput.createByReal(10)
        cube = rootComp.features.extrudeFeatures.addSimple(baseRectangleProfile, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        #Chapter3
        #Create Roof Sketch
        #todo hier muss möglicherweise anders vorgegangen werden. Sideface nehmen und von dort aus statt combine
        face = cube.endFaces.item(0)
        triangleSketchBase = sketches.add(face)
        triangleSketch = triangleSketchBase.sketchCurves.sketchLines
        baseTriangle1 = triangleSketch.addByTwoPoints(point.create(-5,-5,0),point.create(0,-5,5))
        baseTriangle2 = triangleSketch.addByTwoPoints(point.create(0,-5,5),point.create(5,-5,0))
        baseTriangle3 = triangleSketch.addByTwoPoints(point.create(5,-5,0),point.create(-5,-5,0))

        
        #Chapter4
        #Extrude the triangle
        triangleSketchProfile = triangleSketchBase.profiles.item(1)
        distance = adsk.core.ValueInput.createByReal(-10)
        roof = rootComp.features.extrudeFeatures.addSimple(triangleSketchProfile, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        #Combine the two resulting bodies
        cubeBody = cube.bodies.item(0)
        roofBody = roof.bodies.item(0)
        roofBodyCollection = adsk.core.ObjectCollection.create()
        roofBodyCollection.add(roofBody)
        combFeatInput = rootComp.features.combineFeatures.createInput(cubeBody, roofBodyCollection)
        houseWithRoof = rootComp.features.combineFeatures.add(combFeatInput)

        #Chapter5
        shellEntities = adsk.core.ObjectCollection.create()
        shellEntities.add(cube.startFaces.item(0))


        shellInput = rootComp.features.shellFeatures.createInput(shellEntities, False)
        thickness = adsk.core.ValueInput.createByReal(1)
        shellInput.insideThickness = thickness
        print(shellInput)
        shell = rootComp.features.shellFeatures.add(shellInput)



        """
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

        """

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))




def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
