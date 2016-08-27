from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d
import math


CUBE=0
SPHERE=1

class Matrix:
    
    def __init__(self, width=None,height=None, depth=None, edges_size=12, shape=SPHERE):
        self.shape_type = shape
        self.height, self.width, self.depth = edges_size, edges_size, edges_size
        if width:
            self.width = width
        if height:
            self.height = height
        if depth:
            self.depth = depth
        self.max_dist = math.sqrt(width*width+height*height+depth*depth)/2.0
        self.matrix = self.create_matrix()
        self.shader = pi3d.Shader("uv_light")
        self.coffimg = pi3d.Texture("textures/COFFEE.PNG")

        
    def create_matrix(self):
        matrix=[]
        for ix in range(self.width):
            plane = []
            for iy in range(self.height):
                row = []
                for iz in range(self.depth):
                    element = self.create_shape(ix,iy,iz)
                    row.append([element, False])
                plane.append(row)
            matrix.append(plane)
            print('%s of %s' % (ix + 1, self.width))
        return matrix

    def create_shape(self,x,y,z):
        if self.shape_type==CUBE:
            shape = pi3d.Cuboid(x=(x-self.width/2),y=(y-self.height/2),z=(z - self.height / 2))
        if self.shape_type == SPHERE:
            shape = pi3d.Sphere(x=(x - self.width / 2), y=(y - self.height / 2), z=(z - self.height / 2), radius=0.5)
        self.set_material(shape, x, y, z)
        return shape
    
    def get_corners(self):
        return (
            self.matrix[0][0][0],
            self.matrix[self.width-1][0][0],
            self.matrix[0][self.height-1][0],
            self.matrix[self.width-1][self.height-1][0],
            self.matrix[0][0][self.depth-1],
            self.matrix[self.width-1][0][self.depth-1],
            self.matrix[0][self.height-1][self.depth-1],
            self.matrix[self.width-1][self.height-1][self.depth-1]
        )

    def set_material(self, shape, x, y, z):
        dx = (self.width/2.0) - x
        dy = (self.height / 2.0) - y
        dz = (self.depth / 2.0) - z
        d = math.sqrt(dx*dx+dy*dy+dz*dz)
        shape.set_material((abs(math.sin(x/2.0)),abs(math.sin(d/10.0)),abs(math.sin(z/10.0))))
        #c = 1.0-d/self.max_dist
        #shape.set_material((c,c,c))

    def show_corners(self):
        for c in self.get_corners():
            c[1]=True
            #c[0].set_material((1,1,1))

    def set_point(self,point, state):
        x, y, z = point
        self.matrix[x][y][z][1] = state

    def draw_matrix(self):
        for ix in range(self.width):
            for iy in range(self.height):
                for iz in range(self.depth):
                    cube, state = self.matrix[ix][iy][iz]
                    if state:
                        self.draw_element(cube)
                        cube.scale(1, 1, 1)

    def draw_element(self, element):
        element.draw(self.shader, [self.coffimg])
        #element.draw()