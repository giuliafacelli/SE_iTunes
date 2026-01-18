import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):

        self.G = nx.Graph()
        self._edges = []
        self._nodes = []
        self.albums = []
        self.album_playlists_map = {}

        self.id_map = {}


    def load_album(self, duration_min):
        self.albums = DAO.get_album_duration(duration_min)
        self.id_map = {a.id: a for a in self.albums}

    def load_album_playlists(self):
        self.album_playlists_map = DAO.get_album_playlist_map(self.albums)

    def build_graph(self):
        self.G.clear()

        self.G.add_nodes_from(self.albums)

        for i, album1 in enumerate(self.albums):
            for album2 in self.albums[i+1:]:
                if self.album_playlists_map[album1] & self.album_playlists_map[album2]:
                    self.G.add_edge(album1, album2)

    def get_componente_connessa(self, album):
        if album not in self.G:
            return []
        return list(nx.node_connected_component(self.G, album))

    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return self.G.edges()





