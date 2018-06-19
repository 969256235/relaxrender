import numpy as np

from relaxrender.scene import Scene
from relaxrender.camera import PerspectiveCamera
from relaxrender.mesh import Mesh
from relaxrender.texture import Texture, PlaneLightSource, UniformReflection
from relaxrender.points import Point3D, Point2D, Vector, Point, Points
from relaxrender.triangle import Triangle, Triangles
from relaxrender.color import Color, Red, White, Black, Green, Blue, Grey
from relaxrender.math import dist, sphere_sampling, ray_in_triangle

__all__ = ['make_shadow_cornell_box', 'get_shadow']


def make_shadow_cornell_box():
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
    tris.append_rct(np.array([ 1, 1,  0]),
                    np.array([-1, 1,  0]),
                    np.array([-1, 1, -2]),
                    np.array([ 1, 1, -2]))

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

def get_shadow(from_point, mesh):
    tris = []
    for i in range(len(mesh.textures)):
        if mesh.textures[i].damping_rate() < 1e-3:
            tris.append(mesh.triangles[i]);

    ray_sum_sqrt = 3
    ray_hit = 0
    p1 = tris[0].p1
    p2 = tris[0].p2
    p3 = tris[0].p3
    # make p2 be right-angle point
    if np.dot(p1.data-p2.data,p3.data-p2.data) > 1e-3:
        if np.dot(p2.data-p1.data,p3.data-p1.data) < 1e-3:
            tmp = p2
            p2 = p1
            p1 = tmp
        else:
            tmp = p2
            p2 = p3
            p3 = tmp

    interval = 1/ray_sum_sqrt;
    for i in range(ray_sum_sqrt):
        for j in range(ray_sum_sqrt):
            tx = i*interval + interval * np.random.random()
            px = Point3D(p1.data[0]*(1-tx) + p2.data[0]*tx, p1.data[1]*(1-tx)+p2.data[1]*tx, p1.data[2]*(1-tx)+p2.data[2]*tx)
            ty = j*interval + interval * np.random.random()
            py = Point3D(p3.data[0]*(1-tx) + p2.data[0]*tx, p3.data[1]*(1-tx)+p2.data[1]*tx, p3.data[2]*(1-tx)+p2.data[2]*tx)
            light_target = Point3D((p2.data[0]+px.data[0]+py.data[0])/3, (p2.data[1]+px.data[1]+py.data[1])/3, (p2.data[2]+px.data[2]+py.data[2])/3)
            shadow_ray = Vector(from_point, light_target)

            p3d = from_point
            nearest_dist = None
            nearest_ipoint = None
            nearest_triangle = None
            for tri in range(mesh.triangles.size()):
                result_ipoint = ray_in_triangle(shadow_ray, mesh.triangles[tri])
                if result_ipoint is not None:
                    ppdist = dist(p3d, result_ipoint)
                    if nearest_dist is None or ppdist < nearest_dist:
                        nearest_dist = ppdist
                        nearest_triangle = tri
                        nearest_ipoint = result_ipoint
            if nearest_ipoint is None or dist(nearest_ipoint, light_target) < 1e-3:
                ray_hit += 1

    return ray_hit/ray_sum_sqrt**2

