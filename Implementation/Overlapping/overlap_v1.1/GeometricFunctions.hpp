//
//  geometricFunctions.hpp
//  forceModel
//
//  Created by 王丹匀 on 2020/3/7.
//  Copyright © 2020 王丹匀. All rights reserved.
//

#ifndef geometricFunctions_hpp
#define geometricFunctions_hpp

#include <stdio.h>
#include <iostream>
#include <vector>
#include "Graph_instance/reader/DSPInstanceReader.hpp"

struct Vector {
    double dx;
    double dy;
    
    double norm(){
        return sqrt(dx * dx + dy * dy);
    }
    
    bool operator==(const Vector &p) const{
      return (fabs(dx-p.dx) <= 1e-10 && fabs(dy-p.dy) <= 1e-10);
    }
    
    Vector& operator+=(const Vector& other) {
        dx += other.dx;
        dy += other.dy;
        return *this;
    }

    Vector& operator-=(const Vector& other) {
        dx -= other.dx;
        dy -= other.dy;
        return *this;
    }

    Vector& operator*=(double scalar) {
        dx *= scalar;
        dy *= scalar;
        return *this;
    }

    Vector& operator/=(double scalar) {
        dx /= scalar;
        dy /= scalar;
        return *this;
    }
};

    
struct Point {
    double x;
    double y;
    
    bool operator==(const Point &p) const{
      return (fabs(x-p.x) <= 1e-10 && fabs(y-p.y) <= 1e-10);
    }
    
    Point& operator+=(const Point& other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    Point& operator-=(const Point& other) {
        x -= other.x;
        y -= other.y;
        return *this;
    }
};
vector<Point*> initializeDrawing(Graph *g, int range);
    
double calStrightDis(Point *p, Point *a, Point *b); // the distance between line ab and point p
double CheckRepulsiveRange(Point *p, Point *a, Point *b, double h); // if the point p is in the range of repulsion, return the distance between line ab and point p. Else return -1. ( Circle range )
double isPointInEdgeRange(Point *p, Point *a, Point *b, double range); // if the point p is in the range of repulsion, return the distance between line ab and point p. Else return -1. ( Rectangular range )
double get_angle(Point *p, Point *a, Point *b);
double get_cross_angle(Point *a, Point *b, Point *c, Point *d); // angle between ab and cd (-1 when no crossing)
double get_min_angle(vector<Point*> positions, Graph *g);
double get_min_avg_angle(vector<Point*> positions, Graph *g);
    
// double get_min_edge(vector<Point*> positions, Graph *g); // get the minimum edge length
double get_min_dis_p2p(vector<Point*> positions, Graph *g); // get the minimum distance between point to point
double get_min_dis_p2e(vector<Point*> positions, Graph *g); // get the minimum distance between point to edge
int get_num_repulsion(vector<Point*> positions, Graph *g, double* avg_dis); // get the number of point in the range of edge repulsion
int get_num_shortDis(vector<Point*> positions, Graph *g, double threshold, double* avgdis); // get the number of pairs of points when the distance between the pair of points is short
    
double evaluate_drawing(vector<Point*> positions, Graph *g); // the evaluate function
    
void center_and_scale(Graph *g, unsigned int width, unsigned int height, vector<Point*> positions); // adjust the drawing position to the center

    
    //void printAllpoints(vector<Point*> positions);
    
#endif /* geometricFunctions_hpp */
