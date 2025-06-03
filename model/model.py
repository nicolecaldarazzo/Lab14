import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()

    def getStores(self):
        return DAO.getStores()

    def buildGrafoPesato(self,store,giorni):
        self._grafo.clear()
        orders=DAO.getNodes(store)
        self._idMap={}
        for o in orders:
            self._idMap[o.order_id]=o
        self._grafo.add_nodes_from(orders)
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