//
//  main.hpp
//  example
//
//  Created by 王丹匀 on 2019/11/16.
//  Copyright © 2019 王丹匀. All rights reserved.
//
//  Edited by 王惟滨 尤程磊 楷哲韩 on 2021 summer
//

#ifndef main_hpp
#define main_hpp

#define GLUT_DISABLE_ATEXIT_HACK
#include <corecrt_math_defines.h>
#include <GL/glut.h>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include "Graph_instance/reader/DSPInstanceReader.hpp"
#include "GeometricFunctions.hpp"
#include "LayoutAlgorithm.hpp"
#include "GenerateGraph.hpp"
#include "LayoutOverlap.hpp"

#endif /* main_hpp */

using namespace std;

GLfloat Xplace;
GLfloat Yplace;
GLfloat keyboardMove;
GLfloat rotateMove;
GLfloat lableRotateMove;
GLfloat lableRotateTheta;
GLfloat rotateTheta;
GLfloat characterWidth;
GLfloat characterHeight;
GLfloat characterSpaceRate;
GLfloat coverInterval;
GLfloat coverWidth;
GLfloat scale;
GLfloat scaleSize;
GLfloat scaleMove;
int frameType;
int maxFrameType;

Graph *g;
vector<Point*> drawing;
vector<Point*> init_drawing;
vector<Point*> *curt_drawing;

void drawGraph(vector<Point*> positions, Graph *g);
void drawPoint(GLfloat x, GLfloat y, GLfloat size);
void drawRect(GLfloat x, GLfloat y);
void drawCircle(GLfloat x, GLfloat y, GLfloat l, GLfloat w);
void drawRectCover(GLfloat x, GLfloat y, GLfloat l, GLfloat w);
void drawCircleCover(GLfloat x, GLfloat y, GLfloat l, GLfloat w);
void draw_graph_algorithm();

void keyboard(unsigned char key, int x, int y);
void reshape(int w, int h);
void display(void);
void copyDrawing(vector<Point*> p, vector<Point*> des);
void printAllpoints(vector<Point*> positions);
