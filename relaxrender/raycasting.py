
import numpy as np

from .points import Vector, Point3D, Point, Points
from .color import Color
from .math import dist, sphere_sampling, ray_in_triangle

class RayCasting:
    def __init__(self, context):
        self.context = context

    def drive_raycasting(self, triangles):
        pass

    def cast_ray(self, input_x, input_y, triangles):
        pass

    def forward_history(self, history):
        pass


class SimpleReverseRayCasting(RayCasting):
    def __init__(self, context):
        super().__init__(context)

    def drive_raycasting(self, scene):
        input_xy = np.empty((self.context.raycasting_iteration, 2))
        output_color = np.empty((self.context.raycasting_iteration, 4))

        mesh = scene.mesh
        camera = scene.camera

        # translocate camera to origin.
        mesh.triangles = camera.relocate_world_by_camera(mesh.triangles)
        
        for index in range(self.context.raycasting_iteration):
            if index % 100000 == 0:
                print("working on ray: {}.".format(index))
            
            ray_samples, xy = camera.sample_vector()
            start_vector = ray_samples[0]
            input_xy[index, :] = xy[0]

            # l = (75, 290)
            # x = xy[0][0]
            # y = xy[0][1]
            # l_l = l[0] / 800
            # l_r = (l[0] + 80) / 800
            # l_t = l[1] / 600
            # l_b = (l[1] + 130) / 600
            # l_l = l_l*2-1
            # l_r = l_r*2-1
            # l_t = l_t*2-1
            # l_b = l_b*2-1
            # if x < l_l or x > l_r or y < l_t or y > l_b:
            #     continue
            # every element of the history is a triple.
            # 1st element is the ray segment start point before the triangle.
            # 1st element is the ray segment end point on the triangle.
            # 2nd element is the index for the triangle in the mesh.
            ray_history = []

            power = 1
            if xy[0][0]>0.5 and xy[0][1]>0.5:
                bk = int(0)
                start_vector.end.data[0] = 0.5
                start_vector.end.data[1] = 0.5
            res_vec, power = self.cast_ray(start_vector, ray_history, mesh, power)
            while res_vec is not None and res_vec.mode != 'place_holder' and power > 1e-3:
                res_vec, power = self.cast_ray(res_vec, ray_history, mesh, power)

            final_color = self.forward_history(ray_history, mesh)
            if final_color is not None:
                #color_data = np.concatenate((final_color.color,
                #                            Color.supported_color_space[final_color.mode]))
                output_color[index, :] = final_color.color

        return (input_xy, output_color)
            
            

    def cast_ray(self, start_vector, ray_history, mesh, power):
        p3d = start_vector.start
        nearest_dist = None
        nearest_ipoint = None
        nearest_triangle = None
        for tri in range(mesh.triangles.size()):
            result_ipoint = ray_in_triangle(start_vector, mesh.triangles[tri])
            if result_ipoint is not None:
                ppdist = dist(p3d, result_ipoint)
                if nearest_dist is None or ppdist < nearest_dist:
                    nearest_dist = ppdist
                    nearest_triangle = tri
                    nearest_ipoint = result_ipoint

        ret_power = mesh.textures[tri].damping_rate()*power

        if nearest_dist is None:
            return None, 0
        else:
            ray_history.append((p3d, nearest_ipoint, nearest_triangle))
            x, y, z = sphere_sampling(1)
            return Vector(nearest_ipoint,
                          Point3D(nearest_ipoint.data[0] + x,
                                  nearest_ipoint.data[1] + y,
                                  nearest_ipoint.data[2] + z,)), ret_power
            

    def forward_history(self, history, mesh):
        target_point = history[0][1]
        tris = []
        for i in range(len(history)):
            if mesh.textures[i].damping_rate() < 1e-3:
                tris.append(mesh.triangles[i]);
            
        ray_sum_sqrt = 3
        ray_hit = 0
        p1 = tris[0].p1
        p2 = tris[0].p2
        p3 = tris[0].p3

        intver = 1/ray_sum_sqrt;
        for i in range(ray_sum_sqrt):
            for j in range(ray_sum_sqrt):
                tx = i*intver + intver * np.random.random()
                px = Point3D(p1.data[0]*(1-tx) + p2.data[0]*tx, p1.data[1]*(1-tx)+p2.data[1]*tx, p1.data[2]*(1-tx)+p2.data[2]*tx)
                ty = j*intver + intver * np.random.random()
                py = Point3D(p3.data[0]*(1-tx) + p2.data[0]*tx, p3.data[1]*(1-tx)+p2.data[1]*tx, p3.data[2]*(1-tx)+p2.data[2]*tx)
                pt = Point3D(p2.data[0]+px.data[0]+py.data[0], p2.data[1]+px.data[1]+py.data[1], p2.data[2]+px.data[2]+py.data[2])
                ra = Vector(target_point, pt)

                hit = False;
                for tri in range(mesh.triangles.size()):
                    triangle = mesh.triangles[tri]
                    result_ipoint = ray_in_triangle(ra, triangle)
                    if result_ipoint is not None:
                        hit = True
                        break

                if not hit:
                    ray_hit += 1
                

        color = None
        while len(history) > 0:
            (p_start, p_end, tri) = history.pop()
            ttex = mesh.textures[tri]
            ttex_pos = mesh.texture_pos[tri]
            color = ttex.get_color(color, 0, 0, 0, 0, None, None)
        if color is None:
            return color
        else:
            return color*ray_hit/ray_sum_sqrt**2

            
        
