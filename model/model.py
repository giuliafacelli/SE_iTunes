import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):

        self.G = nx.Graph()
        self._edges = []
        self._nodes = []
        self.albums = []
        self.album_playlists_map = {}
        self.soluzione_best = []

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


    def max_album_componente_connessa(self, start_album, max_duration):
        component = self.get_componente_connessa(start_album)

        self.soluzione_best = []
        self.ricorsione(component, [start_album], start_album.duration, max_duration)

        return self.soluzione_best

    def ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

            for album in albums:
                if album in current_set:
                    continue
                new_duration = current_duration + album.duration
                if new_duration <= max_duration:
                    current_set.append(album)
                    self.ricorsione(albums, current_set, new_duration, max_duration)
                    current_set.pop()









