import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_peso = None
        self.best_sol = None
        self.graph = None
        self.countries = DAO.get_all_countries()

    def build_graph(self, country, year):
        self.graph = nx.Graph()
        nodes = DAO.get_nodes(country)
        self.graph.add_nodes_from(nodes)
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if u != v:
                    peso = DAO.get_peso(u.Retailer_code, v.Retailer_code, year)
                    if peso > 0:
                        self.graph.add_edge(u, v, weight=peso)

    def get_graph_details(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def get_volumi(self):
        sorted_nodes = []
        for node in self.graph.nodes:
            sorted_nodes.append((node, self.get_volume_nodo(node)))
        sorted_nodes.sort(key=lambda t: t[1], reverse=True)
        return sorted_nodes

    def get_volume_nodo(self, node):
        vol = 0
        for n in self.graph.neighbors(node):
            vol += self.graph[node][n]['weight']
        return vol

    def get_percorso(self, lung):
        self.best_sol = []
        self.best_peso = 0
        for node in self.graph.nodes:
            parziale = [node]
            self.ricorsione(parziale, lung)
            parziale.pop()
        return self.best_sol, self.best_peso

    def ricorsione(self, parziale, lung):
        ultimo = parziale[-1]
        if len(parziale) == lung+1 and ultimo == parziale[0]:
            peso_sol = self.get_peso_percorso(parziale)
            if peso_sol > self.best_peso:
                self.best_sol = copy.deepcopy(parziale)
                self.best_peso = peso_sol
                print(parziale)
        else:
            for neighbor in self.graph.neighbors(ultimo):
                if len(parziale) == lung:
                    parziale.append(neighbor)
                    self.ricorsione(parziale, lung)
                    parziale.pop()
                elif len(parziale) < lung:
                    if neighbor not in parziale:
                        parziale.append(neighbor)
                        self.ricorsione(parziale, lung)
                        parziale.pop()

    def get_peso_percorso(self, percorso):
        peso = 0
        for i in range(len(percorso)-1):
            peso += self.graph[percorso[i]][percorso[i+1]]['weight']
        return peso
