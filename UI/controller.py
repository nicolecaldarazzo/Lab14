import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        allStores=self._model.getStores()
        for s in allStores:
            self._view._ddStore.options.append(ft.dropdown.Option(s))


    def handleCreaGrafo(self, e):
        store=self._view._ddStore.value
        giorni=self._view._txtIntK.value
        self._model.buildGrafoPesato(store,giorni)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamanete creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumEdges()}"))
        self._view.update_page()

    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass
