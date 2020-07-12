# This file contains all kinds of utilities. 

from collections import defaultdict

class simple_graph(object):

    """
    The idea is to group the features/descriptors under different labels using a very simple graph.
    Although the overall approach might seem trivial, it helps with keeping track of all the different definitions, especially when there are a lot.
    """

    def __init__(self):
        self.graph_dict = defaultdict(dict)

    def add_node(self, node):
        if node not in self.graph_dict:
            self.graph_dict[node] = {}

    def add_edge(self, node, neighbor):
        self.graph_dict[node][neighbor] = 1
        self.graph_dict[neighbor][node] = 1

    def delete_node(self, node):
        _ = self.graph_dict.pop(node, None)
        for key in self.graph_dict:
            _ = self.graph_dict[key].pop(node, None)

    def delete_edge(self, node_1, node_2):
        _ = self.graph_dict[node_1].pop(node_2, None)
        _ = self.graph_dict[node_2].pop(node_1, None)

    def get_nodes(self):
        return list(self.graph_dict.keys())
        
    def extract(self, node):
        return list(self.graph_dict[node].keys())
    
    def extract_intersection(self, nodes):
        results = set(self.extract(nodes[0]))
        for node in nodes[1:]:
            results &= set(self.extract(node))
        return list(results)
    
    def extract_union(self, nodes):
        results = set(self.extract(nodes[0]))
        for node in nodes[1:]:
            results |= set(self.extract(node))
        return list(results)
    
def create_graph(features, translation=None) -> simple_graph:

    """
    Creates a very simple graph that connects the all the features and the groups that they belong to. 
    Assuming all the feature names follow the same patter A_B_C, which means the feature belongs to groups A, B and C.
    The parameter translation should be a dictionary. For example,
    translation = {'1': 'first'}
    means feature names with '1' in them should be labeled 'first'.
    """

    graph = simple_graph()

    for feature in features:
        labels = feature.split('_')
        for label in labels:
            if translation and label in translation:
                label = translation[label]
            graph.add_edge(feature, label)
    
    return graph