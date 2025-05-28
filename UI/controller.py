import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None

    def handleCreaGrafo(self, e):
        dMinTxt = self._view._txtInDurata.value
        if dMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: valore minimo di durata non inserito", color="red"))
            self._view.update_page()
            return
        try:
            dMin = int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: non hai inserito un valore numerico positivo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(dMin)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito di {n} nodi e {a} archi."))
        self._fillDD(self._model.getAllNodes())
        self._view.update_page()

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare un album", color="red"))
            self._view.update_page()
            return
        size, dTotCC = self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD} ha {size} nodi e una durata totale di {dTotCC} minuti"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: soglia massima di durata non inserita", color="red"))
            self._view.update_page()
            return
        try:
            soglia = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: non hai inserito un valore intero positivo", color="red"))
            self._view.update_page()
            return
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare un album dal menù", color="red"))
            self._view.update_page()
            return
        setOfNodes, sumDurate = self._model.getSetOfNodes(self._choiceDD, soglia)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione= {len(setOfNodes)}, durata totale= {sumDurate}"))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito, gli album che fanno parte della solzuione trovata:"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def _fillDD(self, listOfNodes):
        listOfNodes.sort(key= lambda x: x.Title)
        listOfOptions = map(lambda x: ft.dropdown.Option(text=x.Title, on_click=self.getSelectedAlbum, data=x), listOfNodes)
        # for n in listOfNodes:
        #     listOfOptions.append(ft.dropdown.Option(text=x.Title, on_click=self.getSelectedAlbum, data=x))
        self._view._ddAlbum.options = list(listOfOptions)

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            print("error in reading DD")
            self._choiceDD = None
        self._choiceDD = e.control.data
