import unittest

import relaxrender.points as rp
import relaxrender.color as color
import relaxrender.mesh as mesh
import relaxrender.example_scene as example
import relaxrender.raycasting as raycasting
import relaxrender.context as ctx
import relaxrender.screenwriter as sw

class TestRelaxRender(unittest.TestCase):

    def test_simple_render(self):
        
        scene = example.cornell_box
        
        myContext = ctx.Context()
        myContext.raycasting_iteration = int(1e6)
        render = raycasting.SimpleReverseRayCasting(myContext)
        input_xy, output_color = render.drive_raycasting(scene)
        
        writer = sw.NormalizedWriter(myContext)
        writer.write(input_xy, output_color, 'output_test.jpg')


if __name__ == "__main__":
    test = TestRelaxRender()
    test.test_simple_render()