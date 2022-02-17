#include "LayoutOverlap.hpp"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>

// Split the string literals with blank space
vector<string> splitStr(const string& str, const string& pattern)
{
    vector<string> ret;
    if (pattern.empty()) return ret;
    size_t start = 0, index = str.find_first_of(pattern, 0);
    while (index != str.npos)
    {
        if (start != index)
            ret.push_back(str.substr(start, index - start));
        start = index + 1;
        index = str.find_first_of(pattern, start);
    }
    if (!str.substr(start).empty())
        ret.push_back(str.substr(start));
    return ret;
}

// Constructer of class LayoutOverlap
LayoutOverlap::LayoutOverlap(Graph* g, Vector center)
    : g(g)
    , disp(g->getNumberOfVertices()) {
    vertexNum = g->getNumberOfVertices();
    centerX = center.dx;
    centerY = center.dy;
}

void LayoutOverlap::oneLiteralOverlap(vector<Point*> positions)
{
    /* initialize displacement vector */
    Vector zero; zero.dx = 0; zero.dy = 0;
    fill(disp.begin(), disp.end(), zero);  

    vector<Vertex*> vertices = g->getVertexList();

    double rotateRate = 360 / vertexNum;

    //
    cout << endl << "-----------------------------" << endl << "Start calculating positions:" << endl;
    //cout << "centerX: " << centerX << " cneterY: " << centerY << endl;
    //

    for (int vID = 0; vID < vertexNum; vID++) {
        Vertex* v = vertices.at(vID);

        string v_name = v->getName();
        vector<string> v_nodes = splitStr(v_name, " ");

        //double vertexLength = (v->getNameLength() * (1 - characterSpaceRate) + strlen(vertices[vID]->getName().c_str()) * characterSpaceRate) * characterWidth;
        //double vertexHeight = (v->getNameLength()  * (1 - characterSpaceRate) + strlen(vertices[vID]->getName().c_str()) * characterSpaceRate) * characterHeight;
        double vertexLength = (v->getNameLength() + strlen(vertices[vID]->getName().c_str()) * characterSpaceRate) * characterWidth;
        double vertexHeight = characterHeight * (1 + characterSpaceRate);
        // Debug code
        cout << "When calculating, the length is: " << vertexLength << "and the height is: " << vertexHeight << endl;
        //
        //double calLength = vertexLength / 2;
        double calLength = vertexLength / 2 - characterWidth * characterSpaceRate / 2;

        double rotateAngle = rotateRate * vID;

        // Calculation
        //double vertexCenterX = centerX + calLength * cos(rotateAngle / 180);
        double vertexCenterX = centerX + calLength * cos(rotateAngle * 2 * M_PI / 360);
        //double vertexCenterY = centerY + calLength * sin(rotateAngle / 180);
        double vertexCenterY = centerY + calLength * sin(rotateAngle * 2 * M_PI / 360);
        //disp[vID].dx = vertexCenterX + (vertexHeight / 2) * sin(rotateAngle / 180);
        //disp[vID].dy = vertexCenterY - (vertexHeight / 2) * cos(rotateAngle / 180);

        //positions[vID]->x = disp[vID].dx;
        //positions[vID]->x = vertexCenterX + (vertexHeight / 2) * sin(rotateAngle / 180);
        positions[vID]->x = vertexCenterX + (vertexHeight / 2) * sin(rotateAngle * 2 * M_PI / 360);
        //positions[vID]->y = disp[vID].dy;
        //positions[vID]->y = vertexCenterY - (vertexHeight / 2) * cos(rotateAngle / 180);
        positions[vID]->y = vertexCenterY - (vertexHeight / 2) * cos(rotateAngle * 2 * M_PI / 360);

        //
        cout << "The center position for vertex " << vID << " is ( " << positions[vID]->x << ", " << positions[vID]->y << " )" << endl;
        //
    }

    //
    cout << "End calculating positions" << endl << "-----------------------------" << endl;
    //
}