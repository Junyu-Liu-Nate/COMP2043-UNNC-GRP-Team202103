//
//  GenerateGraph.cpp
//  forceModel
//
//  Created by 王丹匀 on 2020/4/25.
//  Copyright © 2020 王丹匀. All rights reserved.
//

#include "GenerateGraph.hpp"

// for doing experiements
void experiement1() {
    // this experiment is for the control experiment
    string filename = "./Graph_instance/My_dataset/Group1/test0.txt";
    run_graph_instance(filename, "./Graph_instance/My_dataset/Group1/test0_result.txt", "./Graph_instance/My_dataset/Group1/test0_graphviz.dot", "./Graph_instance/My_dataset/Group1/test0_graphviz.txt", "./Graph_instance/My_dataset/Group1/test0_graphviz.plain");
    
    // run all the cases in group 1 iteratively
    for(int i=1; i<10; i++) {
        ostringstream os, os1, os2, os3, os4;
        os << "./Graph_instance/My_dataset/Group1/test" << i << "0.txt";
        os1 << "./Graph_instance/My_dataset/Group1/test" << i << "0_result.txt";
        os2 << "./Graph_instance/My_dataset/Group1/test" << i << "0_graphviz.dot";
        os3 << "./Graph_instance/My_dataset/Group1/test" << i << "0_graphviz.txt";
        os4 << "./Graph_instance/My_dataset/Group1/test" << i << "0_graphviz.plain";
        filename = os.str();
        string output = os1.str();
        string dotfile = os2.str();
        string graphvizResult = os3.str();
        string graphvizInput = os4.str();
        run_graph_instance(filename, output, dotfile, graphvizResult, graphvizInput); // calculate the layout
    }
}

void experiement2() {
    // // this experiment is for the kn graph; n = 1,2,3...10 and 20, 30, 40, 50...100
    for(int i=3; i<=3; i++) {
        Graph* g = generate_Kn_graph(i*100);
        
        // intialise the positions
        int vsize = g->getNumberOfVertices();
        vector<Vertex*> vlist = g->getVertexList();
            

        /* ------------------------------------------------ */
        vector<Point*> drawing = initializeDrawing(g, 1);  // allocate memory
    
        // run my algorithm
        clock_t start_time=clock();
        LayoutAlgorithm fr(g); // run the algorithm
        fr.FR(drawing, 1000);
        clock_t end_time=clock();
        double runtime = (double)(end_time - start_time) / CLOCKS_PER_SEC; // the run time for the algorithm
        
        // evaluate the layout
        double angle = get_min_angle(drawing, g);
        double p2e = get_min_dis_p2e(drawing, g);
        double p2p = get_min_dis_p2p(drawing, g);
        double f = evaluate_drawing(drawing, g);
    
        ostringstream os, os1, os2, os3, os4;
        os << "./Graph_instance/My_dataset/Group2/k" << i << "00_graph_result.txt";
        os1 << "./Graph_instance/My_dataset/Group2/k" << i << "00_graph_graphviz.dot";
        os2 << "./Graph_instance/My_dataset/Group2/k" << i << "00_graph_graphviz.txt";
        os3 << "./Graph_instance/My_dataset/Group2/k" << i << "00_graph_graphviz.plain";
        string output = os.str();
        string dotfile = os1.str();
        string graphvizResult = os2.str();
        string graphvizInput = os3.str();
        
        // copy the positions to the graph instance
        for(int i=0; i<vsize; ++i) {
            vlist[i]->x = drawing[i]->x;
            vlist[i]->y = drawing[i]->y;
        }
        
        DSPInstanceReader a; a.graph = g;
        a.outputDSPInstance(g, output, angle, p2e, p2p, f, runtime); // ouput the result to txt file
        ouputDotFile(g, dotfile); // transfrom the graph to dot file
        
        for(int j=0; j<g->getNumberOfVertices();++j) {
            delete drawing[j];
        }
        /* ------------------------------------------------ */
    }

//        int k = 10;
//        int h = 4;
//    Graph g = generate_k_ary_tree(k, h);
}

void experiement3() {
    
}

void run_graph_instance(string filename, string output, string dotfile, string graphvizResult, string graphvizInput) {
    // read from files and get the graph
    DSPInstanceReader a;
    a.readDSPInstance(filename);
    Graph* g = a.graph;
    
    // intialise the positions
    int vsize = g->getNumberOfVertices();
    vector<Vertex*> vlist = g->getVertexList();
    
    
    /* ------------------------------------------------ */
//    vector<Point*> drawing = initializeDrawing(g, 1);  // allocate memory
//
//    // run my algorithm
//    clock_t start_time=clock();
//    LayoutAlgorithm fr(g); // run the algorithm
//    fr.FR(drawing, 1000);
//    clock_t end_time=clock();
//    double runtime = (double)(end_time - start_time) / CLOCKS_PER_SEC; // the run time for the algorithm
////    cout << "The run time is: " << runtime << "s" << endl;
//
//    // copy the positions to the graph instance
//    for(int i=0; i<vsize; ++i) {
//        vlist[i]->x = drawing[i]->x;
//        vlist[i]->y = drawing[i]->y;
//    }
//
//    // evaluate the layout
//    double angle = get_min_angle(drawing, g);
//    double p2e = get_min_dis_p2e(drawing, g);
//    double p2p = get_min_dis_p2p(drawing, g);
//    double f = evaluate_drawing(drawing, g);
//
//    // output the graph positions and other info
//    a.outputDSPInstance(g, output, angle, p2e, p2p, f, runtime); // ouput the result to txt file
//    ouputDotFile(g, dotfile); // transfrom the graph to dot file
    
     /* ------------------------------------------------ */
    
    /* Graphviz */
    vector<Point*> pos = readpPlainFile(g, graphvizInput);     // read plain file
    // copy the positions to the graph instance
    for(int i=0; i<vsize; ++i) {
        vlist[i]->x = pos[i]->x;
        vlist[i]->y = pos[i]->y;
    }
    // evaluate the layout
    double angle = get_min_angle(pos, g);
    double p2e = get_min_dis_p2e(pos, g);
    double p2p = get_min_dis_p2p(pos, g);
    double f = evaluate_drawing(pos, g);

    // output the graph positions and other info
    a.outputDSPInstance(g, graphvizResult, angle, p2e, p2p, f, -1); // ouput the result to txt file
    
    /* ------------------------------------------------ */
    // clear memory
    delete g;
    for(int i=0; i<vsize; ++i) {
//        delete drawing[i];
        delete pos[i];
    }
}


Graph* generate_Kn_graph(int n) {
    if(n >= 500) {
        cout << "The size should be less than 500." << endl;
        return NULL;
    }
    
    vector<Vertex *>  vertexs;
    Vertex* v;
    
    for( int i = 0; i < n; i++ ){
        char vertex_name[10];
        sprintf_s(vertex_name,"%d",i);
        
        v = new Vertex(vertex_name); // allocate new vertices
        v->vid = i;
        vertexs.push_back(v);
    }
    
    for( int i = 0; i < n; i++ ){
        for( int j = 0; j < n; j++ ){
            if(i != j) {
                vertexs[i]->addNeighbour(j); // Complete graph
            }
        }
    }
    
    Graph * graph = new Graph();
    graph->setVertexList(vertexs);
    graph->num_of_edges = n*(n-1)/2;
    return graph;
}


Graph* generate_k_ary_tree(int k, int h) {
    if(k<2 || k>10) {
        cout << "k should in range(2,10)." << endl;
    }
        
    int n = (pow(k, h)-1)/(k-1);
    cout << "The size of tree:" << n << "." << endl;
    
    vector<Vertex *> vertexs;
    Vertex* v;
    
    
    for( int i = 0; i < n; i++ ){
        char vertex_name[10];
        sprintf_s(vertex_name,"%d",i);
        
        v = new Vertex(vertex_name); // allocate new vertices
        v->vid = i;
        vertexs.push_back(v);
    }
    
    for( int i = 0; i < n; i++ ){
        if(i == (pow(k, h-1)-1)/(k-1) ) {
            break;  // leaf node
        }
        
        for( int j = 0; j < k; j++ ){
            vertexs[i]->addNeighbour(k*(i+1)-(k-2)+j-1);  // i starts from 0, where the id in trees starts from 1
        }
    }
    
    Graph * graph = new Graph();
    graph->setVertexList(vertexs);
    graph->num_of_edges = (graph->getNumberOfVertices()-pow(2, h-1))*k;
    return graph;
}

Graph* generate_grids(int w, int h) {
    if(w <= 0 || h <= 0) {
        cout << "The width and height should be greater than 0!" << endl;
        return NULL;
    }
    
    int n = w*h;
    
    vector<Vertex *> vertexs;
    Vertex* v;
    
    for( int i = 0; i < n; i++ ){
        char vertex_name[10];
        sprintf_s(vertex_name,"%d",i);
        
        v = new Vertex(vertex_name); // allocate new vertices
        v->vid = i;
        vertexs.push_back(v);
    }
    
    for( int i = 0; i < h; i++ ){
        for( int j = 0; j < w; j++ ){
            if(i != j) {
                vertexs[i]->addNeighbour(j); // Complete graph
            }
        }
    }
    
    Graph * graph = new Graph();
    graph->setVertexList(vertexs);
    return graph;
}

void ouputDotFile(Graph* g, string filename) {
    ofstream fileout;
    fileout.open(filename);
    if (!fileout) {
        cout << "Failed to create dot file." << endl;
        exit (0);
    }
    
    fileout << "strict graph {\n    splines=\"line\";\n    node [margin=0 shape=point style=filled];\n\n";
    
    for( int i = 0; i < g->getNumberOfVertices(); i++ ){
        fileout << "    " << i << " [label=\"n" << i <<"\"]\n";
//        printf("%d %d\n",g->getNumberOfVertices(), i);
    }

    // edges
    vector<Vertex *> vlist = g->getVertexList();
    const int size = g->getNumberOfVertices();
    //int sign[size][size];
    vector<int> w(size);  // 列数
    vector< vector<int> > sign(size, w);   //行数
    for( int i = 0; i < size; i++ ){
        for(int j = 0; j < size; j++) {
            sign[i][j] = 0; // initalize
        }
    }
     
    fileout << "\n";
    for( int i = 0; i < g->getNumberOfVertices(); i++ ){
        for(int j = 0; j < vlist[i]->getNumberOfNeighbour(); j++) {
            int j_id = vlist[i]->getNeighbour()[j];
            if(sign[i][j_id] == 0 && sign[j_id][i] == 0 ) {
                fileout << "    " << i << " -- " << vlist[i]->getNeighbour()[j] << "\n";
                sign[i][j_id] = 1;
                sign[j_id][i] = 1;
            }
        }
    }
    fileout << "}";
    fileout.close();
}

vector<Point*> readpPlainFile(Graph* g, string filename) {
    int vsize = g->getNumberOfVertices();
        
    // allocate memory and initialise
    vector<Point*> draw(vsize);
    for(int i=0; i<vsize; ++i) {
        draw[i] = new Point;
        draw[i]->x = 0;
        draw[i]->y = 0;
    }
    
    // read from file
    ifstream file;
    file.open(filename);
    if (!file) {
        cout << "Failed to open plain file" << endl;
        exit (0);
    }
    
    string temp;
    for(int i=0; i<vsize; ++i) {
        while(temp != "node") {
            file >> temp;
        }
        
        file >> temp; // the node id
        file >> draw[i]->x; // position
        file >> draw[i]->y;
    }
    file.close();
    
    center_and_scale(g, 1, 1, draw);
    return draw;
}

