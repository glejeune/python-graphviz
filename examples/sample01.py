from graphviz.graph import Graph

g = Graph("G", "digraph")
n1 = g.add_node("Hello")
g2 = g.add_graph("c1")
e = g.add_edge("Hello", "World")
g2.add_edge("Toto", "Titi")
print g.output()
g.save("test.png")
