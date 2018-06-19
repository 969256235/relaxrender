
import relaxrender.raycasting as raycasting
import relaxrender.context as ctx
import relaxrender.screenwriter as sw
from stochastic_ray_tracing.render import make_shadow_cornell_box

class STRRelaxRender():

    def render(self):

        scene = make_shadow_cornell_box()

        myContext = ctx.Context()
        myContext.raycasting_iteration = int(1e8)
        render = raycasting.SimpleReverseRayCasting(myContext)
        input_xy, output_color = render.drive_raycasting(scene)

        writer = sw.NormalizedWriter(myContext)
        writer.write(input_xy, output_color, 'output_test.jpg')

if __name__ == "__main__":
    test = STRRelaxRender()
    test.render()