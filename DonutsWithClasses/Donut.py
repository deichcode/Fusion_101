import math
from typing import Any
import adsk.fusion as fusion
import adsk.core as core

from .Circle import Circle


class Donut:
    """Creates a donut by revolving a circle. Defined by circle and revolve axis"""

    def __init__(self,
                 circle_sketch: fusion.Sketch,
                 revolve_axis: Any,
                 revolve_degree=math.pi * 2,
                 revolve_counter_clockwise=False):
        component = circle_sketch.parentComponent
        profile = circle_sketch.profiles.item(0)
        revolves = component.features.revolveFeatures
        newBody = fusion.FeatureOperations.NewBodyFeatureOperation
        revolveInput = revolves.createInput(profile, revolve_axis, newBody)
        revolveAngel = revolve_degree
        if revolve_counter_clockwise:
            revolveAngel = revolve_degree * -1
        angle = core.ValueInput.createByReal(revolveAngel)
        revolveInput.setAngleExtent(False, angle)
        revolves.add(revolveInput)
        pass

    @classmethod
    def fromValues(cls, sketch: fusion.Sketch,
                   center_x: float, center_y: float, center_z: float, radius: float,
                   axis: Any,
                   revolve_degree=math.pi * 2,
                   revolve_counter_clockwise=False):
        Circle.create(sketch, center_x, center_y, center_z, radius)
        return cls(sketch, axis, revolve_degree, revolve_counter_clockwise)

    @classmethod
    def fromPoint(cls, sketch: fusion.Sketch,
                  center: core.Point3D, radius: float,
                  axis: Any,
                  revolve_degree=math.pi * 2,
                  revolve_counter_clockwise=False):
        Circle.create(sketch, center, radius)
        return cls(sketch, axis, revolve_degree, revolve_counter_clockwise)

    @classmethod
    def fromCircle(cls, circle, axis,
                   revolve_degree=math.pi * 2,
                   revolve_counter_clockwise=False):
        return cls(circle, axis, revolve_degree, revolve_counter_clockwise)
