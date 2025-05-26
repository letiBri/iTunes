import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allNodi = []
        self._idMapAlbum = {}
        self._allEdges = []

    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi = DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId: n for n in self._allNodi}
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()
