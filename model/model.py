import networkx as nx
from networkx.algorithms.traversal import dfs_successors, dfs_tree, dfs_predecessors

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()
        self._orders=[]
        self._visitati=None
        self._parziale=[]
        self.peso_attuale=10000000
        self._maxPercorso=[]
        self._maxPeso=0

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
        tree=nx.bfs_tree(self._grafo,self._idMap[start])
        nodi=list(tree.nodes())
        return nodi[1:]

    def getPercorsoPesoMassimo(self,source):
        source2=self._idMap[source]
        percorso, peso=self._ricorsione(source2)
        return percorso

    def _ricorsione(self, nodo):
        self._parziale.append(nodo)
        if not list(self._grafo.successors(nodo)):
            if self.peso_attuale>self._maxPeso:
                self._maxPeso=self.peso_attuale
                self._maxPercorso[:]=self._parziale
            return self._maxPercorso,self._maxPeso
        for successore in self._grafo.successors(nodo):
            peso_arco=self._grafo[nodo][successore]["weight"]

            if peso_arco<self.peso_attuale:
                self._ricorsione(successore)
        return self._maxPercorso, self._maxPeso


