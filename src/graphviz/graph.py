class Attributs(object):
    def __init__(self, attributes={}):
        self.__attributs = attributes

    def __getitem__(self, key):
        if key in self.__attributs:
            return self.__attributs[key]
        return Node

    def __setitem__(self, key, value):
        self.__attributs[key] = value

    def output(self, pre="", post=""):
        """
        Output data for attributes in a graphviz graph
        >>> Attributs(attributes={'key': 'value'}).output()
        ' [key = "value"]'
        >>> Attributs(attributes={'key': 'value'}).output(pre="lol")
        'lol [key = "value"]'
        >>> Attributs(attributes={'key': 'value'}).output(pre="glop", post="pas-glop")
        'glop [key = "value"]pas-glop'
        """
        if self.__attributs:
            items = ['%s = "%s"' % (key, value)
                     for (key, value)
                     in self.__attributs.items()]
            return "%s [%s]%s" % (pre,
                   ', '.join(items),
                post)
        return ""


class Node(object):
    def __init__(self, name):
        self.name = name
        self.__attributs = Attributs()

    def __getitem__(self, key):
        self.__attributs[key]

    def __setitem__(self, key, value):
        self.__attributs[key] = value

    def output(self, unused=""):
        """
        Output data for nodes
        >>> Node("hello").output()
        '\\thello;\\n'
        """
        return "\t" + self.name + self.__attributs.output() + ";\n"


class Edge(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.__attributs = Attributs()

    def __getitem__(self, key):
        self.__attributs[key]

    def __setitem__(self, key, value):
        self.__attributs[key] = value

    def output(self, link=" -- "):
        return "\t%s%s%s%s;\n" % (
               self.head.name,
               link,
               self.tail.name,
               self.__attributs.output()
        )


class Graph(object):
    def __init__(self, name, type="graph", parent=None):
        self.name = name
        self.__parent_graph = parent
        self.__type = type
        self.__nodes = {}
        self.__edges = []
        self.__subgraphs = []
        self.__output_order = []
        self.__links = {"graph": " -- ", "digraph": " -> "}
        self.__attributs = Attributs()
        self.node = Attributs()
        self.edge = Attributs()

    def __getitem__(self, key):
        self.__attributs[key]

    def __setitem__(self, key, value):
        self.__attributs[key] = value

    def __order(self, o):
        self.__output_order.append(o)

    def add_node(self, name):
        self.__nodes[name] = Node(name)
        self.__order(self.__nodes[name])
        return self.__nodes[name]

    def add_edge(self, head, tail):
        _h, _t = head, tail

        if not type(head) == Node:
            if not head in self.__nodes:
                _h = self.__nodes[head] = Node(head)
                self.__order(self.__nodes[head])
            else:
                _h = self.__nodes[head]

        if not type(tail) == Node:
            if not tail in self.__nodes:
                _t = self.__nodes[tail] = Node(tail)
                self.__order(self.__nodes[tail])
            else:
                _t = self.__nodes[tail]

        e = Edge(_h, _t)
        self.__order(e)
        self.__edges.append(e)
        return e

    def add_graph(self, name):
        g = Graph(name, "subgraph", self)
        self.__subgraphs.append(g)
        self.__order(g)
        return g

    def __link(self):
        if self.__type in ["graph", "digraph"]:
            return self.__links[self.__type]
        else:
            return self.__parent_graph.__link()

    def __which(self, program):
        import os

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    def output(self, unused=""):
        data = self.__type + " \"" + self.name + "\" {\n"
        data = data + self.__attributs.output("graph", ";\n")
        data = data + self.node.output("node", ";\n")
        data = data + self.edge.output("edge", ";\n")
        for x in self.__output_order:
            data = data + x.output(self.__link())
        data = data + "}\n"
        return data

    def save(self, filename):
        from subprocess import Popen, PIPE
        from tempfile import NamedTemporaryFile
        import os
        f = NamedTemporaryFile(delete=False)
        f.write(self.output())
        f.close()
        dot = self.__which("dot")
        if dot:
            cmd = dot + " -Tpng -o" + filename + " " + f.name
            print(Popen(cmd, stdout=PIPE, shell=True).stdout.read())
        else:
            print("Can't find dot")
        os.unlink(f.name)
