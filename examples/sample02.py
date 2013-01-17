from graphviz.graph import Graph

g = Graph("G")

c0 = g.add_graph( "cluster0" )
c0["label"] = "process #1"
c0["style"] = "filled"
c0["color"] = "lightgrey"
c0.node["style"] = "filled"
c0.node["color"] = "white"

a0 = c0.add_node( "a0" )
a1 = c0.add_node( "a1" )
a2 = c0.add_node( "a2" )
a3 = c0.add_node( "a3" )
c0.add_edge( a0, a1 )
c0.add_edge( a1, a2 )
c0.add_edge( a2, a3 )

c1 = g.add_graph( "cluster1" )
c1["label"] = "process #2"
c1["color"] = "blue"
c1.node["style"] = "filled"

b0 = c1.add_node( "b0" )
b1 = c1.add_node( "b1" )
b2 = c1.add_node( "b2" )
b3 = c1.add_node( "b3" )
c1.add_edge( b0, b1 )
c1.add_edge( b1, b2 )
c1.add_edge( b2, b3 )

start = g.add_node( "start" )
start["shape"] = "Mdiamond"
endn  = g.add_node( "end")
endn["shape"] = "Msquare"

g.add_edge( start, a0 )
g.add_edge( start, b0 )
g.add_edge( a1, b3 )
g.add_edge( b2, a3 )
g.add_edge( a3, a0 )
g.add_edge( a3, endn )
g.add_edge( b3, endn )

print g.output()
g.save("cluster.png")
