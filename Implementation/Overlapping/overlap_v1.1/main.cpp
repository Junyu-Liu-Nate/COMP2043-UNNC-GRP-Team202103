//
//  main.cpp
//  forceModel
//
//  Created by 王丹匀 on 2019/11/16.
//  Copyright © 2019 王丹匀. All rights reserved.
//
//  Edited by 王惟滨 尤程磊 楷哲韩 on 2021 summer
//  Edited by Junyu Liu on GRP project in 2021-2022 academic year
//

#include "main.hpp"

// Initialize basic settings for drawing
void init() {
    // load graph instance
    DSPInstanceReader a;
    a.readDSPInstance("overlap1.txt");
    g = a.graph;

    // allocate memory
    drawing = initializeDrawing(g, 1);
    curt_drawing = &init_drawing;
    init_drawing = initializeDrawing(g, 1);
    copyDrawing(init_drawing, drawing);

    // set showing parameters
    scale = g->getNumberOfVertices() / 100 + 2;//graph scale size
    scaleSize = 2;//counter for graph scale size
    scaleMove = 0.05; // step size of graph scale
    Xplace = 1; // current X position
    Yplace = 1; // current Y position
    keyboardMove = 0.1; // step size of X/Y position moving
    rotateMove = 3; // step size of whole graph rotating
    rotateTheta = 0; // current rotating angle for whole graph
    frameType = 0; // current lable frame type number
    maxFrameType = 2; // max lable frame type number (now for rectangular & circle)
    characterWidth = 0.039; // average character width for the bit character in glut when grasph in original size
    characterHeight = 0.04; // average character height for the bit character in glut when grasph in original size
    characterSpaceRate = 0.6; // the rate of average character width and space width (1 space = 0.6 average character width)
    coverInterval = 0.01; // the interval between each stripe on cover layer
    coverWidth = 0.003; // the stripe width on cover layer
    lableRotateMove = 3; // step size of lable rotating
    lableRotateTheta = 0; // current rotating angle for all lable

    glClearColor(1.f, 1.f, 1.f, 1.f); // set white as background
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_DITHER);
    glShadeModel(GL_SMOOTH);
    glEnable(GL_POINT_SMOOTH);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

int main(int argc,char* argv[])
{
    glutInit(&argc,argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(600,600);
    glutCreateWindow("Drawing graph");
       init();
    glutDisplayFunc(display);
       draw_graph_algorithm();
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutMainLoop();
}

// Call LayoutAlgorithm methods and evaluate the runtime for the algorithm
void draw_graph_algorithm() {
    // calculate positions
    clock_t start_time = clock();

    //LayoutAlgorithm fr(g);
    //fr.FR(drawing, 100);

    // Layout of a group of overlapped supernodes
    Vector initialCenter;
    initialCenter.dx = 0.5;
    initialCenter.dy = 0.5;
    LayoutOverlap layoutOverlap(g, initialCenter);
    layoutOverlap.oneLiteralOverlap(drawing);

    clock_t end_time = clock();
    double runtime = (double)(end_time - start_time) / CLOCKS_PER_SEC; // the run time for the algorithm
    cout << "time: " << runtime << endl;

    printf("evaluate_drawing:%f\n", evaluate_drawing(drawing, g));
}

// call the drawGraph method to display the graph
void display(void) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    glPushMatrix();
    glTranslatef(-Xplace, -Yplace, 0);
    glScalef(scale, scale, 1);
    
    // draw
    drawGraph(*curt_drawing, g);
    
    glPopMatrix();
    glutSwapBuffers();
}

//---------------------------------------------//    ||
// x for x position of node                    //    ||
// y for y position of node                    //    ||
// size for size of point                      //    ||
// l for length of node name when horizontal   //    ||
// a for altitude of node name when vertical   //   _||_
// lableRotateTheta for rotate theta of lable  //  \ || /
// name for node name                          //   \||/
//---------------------------------------------//    \/

void drawPoint(GLfloat x, GLfloat y, GLfloat size){
    int rectEdge = 80;

    glBegin(GL_POLYGON);
    glColor3f(0.f, 0.f, 0.f);
    for (int i = 0; i < rectEdge; i++) {
        glVertex2f(x + size * cos(2 * M_PI * i / rectEdge), y + size * sin(2 * M_PI * i / rectEdge));
    }
    glEnd();
    glFlush();
}

void drawRect(GLfloat x, GLfloat y, GLfloat l, GLfloat a, GLfloat lableRotateTheta) {
    GLfloat w = characterWidth;
    GLfloat h = characterHeight;
    y = y - w / 2;
//    y -= 0.0025;
//    x -= 0.002;

    GLfloat x1, y1, x2, y2;

    if (abs(lableRotateTheta) <= 45) {
        l = l / cos(lableRotateTheta * 2 * M_PI / 360) + abs(h * tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * h;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * h;
    }
    else {
        a = - a / sin(lableRotateTheta * 2 * M_PI / 360) + abs(w / tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * w;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * w;
    }

    // draw background
    glBegin(GL_POLYGON);
    glColor4f(0.f, 0.75f, 0.75f, 0.5);
    glVertex2f(x - x1, y - y1);
    glVertex2f(x + x1, y + y1);
    glVertex2f(x + x1 - x2, y + y1 + y2);
    glVertex2f(x - x1 - x2, y - y1 + y2);
    glEnd();
    glFlush();
}

void drawRectCover(GLfloat x, GLfloat y, GLfloat l, GLfloat a, GLfloat lableRotateTheta) {
    GLfloat w = characterWidth;
    GLfloat h = characterHeight;
    y = y - w / 2;
//    y -= 0.0025;
//    x -= 0.002;

    GLfloat x1, y1, x2, y2;

    if (abs(lableRotateTheta) <= 45) {
        l = l / cos(lableRotateTheta * 2 * M_PI / 360) + abs(h * tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * h;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * h;
    }
    else {
        a = - a / sin(lableRotateTheta * 2 * M_PI / 360) + abs(w / tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * w;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * w;
    }

    // draw frame
    glBegin(GL_LINES);
    glColor3f(0.f, 0.f, 0.f);
    glVertex2f(x - x1, y - y1);
    glVertex2f(x + x1, y + y1);
    glVertex2f(x + x1, y + y1);
    glVertex2f(x + x1 - x2, y + y1 + y2);
    glVertex2f(x + x1 - x2, y + y1 + y2);
    glVertex2f(x - x1 - x2, y - y1 + y2);
    glVertex2f(x - x1 - x2, y - y1 + y2);
    glVertex2f(x - x1, y - y1);
    glEnd();

    // draw cover
    glColor4f(0.f, 0.75f, 0.75f, 0.5);
    for (GLfloat i = max(x - x1, x - x1 -x2); i < min(x + x1, x + x1 - x2); i += coverInterval) {
        glBegin(GL_POLYGON);
        glVertex2f(i, max((i - x) * y1 / x1 + y, (i + coverWidth - x) * y1 / x1 + y));
        glVertex2f(min(i + coverWidth, min(x + x1, x + x1 - x2)), max((i - x) * y1 / x1 + y, (i + coverWidth - x) * y1 / x1 + y));
        glVertex2f(min(i + coverWidth, min(x + x1, x + x1 - x2)), min((i - x) * y1 / x1 + y, (i + coverWidth - x) * y1 / x1 + y) + w / cos(lableRotateTheta * 2 * M_PI / 360));
        glVertex2f(i, min((i - x) * y1 / x1 + y, (i + coverWidth - x) * y1 / x1 + y) + w / cos(lableRotateTheta * 2 * M_PI / 360));
        glEnd();
    }
    for (GLfloat i = max(y - y1, y - y1 + y2); i < min(y + y1, y + y1 + y2); i += coverInterval) {
        glBegin(GL_POLYGON);
        glVertex2f(max((i - y) * x1 / y1 + x, (i + coverWidth - y) * x1 / y1 + x), i);
        glVertex2f(min((i - y) * x1 / y1 + x, (i + coverWidth - y) * x1 / y1 + x) - w / sin(lableRotateTheta * 2 * M_PI / 360), i);
        glVertex2f(min((i - y) * x1 / y1 + x, (i + coverWidth - y) * x1 / y1 + x) - w / sin(lableRotateTheta * 2 * M_PI / 360), min(i + coverWidth, min(y + y1, y + y1 + y2)));
        glVertex2f(max((i - y) * x1 / y1 + x, (i + coverWidth - y) * x1 / y1 + x), min(i + coverWidth, min(y + y1, y + y1 + y2)));
        glEnd();
    }
    for (GLfloat i = min(y - y1, y - y1 + y2); i > max(y + y1, y + y1 + y2); i -= coverInterval) {
        glBegin(GL_POLYGON);
        glVertex2f(max((i - y) * x1 / y1 + x, (i - coverWidth - y) * x1 / y1 + x), i);
        glVertex2f(min((i - y) * x1 / y1 + x, (i - coverWidth - y) * x1 / y1 + x) - w / sin(lableRotateTheta * 2 * M_PI / 360), i);
        glVertex2f(min((i - y) * x1 / y1 + x, (i - coverWidth - y) * x1 / y1 + x) - w / sin(lableRotateTheta * 2 * M_PI / 360), max(i - coverWidth, max(y + y1, y + y1 + y2)));
        glVertex2f(max((i - y) * x1 / y1 + x, (i - coverWidth - y) * x1 / y1 + x), max(i - coverWidth, max(y + y1, y + y1 + y2)));
        glEnd();
    }
    glFlush();
}

void drawCircle(GLfloat x, GLfloat y, GLfloat l, GLfloat a, GLfloat lableRotateTheta) {
    int rectEdge = 80;
    GLfloat w = characterWidth;
    GLfloat h = characterHeight;
    GLfloat R;

    if (abs(lableRotateTheta) <= 45) {
        l = l / cos(lableRotateTheta * 2 * M_PI / 360);
        R = sqrt(l * l + h * h) / 2;
    }
    else {
        a = - a / sin(lableRotateTheta * 2 * M_PI / 360);
        R = sqrt(a * a + w * w) / 2;
    }

    // draw background
    glBegin(GL_POLYGON);
    glColor4f(0.f, 0.75f, 0.75f, 0.5);
    for (int i = 0; i < rectEdge; i++) {
        glVertex2f(x + R * cos(2 * M_PI * i / rectEdge), y + R * sin(2 * M_PI * i / rectEdge));
    }
    glEnd();
    glFlush();
}

void drawCircleCover(GLfloat x, GLfloat y, GLfloat l, GLfloat a, GLfloat lableRotateTheta) {
    int rectEdge = 80;
    GLfloat w = characterWidth;
    GLfloat h = characterHeight;
    GLfloat R;

    if (abs(lableRotateTheta) <= 45) {
        l = l / cos(lableRotateTheta * 2 * M_PI / 360);
        R = sqrt(l * l + h * h) / 2;
    }
    else {
        a = - a / sin(lableRotateTheta * 2 * M_PI / 360);
        R = sqrt(a * a + w * w) / 2;
    }

    // draw frame
    glBegin(GL_LINE_LOOP);
    glColor3f(0.f, 0.f, 0.f);
    for (int i = 0; i < rectEdge; i++) {
        glVertex2f(x + R * cos(2 * M_PI * i / rectEdge), y + R * sin(2 * M_PI * i / rectEdge));
    }
    glVertex2f(x + R * cos(2 * M_PI * 0 / rectEdge), y + R * sin(2 * M_PI * 0 / rectEdge));
    glEnd();

    // draw cover
    glColor4f(0.f, 0.75f, 0.75f, 0.5);
    for (GLfloat i = x - R; i < x + R; i += coverInterval) {
        glBegin(GL_POLYGON);
        glVertex2f(i, y - min(sqrt(R * R - (x - i) * (x - i)), sqrt(R * R - (x - i - coverWidth) * (x - i - coverWidth))));
        glVertex2f(min(i + coverWidth, x + R), y - min(sqrt(R * R - (x - i) * (x - i)), sqrt(R * R - (x - i - coverWidth) * (x - i - coverWidth))));
        glVertex2f(min(i + coverWidth, x + R), y + min(sqrt(R * R - (x - i) * (x - i)), sqrt(R * R - (x - i - coverWidth) * (x - i - coverWidth))));
        glVertex2f(i, y + min(sqrt(R * R - (x - i) * (x - i)), sqrt(R * R - (x - i - coverWidth) * (x - i - coverWidth))));
        glEnd();
    }
    for (GLfloat i = y - R; i < y + R; i += coverInterval) {
        glBegin(GL_POLYGON);
        glVertex2f(x - min(sqrt(R * R - (y - i) * (y - i)), sqrt(R * R - (y - i - coverWidth) * (y - i - coverWidth))), i);
        glVertex2f(x + min(sqrt(R * R - (y - i) * (y - i)), sqrt(R * R - (y - i - coverWidth) * (y - i - coverWidth))), i);
        glVertex2f(x + min(sqrt(R * R - (y - i) * (y - i)), sqrt(R * R - (y - i - coverWidth) * (y - i - coverWidth))), min(i + coverWidth, y + R));
        glVertex2f(x - min(sqrt(R * R - (y - i) * (y - i)), sqrt(R * R - (y - i - coverWidth) * (y - i - coverWidth))), min(i + coverWidth, y + R));
        glEnd();
    }
    glFlush();
}

void drawLabel(GLfloat x, GLfloat y, GLfloat l, GLfloat a, string name, GLfloat lableRotateTheta) {
    GLfloat w = characterWidth;
    GLfloat h = characterHeight;
    y = y - w / 2;
    x = x + 0.005;
//    y -= 0.0025;
//    x -= 0.002;
    GLfloat x1, y1, x2, y2;

    if (abs(lableRotateTheta) <= 45) {
        l = l / cos(lableRotateTheta * 2 * M_PI / 360) + abs(h * tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * l / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * h;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * h;

        char nameArray[100] = { 0 };
        GLfloat tempX = 0;
        strcpy_s(nameArray, name.c_str());
        glColor3f(0, 0, 0);
        for (int i = 0; i < strlen(nameArray); i++) {
            glRasterPos2f(max(- x1, - x1 - x2) + tempX + x, (max(- x1, - x1 - x2) + tempX) * y1 / x1 + y);
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, nameArray[i]);
            if (nameArray[i] == ' ') {
                tempX += characterWidth * characterSpaceRate;
            }
            else {
                tempX += characterWidth;
            }
        }
        glFlush();
    }
    else {
        a = - a / sin(lableRotateTheta * 2 * M_PI / 360) + abs(w / tan(lableRotateTheta * 2 * M_PI / 360));
        x1 = cos(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        y1 = sin(lableRotateTheta * 2 * M_PI / 360) * a / 2;
        x2 = sin(lableRotateTheta * 2 * M_PI / 360) * w;
        y2 = cos(lableRotateTheta * 2 * M_PI / 360) * w;

        char nameArray[100] = { 0 };
        GLfloat tempY = -0.037;
        strcpy_s(nameArray, name.c_str());
        glColor3f(0, 0, 0);
        for (int i = 0; i < strlen(nameArray); i++) {
            glRasterPos2f((- min(y1, y1 + y2) + tempY) * x1 / y1 + x, - min(y1, y1 + y2) + tempY + y);
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, nameArray[i]);
            if (nameArray[i] == ' ') {
                tempY -= characterHeight * characterSpaceRate;
            }
            else {
                tempY -= characterHeight;
            }
        }
        glFlush();
    }
}

void drawGraph(vector<Point*> position, Graph *g){
    int vsize = g->getNumberOfVertices();
    vector<Vertex *> vertices = g->getVertexList();

    double rotateRate = 360 / vsize; // Calculate the rotate rate

    // Debug code
    cout << endl << "-----------------------------" << endl << "Start drawing:" << endl;
    //

    // draw: lable frame, lable cover, lable name, point(dot)
    // for cover: use a cover layer to make inevitable lable or edge overlay display clearer
    //rotateTheta = 0;
    lableRotateTheta = 0;
    for (int i = 0; i < vsize; i++) {
        Vertex* v = g->getVertexList().at(i);
        GLfloat tempX = position[i]->x;
        GLfloat tempY = position[i]->y;
        //GLfloat tempR = sqrt((tempX - 0.5) * (tempX - 0.5) + (tempY - 0.5) * (tempY - 0.5));
        //GLfloat tempT = asin((tempY - 0.5) / tempR);
        GLfloat nameLength = (v->getNameLength() * (1 - characterSpaceRate) + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterWidth; 
        GLfloat nameHeight = (v->getNameLength() * (1 - characterSpaceRate) + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterHeight;
        //GLfloat nameLength = (v->getNameLength() + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterWidth;
        //GLfloat nameHeight = characterHeight * (1 + characterSpaceRate);

        // Debug code
        // cout << "When drawing, the length is: " << nameLength << "and the height is: " << nameHeight << endl;
        //

        //rotateTheta = rotateRate * i;
        /*if (tempX > 0.5) {
            tempT = (rotateTheta / 360 * 2 * M_PI) - tempT;
        }
        else {
            tempT = ((rotateTheta - 180) / 360 * 2 * M_PI) + tempT;
        }*/
        //tempX = 0.5 + tempR * cos(tempT);
        //tempY = 0.5 + tempR * sin(tempT);
        
        lableRotateTheta = rotateRate * i;
        if (lableRotateTheta > 90) {
            if (lableRotateTheta <= 270) {
                // resort
                lableRotateTheta = lableRotateTheta - 180;
            }
            /*if ((lableRotateTheta > 180) && (lableRotateTheta <= 270)) {
                // resort
                lableRotateTheta = lableRotateTheta - 180;
            }*/
            if (lableRotateTheta > 270) {
                lableRotateTheta = lableRotateTheta - 360;
            }
            cout << "lableRotateTheta is " << lableRotateTheta << endl;
        }

        // Debug code
        cout << "The center position for vertex " << i << " is ( " << tempX << ", " << tempY << " )" << endl;
        //
        switch (frameType) {
        case 0:
            drawLabel(tempX, tempY + characterHeight / 2 + 0.005, nameLength, nameHeight, vertices[i]->getName(), lableRotateTheta);
            drawPoint(tempX, tempY, 0.003);
            drawRectCover(tempX, tempY + 0.02, nameLength, nameHeight, lableRotateTheta);
            break;
        case 1:
            drawLabel(tempX, tempY + characterHeight / 2 + 0.005, nameLength, nameHeight, vertices[i]->getName(), 0);
            drawPoint(tempX, tempY, 0.003);
            drawCircleCover(tempX, tempY + 0.02, nameLength, nameHeight, 0);
            break;
        default:
            break;
        }
    }

    // draw: edges
    for (int i = 0; i < vsize; i++) {
        Vertex* v = g->getVertexList().at(i);
        long nsize = v->getNeighbour().size();

        for (int j = 0; j < nsize; j++) {
            int neibor = v->getNeighbour().at(j);

            GLfloat tempXf = position[i]->x;
            GLfloat tempYf = position[i]->y;
            //GLfloat tempRf = sqrt((tempXf - 0.5) * (tempXf - 0.5) + (tempYf - 0.5) * (tempYf - 0.5));
            //GLfloat tempTf = asin((tempYf - 0.5) / tempRf);
            GLfloat tempXt = position[neibor]->x;
            GLfloat tempYt = position[neibor]->y;
            //GLfloat tempRt = sqrt((tempXt - 0.5) * (tempXt - 0.5) + (tempYt - 0.5) * (tempYt - 0.5));
            //GLfloat tempTt = asin((tempYt - 0.5) / tempRt);

            /*if (tempXf > 0.5) {
                tempTf = (rotateTheta / 360 * 2 * M_PI) - tempTf;
            }
            else {
                tempTf = ((rotateTheta - 180) / 360 * 2 * M_PI) + tempTf;
            }*/
            //tempXf = 0.5 + tempRf * cos(tempTf);
            //tempYf = 0.5 + tempRf * sin(tempTf);

            /*if (tempXt > 0.5) {
                tempTt = (rotateTheta / 360 * 2 * M_PI) - tempTt;
            }
            else {
                tempTt = ((rotateTheta - 180) / 360 * 2 * M_PI) + tempTt;
            }*/
            //tempXt = 0.5 + tempRt * cos(tempTt);
            //tempYt = 0.5 + tempRt * sin(tempTt);

            glBegin(GL_LINES);
            glColor3f(0.f, 0.f, 0.f);
            glVertex2f(tempXf, tempYf);
            glVertex2f(tempXt, tempYt);
            glEnd();
        }
    }

    // draw: lable background
    //rotateTheta = 0;
    lableRotateTheta = 0;
    for(int i=0;i<vsize;i++){
        Vertex *v = g->getVertexList().at(i);
        GLfloat tempX = position[i]->x;
        GLfloat tempY = position[i]->y;
        //GLfloat tempR = sqrt((tempX - 0.5) * (tempX - 0.5) + (tempY - 0.5) * (tempY - 0.5));
        //GLfloat tempT = asin((tempY - 0.5) / tempR);
        GLfloat nameLength = (v->getNameLength() * (1 - characterSpaceRate) + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterWidth;
        GLfloat nameHeight = (v->getNameLength() * (1 - characterSpaceRate) + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterHeight;
        //GLfloat nameLength = (v->getNameLength() + strlen(vertices[i]->getName().c_str()) * characterSpaceRate) * characterWidth;
        //GLfloat nameHeight = characterHeight * (1 + characterSpaceRate);

        //rotateTheta = rotateRate * i;
        /*if (tempX > 0.5) {
            tempT = (rotateTheta / 360 * 2 * M_PI) - tempT;
        }
        else {
            tempT = (( rotateTheta - 180) / 360 * 2 * M_PI) + tempT;
        }*/
        //tempX = 0.5 + tempR * cos(tempT);
        //tempY = 0.5 + tempR * sin(tempT);

        lableRotateTheta = rotateRate * i;
        if (lableRotateTheta > 90) {
            if (lableRotateTheta <= 270) {
                // resort
                lableRotateTheta = lableRotateTheta - 180;
            }
            /*if ((lableRotateTheta > 180) && (lableRotateTheta <= 270)) {
                // resort
                lableRotateTheta = lableRotateTheta - 180;
            }*/
            if (lableRotateTheta > 270) {
                lableRotateTheta = lableRotateTheta - 360;
            }
        }
        switch (frameType) {
        case 0:
            drawRect(tempX, tempY + 0.02, nameLength, nameHeight, lableRotateTheta);
            break;
        case 1:
            drawCircle(tempX, tempY + 0.02, nameLength, nameHeight, 0);
            break;
        default:
            break;
        }
    }

    //
    cout << "End drawing" << endl << "-----------------------------" << endl;
    //
}

void reshape(int w, int h) {
    GLfloat aspect = (GLfloat)w / (GLfloat)h;
    GLfloat nRange = 2.0f;
    glViewport(0,0,w,h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if (w<=h)
    {  glOrtho(-nRange, nRange, -nRange * aspect, nRange * aspect, -nRange, nRange);  }
    else
    {  glOrtho(-nRange, nRange, -nRange / aspect, nRange / aspect, -nRange, nRange);  }
}

void keyboard(unsigned char key, int x, int y) {
    switch (key) {
        case 'w':
            Yplace += keyboardMove;
            glutPostRedisplay();
            break;
        case 's':
            Yplace -= keyboardMove;
            glutPostRedisplay();
            break;
        case 'a':
            Xplace -= keyboardMove;
            glutPostRedisplay();
            break;
        case 'd':
            Xplace += keyboardMove;
            glutPostRedisplay();
            break;
        case 'j':
            scale += scaleMove;
            scaleSize += scaleMove;
            glutPostRedisplay();
            break;
        case 'k':
            if (scaleSize > 0) {
                scale -= scaleMove;
                scaleSize -= scaleMove;
            }
            glutPostRedisplay();
            break;
        case 'n':
            if(curt_drawing == &drawing)
                curt_drawing = &init_drawing;
            else
                curt_drawing = &drawing;
            glutPostRedisplay();
            break;
        case 'q':
            rotateTheta += rotateMove;
/*          Wasted plan (rotate full graph, but bit character in glut won't rotate)
            Xplace += 2*sqrt(2) * sin((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            Yplace -= 2*sqrt(2) * cos((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            rotateTheta += rotateMove;
            Xplace -= 2*sqrt(2) * sin((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            Yplace += 2*sqrt(2) * cos((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
*/
            glutPostRedisplay();
            break;
        case 'e':
            rotateTheta -= rotateMove;
/*          Wasted plan (rotate full graph, but bit character in glut won't rotate)
            Xplace += 2*sqrt(2) * sin((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            Yplace -= 2*sqrt(2) * cos((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            rotateTheta -= rotateMove;
            Xplace -= 2*sqrt(2) * sin((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
            Yplace += 2*sqrt(2) * cos((45 + rotateTheta/2) * M_PI / 180) * sin((rotateTheta / 2) * M_PI / 180);
*/
            glutPostRedisplay();
            break;
        case 'z':
            lableRotateTheta += lableRotateMove;
            if (lableRotateTheta > 0) {
                lableRotateTheta = 0;
            }
            glutPostRedisplay();
            break;
        case 'c':
            lableRotateTheta -= lableRotateMove;
            if (lableRotateTheta < -90) {
                lableRotateTheta = -90;
            }
            glutPostRedisplay();
            break;
        case 't':
            frameType = (frameType + 1) % maxFrameType;
            glutPostRedisplay();
            break;
        case 27:
            exit(0);
        default:
            break;
    }
}

void copyDrawing(vector<Point*> p, vector<Point*> des) {
    for(int i=0; i<p.size();i++) {
        p[i]->x = des[i]->x;
        p[i]->y = des[i]->y;
    }
}