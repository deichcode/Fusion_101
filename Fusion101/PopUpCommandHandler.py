import adsk.core
import adsk.fusion
import adsk.cam


# Event handler for the commandCreated event
class PopUpCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers):
        self.handlers = handlers
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)

        # Get the command
        command = eventArgs.command

        # Get the CommandInputs collection for new inputs
        inputs = command.commandInputs

        command.cancelButtonText = 'Close'
        command.okButtonText = 'Start Fusion 101'

        # Create a "textBox" with the welcoming text
        welcomeText = inputs.addTextBoxCommandInput(
            'welcomeText',
            '',
            '<div align="left"><h3>Welcome to Fusion 101!</h3></div>',
            2,
            True
        )

        # Create a "textBox" with the description of the tutorial
        introductionText = inputs.addTextBoxCommandInput(
            'introductionText',
            '',
            '<div align="left" style="width: 100%">This interactive tutorial will guide you through' +
            ' your first steps in Fusion 360. You will get to know the most important' +
            ' tools, workflows and concepts to kickstart your own ideas.</div>',
            6,
            True
        )

        # Create a "textBox" with the second description of the tutorial
        introductionText2 = inputs.addTextBoxCommandInput(
            'introductionText2',
            '',
            '<div align="left" style="width: 100%">To start Fusion 101 later just click on the <strong>graduation '
            'hat</strong>' +
            'next to your profile picture or initials in the <strong>upper right</strong> Quick Access Bar of your '
            'screen.</div>',
            6,
            True
        )

        # Create a check box asking for random or explicit number of rings
        dontShowAgain = inputs.addBoolValueInput('dontShowAgain', 'Don\'t show again', True, '', False)

        command.setDialogInitialSize(300, 200)

        # Connect to the execute event
        onExecute = PopUpCommandExecuteHandler()
        command.execute.add(onExecute)
        self.handlers.append(onExecute)

        # Connect to the inputChanged event
        onInputChanged = PopUpCommandInputChangedHandler()
        command.inputChanged.add(onInputChanged)
        self.handlers.append(onInputChanged)


# Event handler for the inputChanged event
class PopUpCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.InputChangedEventArgs.cast(args)

        # Check the value of dont show again
        changedInput = eventArgs.input
        if changedInput.id == 'dontShowAgain':

            if changedInput.value:
                # inputs = eventArgs.firingEvent.sender.commandInputs
                # sliderInput = inputs.itemById('explicitAmountOfRings')
                # command = adsk.core.CommandCreatedEventArgs.cast(args)
                # commands = command.firingEvent.sender.command
                # commands = "Remind me next time"
                # command.cancelButtonText = 'Remind me next time'
                isDontShowAgain = True
            else:

                isDontShowAgain = False


# Event handler for the execute event
class PopUpCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandEventArgs.cast(args)

        # Code to react to the event
        app = adsk.core.Application.get()
        ui = app.userInterface
        # ui.messageBox('Tutorial will start now')

        # Get values from command inputs
        # inputs = eventArgs.command.commandInputs

        cmd = ui.commandDefinitions.itemById('TutorialButtonOnQATRight')
        cmd.execute()
