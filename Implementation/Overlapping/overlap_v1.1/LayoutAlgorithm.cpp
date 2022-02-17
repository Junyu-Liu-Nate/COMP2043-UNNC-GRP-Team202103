//
//  fruchterman_reingold.cpp
//  forceModel
//
//  Created by 王丹匀 on 2020/3/8.
//  Copyright © 2020 王丹匀. All rights reserved.
//
//  Edited by 王惟滨 尤程磊 楷哲韩 on 2021 summer
//

#include "LayoutAlgorithm.hpp"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

vector<string> split(const string& str, const string& pattern)
{
    vector<string> ret;
    if(pattern.empty()) return ret;
    size_t start=0,index=str.find_first_of(pattern,0);
    while(index!=str.npos)
    {
        if(start!=index)
            ret.push_back(str.substr(start,index-start));
        start=index+1;
        index=str.find_first_of(pattern,start);
    }
    if(!str.substr(start).empty())
        ret.push_back(str.substr(start));
    return ret;
}


LayoutAlgorithm::LayoutAlgorithm(Graph *g)
    : g(g)
    , temp_(0.15) // 0.2*sqrt(g->getNumberOfVertices())
    , disp(g->getNumberOfVertices()) {
        k = 1*sqrt(1/(double)g->getNumberOfVertices());
        k_squared = k*k;
}


void LayoutAlgorithm::frOperator_(vector<Point*> positions, int s) {
    Vector zero; zero.dx = 0; zero.dy = 0;
    fill(disp.begin(), disp.end(), zero);  /* initialize displacement vector */
    
    int size = g->getNumberOfVertices();
    
    vector<Vertex *> vertices = g->getVertexList();

    // Repulsion force between vertice pairs
    for (int v_id = 0; v_id < size; v_id++) {
        string v_name = vertices.at(v_id)->getName();
        vector<string> v_nodes = split(v_name, " ");
        for (int other_id = v_id + 1; other_id < size; other_id++) {
            if (v_id == other_id) {
                continue;
            }
            
//            int sameNodesNumber = 0;
//
//            string other_name = vertices.at(other_id)->getName();
//            vector<string> other_nodes = split(other_name, " ");
//
//            for (int i = 0; i < v_nodes.size(); i++) {
//                for (int j = 0; j < other_nodes.size(); j++) {
//                    if (v_nodes.at(i) == other_nodes.at(j)) {
//                        sameNodesNumber++;
//                    }
//                }
//            }
            

            Vector delta;
            delta.dx = positions[v_id]->x - positions[other_id]->x;
            delta.dy = positions[v_id]->y - positions[other_id]->y;
            
            double distance = delta.norm();
            // TODO: handle distance == 0.0

            // > 1.0: not worth computing
            if (distance > 1.0) {
                continue;
            }

            double repulsion = k_squared * 10000 / distance;
//            if (sameNodesNumber != 0) {
//                disp[v_id].dx += delta.dx / (distance * sameNodesNumber * 10) * repulsion;
//                disp[v_id].dy += delta.dy / (distance * sameNodesNumber * 10) * repulsion;
//                disp[other_id].dx -= delta.dx / (distance * sameNodesNumber * 10) * repulsion;
//                disp[other_id].dy -= delta.dy / (distance * sameNodesNumber * 10) * repulsion;
//            }else {
//                disp[v_id].dx += delta.dx / distance * repulsion;
//                disp[v_id].dy += delta.dy / distance * repulsion;
//                disp[other_id].dx -= delta.dx / distance * repulsion;
//                disp[other_id].dy -= delta.dy / distance * repulsion;
//            }
            
            disp[v_id].dx += delta.dx / distance * repulsion;
            disp[v_id].dy += delta.dy / distance * repulsion;
            disp[other_id].dx -= delta.dx / distance * repulsion;
            disp[other_id].dy -= delta.dy / distance * repulsion;
        }

        // Attraction force between edges
        // for each neighbor of v_id
        Vertex *v = g->getVertexList().at(v_id);
        for (int i = 0; i < v->num_of_neighbour; i++) {
            int adj_id = v->getNeighbour().at(i);
            
            Vector delta;
            delta.dx = positions[v_id]->x - positions[adj_id]->x;
            delta.dy = positions[v_id]->y - positions[adj_id]->y;
            
            double distance = delta.norm();
            if (fabs(distance) < 1e-10) {
                continue;
            }

            double attraction = 1.0 * distance * distance / k;
            disp[v_id].dx -=  delta.dx / distance * attraction;
            disp[v_id].dy -= delta.dy / distance * attraction;
            disp[adj_id].dx += delta.dx / distance * attraction;
            disp[adj_id].dy += delta.dy / distance * attraction;
            
            if(s == 0)
                continue;
            
            // Edges Replusion
            for (int j = 0; j < size; j++) {
                if(j==v_id || j== adj_id) {
                    continue;
                }
                
                
                double l = sqrt(pow(positions[v_id]->x-positions[adj_id]->x, 2)+pow(positions[v_id]->y-positions[adj_id]->y, 2));
                double h = min(0.2, (l+k)/4);
                
                double d = CheckRepulsiveRange(positions[j], positions[v_id], positions[adj_id], h);
                if(d > 0) {
                    // in the range
                    //  GetFootOfPerpendicular
                    Point retVal;
                    if(fabs(delta.dx) < 1e-10 && fabs(delta.dy) < 1e-10 ) {
                        retVal.x = positions[i]->x; retVal.y = positions[i]->y;
                    }
                    double u = (positions[j]->x - positions[v_id]->x)*(positions[v_id]->x - positions[adj_id]->x) +
                    (positions[j]->y - positions[v_id]->y)*(positions[v_id]->y - positions[adj_id]->y);
                    
                    u = u/((delta.dx*delta.dx)+(delta.dy*delta.dy));
                    retVal.x = positions[v_id]->x + u*delta.dx;
                    retVal.y = positions[v_id]->y + u*delta.dy;
                    
                    // the vector from foot point to the vertex
                    double dx = (positions[j]->x - retVal.x)/d;
                    double dy = (positions[j]->y - retVal.y)/d;
                    
//                    float c1 = 20000;
//                    float c2 = 1e-10;
//                    double EdgeRepulsion = min(0.5, 1 /(c1*d*d + c2));
                    
//                    double EdgeRepulsion = min(h, (h-d));
//                    double EdgeRepulsion = 10000*(h-d)*(h-d);
//                    printf("d:%f %f %f %f\n", d, EdgeRepulsion, c1*d*d, c2);
////
//                    double EdgeRepulsion = min(0.5, 1/(d*d)*1e-3);
                    double EdgeRepulsion = 1/(d*d)*1e-3;
//                    if(d < 0.1)
//                        printf("edge rep: %f %f\n", EdgeRepulsion, 1/(d*d)*1e-3);
                    
                    disp[j].dx +=  dx * EdgeRepulsion;
                    disp[j].dy += dy * EdgeRepulsion;
                }
            }
        }
        
        //Attraction between supernodes have the same node
        for (int other_id = v_id + 1; other_id < size; other_id++) {
            if (other_id == v_id) {
                continue;
            }
            
            Vector delta;
            delta.dx = positions[v_id]->x - positions[other_id]->x;
            delta.dy = positions[v_id]->y - positions[other_id]->y;
            
            double distance = delta.norm();
            // TODO: handle distance == 0.0

            // > 1.0: not worth computing
            if (fabs(distance) < 1e-10) {
                cout << distance << endl;
                continue;
            }
            
            int sameNodesNumber = 0;
            string other_name = vertices.at(other_id)->getName();
            vector<string> other_nodes = split(other_name, " ");
            
            for (int i = 0; i < v_nodes.size(); i++) {
                for (int j = 0; j < other_nodes.size(); j++) {
                    if (v_nodes.at(i) == other_nodes.at(j)) {
                        sameNodesNumber++;
                    }
                }
            }
            
            double attraction = distance * distance / k;
            if (sameNodesNumber != 0) {
                attraction = sameNodesNumber * sameNodesNumber * 50 * distance * distance / k;
            }
            
            disp[v_id].dx -= delta.dx / distance * attraction;
            disp[v_id].dy -= delta.dy / distance * attraction;
            disp[other_id].dx += delta.dx / distance * attraction;
            disp[other_id].dy += delta.dy / distance * attraction;
            
            
        }
    }

    
    double energy = 0;
    // Max movement capped by current temperature
    for (int v_id = 0; v_id < size; v_id++) {
        double disp_norm = disp[v_id].norm();
        // too small, not worth computing
        if (disp_norm < 1e-10) {
            continue;
        }
        
        /* limit max displacement to frame; use temp. t to scale */
        positions[v_id]->x += disp[v_id].dx / disp_norm * min(disp_norm, temp_);
        positions[v_id]->y += disp[v_id].dy / disp_norm * min(disp_norm, temp_);
        
        energy += sqrt(pow(disp[v_id].dx,2) + pow(disp[v_id].dy, 2));
//        positions[v_id]->x = min(1.0, max(0.0, positions[v_id]->x));
//        positions[v_id]->y = min(1.0, max(0.0, positions[v_id]->y));
    }
     
    // Cool down fast until we reach 0.001, then stay at low temperature
    if (temp_ > 0.001) {
        temp_ *= 0.95;
    } else {
        temp_ = 0.001;
    }
}


void LayoutAlgorithm::FR(vector<Point*> positions, int iters_count) {
    for (int i = 0; i < iters_count; i++) {
        if(i < iters_count/2) { // iters_count
            frOperator_(positions, 0);
        }
        else {
            frOperator_(positions, 1);
        }
    }
    center_and_scale(g, 1, 1, positions);
}
