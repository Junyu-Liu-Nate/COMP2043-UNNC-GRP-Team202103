//
//  GenerateGraph.hpp
//  forceModel
//
//  Created by 王丹匀 on 2020/4/25.
//  Copyright © 2020 王丹匀. All rights reserved.
//

#ifndef GenerateGraph_hpp
#define GenerateGraph_hpp

#include <stdio.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <time.h> 
#include "Graph_instance/reader/DSPInstanceReader.hpp"
#include "geometricFunctions.hpp"
#include "LayoutAlgorithm.hpp"

using namespace std;

Graph* generate_Kn_graph(int n);
Graph* generate_k_ary_tree(int k, int h); // h is the level/height
Graph* generate_grids(int w, int h);

// graphviz related I/O
void ouputDotFile(Graph* g, string filename); // transform the graph to dot file
vector<Point*> readpPlainFile(Graph* g, string filename);  // the positions generate by graphviz
void run_graph_instance(string filename, string output, string dotfile, string graphvizResult, string graphvizInput); // run a graph and produce dot files
void printAllpoints(vector<Point*> positions);
// for doing experiments
void experiement1();
void experiement2();
void experiement3();


#endif /* GenerateGraph_hpp */
