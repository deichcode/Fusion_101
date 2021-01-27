import adsk.core
import adsk.fusion
import adsk.cam

class MyCommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self, palette):
        self.palette = palette
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)
        args = eventArgs

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

        # Create new sketch on xy plane
        sketches = rootComp.sketches

        if eventArgs.commandId == 'ShapeRectangleCenter':
            if sketches.count != 0:
                sketch = sketches.item(0)
                self.validateBaseSquare(sketch)

        print(eventArgs.commandId, 'Terminating')
        # Code to react to the event.
        # _ui.messageBox(str(eventArgs))

    def validateBaseSquare(self, sketch):
        sketchHasLeastOneProfile = sketch.profiles.count != 0
        if sketchHasLeastOneProfile:
            areaProps = sketch.profiles.item(0).areaProperties(
                adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy)
            centroid1 = areaProps.centroid

            # Rectangle
            rectangleLine1 = sketch.sketchCurves.sketchLines.item(0).length
            rectangleLine2 = sketch.sketchCurves.sketchLines.item(1).length
            # Check if rectangle is 100x100 does not always work
            squareIsOfSize10by10cm = (rectangleLine1 >= 9.999) and (rectangleLine2 >= 9.999) and (
                    rectangleLine1 <= 10.001) and (
                                             rectangleLine2 <= 10.001)
            if squareIsOfSize10by10cm:
                self.palette.sendInfoToHTML('send', 'specify100100square')
            rectangleCenterIsInX0Y0 = (centroid1.x == 0.0) and (centroid1.y == 0.0) and (centroid1.z == 0.0)
            if rectangleCenterIsInX0Y0:
                self.palette.sendInfoToHTML('send', 'setCenterRectangleCenter')