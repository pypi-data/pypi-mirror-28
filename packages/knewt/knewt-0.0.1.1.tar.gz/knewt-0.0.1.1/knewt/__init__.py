
class Node():
    def __init__(self,g):
        self.__graph__ = g 

    def in_degree(self,n):
        in_deg = lambda g,n :  [ e for e in g.edges if e[1] == n  ]
        return len(in_deg(self.__graph__,n)) 

    def out_degree(self,n):
        out_deg = lambda g,n :  [ e for e in g.edges if e[0] == n  ]

        return len(out_deg(self.__graph__,n)) 


class Graph():
    def __init__(self,label=None):
        if label is  None:
            label = "__UNDEF_"
        self.__edges__ = set([]) 
        self.__nodes__ = set([]) 
        self.__adjacency_list__ =  {} 
        self.__label__ = label 
        
    def __str__(self):
        return "<label=%s,nodes=%s,edges=%s>" % (self.__label__, len(self.__nodes__),len(self.__edges__))


    ### properties ####

    @property
    def edges(self):
        return self.__edges__ 

    @property
    def nodes(self):
        return self.__nodes__ 

    ### methods ###

    def add_node(self,v):
        if v not in self.__nodes__:
            self.__nodes__.add(v)
        if v not in self.__adjacency_list__:
            self.__adjacency_list__[v] = set([])

    def add_path(self,path):
        for (i,el)  in enumerate(path):
            if i == 0:
                self.add_node(path[i]) 
                continue 
            a = path[i-1]
            b = path[i] 

            self.add_edge(a,b) 

    def update(self,other_graph):
        self.__nodes__ =  self.__nodes__.union(other_graph.__nodes__)
        for e in other_graph.__edges__:
            self.add_edge(e[0],e[1]) 

    def union(self,other):
        g = Graph()
        edges = self.__edges__.union( other.__edges__ ) 
        nodes = self.__nodes__.union( other.__nodes__ ) 
        for e in edges:
            g.add_edge(e[0],e[1]) 
        for n in nodes:
            g.add_node(n) 

        return g 
    def add_edge(self,a,b):
        # Add new nodes to Nodes 
        [self.__nodes__.add(v)  for v in  (a,b) if v not in self.__nodes__]
        self.__edges__.add((a,b))
        
        #Add new entries into adjacency list 
        new_entries = [(v,set([]))  for v in  (a,b) if v not in self.__adjacency_list__]
        self.__adjacency_list__.update(dict(new_entries))
        
        if (a,b) not in self.__adjacency_list__[a]:
            self.__adjacency_list__[a].add(b)
        
    @staticmethod 
    def from_tuples(edges):
        g =  Graph() 
        for e in  edges:
            a =  e[0]
            b =  e[1]
            g.add_edge(a,b)
        return g 


class Traverser():
    DEPTH = "__depth__"
    NEIGHBOURS = "neighbours"
    PATH="__path__"
    def __init__(self):
        self.__component_groupers__ = {}
        self.__partition_schemes__ = {} 

    def grouper_add(self,name,fn):
        self.__component_groupers__ [name] = fn

    def partition(self,name,fn):
        self.__partition_schemes__[name] = fn  

    def update_components(self):
        self.component_start_depths = {} 
        for name in self.__components__:
            self.__components__[name].append(None)

            c =  Graph("%s_%s" %  (name,len(self.__components__[name])) )
            self.__components__[name][-1]= c 

    def bfs(self,g):

        self.__components__ = {}
        self.__visited__ = set([])

        for node  in  list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()  #  create a new iteration slot for the traversal
            self.__traversal_visited__ = set([])
            self.alg_bfs(g,node)

    def dfs(self,g,ignore_cycles=False):

        #print "graph>",g.edges  
        self.__components__ = {}
        self.__partitions__ = {} 

        self.__visited__ = set([])
        self.__iteration__ = 0 
        for node  in  list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()  #  create a new iteration slot for the traversal
            self.__traversal_visited__ = set([])
            self.alg_dfs(g,node,ignore_cycles=ignore_cycles)

            self.component_start_depths = {} 
            self.__iteraton__ = self.__iteration__ + 1 


    def alg_dfs(self,g,node=None,depth=0,context=None,ignore_cycles=False):
        # update global 
        self.__visited__.add(node)
        self.__traversal_visited__.add(node)
        # update context 
        # context:  neighbours, depth
        neighbours = g.__adjacency_list__[node]
        # if depth==0:
        #     self.update_components()
        if context is None:
            context = self.context( {"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours, Traverser.PATH : [node] }    )
        else:
            ctxt = self.context( {"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours }    )
            context.update(ctxt) 

        #print node,context[Traverser.NEIGHBOURS]
        #apply lambdas 
        #self.apply_component_lambdas(g,node=node,edge=None,context=context)


        for n in neighbours:
        
            self.apply_component_lambdas(g,node,(node,n),context=context)
            self.apply_partition_lambdas(g,node,(node,n),context=context) 
            #self.apply_component_lambdas(g,node,(node,n),{"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours})
            if n in self.__traversal_visited__:
                if ignore_cycles is False:
                    raise Exception("Cylce Detected  (%s,%s)" % (node,n))
                continue

            path = context[Traverser.PATH]
            new_context = {}
            new_context.update(context)

            new_path = []
            new_path.extend(path)
            new_path.append(n)
            new_context[Traverser.PATH] = new_path
            #print node,n,path,new_path



            self.alg_dfs(g,node=n,depth=depth+1,context=new_context,ignore_cycles=ignore_cycles)


    def context(self,c):
        traversal_context = {"iteration": self.__iteration__  }
        traversal_context.update(c)
        return  traversal_context

    def groups(self):
        return self.__components__

    def partitions(self):
        return self.__partitions__ 


    def apply_partition_lambdas1 (self,g,node,edge,context):
        for name in self.__partition_schemes__: 
            fn = self.__partition_schemes__[name] 
            
            (n,e,hash_id) = fn(node,edge,context) 

            partition_name =  "%s_%s" % (name,hash_id) 

            if n is None and e is None:
                continue 
            
            if hash_id is None:
                continue 

            if partition_name not in self.__partitions__:
                self.__partitions__[partition_name] = [] 
                g = Graph(partition_name)
                self.__partitions__[partition_name].append(g) 

            p  = self.__partitions__[partition_name][0]   

            if e is not None:
                p.add_edge(e[0],e[1])
            if n is not None:
                p.add_node(n) 



    def apply_partition_lambdas (self,g,node,edge,context):
        for name in self.__partition_schemes__: 
            fn = self.__partition_schemes__[name] 
           

            
            if type(fn(node,edge,context)) == tuple:
                result = [ fn(node,edge,context) ]  
            else:
                result = fn(node,edge,context) 

            for r in result: 
                print r 
                (n,e,hash_id) = (r[0],r[1],r[2])  #fn(node,edge,context) 

                partition_name =  "%s_%s" % (name,hash_id) 

                if n is None and e is None:
                    continue 
                
                if hash_id is None:
                    continue 

                if partition_name not in self.__partitions__:
                    self.__partitions__[partition_name] = [] 
                    g = Graph(partition_name)
                    self.__partitions__[partition_name].append(g) 

                p  = self.__partitions__[partition_name][0]   

                if e is not None:
                    p.add_edge(e[0],e[1])
                if n is not None:
                    p.add_node(n) 

    def apply_component_lambdas(self,g,node,edge,context):
        for name in  self.__component_groupers__:
            if name not in self.component_start_depths:
                self.component_start_depths[name] = context[Traverser.DEPTH] 


            fn = self.__component_groupers__[name]

            #print "name",name," considering:",edge
            (n,e) = fn(node,edge,context)
            #print "Applying:",name,",Result:",(n,e),"Context:",context 
            if e is None and n is None:
                return 


            if (name in self.__components__) == False:
                self.__components__[name] = []
                c =  Graph("%s_%s" %  (name,0) )
                self.__components__[name].append(c) 
 
            # elif self.component_start_depths[name] ==  context[Traverser.DEPTH]:
            #     c =  Graph("%s_%s" %  (name,len(self.__components__[name]) ))
            #     self.__components__[name].append(c)


            c = self.__components__[name][-1]

            
            if e is not None:
                #print "label:",c.__label__,",Adding",e," to ",c.__edges__  
                c.add_edge(e[0],e[1])

            if n is not None:
                c.add_node(n)



