# Author-
# Description-

import adsk.core as core
import adsk.fusion as fusion
import traceback
import math
import random

from .Donut import Donut

global app
global ui
global totalDonuts

FULL_CIRCLE = math.pi * 2


def getRootComponents():
    global ui
    global app
    design = fusion.Design.cast(app.activeProduct)

    if not design:
        ui.messageBox("The Computer says no! No design found")
    return design.rootComponent


def run(context):
    global ui
    global totalDonuts
    global app
    # noinspection PyBroadException
    try:
        app = core.Application.get()
        ui = app.userInterface

        totalDonuts = random.randrange(5, 10)
        rootComponent = getRootComponents()
        revolveAxis = rootComponent.yConstructionAxis
        thickness = 0.3
        for count in range(totalDonuts):
            sketch = rootComponent.sketches.add(rootComponent.yZConstructionPlane)
            centerX = 1.0
            centerY = thickness * 3.3 * count
            centerZ = 0.0
            revolveDegree = (FULL_CIRCLE / totalDonuts) * (count + 1)
            Donut.fromValues(sketch,
                             centerX, centerY, centerZ, thickness,
                             revolveAxis, revolveDegree, revolve_counter_clockwise=True)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
