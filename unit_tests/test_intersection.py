# -*- coding: utf-8 -*-
import math
import unittest
from Geometry3D import *
import Geometry3D
import copy

class PointIntersectionTest(unittest.TestCase):
    def test_intersection_point_point(self):
        self.assertEqual(intersection(origin(),Point(0,0,0)),origin())
        self.assertEqual(intersection(Point(0,0,0),origin()),origin())
        self.assertTrue(intersection(origin(),Point(1,1,0)) is None)
    
    def test_intersection_point_line(self):
        self.assertTrue(intersection(x_axis(),origin()) == origin())
        self.assertTrue(intersection(origin(),x_axis()) == origin())
        self.assertTrue(intersection(Point(1,0,3),y_axis()) is None)
    
    def test_intersection_point_plane(self):
        self.assertEqual(intersection(Point(1,2,0),xy_plane()),Point(1,2,0))
        self.assertEqual(intersection(xy_plane(),Point(1,2,0)),Point(1,2,0))
        self.assertTrue(intersection(xy_plane(),Point(0,0,0.1)) is None)

    def test_intersection_point_segment(self):
        self.assertEqual(intersection(origin(),Segment(Point(-1,0,0),Point(1,0,0))),origin())
        self.assertEqual(intersection(Segment(Point(-1,0,0),Point(1,0,0)),origin()),origin())
        self.assertEqual(intersection(Segment(Point(0,0,0),Point(1,0,0)),origin()),origin())
        self.assertEqual(intersection(Segment(Point(-1,-1,-1),Point(1,1,1)),origin()),origin())
        self.assertTrue(intersection(Segment(Point(-1,-1,-1),Point(1,1,1)),Point(0,0,0.1)) is None)

    def test_intersection_point_convexpolygon(self):
        cpg = Parallelogram(origin(),Vector(1,0,1),Vector(0,1,1))
        self.assertEqual(intersection(origin(),cpg),origin())
        self.assertEqual(intersection(Point(1,0,1),cpg),Point(1,0,1))
        self.assertEqual(intersection(Point(0.5,0,0.5),cpg),Point(0.5,0,0.5))
        self.assertEqual(intersection(cpg,Point(0.5,0.5,1)),Point(0.5,0.5,1))
        self.assertTrue(intersection(cpg,Point(0.5,0.5,1.02)) is None)

    def test_intersection_point_convexpolyhedron(self):
        cph = Parallelepiped(origin(),Vector(1,0,0),Vector(0,1,0),Vector(0,0,2))
        self.assertEqual(intersection(cph,origin()),origin())
        self.assertEqual(intersection(Point(0.5,0,0),cph),Point(0.5,0,0))
        self.assertEqual(intersection(cph,Point(0.5,0.5,0)),Point(0.5,0.5,0))
        self.assertEqual(intersection(Point(0.5,0.5,1),cph),origin().move(Vector(0.5,0.5,1)))
        self.assertTrue(intersection(cph,Point(-0.1,0.5,0.5)) is None)

    def test_intersection_point_halfline(self):
        h = HalfLine(origin(),x_unit_vector())
        self.assertEqual(intersection(h,origin()),origin())
        self.assertEqual(intersection(Point(5,0,0),h),Point(5,0,0))
        self.assertTrue(intersection(h,Point(-2,0,0)) is None)
        self.assertTrue(intersection(Point(0,-1,0),h) is None)

class LineIntersectionTest(unittest.TestCase):
    def test_intersection_line_line(self):
        l1 = x_axis()
        l2 = Line(Point(1,0,0),Point(2,0,0))
        l3 = z_axis()
        l4 = Line(Point(1,2,0),Point(2,3,0))
        self.assertEqual(intersection(l1,l2),l1)
        self.assertEqual(intersection(l1,l3),origin())
        self.assertTrue(intersection(l3,l4) is None)
    
    def test_intersection_line_plane(self):
        l1 = x_axis()
        p1 = xy_plane()
        l2 = z_axis()
        l3 = Line(Point(2,3,2),Point(3,5,2))
        self.assertEqual(intersection(l1,p1),l1)
        self.assertEqual(intersection(p1,l2),origin())
        self.assertTrue(intersection(p1,l3) is None)
    
    def test_intersection_line_segment(self):
        l1 = x_axis()
        s1 = Segment(origin(),Point(1,0,0))
        l2 = z_axis()
        s2 = Segment(Point(-0.5,0,0),Point(0.5,0,0))
        s3 = Segment(Point(0.43,0.2224,-0.34),Point(0.23,0.234,0.241))
        s4 = Segment(Point(0.21,1321,1),Point(-0.24,-93,1))
        self.assertEqual(intersection(l1,s1),s1)
        self.assertEqual(intersection(l2,s1),origin())
        self.assertEqual(intersection(s2,l2),origin())
        self.assertTrue(intersection(s3,l2) is None)
        self.assertTrue(intersection(s4,l2) is None)

    def test_intersection_line_convexpolygon(self):
        cpg = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        l1 = x_axis()
        l2 = Line(Point(1,1,0),Point(0,0,0))
        l3 = Line(Point(1,1,0),Point(0.5,0,0))
        l4 = Line(Point(0.5,0,0),Point(1,0.5,0))
        l5 = Line(Point(1,0,0),Point(2,1,0))
        l6 = Line(Point(0.5,0.5,0),Point(0.6,0.6,2))
        l7 = Line(origin(),Point(1,1,1))
        l8 = Line(Point(0,0,1), Point(1,1,1))
        l9 = Line(Point(0,0,0.5),Point(1,1,1))
        self.assertEqual(intersection(cpg,l1),Segment(origin(),Point(1,0,0)))
        self.assertEqual(intersection(cpg,l2),Segment(origin(),Point(1,1,0)))
        self.assertEqual(intersection(cpg,l3),Segment(Point(0.5,0,0),Point(1,1,0)))
        self.assertEqual(intersection(cpg,l4),Segment(Point(0.5,0,0),Point(1,0.5,0)))
        self.assertEqual(intersection(cpg,l5),Point(1,0,0))
        self.assertEqual(intersection(cpg,l6),Point(0.5,0.5,0))
        self.assertEqual(intersection(cpg,l7),Point(0,0,0))
        self.assertTrue(intersection(cpg,l8) is None)
        self.assertTrue(intersection(cpg,l9) is None)
        
    def test_intersection_line_convexpolyhedron(self):
        cph = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        l1 = x_axis()
        l2 = Line(Point(1,1,0),Point(0,0,0))
        l3 = Line(Point(1,1,0),Point(0.5,0,0))
        l4 = Line(Point(0.5,0,0),Point(1,0.5,0))
        l5 = Line(Point(1,0,0),Point(2,1,0))
        l6 = Line(Point(0.5,0.5,0),Point(0.6,0.6,1))
        l7 = Line(origin(),Point(1,1,1))
        l8 = Line(Point(0,0,1), Point(1,1,1))
        l9 = Line(Point(0,0,0.5),Point(1,1,1))
        l10 = Line(Point(-1,-1,-1),Point(-2,-2,0))
        l11 = Line(Point(-1,0,0),Point(1,0,1))
        l12 = Line(Point(0,0,2),Point(2,2,0))
        l13 = Line(Point(1,-1,0),Point(0,1,2))
        l14 = Line(Point(0.5,0,0),Point(1,1,1))
        self.assertEqual(intersection(cph,l1),Segment(origin(),Point(1,0,0)))
        self.assertEqual(intersection(cph,l2),Segment(origin(),Point(1,1,0)))
        self.assertEqual(intersection(cph,l3),Segment(Point(0.5,0,0),Point(1,1,0)))
        self.assertEqual(intersection(cph,l4),Segment(Point(0.5,0,0),Point(1,0.5,0)))
        self.assertEqual(intersection(cph,l5),Point(1,0,0))
        self.assertEqual(intersection(cph,l6),Segment(Point(0.5,0.5,0),Point(0.6,0.6,1)))
        self.assertEqual(intersection(cph,l7),Segment(Point(0,0,0),Point(1,1,1)))
        self.assertEqual(intersection(cph,l8),Segment(Point(0,0,1),Point(1,1,1)))
        self.assertEqual(intersection(cph,l9),Segment(Point(0,0,0.5),Point(1,1,1)))
        self.assertTrue(intersection(cph,l10) is None)
        self.assertEqual(intersection(cph,l11),Segment(Point(0,0,0.5),Point(1,0,1)))
        self.assertEqual(intersection(cph,l12),Point(1,1,1))
        self.assertEqual(intersection(cph,l13),Point(0.5,0,1))
        self.assertEqual(intersection(cph,l14),Segment(Point(0.5,0,0),Point(1,1,1)))

    def test_intersection_line_halfline(self):
        h = HalfLine(origin(),x_unit_vector())
        l1 = x_axis()
        l2 = x_axis().move(y_unit_vector())
        l3 = y_axis().move(x_unit_vector())
        l4 = y_axis().move(-x_unit_vector())
        l5 = y_axis()
        self.assertEqual(intersection(h,l1),h)
        self.assertTrue(intersection(h,l2) is None)
        self.assertEqual(intersection(l3,h),Point(1,0,0))
        self.assertTrue(intersection(h,l4) is None)
        self.assertEqual(intersection(l5,h),origin())

class PlaneIntersectionTest(unittest.TestCase):
    def test_intersection_plane_plane(self):
        p1 = xy_plane()
        p2 = xy_plane()
        p3 = xz_plane()
        p4 = xy_plane().move(z_unit_vector())
        self.assertEqual(intersection(p1,p2),xy_plane())
        self.assertEqual(intersection(p1,p3),x_axis())
        self.assertTrue(intersection(p1,p4) is None)
    
    def test_intersection_plane_segment(self):
        p1 = xy_plane()
        s1 = Segment(Point(0,0,-1),Point(0,0,1))
        s2 = Segment(Point(-2,3,0),Point(2,34.3,0))
        s3 = Segment(Point(1,3,0.1),Point(2,34,0.1))
        self.assertEqual(intersection(p1,s1),origin())
        self.assertEqual(intersection(s2,p1),s2)
        self.assertTrue(intersection(s3,p1) is None)

    def test_intersection_plane_convexpolygon(self):
        p1 = xy_plane()
        cpg1 = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        cpg2 = Parallelogram(origin(),x_unit_vector(),z_unit_vector())
        cpg3 = Parallelogram(origin(),Vector(0,1,1),Vector(0,-1,1))
        cpg4 = copy.deepcopy(cpg2).move(Vector(0,0,-0.5))
        cpg5 = Parallelogram(origin().move(z_unit_vector()),x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(p1,cpg1),cpg1)
        self.assertEqual(intersection(p1,cpg2),Segment(origin(),Point(1,0,0)))
        self.assertEqual(intersection(p1,cpg3),origin())
        self.assertEqual(intersection(p1,cpg4),Segment(origin(),Point(1,0,0)))
        self.assertTrue(intersection(p1,cpg5) is None)
    
    def test_intersection_plane_convexpolyhedron(self):
        cph = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        p1 = xy_plane()
        p2 = xy_plane().move(Vector(0,0,0.5))
        p3 = Plane(Point(1,1,1),Vector(1,1,1))
        p4 = Plane(origin(),Vector(-1,-1,0))
        p5 = Plane(Point(0.1,0.1,0.1),Vector(1,1,1))
        p6 = Plane(Point(-0.1,-0.1,-0.1),Vector(-1,-1,-1))
        p7 = xy_plane().move(-z_unit_vector())
        self.assertTrue(intersection(cph,p1) == (Parallelogram(origin(),x_unit_vector(),y_unit_vector())))
        self.assertTrue(intersection(cph,p2) == (Parallelogram(origin().move(0.5*z_unit_vector()),x_unit_vector(),y_unit_vector())))
        self.assertEqual(intersection(cph,p3),Point(1,1,1))
        self.assertEqual(intersection(cph,p4),Segment(origin(),Point(0,0,1)))
        self.assertTrue(intersection(cph,p5) == (ConvexPolygon((Point(0,0,0.3),Point(0,0.3,0),Point(0.3,0,0)))))
        self.assertTrue(intersection(cph,p6) is None)
        self.assertTrue(intersection(cph,p7) is None)

    def test_intersection_plane_halfline(self):
        h = HalfLine(origin(),Point(1,0,0))
        p1 = xy_plane()
        p2 = xy_plane().move(z_unit_vector())
        p3 = yz_plane()
        p4 = yz_plane().move(x_unit_vector())
        p5 = yz_plane().move(-x_unit_vector())
        self.assertEqual(intersection(h,p1),h)
        self.assertEqual(intersection(p3,h),origin())
        self.assertEqual(intersection(h,p4),Point(1,0,0))
        self.assertTrue(intersection(h,p2) is None)
        self.assertTrue(intersection(p5,h) is None)        

class SegmentIntersectionTest(unittest.TestCase):
    def test_intersection_segment_segment(self):
        p1 = Point(-0.5,0,0)
        p2 = origin()
        p3 = Point(0.5,0,0)
        p4 = Point(1,0,0)
        p5 = Point(0,-0.5,0)
        p6 = Point(0,0.5,0)
        p7 = Point(-0.5,1,0)
        p8 = Point(1,1,0)
        self.assertEqual(intersection(Segment(p1,p2),Segment(p2,p4)),p2)
        self.assertEqual(intersection(Segment(p1,p3),Segment(p2,p4)),Segment(p2,p3))
        self.assertEqual(intersection(Segment(p1,p4),Segment(p2,p3)),Segment(p2,p3))
        self.assertTrue(intersection(Segment(p1,p2),Segment(p3,p4)) is None)
        self.assertEqual(intersection(Segment(p5,p6),Segment(p1,p4)),p2)
        self.assertTrue(intersection(Segment(p7,p8),Segment(p1,p2)) is None)
        self.assertTrue(intersection(Segment(p7,p4),Segment(p2,p3)) is None)
        self.assertEqual(intersection(Segment(p1,p4),Segment(p4,p5)),p4)

    def test_intersection_segment_convexpolygon(self):
        cpg = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        s1 = Segment(origin(),Point(1,0,0))
        s2 = Segment(Point(-0.5,0.5,0),Point(0.5,0.5,0))
        s3 = Segment(Point(-0.5,0.5,0),Point(1.5,0.5,0))
        s4 = Segment(Point(0.2,0.5,0),Point(0.8,0.5,0))
        s5 = Segment(origin(),origin().move(z_unit_vector()))
        s6 = Segment(Point(-1,-1,0),Point(1.5,1.5,0))
        s7 = copy.deepcopy(s5).move(Vector(-0.1,-0.1,0))
        s8 = Segment(Point(0.5,0.5,0.5),Point(0.5,0.5,1))
        s9 = Segment(Point(0.5,0.4,1),Point(0.5,0.5,1))
        self.assertEqual(intersection(cpg,s1),s1)
        self.assertEqual(intersection(cpg,s2),Segment(Point(0,0.5,0),Point(0.5,0.5,0)))
        self.assertEqual(intersection(s3,cpg),Segment(Point(0,0.5,0),Point(1,0.5,0)))
        self.assertEqual(intersection(cpg,s4),s4)
        self.assertEqual(intersection(cpg,s5),origin())
        self.assertEqual(intersection(cpg,s6),Segment(origin(),Point(1,1,0)))
        self.assertTrue(intersection(s7,cpg) is None)
        self.assertTrue(intersection(cpg,s8) is None)
        self.assertTrue(intersection(s9,cpg) is None)

    def test_intersection_segment_convexpolyhedron(self):
        cph = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        s1 = Segment(origin(),Point(1,0,0))
        s2 = Segment(Point(-0.5,0.5,0),Point(0.5,0.5,0))
        s3 = Segment(Point(-0.5,0.5,0),Point(1.5,0.5,0))
        s4 = Segment(Point(0.2,0.5,0),Point(0.8,0.5,0))
        s5 = Segment(origin(),origin().move(z_unit_vector()))
        s6 = Segment(Point(-1,-1,0),Point(1.5,1.5,0))
        s7 = copy.deepcopy(s5).move(Vector(-0.1,-0.1,0))
        s8 = Segment(Point(0.5,0.5,0.5),Point(0.5,0.5,1))
        s9 = Segment(Point(0.5,0.4,1.1),Point(0.5,0.5,1.1))
        s10 = Segment(Point(0.2,0.3,0.4),Point(0.54,0.324,0.25))
        s11 = Segment(Point(0,0,0),Point(1,1,1))
        s12 = Segment(Point(0,-1,0),Point(2,1,0))
        s13 = copy.deepcopy(s12).move(0.5 * z_unit_vector())
        s14 = Segment(Point(0,-0.5,0),Point(1.5,1,0))
        s15 = Segment(Point(0,-0.5,0.5),Point(1.5,1,0.5))
        center_p = Point(0.5,0.5,0.5)
        a = Point(0.5,0.5,2)
        b = Point(0.5,-0.5,-0.5)
        c = Point(2,2,2)
        s16 = Segment(center_p,a)
        s17 = Segment(center_p,b)
        s18 = Segment(center_p,c)
        self.assertEqual(intersection(cph,s1),s1)
        self.assertEqual(intersection(cph,s2),Segment(Point(0,0.5,0),Point(0.5,0.5,0)))
        self.assertEqual(intersection(s3,cph),Segment(Point(0,0.5,0),Point(1,0.5,0)))
        self.assertEqual(intersection(s4,cph),s4)
        self.assertEqual(intersection(cph,s5),Segment(origin(),Point(0,0,1)))
        self.assertEqual(intersection(cph,s6),Segment(origin(),Point(1,1,0)))
        self.assertTrue(intersection(cph,s7) is None)
        self.assertEqual(intersection(s8,cph),s8)
        self.assertTrue(intersection(cph,s9) is None)
        self.assertEqual(intersection(cph,s10),s10)
        self.assertEqual(intersection(s11,cph),s11)
        self.assertEqual(intersection(s12,cph),Point(1,0,0))
        self.assertEqual(intersection(s13,cph),Point(1,0,0.5))
        self.assertEqual(intersection(cph,s14),Segment(Point(0.5,0,0),Point(1,0.5,0)))
        self.assertEqual(intersection(cph,s15),Segment(Point(0.5,0,0.5),Point(1,0.5,0.5)))
        self.assertEqual(intersection(s16,cph),Segment(center_p,Point(0.5,0.5,1)))
        self.assertEqual(intersection(s17,cph),Segment(center_p,Point(0.5,0,0)))
        self.assertEqual(intersection(s18,cph),Segment(center_p,Point(1,1,1)))

    def test_intersection_segment_halfline(self):
        h = HalfLine(origin(),x_unit_vector())
        s1 = Segment(Point(-2,0,0),Point(-1,0,0))
        s2 = copy.deepcopy(s1).move(x_unit_vector())
        s3 = copy.deepcopy(s2).move(x_unit_vector())
        s4 = copy.deepcopy(s3).move(x_unit_vector())
        s5 = Segment(Point(-1,0,0),Point(1,0,0))
        s6 = Segment(Point(0,0,1),Point(1,0,1))
        s7 = Segment(Point(1,1,0),Point(1,2,0))
        s8 = Segment(Point(0,-1,0),Point(0,1,0))
        s9 = Segment(Point(1,-1,0),Point(1,1,0))
        s10 = Segment(Point(-1,-1,0),Point(-1,1,0))
        self.assertEqual(intersection(h,s2),origin())
        self.assertEqual(intersection(s3,h),s3)
        self.assertEqual(intersection(h,s4),s4)
        self.assertEqual(intersection(s5,h),s3)
        self.assertEqual(intersection(h,s8),origin())
        self.assertEqual(intersection(s9,h),Point(1,0,0))
        self.assertTrue(intersection(h,s1) is None)
        self.assertTrue(intersection(s6,h) is None)
        self.assertTrue(intersection(h,s7) is None)
        self.assertTrue(intersection(s10,h) is None)

class ConvexPolygonIntersectionTest(unittest.TestCase):
    def test_intersection_convexpolygon_convexpolygon(self):
        cpg0 = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        cpg1 = Parallelogram(origin(),2 * x_unit_vector(),2 * y_unit_vector())
        self.assertTrue(intersection(cpg0,cpg1) == (cpg0))
        cpg2 = Parallelogram(origin(),-x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cpg0,cpg2),Segment(origin(),Point(0,1,0)))
        cpg3 = Parallelogram(origin(),-2 * x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cpg0,cpg3),Segment(origin(),Point(0,1,0)))
        cpg4 = Parallelogram(Point(0.5,0.5,0),x_unit_vector(),y_unit_vector())
        self.assertTrue(intersection(cpg0,cpg4) == (Parallelogram(Point(0.5,0.5,0),0.5*x_unit_vector(),0.5*y_unit_vector())))
        cpg5 = Parallelogram(Point(1,0.5,0),Vector(1,1,0),Vector(1,-1,0))
        self.assertEqual(intersection(cpg0,cpg5),Point(1,0.5,0))
        cpg6 = Parallelogram(Point(1,-0.5,0),x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cpg0,cpg6),Segment(Point(1,0,0),Point(1,0.5,0)))
        cpg7 = Parallelogram(origin().move(z_unit_vector()),x_unit_vector(),y_unit_vector())
        self.assertTrue(intersection(cpg0,cpg7) is None)
        cpg8 = Parallelogram(Point(0.5,0,-0.5),x_unit_vector(),z_unit_vector())
        self.assertEqual(intersection(cpg0,cpg8),Segment(Point(0.5,0,0),Point(1,0,0)))
        cpg9 = Parallelogram(Point(0.5,0.5,-0.5),Vector(2,-2,0),z_unit_vector())
        self.assertEqual(intersection(cpg0,cpg9),Segment(Point(0.5,0.5,0),Point(1,0,0)))
        cpg10 = Parallelogram(Point(0.5,0.5,-0.5),Vector(0.2,-0.2,0),z_unit_vector())
        self.assertEqual(intersection(cpg0,cpg10),Segment(Point(0.5,0.5,0),Point(0.7,0.3,0)))
        cpg11 = Parallelogram(Point(0,0,2),Vector(1,0,-1),y_unit_vector())
        cpg12 = Parallelogram(Point(0.5,0.5,0),Vector(2,-2,0),z_unit_vector())
        self.assertEqual(intersection(cpg0,cpg12),Segment(Point(0.5,0.5,0),Point(1,0,0)))
        cpg13 = ConvexPolygon((Point(171.76, 98.39, -36.5), Point(0.0, 0.0, -0.0), Point(171.76, 0.0, -0.0))) 
        cpg14 = ConvexPolygon((Point(-50.0, 10.0, -86.5), Point(-50.0, 10.0, 50.0), Point(221.76, 10.0, 50.0), Point(221.76, 10.0, -86.5)))
        self.assertEqual(intersection(cpg13,cpg14),Segment(Point(171.76, 10.0, -3.7097265982315193),Point(17.457058644171155, 10.0, -3.7097265982315193)))
        cpg15 = ConvexPolygon((Point(61.32, 0.0, 0.58), Point(-0.21, 50.58, -28.91), Point(-0.21, 0.0, -28.91)))
        cpg16 = ConvexPolygon((Point(-50.21, 20.0, -78.91), Point(-50.21, 20.0, 50.58), Point(111.32, 20.0, 50.58), Point(111.32, 20.0, -78.91)))
        self.assertEqual(intersection(cpg15,cpg16),Segment(Point(36.99022538552788, 20.0, -11.08073546856465),Point(-0.21, 20.0, -28.91)))
        cpg17 = ConvexPolygon((Point(156.05, 0.0, -1189.0), Point(156.05, 1000.0, -122.42), Point(156.05, 0.0, -122.42)))
        cpg18 = ConvexPolygon((Point(106.05000000000001, 330.0, -1239.0), Point(106.05000000000001, 330.0, -72.42), Point(206.05, 330.0, -72.42), Point(206.05, 330.0, -1239.0)))
        self.assertEqual(intersection(cpg17,cpg18), Segment(Point(156.05, 330.0, -837.0286), Point(156.05, 330.0, -122.42000000000007)))
        
    def test_intersection_convexpolygon_convexpolyhedron(self):
        cph = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        cpg0 = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        cpg1 = Parallelogram(origin(),2 * x_unit_vector(),2 * y_unit_vector())
        self.assertTrue(intersection(cph,cpg1) == (cpg0))
        cpg2 = Parallelogram(origin(),-x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cph,cpg2),Segment(origin(),Point(0,1,0)))
        cpg3 = Parallelogram(origin(),-2 * x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cpg3,cph),Segment(origin(),Point(0,1,0)))
        cpg4 = Parallelogram(Point(0.5,0.5,0),x_unit_vector(),y_unit_vector())
        self.assertTrue(intersection(cph,cpg4) == (Parallelogram(Point(0.5,0.5,0),0.5*x_unit_vector(),0.5*y_unit_vector())))
        cpg5 = Parallelogram(Point(1,0.5,0),Vector(1,1,0),Vector(1,-1,0))
        self.assertEqual(intersection(cph,cpg5),Point(1,0.5,0))
        cpg6 = Parallelogram(Point(1,-0.5,0),x_unit_vector(),y_unit_vector())
        self.assertEqual(intersection(cph,cpg6),Segment(Point(1,0,0),Point(1,0.5,0)))
        cpg7 = Parallelogram(origin().move(0.5*z_unit_vector()),x_unit_vector(),y_unit_vector())
        self.assertTrue(intersection(cph,cpg7) == (cpg7))
        cpg8 = Parallelogram(Point(0.5,0,-0.5),x_unit_vector(),z_unit_vector())
        self.assertTrue(intersection(cph,cpg8) == (Parallelogram(Point(0.5,0,0),0.5*x_unit_vector(),0.5*z_unit_vector())))
        cpg9 = Parallelogram(Point(0.5,0.5,-0.5),Vector(2,-2,0),z_unit_vector())
        self.assertTrue(intersection(cpg9,cph) == (Parallelogram(Point(0.5,0.5,0),Vector(0.5,-0.5,0),0.5*z_unit_vector())))
        cpg10 = Parallelogram(Point(0.5,0.5,-0.5),Vector(0.2,-0.2,0),z_unit_vector())
        self.assertTrue(intersection(cph,cpg10) == (Parallelogram(Point(0.5,0.5,0),Vector(0.2,-0.2,0),0.5*z_unit_vector())))
        cpg11 = Parallelogram(Point(0,0,2),Vector(1,0,-1),y_unit_vector())
        self.assertEqual(intersection(cph,cpg11),Segment(Point(1,0,1),Point(1,1,1)))
        cpg12 = Parallelogram(Point(0.5,0.5,0),Vector(2,-2,0),z_unit_vector())
        self.assertTrue(intersection(cpg12,cph) == (Parallelogram(Point(0.5,0.5,0),z_unit_vector(),Vector(0.5,-0.5,0))))
        cpg13 = Parallelogram(Point(0,0,3),Vector(1,0,-1),y_unit_vector())
        self.assertTrue(intersection(cph,cpg13) is None)
        cpg14 = Parallelogram(Point(0,0,2),x_unit_vector(),y_unit_vector())
        self.assertTrue(intersection(cph,cpg14) is None)
    
    def test_intersection_convexpolygon_halfline(self):
        cpg = Parallelogram(origin(),x_unit_vector(),y_unit_vector())
        h1 = HalfLine(Point(0.5,0.5,0),x_unit_vector())
        h2 = HalfLine(origin(),Point(1,1,0))
        h3 = HalfLine(origin(),z_unit_vector())
        h4 = HalfLine(Point(2,2,2),Point(3,3,3))
        h5 = HalfLine(Point(2,2,2),origin())
        h6 = HalfLine(Point(1,1,2),Point(1,1,0))
        h7 = HalfLine(Point(2,2,2),Point(1,1,0))
        h8 = HalfLine(Point(2,2,2),Point(1.1,1.1,0))
        h9 = HalfLine(Point(1.5,0.5,0),Point(-0.5,0.5,0))
        self.assertEqual(intersection(cpg,h1),Segment(Point(0.5,0.5,0),Point(1,0.5,0)))
        self.assertEqual(intersection(h2,cpg),Segment(origin(),Point(1,1,0)))
        self.assertEqual(intersection(h3,cpg),origin())
        self.assertEqual(intersection(h5,cpg),origin())
        self.assertEqual(intersection(cpg,h6),Point(1,1,0))
        self.assertEqual(intersection(h7,cpg),Point(1,1,0))
        self.assertEqual(intersection(cpg,h9),Segment(Point(0,0.5,0),Point(1,0.5,0)))
        self.assertTrue(intersection(cpg,h4) is None)
        self.assertTrue(intersection(h8,cpg) is None)

class ConvexPolyhedronIntersectionTest(unittest.TestCase):
    def test_intersection_convexpolyhedron_convexpolyhedron(self):
        cph0 = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        cph1 = copy.deepcopy(cph0).move(Vector(1,1,1))
        cph2 = copy.deepcopy(cph0).move(x_unit_vector())
        cph3 = copy.deepcopy(cph0).move(Vector(1,1,0))
        cph4 = copy.deepcopy(cph0).move(Vector(0.5,0.5,0.5))
        cph5 = copy.deepcopy(cph0).move(Vector(1.5,1.5,1.5))
        cph6 = Parallelepiped(origin(),2 * x_unit_vector(),2 * y_unit_vector(),2 * z_unit_vector())
        self.assertEqual(intersection(cph0,cph0),cph0)
        self.assertEqual(intersection(cph0,cph1),Point(1,1,1))
        self.assertTrue(intersection(cph0,cph2) == (Parallelogram(Point(1,0,0),y_unit_vector(),z_unit_vector())))
        self.assertEqual(intersection(cph0,cph3),Segment(Point(1,1,0),Point(1,1,1)))
        self.assertEqual(intersection(cph4,cph0),Parallelepiped(Point(0.5,0.5,0.5),0.5*x_unit_vector(),0.5*y_unit_vector(),0.5*z_unit_vector()))
        self.assertTrue(intersection(cph5,cph0) is None)
        self.assertEqual(intersection(cph0,cph6),cph0)

    def test_intersection_convexpolyhedron_halfline(self):
        cph = Parallelepiped(origin(),x_unit_vector(),y_unit_vector(),z_unit_vector())
        h1 = HalfLine(Point(0.5,0.5,0.5),x_unit_vector())
        h2 = HalfLine(origin(),Point(1,1,1))
        h3 = HalfLine(origin(),Point(1,1,0))
        h4 = HalfLine(origin(),z_unit_vector())
        h5 = HalfLine(Point(2,2,2),Point(3,3,3))
        h6 = HalfLine(Point(2,2,2),origin())
        h7 = HalfLine(Point(1,1,2),Point(1,1,0))
        h8 = HalfLine(Point(2,2,2),Point(1,1,0))
        h9 = HalfLine(Point(2,2,2),Point(1.1,1.1,0))
        h10 = HalfLine(Point(1.5,0.5,0),Point(-0.5,0.5,0))
        h11 = HalfLine(origin(),-x_unit_vector())
        h12 = HalfLine(origin(),-x_unit_vector() - y_unit_vector() - z_unit_vector())
        self.assertEqual(intersection(cph,h1),Segment(Point(0.5,0.5,0.5),Point(1,0.5,0.5)))
        self.assertEqual(intersection(h2,cph),Segment(origin(),Point(1,1,1)))
        self.assertEqual(intersection(cph,h3),Segment(origin(),Point(1,1,0)))
        self.assertEqual(intersection(h4,cph),Segment(origin(),Point(0,0,1)))
        self.assertEqual(intersection(h6,cph),Segment(origin(),Point(1,1,1)))
        self.assertEqual(intersection(cph,h7),Segment(Point(1,1,1),Point(1,1,0)))
        self.assertEqual(intersection(h8,cph),Point(1,1,0))
        self.assertEqual(intersection(h11,cph),Point(0,0,0))
        self.assertEqual(intersection(h12,cph),Point(0,0,0))
        self.assertEqual(intersection(cph,h10),Segment(Point(0,0.5,0),Point(1,0.5,0)))
        self.assertTrue(intersection(cph,h5) is None)
        self.assertTrue(intersection(h9,cph) is None)

class HalfLineIntersectionTest(unittest.TestCase):
    def test_intersection_halfline_halfline(self):
        h1 = HalfLine(origin(),x_unit_vector())
        h2 = HalfLine(Point(1,0,0),x_unit_vector())
        h3 = HalfLine(Point(1,0,0),-x_unit_vector())
        h4 = HalfLine(origin(),Point(0,1,0))
        h5 = HalfLine(Point(1,-1,0),y_unit_vector())
        h6 = HalfLine(Point(1,1,0),y_unit_vector())
        h7 = HalfLine(origin(),x_unit_vector())
        self.assertEqual(intersection(h1,h2),h2)
        self.assertEqual(intersection(h1,h3),Segment(origin(),Point(1,0,0)))
        self.assertEqual(intersection(h1,h4),origin())
        self.assertEqual(intersection(h1,h5),Point(1,0,0))
        self.assertTrue(intersection(h1,h6) is None)
        self.assertEqual(intersection(h1,h7),h7)