from IPython.core.display import Image, display 
import pydot 
embed_image = lambda img  :Image(filename=img)



def dot_render(g):
    line = "digraph {\n"
    labels =  list(g.__nodes__)
    nodes = [ "a%s" % n[0] for n in enumerate(list(g.__nodes__)) ]
    l_2_n = dict(zip(labels,nodes))
    for e in g.__edges__:
        a = l_2_n [ e[0] ] 
        b = l_2_n [ e[1]  ] 
        line = line +  "%s->%s;\n" % (a,b)
    for n in g.__nodes__:
        a = l_2_n [ n ] 
        line = line + "%s [ label=\"%s\" ]; \n" % (a,n)
    line = line + "}"
    #print line 
    display(display_graph("out",line))

def display_graph(label,dot_string):
    dot_graph = pydot.graph_from_dot_data(dot_string)
    dot_graph[0].label = label
    dot_graph[0].write_png("%s.png" % label)
    return embed_image("%s.png" % label )


