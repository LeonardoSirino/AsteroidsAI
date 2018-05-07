import random


class Connection:
    def __init__(self):
        self.input = 0
        self.output = 0
        self.weight = random.random()
        self.innovation_number = 0
        self.from_layer = 0

    def SetConnection(self, input, output, innovation, layer):
        self.input = input
        self.output = output
        self.innovation_number = innovation
        self.from_layer = layer
        self.to_layer = layer + 1

    def SetWeight(self, weight):
        self.weight = weight

    def __str__(self):
        text = "Do nó " + str(self.input) + " (L: " + str(self.from_layer) + ") ao nó " + str(self.output) + " (L: " + str(self.to_layer) + ") com peso " + \
            str(round(self.weight, 2)) + " - IN: " + \
            str(self.innovation_number)
        return text


class Genome:
    def __init__(self):
        self.connections = [[]]
        """
        As conexões são formadas por listas, cada elemento da lista é um layer da rede.
        Cada layer possui uma lista de conexões
        """

        self.innovation_number = 0

    def InitGenome(self, inputs, outputs):
        self.inputs = inputs + 1  # Bias neuron
        self.outputs = outputs
        self.CromIndex = inputs + 1 + outputs
        self.WeightedSums = [0] * (self.inputs + self.outputs)
        self.Activations = [0] * (self.inputs + self.outputs)
        """
        As weighted sums e as activations são toda a informação contida na rede.
        Os primeiros elementos são destinados aos nós de entrada, sendo seguidos pelos nós de saída.
        Os nós intermediários vêm por último
        """

        first_connections = []
        for i in range(0, self.inputs):
            for j in range(0, self.outputs):
                new_connection = Connection()
                new_connection.SetConnection(
                    i, self.inputs + j, self.innovation_number, 0)
                self.innovation_number += 1
                first_connections.append(new_connection)

        self.connections[0] = first_connections

    def InputData(self, data):
        data += [1]
        if len(data) == self.inputs:
            self.Activations[0:self.inputs] = data
        else:
            print("Número de inputs inadequado")

    def FeedForward(self):
        for layer in self.connections:
            for connection in layer:
                if connection.from_layer > 0:
                    # Para o input layer não é preciso calcular as ativações
                    ws = self.WeightedSums[connection.input]
                    a = self.ActivateFunction(ws)
                    self.Activations[connection.input] = a

                a = self.Activations[connection.input]
                w = connection.weight
                self.WeightedSums[connection.output] += a * w

        for k in range(0, self.outputs):
            ws = self.WeightedSums[k + self.inputs]
            a = self.ActivateFunction(ws)
            self.Activations[k + self.inputs] = a

    def ReturnOutput(self):
        output = self.Activations[self.inputs:self.inputs + self.outputs]
        return output

    def ClearNet(self):
        size = len(self.WeightedSums)
        self.WeightedSums = [0] * size
        self.Activations = [0] * size

    def AddNode(self):
        """
        Pensar em outra forma de selecionar a conexão a ser mutada
        Da forma atual, as conexões em layers mais densos tem menor probabilidade de mutação
        Desta forma a rede tende a se extender demais e ter layers muito vazios
        """

        layer_index = random.randint(0, len(self.connections) - 1)
        layer = self.connections[layer_index]
        connection_index = random.randint(0, len(layer) - 1)
        connection = layer[connection_index]
        newNode_layer = connection.from_layer + 1

        if connection.to_layer == newNode_layer:
            # Insere nova layer se necessário
            self.InsertLayer(newNode_layer)

        Con1 = Connection()
        Con1.SetConnection(connection.input, self.CromIndex,
                           self.innovation_number, connection.from_layer)
        Con1.SetWeight(connection.weight)
        self.connections[connection.from_layer].append(Con1)
        self.innovation_number += 1

        Con2 = Connection()
        Con2.SetConnection(self.CromIndex, connection.output,
                           self.innovation_number, newNode_layer)
        Con2.SetWeight(1)
        self.connections[newNode_layer].append(Con2)
        self.innovation_number += 1

        # Alocação de espaço para o novo nó
        self.CromIndex += 1
        self.WeightedSums += [0]
        self.Activations += [0]

        self.connections[layer_index].__delitem__(connection_index)

    def InsertLayer(self, layer_index):
        for layer in self.connections:
            for connection in layer:
                if connection.from_layer >= layer_index:
                    connection.from_layer += 1
                if connection.to_layer >= layer_index:
                    connection.to_layer += 1

        self.connections.insert(layer_index, [])

    def AddConection(self):
        pass

    def ActivateFunction(self, ws):
        if ws > 0:
            return ws
        else:
            return 0

    def __str__(self):
        text = ""
        i = 0
        for layer in self.connections:
            text += "\n Layer " + str(i) + "\n"
            for connection in layer:
                text += connection.__str__()
                text += "\n"
            i += 1

        return text


player = Genome()
player.InitGenome(2, 3)
print(player)
nodes = 10
for i in range(0, nodes):
    player.AddNode()
print(player)
player.InputData([2.5, 3.6])
player.FeedForward()
result = player.ReturnOutput()


player.ClearNet()

print(result)
