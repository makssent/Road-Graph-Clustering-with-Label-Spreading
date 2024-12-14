## Road graph clustering using Label Spreading method

## Table of Contents
- [Introduction](#introduction)
- [Description of the algorithm](#description-of-the-algorithm)
- [Usage](#usage)
  - [Step 1: Configuring a city](#step-1-configuring-a-city)
  - [Step 2: Start the project](#step-2-start-the-project)
  - [Step 3: Select the operation mode](#step-3-select-the-operation-mode)
- [Features](#features)
- [Examples](#examples)

## Introduction

This project deals with the application of the Label Spreading algorithm to divide a city into separate neighborhoods based on a road graph. The implementation of the algorithm is done without using a ready-made library, relying on the description of the approach presented in the article from Ozon on Hubra: [How algorithms on graphs help to gather groups](https://habr.com/ru/companies/ozontech/articles/791684/)

## Description of the algorithm
The algorithm takes initial data about some nodes in the graph with predetermined labels (i.e., these nodes belong to certain classes) and seeks to propagate this information to all other nodes. To do this, it:

- Forms an adjacency matrix from the graph structure, reflecting the relationships between the nodes.             
```Python.
A = nx.adjacency_matrix(G).todense() 
```
- The degree of each node (the number of edges associated with it) is then computed:
```Python
d = np.array(A.sum(axis=1)).flatten()
```
- Based on the degrees of the nodes, a diagonal matrix is created for normalization:
```Python
D = np.diagflat(1 / np.sqrt(d))
```
- Finally, the adjacency matrix is normalized with respect to the degrees of the nodes, forming the similarity matrix S:
``` Python
S = D @ A @ D # @ @ - matrix multiplication
```
- Initialization of the initial label matrix Y0:
```Python
Y0 = np.zeros((len(G.nodes), 2))
Y0[node_to_index[fixed_labels[0]], 0] = 1
Y0[node_to_index[fixed_labels[1]], 1] = 1 
```
Here Y0 is a matrix of size (number_of_nodes x 2), where 2 corresponds to the number of classes. The example denotes two nodes with known labels: one is assigned a class 0 label, the other a class 1 label. The other nodes initially have no labels (zeros).

- We copy the initial labels into a Y variable for further iterative processing, and Y_history will store the history of label changes at each step:
```Python
Y = np.array(Y0)
Y_history = [Y.copy()]
```
- The main label propagation loop:
```Python
For _ in range(num_iterations):
    Y = alpha * S @ Y + (1 - alpha) * Y0
    Y_history.append(np.array(Y)) 
```
At each step, we use the label propagation formula.

* S @ Y is the multiplication of the normalized similarity matrix S by the current labels of Y, which redistributes the class membership information over the graph.  
* alpha * S @ Y - weighted influence of labels from the previous step.  
* (1 - alpha) * Y0 - return to the original “anchor” labels so that the algorithm does not “stray” too far from the initial data.
Each iteration brings the final label distribution closer to a steady state, and Y_history captures these changes for further analysis. At the end, Y_history is returned so that the evolution of the labels can be traced.

## Usage
#### Step 1: Configuring a city.

In the `create_graph_osm` function, enter the name of the city you want to cluster. For example:
```python
def create_graph_osm(place_name=“Murom, Russia”):
```
-----
#### Step 2: Start the project.
1. Run the main.py file.
2. The program will prompt you to select two points on the graph, which will be the initial basis for clustering.
3. After launching, the graph of the city road network will be displayed on the screen.
4. Select two points by clicking on them with the mouse. The selected points will be highlighted in red.
---
#### Step 3. Select the operation mode.

After selecting the points, the program will prompt you to choose one of two modes of operation:
- Clustering by iterations:

This mode allows you to observe the process of the algorithm step by step.  Enter the number of iterations for clustering.
Specify the interval (in milliseconds) between animation frames.
After entering the parameters, the animation will start, showing the change of labels at each step.
- Finished clustering:

This mode will immediately output the final result after 100 iterations of the algorithm. The final visualization will show the clustering result given the selected starting points.

---

## Features

The graph may not be fully clustered if you specify a small number of iterations.
Red dots indicate the first group of points. Blue points point to another group. Black points are points without labels, i.e. not clustered. Purple points are those that can be included in both red and blue groups.




<details>
<summary>Alternative visualization</summary>

There is a commented out alternative plot_graph_live method in the code that shows the clustering process with a more accurate visualization. In this alternative, the points change their size depending on their labels.

If you want to use it instead of the current method, replace plot_graph_live in the code with the commented version.


</details>.

The algorithm can be refined by increasing the number of points.

### Examples:

### Road Count
![Road graph](https://github.com/makssent/Road-Graph-Clustering-with-Label-Spreading/blob/main/images/graph.png?raw=true)

### Selected point graph
![Selected Point Graph](https://github.com/makssent/Road-Graph-Clustering-with-Label-Spreading/blob/main/images/highlighted_graph.png?raw=true)

### Menu
![Menu](https://github.com/makssent/Road-Graph-Clustering-with-Label-Spreading/blob/main/images/menu.png?raw=true)

### Start Clustering
![Start Clustering](https://github.com/makssent/Road-Graph-Clustering-with-Label-Spreading/blob/main/images/start_clust.png?raw=true)

### End Clustering
![End Clustering](https://github.com/makssent/Road-Graph-Clustering-with-Label-Spreading/blob/main/images/finish_clust.png?raw=true)
