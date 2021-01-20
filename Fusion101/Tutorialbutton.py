#Julia Reim, Sören Schröder
#PopUp Handlers



import adsk as adsk




###########AddInSample#################################


#CommandExecuteHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.firingEvent.sender
                    _ui.messageBox('command: {} executed successfully').format(command.parentCommandDefinition.id)
                except:
                    if _ui:
                        _ui.messageBox('command executed failed: {}').format(traceback.format_exc())

#CommandCreatedHandler for Tutorial Button on Right QAT bar. AddInSample.py has been used as reference
class CommandCreatedEventHandlerQATRight(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.command
                    #onExecute = CommandExecuteHandler()
                    onExecute = ShowPaletteCommandExecuteHandler()
                    command.execute.add(onExecute)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    #_ui.messageBox('Right QAT command created successfully')
                except:
                    _ui.messageBox(' Right QAT command created failed: {}').format(traceback.format_exc())               
###########AddinSample#################