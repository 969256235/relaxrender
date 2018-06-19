import unittest

import numpy as np

from relaxrender.color import Color, Red, White, Black, Green, Blue, Grey
from relaxrender.texture import Texture, PlaneLightSource, UniformReflection
from stochastic_ray_tracing.render import get_shadow
from stochastic_ray_tracing.render import make_shadow_cornell_box
import relaxrender.raycasting as raycasting
import relaxrender.context as ctx
import relaxrender.screenwriter as sw
from relaxrender.points import Point3D

class TestRender(unittest.TestCase):

    def test_make_shadow_cornell_box(self):
        cornell_box = make_shadow_cornell_box()
        
    def test_get_shadow(self):

        scene = make_shadow_cornell_box()
        get_shadow(Point3D(0, 0, 0), scene.mesh)

        for i in range(len(scene.mesh.textures)):
            if scene.mesh.textures[i].damping_rate() < 1e-3:
                scene.mesh.triangles.triangles[i, 0], scene.mesh.triangles.triangles[i, 1], scene.mesh.triangles.triangles[i, 2] = \
                    scene.mesh.triangles.triangles[i, 0], scene.mesh.triangles.triangles[i, 2], scene.mesh.triangles.triangles[i, 1]
        get_shadow(Point3D(0, 0, 0), scene.mesh)

        for i in range(len(scene.mesh.textures)):
            if scene.mesh.textures[i].damping_rate() < 1e-3:
                scene.mesh.triangles.triangles[i, 0], scene.mesh.triangles.triangles[i, 1], scene.mesh.triangles.triangles[i, 2] = \
                    scene.mesh.triangles.triangles[i, 2], scene.mesh.triangles.triangles[i, 0], scene.mesh.triangles.triangles[i, 1]
        get_shadow(Point3D(0, 0, 0), scene.mesh)
