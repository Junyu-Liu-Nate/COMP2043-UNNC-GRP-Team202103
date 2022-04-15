# Test

The test is divided into two parts: Interface testing and visualisation testing. 

## Attention
Windows system only.  

Because our algorithm has a certain amount of computation so there may be some slow responses when using PC with low-level processor.

- And out test PC is Dell- inspiration 7590 and the processor is Intel(R) Core(TM) i7-7590H. There are some slow responses when test.




## Interface testing
Interface testing is the process to check whether all the clicks will have the correct related response to the next.




## Visualisation testing
The visualisation can be divided into three categories: diagram with no overlapping nodes, diagram with overlapping on single letter node and diagram with overlapping on multiple letters. And the input files are provided in the directory 'inputFiles' and the results are shown in the directory 'outputDiagrams' . 

### 1. Test no overlapping nodes
We test this part with this procedure.
- Single node.
- Single node with subscripts after different letters.
- Multiple nodes.
- Multiple nodes with subscripts after different letters.
- Multiple nodes.
- Multiple nodes with edges.
- Multiple nodes with subscripts after different letters and edges.

###  2. Test nodes with overlaps on single letter
- One overlap on single letter with several nodes.
- One overlap on single letter with several nodes and number subscript.
- One overlap on single letter with several nodes, number subscript and edges.
- Multiple overlaps on single letter with several nodes, number subscripts and edges.
- Multiple overlaps on single letter with several nodes, number subscript and edges. And plus some nodes with no overlaps but number subscripts and edges.

### 3. Test nodes with overlaps on multiple letters
- One overlap on multiple letters with several nodes.
- One overlap on multiple letter with several nodes and number subscript.
- One overlap on multiple letters with several nodes, number subscript and edges.
- Multiple overlaps on multiple letters with several nodes, number subscripts and edges.
- Multiple overlaps on multiple letters with several nodes, number subscript and edges. And plus some nodes with no overlaps but number subscripts and edges.
