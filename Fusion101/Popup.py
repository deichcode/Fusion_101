#Julia Reim, Sören Schröder
#PopUp Handlers



import adsk.fusion as fusion
import adsk.core as core





#Event handler for the commandCreated event
class popUpCommandCreatedEventHandler(core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = core.CommandCreatedEventArgs.cast(args)
        
        #Get the command
        command = eventArgs.command

        #Get the CommandInputs collection for new inputs
        inputs = command.commandInputs


        command.cancelButtonText = 'Close'
        command.okButtonText = 'Start Fusion 101'

        #Create a "textBox" with the welcoming text
        welcomeText = inputs.addTextBoxCommandInput(
            'welcomeText', 
            '',
            '<div align="center"><b>Welcome to Fusion 101!</b></div>',
            3,
            True
        )

        #Create a "textBox" with the description of the tutorial
        introductionText = inputs.addTextBoxCommandInput(
            'introductionText', 
            '',
            '<div align="center">This interactive tutorial will guide you through'+
            ' your first steps in Fusion 360. You will get to know the most important'+
            ' tools, workflows and concepts to kickstart your own ideas</div>.',
            6,
            True
        )

        #Create a "textBox" with the second description of the tutorial
        introductionText2 = inputs.addTextBoxCommandInput(
            'introductionText2', 
            '',
            '<div align="center">To start Fusion 101 later just click on the HAT symbol'+
            ' next to your profile picture or initials in the upper right Quick Access Bar of your screen</div>.',
            6,
            True
        )

        #Create a check box asking for random or explicit number of rings
        dontShowAgain = inputs.addBoolValueInput('dontShowAgain', 'Don\'t show again', True, '', False)



        #Connect to the execute event
        onExecute = popUpCommandExecuteHandler()
        command.execute.add(onExecute)
        handlers.append(onExecute)

        #Connect to the inputChanged event
        onInputChanged = popUpCommandInputChangedHandler()
        command.inputChanged.add(onInputChanged)
        handlers.append(onInputChanged)

#Event handler for the inputChanged event
class popUpCommandInputChangedHandler(core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = core.InputChangedEventArgs.cast(args)

        #Check the value of dont show again
        changedInput = eventArgs.input
        if changedInput.id == 'dontShowAgain':
            
        

            if changedInput.value == True:
                #inputs = eventArgs.firingEvent.sender.commandInputs
                #sliderInput = inputs.itemById('explicitAmountOfRings')
                #command = adsk.core.CommandCreatedEventArgs.cast(args)
                #commands = command.firingEvent.sender.command
                #commands = "Remind me next time"
               # command.cancelButtonText = 'Remind me next time'
                print(eventArgs.objectType)
                isDontShowAgain = True
                print(isDontShowAgain)
            else:

                isDontShowAgain = False
                print(isDontShowAgain)

#Event handler for the execute event
class popUpCommandExecuteHandler(core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = core.CommandEventArgs.cast(args)
        print("nice")
        #Code to react to the event
        app = core.Application.get()
        ui = app.userInterface
        ui.messageBox('Tutorial will start now')

        #Get values from command inputs
        inputs = eventArgs.command.commandInputs

        cmd = ui.commandDefinitions.itemById('TutorialButtonOnQATRight')
        cmd.execute()