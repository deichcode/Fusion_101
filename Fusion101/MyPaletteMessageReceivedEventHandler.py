# Event handler for the palette HTML event.
import json
import traceback

import adsk.core
import adsk.fusion
import adsk.cam

from .constants import PALLET_ID


class MyPaletteMessageReceivedEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        try:
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)
            data = json.loads(htmlArgs.data)

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
            xyPlane = rootComp.xYConstructionPlane
            sketch = sketches.add(xyPlane)
            # msg = "An event has been fired from the html to Fusion with the following data:\n"
            # msg += '    Command: {}\n    arg1: {}\n    arg2: {}'.format(htmlArgs.action, data['arg1'], data['arg2'])
            if data['command'] == 'close':
                palette = self.ui.palettes.itemById(PALLET_ID)
                if palette:
                    palette.isVisible = False

            # determine which chapter should be skipped (implementation not finished yet)
            chaptersToBeSkipped = 0
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
            self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
