#ifndef LayoutOverlap_hpp
#define LayoutOverlap_hpp

#include <stdio.h>
#include <vector>
#include "geometricFunctions.hpp"
#include <corecrt_math_defines.h>

class LayoutOverlap {

public:
    LayoutOverlap(Graph* g, Vector center);
    void oneLiteralOverlap(vector<Point*> positions);

private:
    double characterWidth = 0.039; // average character width for the bit character in glut when grasph in original size
    double characterHeight = 0.04; // average character height for the bit character in glut when grasph in original size
    double characterSpaceRate = 0.6; // the rate of average character width and space width (1 space = 0.6 average character width)
    
    double centerX;
    double centerY;

    Graph* g;
    int vertexNum;
    vector<Vector> disp;
};

#endif

