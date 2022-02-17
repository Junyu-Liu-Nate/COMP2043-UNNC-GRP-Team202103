//
//  geometricFunctions.cpp
//  forceModel
//
//  Created by 王丹匀 on 2020/3/7.
//  Copyright © 2020 王丹匀. All rights reserved.
//

#include "geometricFunctions.hpp"
#include <corecrt_math_defines.h>

vector<Point*> initializeDrawing(Graph *g, int range) {
    int vsize = g->getNumberOfVertices();
    
    // allocate memory
    vector<Point*> draw(vsize);
    
//    // randomly generate
//    for(int i=0; i<vsize; ++i) {
//        draw[i] = new Point;
//        draw[i]->x = rand()/double(RAND_MAX)*range;
//        draw[i]->y = rand()/double(RAND_MAX)*range;
//    }
    
    // circle in [0,1]
    double angle = 2.0 * M_PI / vsize;
    for (int i=0; i<vsize; ++i) {
        draw[i] = new Point;
        draw[i]->x = cos(i * angle)*range/2+(double)range/2;
        draw[i]->y = sin(i * angle)*range/2+(double)range/2;
    }
    return draw;
}

double calStrightDis(Point *p, Point *a, Point *b) {
    if(*a == *b){
        return sqrt(pow(p->y - a->y, 2) + pow(p->x - a->x, 2));
    }
    else {
        double c = (p->x - a->x) * (b->y - a->y) + (a->x - b->x) * (p->y - a->y);
        c *= c;
        c /= (pow(b->y - a->y, 2) + pow(a->x - b->x, 2));
        return sqrt(c);
    }
}

double get_angle(Point *p, Point *a, Point *b) {
    // angle apb, point P is the center point
    double theta = atan2(a->x - p->x, a->y - p->y) - atan2(b->x - p->x, b->y - p->y);
        if (theta > M_PI)
            theta -= 2 * M_PI;
        if (theta < -M_PI)
            theta += 2 * M_PI;
     
    theta = abs(theta * 180.0 / M_PI);
    return theta;
}

double get_cross_angle(Point *a, Point *b, Point *c, Point *d) {
    // get the crossing point
    Vector v1, v2;
    v1.dx = b->x - a->x;
    v1.dy = b->y - a->y;
    v2.dx = d->x - c->x;
    v2.dy = d->y - c->y;
    
    if(v1.dx*v2.dy - v2.dx*v1.dy < 1e-10) {
        return -1; // Collinear or parallel
    }
    
    float s, t;
    s = (-v1.dy * (a->x - c->x) + v1.dx * (a->y - c->y)) / (-v2.dx * v1.dy + v1.dx * v2.dy);
    t = ( v2.dx * (a->y - c->y) - v2.dy * (a->x - c->x)) / (-v2.dx * v1.dy + v1.dx * v2.dy);

    Point p;
    if(s >= 0 && s <= 1 && t >= 0 && t <= 1) {
        // Collision detected
        p.x = a->x + (t * v1.dx);
        p.y = a->y + (t * v1.dy);
    }
    else {
        return -1; // No collision
    }
    
//    printf("(%f, %f)\n", p.x, p.y);
    
    double angle1 = get_angle(&p, a, c);
    double angle2 = get_angle(&p, a, d);
    
    if(angle1 + angle2 >181 || angle1 + angle2 <179) {
        printf("Error occurs!\n");
        cout << angle1 + angle2 << endl;
        return -1;
    }
    
    if(angle1 > angle2)
        return angle2;
    else
        return angle1;
}


double get_min_angle(vector<Point*> positions, Graph *g) {
    int size = g->getNumberOfVertices();
    double theta = 180;


    for (int v_id = 0; v_id < size; v_id++) {
        Vertex *v = g->getVertexList().at(v_id);
        
        
        /* check all incident angles */
        if(v->num_of_neighbour >= 2) {
            // when neighbour <= 1, there is no incident angle
            for (int i = 0; i < v->num_of_neighbour; i++) {
                int adj_id1_ = v->getNeighbour().at(i);
                
                for (int j = i+1; j < v->num_of_neighbour; j++){
                    int adj_id2_ = v->getNeighbour().at(j);
                    
                    double angle = get_angle(positions[v_id], positions[adj_id1_], positions[adj_id2_]);
    //                printf("%f\n", angle);
                    if(angle < theta && angle > 0) {
                        theta = angle;
                    }
                }
            }
        }
        

        /* check all crossing edge angles */
        for (int i = 0; i < v->num_of_neighbour; i++) {
            int v_id2 = v->getNeighbour().at(i); // edge -> (v_id, v_id2)
            
            
            // another edge ->（edge1, edge2）
            for (int edge1 = 0; edge1 < size; edge1++){
                if(edge1 == v_id || edge1 == v_id2)
                    continue;
                
                for (int j = 0; j < g->getVertexList().at(edge1)->num_of_neighbour; j++) {
                    int edge2 = g->getVertexList().at(edge1)->getNeighbour().at(j);
                    if(edge2 == v_id || edge2 == v_id2)
                        continue;

                    double angle = get_cross_angle(positions[v_id], positions[v_id2], positions[edge1], positions[edge2]);
//                    if(angle >0) printf("%f\n", angle);
                    if(angle < theta && angle > 0) {
                        theta = angle;
                    }
                }
            }
        }
    }
    return theta;
}

double get_min_avg_angle(vector<Point*> positions, Graph *g) {
    int size = g->getNumberOfVertices();
    double sum = 0;
    double n = 0;

    for (int v_id = 0; v_id < size; v_id++) {
        Vertex *v = g->getVertexList().at(v_id);
        
        /* check all incident angles */
        if(v->num_of_neighbour >= 2) {
            // when neighbour <= 1, there is no incident angle
            double theta = 180;
            for (int i = 0; i < v->num_of_neighbour; i++) {
                int adj_id1_ = v->getNeighbour().at(i);
                
                for (int j = i+1; j < v->num_of_neighbour; j++){
                    int adj_id2_ = v->getNeighbour().at(j);
                    
                    double angle = get_angle(positions[v_id], positions[adj_id1_], positions[adj_id2_]);
    //                printf("%f\n", angle);
                    if(angle < theta && angle > 0) {
                        theta = angle;
                    }
                }
            }
            sum += theta;
            n = n+1;
        }
    }
    return sum/n;
}

// get the minimum distance between point to point
double get_min_dis_p2p(vector<Point*> positions, Graph *g){
    double mindis = 1000000;  // set it very big

    for (int i = 0; i < g->getNumberOfVertices(); i++) {
        for (int j = i+1; j < g->getNumberOfVertices(); j++) {
            double d = sqrt(pow(positions[i]->x-positions[j]->x, 2)+pow(positions[i]->y-positions[j]->y, 2));
            if(d < mindis)
                mindis = d;
        }
    }
    return mindis;
}

// get the number of pairs of points when the distance between the pair of points is short
int get_num_shortDis(vector<Point*> positions, Graph *g, double threshold, double* avgdis) {
    int n = 0;
    double avg_dis = 0;
    for (int i = 0; i < g->getNumberOfVertices(); i++) {
        for (int j = i+1; j < g->getNumberOfVertices(); j++) {
            double d = sqrt(pow(positions[i]->x-positions[j]->x, 2)+pow(positions[i]->y-positions[j]->y, 2));
            if(d <= threshold) {
                avg_dis += d;
                n++;
            }
        }
    }
    if(n != 0)
        avg_dis /= n; // the average distance (less than threshold)
    else
        avg_dis = threshold;
        
    if(avgdis != NULL)
        *avgdis = avg_dis;
    
    return n;
}

// get the minimum distance between point to edge
double get_min_dis_p2e(vector<Point*> positions, Graph *g) {
    double mindis = 1;  // set it very big

    // for each edge, check all other points if they are in repulsion
    for (int v_id = 0; v_id < g->getNumberOfVertices(); v_id++) {
        Vertex *v = g->getVertexList().at(v_id);
        
        for (int i = 0; i < v->num_of_neighbour; i++) {
            int adj_id = v->getNeighbour().at(i);
            
            if(adj_id < v_id) {
                continue;   // this edge has been visited
            }
            else {
                // this edge has not been visited
                for (int j = 0; j < g->getNumberOfVertices(); j++) {
                    if(j==v_id || j== adj_id)
                        continue;

                    double d = CheckRepulsiveRange(positions[j], positions[v_id], positions[adj_id], 1);
                    if(d < mindis && d >= 0) {
                        mindis = d;
                    }
                }
            }
        }
    }
//    printf("mindis:%f\n", mindis);
    return mindis;
}

// get the number of point in the range of edge repulsion
int get_num_repulsion(vector<Point*> positions, Graph *g, double* avg_dis) {
    int n = 0; // the number of point in the range of edge repulsion
    int n_force = 0;  // the number of edge repulsion forces
    double sum_dis = 0;
    
    int* sign = (int*)malloc(g->getNumberOfVertices() * sizeof(int));    // to remember if the point is in the range of edge repulsion
    memset(sign, 0, g->getNumberOfVertices() * sizeof(int));            // initialize to 0
    double k = 1*sqrt(1/(double)g->getNumberOfVertices()); // the ideal length
    
    
    // for each edge, check all other points if they are in repulsion
    for (int v_id = 0; v_id < g->getNumberOfVertices(); v_id++) {
        Vertex *v = g->getVertexList().at(v_id);
        
        for (int i = 0; i < v->num_of_neighbour; i++) {
            int adj_id = v->getNeighbour().at(i);
            
            if(adj_id < v_id) {
                continue;   // this edge has been visited
            }
            else {
                // this edge has not been visited
                for (int j = 0; j < g->getNumberOfVertices(); j++) {
                    if(j==v_id || j== adj_id)
                        continue;
        
                    double l = sqrt(pow(positions[v_id]->x-positions[adj_id]->x, 2)+pow(positions[v_id]->y-positions[adj_id]->y, 2));
                    double h = min(0.15, (l+k)/4);;  //  // double h = min(l/2, k/2);
//                    printf("l/2: %f  k/2: %f %f\n", l/2, k/2,  (l+k)/4);
                    
                    double d_ = CheckRepulsiveRange(positions[j], positions[v_id], positions[adj_id], h);
                    if(d_ >= 0) {
                        // in the range
                        if(sign[j] == 0) {
                            n++;
                            sign[j] = 1;
                        }
                        n_force++;
//                        sum_dis += pow(d_,2);
                        sum_dis += d_;
                    }
                }
            }
        }
    }
    free(sign);
    
    if(n_force != 0)
        *avg_dis = sum_dis/n_force;
    else
        *avg_dis = k/2;
    
//    printf("\n-----%f\n", *avg_dis);
    return n;
}

//// the evaluate function 1
//double evaluate_drawing1(vector<Point*> positions, Graph *g) {
//    double f = 0;
//    double w1, w2, w3, w4, w5;
//    w1 = 0.2;
//    w2 = 0.2;
//    w3 = 0.2;
//    w4 = 0.2;
//    w5 = 0.2;
//
//    double gsize = (double)g->getNumberOfVertices();
//
//    // the measurement for angle
//    double F_angle = min(get_min_angle(positions, g), 60.0)/60.0;
//
//    // the measurement for distance between point to point
//    double k = 1*sqrt(1/gsize); // the ideal length
//    double F_p2p = min(get_min_dis_p2p(positions, g), k)/k;
//
//    double threshold = k/2;
//    double F_pn;
//    if(gsize > 1)
//        F_pn = 1-(double)get_num_shortDis(positions, g, threshold, NULL)/(gsize*(gsize-1)/2); // [0,1]
//    else
//        F_pn = 1;
//
//
//    // the measurement for edge repulsion
//    double F_p2e = min(get_min_dis_p2e(positions, g), k)/k;
//    double avg_dis = 0;
//    double F_en = 1 - (double)get_num_repulsion(positions, g, &avg_dis) / gsize;
//
//    f = w1*F_angle + w2*F_p2p + w3*F_pn + w4*F_p2e + w5*F_en;
//
//    printf("\nEvaluatefunction1:\nF_angle %f\nF_p2p %f \nF_pn %f \nF_p2e %f \nF_en %f\nf:%f\n", F_angle, F_p2p, F_pn, F_p2e, F_en,f);
//    return f;
//}
    
// the evaluate function
double evaluate_drawing(vector<Point*> positions, Graph *g) {
    double f;
    double w1, w2, w3, w4, w5, w6, w7;
    
    // weights
//    w1 = 0.15;
//    w2 = 0.15;
//    w3 = 0.15;
//    w4 = 0.15;
//    w5 = 0.15;
//    w6 = 0.15;
//    w7 = 0.15;
    w1 = (double)1/7;
    w2 = (double)1/7;
    w3 = (double)1/7;
    w4 = (double)1/7;
    w5 = (double)1/7;
    w6 = (double)1/7;
    w7 = (double)1/7;

    double gsize = (double)g->getNumberOfVertices();
   
    // the measurement for angle
    double F_angle = min(get_min_angle(positions, g), 60.0)/60.0;
   
    // the measurement for distance between point to point
    double k = 1*sqrt(1/gsize); // the ideal length
    double F_p2p = min(get_min_dis_p2p(positions, g), k)/k;
   
    double threshold = k/2;
    double avgdis = 0;  // not used
    double nn = (double)get_num_shortDis(positions, g, threshold, &avgdis);
    if(nn >= gsize)
        nn = 0;
    else
        nn = pow(min(1-nn/gsize,1.0),2);
    
        
    double F_pn = 0;
    if(gsize > 1) //        F_pn = 1-nn/(gsize*(gsize-1)/2); // [0,1]
        F_pn = nn; // [0,1]
    else
       F_pn = 1;
    

    // the measurement for edge repulsion
    double p2e = get_min_dis_p2e(positions, g);  //    double F_p2e = min(pow(p2e, 2)/(k*k)*4, 1.0);
    double F_p2e = min(p2e, threshold)/threshold;
    
    double avg_dis = 0;
    double F_en = 1 - (double)get_num_repulsion(positions, g, &avg_dis) / gsize;
   
    double a = pow(avg_dis/threshold, 2);
    double b = min(get_min_avg_angle(positions, g), 60.0)/60.0; // pow(avgdis/threshold, 2);
    
//    printf("_avg_dis:%f  -  %f - %f gsize:%f\n", avg_dis, avg_dis/threshold, threshold, gsize);
   
    f = w1*F_angle + w2*F_p2p + w3*F_pn + w4*F_p2e + w5*F_en + w6*a + w7*b;
//    f = (F_angle + F_p2p + F_pn + F_p2e + F_en + pow(a,2) + pow(b,2))/7;
   
//    printf("\nEvaluatefunction2:\nF_angle %f\nF_p2p %f \nF_pn %f \nF_p2e %f \nF_en %f\navg_dis:  %f\navg_angle:  %f\nf:%f\n ", F_angle, F_p2p, F_pn, F_p2e, F_en,a,b,f);
    cout << "crossing angle: " << get_min_angle(positions, g) <<endl;
    cout << "avg angle: " << get_min_avg_angle(positions, g) <<endl;
    cout << "number p in e: " << get_num_repulsion(positions, g, &avg_dis) <<endl;
    cout << "min p2e: " << get_min_dis_p2e(positions, g) <<endl;
    cout << "avg p2e: " << avg_dis <<endl;
    
    cout << "f: " << f <<endl;
    return f;
}





double CheckRepulsiveRange(Point *p, Point *a, Point *b, double h) {
    double stright_dis = calStrightDis(p, a, b);
    if(stright_dis >= h || *a == *b) {
        return -1; // not in the range or point a and point b overlap
    }
    
    /* Form the repulsive range */
    
    // distance between a and b
    double d = sqrt(pow(b->y - a->y, 2) + pow(b->x - a->x, 2)); // distance between a and b
    
    // calculate Radius
    float R;
    
    if(fabs(d/2-h) <= 1e-6) {
        // when d/2 = h (circle)
        // the center is on the mid of ab
        double midx = (a->x + b->x)/2;
        double midy = (a->y + b->y)/2; // center
        
        if((p->x - midx)*(p->x - midx) + (p->y - midy)*(p->y -midy) < d*d/4) {
            // in the range
            return stright_dis;
        }
        else {
            return -1;
        }
    }
    else if(d/2 > h) {
        R = d*d/(8*h) + h/2;
        
        // calculate centers of 2 circles
        double x1 = a->x; double y1 = a->y; double x2 = b->x; double y2 = b->y;
        double c1 = 0, c2 = 0, A = 0, B = 0, C = 0, y01 = 0, x01 = 0, x02 = 0, y02 = 0;
        c1 = (pow(x2, 2) - pow(x1, 2) + pow(y2, 2) - pow(y1, 2)) / 2 /(x2 - x1);
        c2 = (y2 - y1) / (x2 - x1);
        A = 1.0 + pow(c2, 2);
        B = 2 * (x1 - c1) * c2 - 2 * y1;
        C = pow((x1 - c1), 2) + pow(y1, 2) - pow(R, 2);

        // center 1
        y01 = (-B + sqrt(B*B - 4 * A * C)) / 2 / A;
        x01 = c1 - c2 * y01;
        
        // center 2
        y02 = (-B - sqrt(B*B - 4 * A * C)) / 2 / A;
        x02 = c1 - c2 * y02;
//        cout << "Center 1: (" << x01 << ", " << y01 << ")" << endl;
//        cout << "Center 2: (" << x02 << ", " << y02 << ")" << endl;
        
        /* Check if the point is in two circles */
        double d1 = (p->x - x01)*(p->x - x01) + (p->y - y01)*(p->y - y01);
        double d2 = (p->x - x02)*(p->x - x02) + (p->y - y02)*(p->y - y02);
        
        if( d1<R*R && d2<R*R ) {
            // in the range
            return stright_dis;
        }
        else {
            // not in the range
            return -1;
        }
    }
    else {
        // when d/2 < h
        R = h*h/d + d/4;
        // calculate centers of 2 circles
        Point mid;
        mid.x = (a->x + b->x)/2;
        mid.y = (a->y + b->y)/2;
        
        Vector ab;
        ab.dx = b->x - a->x;
        ab.dy = b->y - a->y;
        double norm = ab.norm();
        ab.dx /= norm;
        ab.dy /= norm; // unit vector
        
        double y01 = 0, x01 = 0, x02 = 0, y02 = 0;
        // center 1
        y01 = mid.y + ab.dy * (R-d/2);
        x01 = mid.x + ab.dx * (R-d/2);
        
        // center 2
        y02 = mid.y - ab.dy * (R-d/2);
        x02 = mid.x - ab.dx * (R-d/2);
//        cout << "Center 1: (" << x01 << ", " << y01 << ")" << endl;
//        cout << "Center 2: (" << x02 << ", " << y02 << ")" << endl;
        
        /* Check if the point is in two circles */
        double d1 = (p->x - x01)*(p->x - x01) + (p->y - y01)*(p->y - y01);
        double d2 = (p->x - x02)*(p->x - x02) + (p->y - y02)*(p->y - y02);
        
        if( d1<R*R && d2<R*R ) {
            return stright_dis; // in the range
        }
        else {
            return -1; // not in the range
        }
    }
    return -1;  // cannot get here
}


double isPointInEdgeRange(Point *p, Point *a, Point *b, double range) {
    double vx = a->x - b->x;
    double vy = a->y - b->y;
    double norm = sqrt(vx*vx + vy*vy);
    // vector ab is (vx, vy), so the perpendicular vectors: (vy, -vx) (-vy, vx)
    
    Point A, B, C, D;
    A.x = a->x + vy/norm*range; A.y = a->y - vx/norm*range;
    B.x = a->x - vy/norm*range; B.y = a->y + vx/norm*range;
    C.x = b->x - vy/norm*range; C.y = b->y + vx/norm*range;
    D.x = b->x + vy/norm*range; D.y = b->y - vx/norm*range;
//    cout << A.x << B.x << C.x << D.x <<endl;
//    cout << calStrightDis(A.x, A.y, a->x, a->y, b->x, b->y) <<endl;

    float x = p->x;
    float y = p->y;
    float a1 = (B.x - A.x)*(y - A.y) - (B.y - A.y)*(x - A.x);
    float b1 = (C.x - B.x)*(y - B.y) - (C.y - B.y)*(x - B.x);
    float c1 = (D.x - C.x)*(y - C.y) - (D.y - C.y)*(x - C.x);
    float d1 = (A.x - D.x)*(y - D.y) - (A.y - D.y)*(x - D.x);
    if((a1 >= 0 && b1 >= 0 && c1 >= 0 && d1 >= 0) || (a1 <= 0 && b1 <= 0 && c1 <= 0 && d1 <= 0)) {
        return calStrightDis(p, a, b);
    }
    else
        return -1;  // not in range
}

void center_and_scale(Graph *g, unsigned int width, unsigned int height, vector<Point*> positions) {
    // find current dimensions
    double x_min = std::numeric_limits<double>::max();
    double x_max = std::numeric_limits<double>::lowest();
    double y_min = std::numeric_limits<double>::max();
    double y_max = std::numeric_limits<double>::lowest();

    for (int v_id = 0; v_id < g->getNumberOfVertices(); v_id++) {
        if (positions[v_id]->x < x_min) {
            x_min = positions[v_id]->x;
        }
        if (positions[v_id]->x > x_max) {
            x_max = positions[v_id]->x;
        }

        if (positions[v_id]->y < y_min) {
            y_min = positions[v_id]->y;
        }
        if (positions[v_id]->y > y_max) {
            y_max = positions[v_id]->y;
        }
    }

    double cur_width = x_max - x_min;
    double cur_height = y_max - y_min;
    
    if(cur_width != 0 && cur_height != 0) {
        // compute scale factor
        double x_scale = width / cur_width;
        double y_scale = height / cur_height;
        double scale = 1.0 * (x_scale < y_scale ? x_scale : y_scale);

        // compute offset and apply it to every position
        Point center;
        center.x = (x_max + x_min)/2;
        center.y = (y_max + y_min)/2;
        
//        double offset_x = center.x / 2.0 * scale;
//        double offset_y = center.y / 2.0 * scale;
        
        double offset_x = center.x * scale - 0.5;
        double offset_y = center.y * scale - 0.5;
        
        for (int v_id = 0; v_id < g->getNumberOfVertices(); v_id++) {
            positions[v_id]->x = positions[v_id]->x * scale - offset_x;
            positions[v_id]->y = positions[v_id]->y * scale - offset_y;
        }
    }
}

//void printAllpoints(vector<Point*> positions) {
////    for (int v_id = 0; v_id < g->getNumberOfVertices(); v_id++) {
////        printf("%d: (%f, %f)\n", positions[v_id]->x,  positions[v_id]->y);
////    }
//}
