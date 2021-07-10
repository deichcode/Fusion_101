# Event handler for the palette HTML event.
import json
import traceback

import adsk.core
import adsk.fusion
import adsk.cam


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
