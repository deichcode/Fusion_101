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
        #Create a shell in the house
        shellEntities = adsk.core.ObjectCollection.create()
        shellEntities.add(cube.startFaces.item(0))


        shellInput = rootComp.features.shellFeatures.createInput(shellEntities, False)
        thickness = adsk.core.ValueInput.createByReal(1)
        shellInput.insideThickness = thickness
        shell = rootComp.features.shellFeatures.add(shellInput)


        #Chapter6
        #Make an Entrance

        #Select the body of our component
        cubeBody = cube.bodies.item(0)
        cubeBodyFaces = cubeBody.faces
        #Count the number of faces
        cubeBodyFacesCount = cubeBody.faces.count

        #The centroid of the frontal face
        frontalCentroid = point.create(-1.1368683772161603e-16, -5.0, 6.333333333333333)

        #Select the face, that has the same centroid as our frontal face
        for face in range(cubeBodyFacesCount):
            if cubeBodyFaces.item(face).centroid.isEqualTo(frontalCentroid):
                potentialFace = cubeBodyFaces.item(face)

        #Create a twoPointRectangle entrance sketch
        #Use the frontal face as sketch base
        entranceSketchBase = sketches.add(potentialFace)
        lines = entranceSketchBase.sketchCurves.sketchLines
        #Create two diagonally facing points for the rectangle
        point1 = point.create(2,0,0)
        point2 = point.create(-2,5,0)
        entranceSketch = lines.addTwoPointRectangle(point1, point2)

        #Extrude the entrance sketch
        entranceSketchProfile = entranceSketchBase.profiles.item(1)
        distance = adsk.core.ValueInput.createByReal(-1)
        entrance = rootComp.features.extrudeFeatures.addSimple(entranceSketchProfile, distance, adsk.fusion.FeatureOperations.CutFeatureOperation)

        #Chapter7 
        #Offset Plane

        # Create construction plane input
        offsetPlaneInput = rootComp.constructionPlanes.createInput()
        
        # Add offset plane
        #Maybe you will have to use another value here too 
        offsetValue = adsk.core.ValueInput.createByReal(16)
        offsetPlaneInput.setByOffset(baseRectangleProfile, offsetValue)
        offsetPlane = rootComp.constructionPlanes.add(offsetPlaneInput)

        #Chapter8
        #Finish Chimney


        #Create a center rectangle box sketch
        #Use the offset plane as sketch base
        boxSketchBase = sketches.add(offsetPlane)
        lines = boxSketchBase.sketchCurves.sketchLines

        #Create center point rectnagle sketch for box
        boxSketch = lines.addCenterPointRectangle(point.create(2.5,0,0), point.create(3.5,1,0))



        #Extrude the box sketch
        boxSketchProfile = boxSketchBase.profiles.item(0)
        extrudeBoxInput = rootComp.features.extrudeFeatures.createInput(boxSketchProfile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeBoxToEntity = adsk.fusion.ToEntityExtentDefinition.create(cubeBody, True)
        extrudeBoxInput.setOneSideExtent(extrudeBoxToEntity, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        box = rootComp.features.extrudeFeatures.add(extrudeBoxInput)

        #Chapter9
        #Go back in time

        #Chapter10
        #Create cylindrical Chimney


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
