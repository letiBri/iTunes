from model.model import Model

mymodel = Model()
mymodel.buildGraph(120)
nodi, archi = mymodel.getGraphDetails()
print("Numero di nodi: ", nodi)
print("Numero di archi: ", archi)
