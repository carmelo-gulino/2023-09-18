import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dds(self):
        for y in range(2015, 2019):
            self.view.dd_anno.options.append(ft.dropdown.Option(f"{y}"))
        for c in self.model.countries:
            self.view.dd_nazione.options.append(ft.dropdown.Option(c))

    def handle_crea_grafo(self, e):
        if self.view.dd_nazione.value is None or self.view.dd_anno.value is None:
            self.view.create_alert("Selezionare una nazione e un anno")
            return
        country = self.view.dd_nazione.value
        year = int(self.view.dd_anno.value)
        self.model.build_graph(country, year)
        self.view.btn_volumi.disabled = False
        self.view.btn_rappresentativi.disabled = False
        self.view.txt_lunghezza.disabled = False
        nodi, archi = self.model.get_graph_details()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nodi} nodi e {archi} archi"))
        self.view.update_page()

    def handle_volumi(self, e):
        sorted_nodes = self.model.get_volumi()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il volume di vendita dei retailers nel grafo è:"))
        for n in sorted_nodes:
            self.view.txt_result.controls.append(ft.Text(f"{n[0]} --> {n[1]}"))
        self.view.update_page()

    def handle_percorso(self, e):
        try:
            lung = int(self.view.txt_lunghezza.value)
            if lung < 2:
                self.view.create_alert("Inserire un numero intero maggiore di 1")
                return
        except ValueError:
            self.view.create_alert("Inserire un numero")
            return
        path, peso_tot = self.model.get_percorso(lung)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso di lunghezza {lung} trovato ha peso {peso_tot}:"))
        for i in range(len(path)-1):
            self.view.txt_result.controls.append(ft.Text(f"{path[i]} -> {path[i+1]}: "
                                                         f"{self.model.graph[path[i]][path[i+1]]['weight']}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
