import adsk.core
import adsk.fusion
import adsk.cam

# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-EBB6C82A-A256-4AB7-9A86-0F7A9653A7E9
class MyCommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self, palette):
        self.palette = palette
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)

        print(eventArgs.commandId, 'Starting')

        app = adsk.core.Application.get()
        ui = app.userInterface

        # Get current design
        design = adsk.fusion.Design.cast(app.activeProduct)
        # If there is no active design, send error message
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        # Get root of active design
        rootComp = design.rootComponent

        # 3D Points
        point = adsk.core.Point3D

        # Create new sketch on xy plane
        sketches = rootComp.sketches

        if sketches.count == 2:
            sketch = sketches.item(1)

            # Check if the frontal plane of the cube has been selected as a sketch base
            if sketch.profiles.count != 0:
                frontalCentroidModel = point.create(-1.1368683772161603e-16, -5.0, 6.333333333333333)
                frontalCentroid = point.create(-1.1368683772161603e-16, 6.333333333333333, 0.0)
                centroid = sketch.modelToSketchSpace(frontalCentroidModel)
                if ((frontalCentroid.x == centroid.x) and (frontalCentroid.y == centroid.y) and (
                        frontalCentroid.z == centroid.z)):
                    self.palette.sendInfoToHTML('send', 'selectCubeFrontPlaneRoof')

                # Check the right points and order of the triangle lines to create the triangle sketch
                if sketch.sketchPoints.count >= 6:
                    # create the right points as points
                    actualFirstPoint = point.create(-5, 10, 0)
                    actualSecondPoint = point.create(0, 15, 0)
                    actualThirdPoint = point.create(5, 10, 0)
                    # check if the right points are equivalent to the selected points as soon as one point has been created
                    firstPoint = sketch.sketchPoints.item(5).geometry
                    if ((actualFirstPoint.x == firstPoint.x) and (actualFirstPoint.y == firstPoint.y) and (
                            actualFirstPoint.z == firstPoint.z)):
                        self.palette.sendInfoToHTML('send', 'clickedFirstTriangleLine')
                    if sketch.sketchPoints.count >= 7:
                        secondPoint = sketch.sketchPoints.item(6).geometry
                        if ((actualSecondPoint.x == secondPoint.x) and (actualSecondPoint.y == secondPoint.y) and (
                                actualSecondPoint.z == secondPoint.z)):
                            self.palette.sendInfoToHTML('send', 'clickedSecondTriangleLine')
                        if sketch.sketchPoints.count >= 8:
                            thirdPoint = sketch.sketchPoints.item(7).geometry
                            if ((actualThirdPoint.x == thirdPoint.x) and (actualThirdPoint.y == thirdPoint.y) and (
                                    actualThirdPoint.z == thirdPoint.z)):
                                self.palette.sendInfoToHTML('send', 'clickedThirdTriangleLine')
                            # Check if the roof has been extruded in the right size by checking the volume
                            if rootComp.features.extrudeFeatures.count == 2:
                                roof = rootComp.features.extrudeFeatures.item(1)
                                roofVolume = roof.bodies.item(0).volume
                                if (roofVolume <= 1250.01) and (roofVolume >= 124.99):
                                    self.palette.sendInfoToHTML('send', 'extrudeRoof')
                                    self.palette.sendInfoToHTML('send', 'confirmExtrudeRoof')

                                    # Check if the right size for the shell has been used by checking the remaining volume of the roof
                                    if (roofVolume <= 508.509668) and (roofVolume >= 508.509666):
                                        self.palette.sendInfoToHTML('send', 'draggedShell')
                                        self.palette.sendInfoToHTML('send', 'confirmShell')

        # Check if an additonal sketch has been created.
        if sketches.count == 3:
            sketch = sketches.item(2)

            # Check if the frontal plane of the cube has been selected as a sketch base
            if sketch.profiles.count != 0:

                # Check if the next profile of the sketch has been created. If so, check if it has the right size by
                # area and centroid
                if sketch.profiles.count == 2:
                    profile = sketch.profiles.item(1)
                    areaProps = sketch.profiles.item(0).areaProperties(
                        adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                    centroid = areaProps.centroid
                    area = areaProps.area
                    if area == 105.0:
                        if (centroid.y == 7.063492063492063) and (centroid.z == 0.0):
                            self.palette.sendInfoToHTML('send', 'created2PointRectangle')

                            # Check if an additional Extrude has been created. If so, check if the volume is right
                            # and confirm afterwards.
                            if rootComp.features.extrudeFeatures.count == 3:
                                entrance = rootComp.features.extrudeFeatures.item(2)
                                entranceVolume = entrance.bodies.item(0).volume
                                if (entranceVolume <= 488.5097) and (entranceVolume >= 488.5095):
                                    self.palette.sendInfoToHTML('send', 'createdEntrance')
                                    self.palette.sendInfoToHTML('send', 'confirmExtrudeEntrance')

                                    # Check if the constructionPlane has been created
                                    if rootComp.constructionPlanes.count != 0:
                                        offsetPlane = rootComp.constructionPlanes.item(0)
                                        xyPlane = rootComp.xYConstructionPlane
                                        # Check if the construction plane is parallel to the xyPlane
                                        if offsetPlane.geometry.isParallelToPlane(xyPlane.geometry):
                                            self.palette.sendInfoToHTML('send', 'selectXYPlane')
                                            self.palette.sendInfoToHTML('send', 'confirmOffsetPlane')
                                            origin = point.create(0, 0, 16)
                                            # Check if the offset Plane has a height of 160mm
                                            if offsetPlane.geometry.origin.z == origin.z:
                                                self.palette.sendInfoToHTML('send', 'draggedOffsetPlane')

                                                # Check if a box has been created. If so, check if it has the right
                                                # volume. Confirm if true
                                                if rootComp.features.boxFeatures.count != 0:
                                                    box = rootComp.features.boxFeatures.item(0).bodies.item(0)
                                                    boxVolume = box.volume
                                                    if (boxVolume <= 2.001) and (boxVolume >= 1.999):
                                                        self.palette.sendInfoToHTML('send', 'createdBox')
                                                        self.palette.sendInfoToHTML('send', 'confirmBox')

        # Check if the cylinder has the right volume. Confirm if true.
        if rootComp.features.cylinderFeatures.count != 0:
            cylinder = rootComp.features.cylinderFeatures.item(0)
            cylinderVolume = cylinder.bodies.item(0).volume
            if (cylinderVolume >= 1.5706) and (cylinderVolume <= 1.5708):
                self.palette.sendInfoToHTML('send', 'selectedCylinderDiameter')
                self.palette.sendInfoToHTML('send', 'confirmCylinder')
                # Check if cylinder is centered to the roof
                if cylinder.bodies.item(0).faces.count > 0:
                    cylinderIsOnRoofCenter = cylinder.bodies.item(0).faces.item(0).centroid.x == 2.5
                    if cylinderIsOnRoofCenter:
                        self.palette.sendInfoToHTML('send', 'clickedCylinderCenter')

                # Check if there has been an additional sketch created
                if sketches.count == 4:
                    sketch = sketches.item(3)

                    if sketch.profiles.count == 2:
                        # Check if the center diameter circle has the right area. Confirm if so.
                        areaProps = sketch.profiles.item(0).areaProperties(
                            adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                        area = areaProps.area
                        if area == 58.14430750429558:
                            self.palette.sendInfoToHTML('send', 'draggedCircleDiameter')

                        # Check if circle center is at the correct postition
                        expectedOrigin = point.create(-1.6849756775338687e-17, 7.086427259780254,
                                                      -8.881784197001252e-16)
                        circleIsAtExpectedPosition = areaProps.centroid.x == expectedOrigin.x and areaProps.centroid.y == expectedOrigin.y and areaProps.centroid.z == expectedOrigin.z
                        if circleIsAtExpectedPosition:
                            self.palette.sendInfoToHTML('send', 'clickedCircleCenter')

        if rootComp.features.loftFeatures.count != 0:
            self.palette.sendInfoToHTML('send', 'draggedCircleDiameter')
            self.palette.sendInfoToHTML('send', 'confirmLoft')
            if rootComp.features.loftFeatures.item(0).bodies.count != 0:
                loftVolume = rootComp.features.loftFeatures.item(0).bodies.item(0).volume
                if 510 < loftVolume < 511:
                    self.palette.sendInfoToHTML('send', 'selectedCircleOnRoof')

                    # Check if the offset plane is visible. Confirm if true.
        if rootComp.constructionPlanes.count != 0:
            offsetPlane = rootComp.constructionPlanes.item(0)
            if offsetPlane.isLightBulbOn:
                self.palette.sendInfoToHTML('send', 'offsetPlaneVisible')

        # Check for the extrusion of the Box. If it has the right volume, confirm
        if rootComp.features.extrudeFeatures.count == 4:
            boxExtrusion = rootComp.features.extrudeFeatures.item(3)
            extend = boxExtrusion.extentOne
            chimneyIsExtruded = boxExtrusion.bodies.count > 0
            if chimneyIsExtruded:
                volume = boxExtrusion.bodies.item(0).volume
                minChimneyVolume = 498
                maxChimneyVolume = 511
                volumeIsInPossibleRange = minChimneyVolume < volume < maxChimneyVolume
                if extend.classType == adsk.fusion.ToEntityExtentDefinition.classType and volumeIsInPossibleRange:
                    self.palette.sendInfoToHTML('send', 'clickedToObject')
                    self.palette.sendInfoToHTML('send', 'selectedSideOfRoof')
                    self.palette.sendInfoToHTML('send', 'confirmExtrudeChimney')

            # Check for the timeline. Confirm, if the marker position is right
            timeline = design.timeline
            if timeline.markerPosition == 8:
                self.palette.sendInfoToHTML('send', 'wentBackInTime')

        # Check for the extrusion of the cube. If it has the right volume, confirm.
        if rootComp.features.extrudeFeatures.count != 0:
            cube = rootComp.features.extrudeFeatures.item(0)
            cubeVolume = cube.bodies.item(0).volume
            if (cubeVolume <= 1000.01) and (cubeVolume >= 999.99):
                self.palette.sendInfoToHTML('send', 'extrudeSquare')
                self.palette.sendInfoToHTML('send', 'confirmExtrudeCube')

        print('ActiveSelectionCount', self.ui.activeSelections.count)

        if not self.palette:
            return
        print('Goes into If')
        if eventArgs.commandId == 'SketchCreate':
            self.palette.sendInfoToHTML('send', 'clickedCreateSketch')
            # Checks if in the current sketch xy plane has been used as reference plane
        elif eventArgs.commandId == 'ShapeRectangleCenter':
            self.palette.sendInfoToHTML('send', 'clickedCenterRectangle')
        elif eventArgs.commandId == 'CommitCommand':
            if sketches.count != 0:
                sketch = sketches.item(0)
                # Das wird leider verspätet aufgerufen. Es wäre gut, wenn man hier ein Event findet was gleichzeitig
                # geworfen wird
                if sketch.referencePlane == rootComp.xYConstructionPlane:
                    self.palette.sendInfoToHTML('send', 'selectXYPlane')
        elif eventArgs.commandId == 'SketchStop':
            # ValidateBaseSquare here
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
        elif eventArgs.commandId == 'PrimitiveCylinder':
            self.palette.sendInfoToHTML('send', 'clickedCylinder')
        elif eventArgs.commandId == 'CircleCenterRadius':
            self.palette.sendInfoToHTML('send', 'clickedCircle')
        elif eventArgs.commandId == 'SolidLoft':
            self.palette.sendInfoToHTML('send', 'clickedLoft')
        # Bad hack to ensure tutorial continues.
        elif eventArgs.commandId == 'VisibilityToggleCmd':
            self.palette.sendInfoToHTML('send', 'offsetPlaneVisible')
