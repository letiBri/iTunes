import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allNodi = []
        self._idMapAlbum = {}
        self._allEdges = []

        self._bestSet = {}
        self._maxLen = 0

    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi = DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId: n for n in self._allNodi}  # equivale a fare il ciclo for
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes())

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._grafo, a1)
        return len(cc), self._getDurataTot(cc)

    def _getDurataTot(self, listOfNodes):
        durataTot = 0
        for n in listOfNodes:
            durataTot += n.dTot
        return durataTot
        # return sum([n.dTot for n in listOfNodes])

    def getSetOfNodes(self, a1, soglia):
        self._bestSet = {}
        self._maxLen = 0
        parziale = {a1}
        cc = nx.node_connected_component(self._grafo, a1)
        cc.remove(a1)  # inzio a scartare i nodi già visti anche se ho un set, risparmio un'iterazione
        for n in cc:
            # richiamo la ricorsione
            parziale.add(n)
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia)
            cc.add(n)
            parziale.remove(n)  # backtracking
        return self._bestSet, self._getDurataTot(self._bestSet)

    def _ricorsione(self, parziale, rimanenti, soglia):  # rimanenti sono i nodi della componente connessa che posso ancora aggiungere
        # 1) verifico che parziale sia una sol ammissibile, ovvero se viola i vincoli
        if self._getDurataTot(parziale) > soglia:
            return  # evito di andare avnti su questa linea di esporazione perchè tanto ho superato il limite
        # 2) se parziale soddisfa i criteri, allora verifico se è migliore di bestSet
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)
        # 3) aggiungo e faccio ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n)  # backtracking al contrario sulla lista dei rimanenti, serve per andare più veloce nella ricorsione
