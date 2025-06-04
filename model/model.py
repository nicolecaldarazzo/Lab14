import networkx as nx
from networkx.algorithms.traversal import dfs_successors, dfs_tree, dfs_predecessors

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()
        self._orders=[]
        self._visitati=None

    def getStores(self):
        return DAO.getStores()

    def buildGrafoPesato(self,store,giorni):
        self._grafo.clear()
        self._orders=DAO.getNodes(store)
        self._idMap={}
        for o in self._orders:
            self._idMap[o.order_id]=o
        self._grafo.add_nodes_from(self._orders)
        allEdges=DAO.getEdges(store,self._idMap,giorni)
        for edge in allEdges:
            u=self._idMap[edge[0].order_id]
            v=self._idMap[edge[1].order_id]
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]["weight"]+=edge[2]
            else:
                self._grafo.add_edge(u,v,weight=edge[2])


    def getNumNodes(self):
        return len(list(self._grafo.nodes))

    def getNumEdges(self):
        return len(list(self._grafo.edges))

    def getNodes(self):
        return self._orders

    #def cercaPercorsoMassimo(self, start, path=[], max_path=[], max_weight=0, current_weight=0):
    def cercaPercorsoMassimo(self,start):
        return dfs_tree(self._grafo,self._idMap[start])