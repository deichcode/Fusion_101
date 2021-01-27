# https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-19D8AC9F-E4F7-4E8A-8B3C-9D128EF932F3
# Event handler for the activeSelectionChanged event.

import adsk.core
import adsk.fusion
import adsk.cam


class Fusion101ActiveSelectionChangedHandler(adsk.core.ActiveSelectionEventHandler):
    def __init__(self, palette):
        self.palette = palette
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.ActiveSelectionEventArgs.cast(args)

        self.app = adsk.core.Application.get()
        ui = self.app.userInterface
        # Get current design
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        # If there is no active design, send error message
        if not design:
            ui.messageBox('No active Fusion 360 design', 'No Design')
            return

        # Get root of active design
        rootComp = design.rootComponent
        # 3D Points
        point = adsk.core.Point3D
        sketches = rootComp.sketches

        print(eventArgs.currentSelection, 'Selection changed')

        if self.ui.activeSelections.count > 0:
            firstActiveSelection = self.ui.activeSelections.item(0).entity
            isFace = firstActiveSelection.classType == adsk.fusion.BRepFace.classType
            if isFace:
                centroid = firstActiveSelection.centroid
                # Check if selected plane is right roof side
                isRightRoofSide = centroid.x == 2.5 and centroid.y == 0 and centroid.z == 12.5
                if isRightRoofSide:
                    self.palette.sendInfoToHTML('send', 'selectedRightSideofRoof')

                # Check if bottom plane of cube is selected
                isInOrigin = centroid.x == 0 and centroid.y == 0 and centroid.z == 0
                print(isInOrigin)
                if isInOrigin:
                    # https://forums.autodesk.com/t5/fusion-360-api-and-scripts/how-find-point-on-face/td-p/7835617
                    # Create four points and check if they sit on the selected plane => If yes it is the bottom plane
                    expectedSquarePointA = adsk.core.Point3D.create(5, 5, 0)
                    res, expectedSquareParamA = firstActiveSelection.evaluator.getParameterAtPoint(expectedSquarePointA)
                    res, newPoint = firstActiveSelection.evaluator.getPointAtParameter(expectedSquareParamA)
                    pointAIsOnSquare = expectedSquarePointA.isEqualToByTolerance(newPoint, 0.01)

                    expectedSquarePointB = adsk.core.Point3D.create(-5, 5, 0)
                    res, expectedSquareParamB = firstActiveSelection.evaluator.getParameterAtPoint(expectedSquarePointB)
                    res, newPoint = firstActiveSelection.evaluator.getPointAtParameter(expectedSquareParamB)
                    pointBIsOnSquare = expectedSquarePointB.isEqualToByTolerance(newPoint, 0.01)

                    expectedSquarePointC = adsk.core.Point3D.create(5, -5, 0)
                    res, expectedSquareParamC = firstActiveSelection.evaluator.getParameterAtPoint(expectedSquarePointC)
                    res, newPoint = firstActiveSelection.evaluator.getPointAtParameter(expectedSquareParamC)
                    pointCIsOnSquare = expectedSquarePointC.isEqualToByTolerance(newPoint, 0.01)

                    expectedSquarePointD = adsk.core.Point3D.create(-5, -5, 0)
                    res, expectedSquareParamD = firstActiveSelection.evaluator.getParameterAtPoint(expectedSquarePointD)
                    res, newPoint = firstActiveSelection.evaluator.getPointAtParameter(expectedSquareParamD)
                    pointDIsOnSquare = expectedSquarePointD.isEqualToByTolerance(newPoint, 0.01)

                    selectionIsBottomFace = pointAIsOnSquare and pointBIsOnSquare and pointCIsOnSquare and pointDIsOnSquare
                    if selectionIsBottomFace:
                        self.palette.sendInfoToHTML('send', 'selectBottomPlane')

                # Check if selected Plane is bottom plane of chimney box or cylinder
                PlaneIsOnZ160 = centroid.z == 16
                xyPlane = rootComp.xYConstructionPlane
                planeIsParallelToXY = firstActiveSelection.geometry.isParallelToPlane(xyPlane.geometry)
                planeIsOn160XYOffsetPlane = PlaneIsOnZ160 and planeIsParallelToXY
                if planeIsOn160XYOffsetPlane:
                    self.palette.sendInfoToHTML('send', 'selectBottomOfBox')
                    self.palette.sendInfoToHTML('send', 'selectBottomOfCylinder')

                if sketches.count == 2:
                    sketch = sketches.item(1)

                    # Check if the frontal plane of the cube has been selected as a sketch base
                    if sketch.profiles.count != 0:
                        frontalCentroidModel = point.create(-1.1368683772161603e-16, -5.0, 6.333333333333333)
                        frontalCentroid = point.create(-1.1368683772161603e-16, 6.333333333333333, 0.0)
                        centroid = sketch.modelToSketchSpace(frontalCentroidModel)
                        if ((frontalCentroid.x == centroid.x) and (frontalCentroid.y == centroid.y) and (
                                frontalCentroid.z == centroid.z)):
                            self.palette.sendInfoToHTML('send', 'selectCubeFrontPlane')

            if firstActiveSelection.classType == adsk.fusion.Profile.classType:
                print('Profile')
                profile = firstActiveSelection
                parentSketch = profile.parentSketch
                if parentSketch == sketches.item(1):
                    self.palette.sendInfoToHTML('send', 'clickedTrianglePlane')
                # Check if Entrance sketch has been selected
                areaProps = profile.areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
                centroid = areaProps.centroid
                area = areaProps.area
                if area == 20.0:
                    if (centroid.x == 0.0) and (centroid.y == 2.5) and (centroid.z == 0.0):
                        self.palette.sendInfoToHTML('send', 'selectEntranceSketch')

                    # Check if an additonal sketch has been created.

            isConstructionPlane = firstActiveSelection.classType == adsk.fusion.ConstructionPlane.classType
            if isConstructionPlane:
                xyPlane = rootComp.xYConstructionPlane
                # Check if the selected construction plane is parallel to the xyPlane
                if firstActiveSelection.geometry.isParallelToPlane(xyPlane.geometry):
                    expectedOrigin = point.create(0, 0, 16)
                    # Check if the selected offset Plane has a height of 160mm
                    if firstActiveSelection.geometry.origin.z == expectedOrigin.z:
                        self.palette.sendInfoToHTML('send', 'selectOffsetPlane')