import unittest

import relaxrender.points as rp
import relaxrender.color as color
import relaxrender.mesh as mesh
import relaxrender.example_scene as example
import relaxrender.raycasting as raycasting
import relaxrender.context as ctx
import relaxrender.screenwriter as sw


import numpy as np

from relaxrender.scene import Scene
from relaxrender.camera import PerspectiveCamera
from relaxrender.mesh import Mesh
from relaxrender.texture import Texture, PlaneLightSource, UniformReflection
from relaxrender.triangle import Triangles
from relaxrender.points import Point3D, Point2D
from relaxrender.triangle import Triangle, Triangles
from relaxrender.color import Color, Red, White, Black, Green, Blue, Grey

__all__ = ['cornell_box']


def make_cornell_box():
    tris = Triangles()
    texs = []
    tex_pos = []

    # add light
    tris.append_rct(np.array([0.5, 0.999, -0.5]),
                    np.array([-0.5, 0.999, -0.5]),
                    np.array([-0.5, 0.999, -1.5]),
                    np.array([0.5, 0.999, -1.5]))

    texs.append(PlaneLightSource())
    texs.append(PlaneLightSource())

    tex_pos.append(None)
    tex_pos.append(None)

    # add ceilling, wall, floor
    # ceiling
    tris.append_rct(np.array([1, 1, 0]),
                    np.array([-1, 1, 0]),
                    np.array([-1, 1, -2]),
                    np.array([1, 1, -2]))

    texs.append(UniformReflection(Grey))
    texs.append(UniformReflection(Grey))

    tex_pos.append(None)
    tex_pos.append(None)

    # left wall
    tris.append_rct(np.array([-1, 1, 0]),
                    np.array([-1, -1, 0]),
                    np.array([-1, -1, -2]),
                    np.array([-1, 1, -2]))

    texs.append(UniformReflection(Red))
    texs.append(UniformReflection(Red))

    tex_pos.append(None)
    tex_pos.append(None)

    # right wall
    tris.append_rct(np.array([1, 1, 0]),
                    np.array([1, 1, -2]),
                    np.array([1, -1, -2]),
                    np.array([1, -1, 0]))

    texs.append(UniformReflection(Green))
    texs.append(UniformReflection(Green))

    tex_pos.append(None)
    tex_pos.append(None)

    # floor
    tris.append_rct(np.array([-1, -1, 0]),
                    np.array([1, -1, 0]),
                    np.array([1, -1, -2]),
                    np.array([-1, -1, -2]))

    texs.append(UniformReflection(Grey))
    texs.append(UniformReflection(Grey))

    tex_pos.append(None)
    tex_pos.append(None)

    # back
    tris.append_rct(np.array([1, 1, -2]),
                    np.array([-1, 1, -2]),
                    np.array([-1, -1, -2]),
                    np.array([1, -1, -2]))

    texs.append(UniformReflection(Grey))
    texs.append(UniformReflection(Grey))

    tex_pos.append(None)
    tex_pos.append(None)

    # shadow gen-plane
    tris.append_rct(np.array([-0.7,  0.5,  0]),
                    np.array([-0.7, -0.1,  0]),
                    np.array([-0.7, -0.1, -2]),
                    np.array([-0.7,  0.5, -2]))

    texs.append(UniformReflection(Green))
    texs.append(UniformReflection(Green))

    tex_pos.append(None)
    tex_pos.append(None)
    

    mesh = Mesh(tris, texs, tex_pos)
    
    c_pos = np.array([0.0, 0.0, 1.0])
    c_up = np.array([0.0, 1.0, 0])
    c_right = np.array([1.0, 0.0, 0])
    camera = PerspectiveCamera(c_pos, c_up, c_right, np.pi/2, np.pi/2)

    ret = Scene(mesh, camera)

    return ret

cornell_box = make_cornell_box()


class TestRelaxRender(unittest.TestCase):

    def test_simple_render(self):
        
        scene = cornell_box
        
        myContext = ctx.Context()
        myContext.raycasting_iteration = int(1e7)
        myContext.output_height = 600
        myContext.output_width = 800
        render = raycasting.SimpleReverseRayCasting(myContext)
        input_xy, output_color = render.drive_raycasting(scene)
        
        writer = sw.NormalizedWriter(myContext)
        writer.write(input_xy, output_color, 'output_test.jpg')


if __name__ == "__main__":
    test = TestRelaxRender()
    test.test_simple_render()

