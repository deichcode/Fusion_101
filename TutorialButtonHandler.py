import traceback

import adsk.core
import adsk.fusion
import adsk.cam

from .ShowPalletEventHandler import ShowPaletteCommandExecutedHandler


# CommandExecuteHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class TutorialButtonCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        try:
            command = args.firingEvent.sender
            self.ui.messageBox('command: {} executed successfully').format(command.parentCommandDefinition.id)
        except:
            if self.ui:
                self.ui.messageBox('command executed failed: {}').format(traceback.format_exc())


# CommandCreatedHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class CommandCreatedEventHandlerQATRight(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers):
        self.handlers = handlers
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        super().__init__()

    def notify(self, args):
        try:
            command = args.command
            # onExecute = CommandExecuteHandler()
            onExecute = ShowPaletteCommandExecutedHandler(self.handlers)
            command.execute.add(onExecute)
            # keep the handler referenced beyond this function
            self.handlers.append(onExecute)
            # _ui.messageBox('Right QAT command created successfully')
        except:
            self.ui.messageBox(' Right QAT command created failed: {}').format(traceback.format_exc())
