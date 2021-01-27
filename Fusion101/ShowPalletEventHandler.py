import traceback

from .Fusion101CommandTerminatedHandler import MyCommandTerminatedHandler
from .Fusion101CommandStartingHandler import MyCommandStartingHandler
from .MyPaletteMessageReceivedEventHandler import MyPaletteMessageReceivedEventHandler
from .constants import PALLET_ID, PALLET_URL, PALLET_NAME
from .Fusion101ActiveSelectionChangedHandler import Fusion101ActiveSelectionChangedHandler

import adsk.core
import adsk.fusion
import adsk.cam


# Event handler for the commandExecuted event.
class ShowPaletteCommandExecutedHandler(adsk.core.CommandEventHandler):
    def __init__(self, handlers):
        self.handlers = handlers
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        try:
            # Open new document
            self.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

            # Create and display the palette.
            palette = self.ui.palettes.itemById(PALLET_ID)
            if not palette:
                palette = self.initializePalette()
                palette.isVisible = True

                # Add handler to HTMLEvent of the palette.
                onHTMLEvent = MyPaletteMessageReceivedEventHandler()
                palette.incomingFromHTML.add(onHTMLEvent)
                self.handlers.append(onHTMLEvent)
            else:
                palette.isVisible = True

            # Add handler to react in palette on startedCommands
            onCommandStarting = MyCommandStartingHandler(palette)
            self.ui.commandStarting.add(onCommandStarting)
            self.handlers.append(onCommandStarting)

            # Add handler to react in palette on terminatedCommands
            onCommandTerminated = MyCommandTerminatedHandler(palette)
            self.ui.commandTerminated.add(onCommandTerminated)
            self.handlers.append(onCommandTerminated)

            # Add handler to react in palette on changes of the active selection
            onActiveSelectionChanged = Fusion101ActiveSelectionChangedHandler(palette)
            self.ui.activeSelectionChanged.add(onActiveSelectionChanged)
            self.handlers.append(onActiveSelectionChanged)
        except:
            self.ui.messageBox('Command executed failed: {}'.format(traceback.format_exc()))

    def initializePalette(self):
        fusion101Palette = self.ui.palettes.add(
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

# Event handler for the commandCreated event.
class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers):
        self.handlers = handlers
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()


    def notify(self, args):
        try:
            command = args.command
            onExecute = ShowPaletteCommandExecutedHandler(self.handlers)
            command.execute.add(onExecute)
            self.handlers.append(onExecute)
        except:
            self.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))