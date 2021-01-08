from adsk import fusion as fusion, core as core


class Circle:
    """Creates a circle on a sketch. Defined by center and radius of circle and revolve axis"""

    def __init__(self, sketch: fusion.Sketch, center: core.Point3D, radius: float):
        sketch.sketchCurves.sketchCircles.addByCenterRadius(center, radius)
        pass

    @classmethod
    def create(cls, sketch: fusion.Sketch, center: core.Point3D, radius: float):
        return cls(sketch, center, radius)

    @classmethod
    def create(cls, sketch: fusion.Sketch, center_x: float, center_y: float, center_z: float, radius: float):
        center = core.Point3D.create(center_x, center_y, center_z)
        return cls(sketch, center, radius)
