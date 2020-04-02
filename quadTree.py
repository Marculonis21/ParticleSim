#!/usr/bin/env python3

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def contains(self, item):
        return (self.x - self.w < item.x < self.x + self.w and
                self.y - self.h < item.y < self.y + self.h)


class QuadTree:
    def __init__(self, area, capacity):
        self.area = area
        self.capacity = capacity 
        self.subdiv = False
        self.items = []

    def subdivide(self):
        nw = Rectangle(self.area.x-self.area.w/2,self.area.y-self.area.h/2, self.area.w/2, self.area.h/2)
        self.NW = QuadTree(nw, self.capacity)
        ne = Rectangle(self.area.x+self.area.w/2,self.area.y-self.area.h/2, self.area.w/2, self.area.h/2)
        self.NE = QuadTree(ne, self.capacity)
        sw = Rectangle(self.area.x-self.area.w/2,self.area.y+self.area.h/2, self.area.w/2, self.area.h/2)
        self.SW = QuadTree(sw, self.capacity)
        se = Rectangle(self.area.x+self.area.w/2,self.area.y+self.area.h/2, self.area.w/2, self.area.h/2)
        self.SE = QuadTree(se, self.capacity)

        self.subdiv = True

    def insert(self, item):
        
        if not (self.area.contains(item)):
            return

        if(len(self.items) < self.capacity):
            self.items += [item]

        else:
            if not (self.subdiv):
                self.subdivide()

            self.NW.insert(item)
            self.NE.insert(item)
            self.SW.insert(item)
            self.SE.insert(item)
