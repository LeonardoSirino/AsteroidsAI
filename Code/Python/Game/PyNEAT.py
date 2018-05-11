import random


class neuron:
    """
    Classe para representar um neurônio da rede e suas conexões seguintes
    Esta classe é usada para a criação das representações e para a mutação de adição de conexão
    """

    def __init__(self, ID):
        self.ID = ID
        self.forward_connections = []
        self.weights = []

    def AddConection(self, ID, weight):
        try:
            self.forward_connections.index(ID)
        except ValueError:
            self.forward_connections.append(ID)
            self.weights.append(weight)

    def AvailableConnections(self, next_layer_neurons):
        AvailableConnections = []
        for ID in next_layer_neurons:
            try:
                self.forward_connections.index(ID)
            except ValueError:
                AvailableConnections.append(ID)

        return AvailableConnections

    def __str__(self):
        base = "De " + str(self.ID) + " para "
        outs = ""
        for neuron in self.forward_connections:
            outs += str(neuron) + ", "

        return base + outs


class Layer:
    """
    Classe para representar uma camada e todos seus neurônios
    Esta classe é usada para se criar a representação e a mutação de adição de conexão
    """

    def __init__(self, number):
        self.number = number
        self.neurons = []
        self.neuronsIDs = []

    def AddConection(self, Connection):
        try:
            # Neurônio já existe, apenas a conexão será inserida
            index = self.neuronsIDs.index(Connection.input)
            selected_neuron = self.neurons[index]
            selected_neuron.AddConection(Connection.output, Connection.weight)
        except ValueError:
            # Neurônio não existe, será criado e adicionado
            self.neuronsIDs.append(Connection.input)
            new_neuron = neuron(Connection.input)
            new_neuron.AddConection(Connection.output, Connection.weight)
            self.neurons.append(new_neuron)

    def ReturnNeurons(self):
        return self.neuronsIDs

    def __str__(self):
        text = "Layer " + str(self.number) + "\n"
        for neuron in self.neurons:
            text += neuron.__str__()
            text += "\n"

        return text


class Connection:
    """
    Classe para representar cada uma das conexões que compõe o genoma
    As informações contidas nesta classe que serão usadas para a o uso da rede neural
    """

    innovation_number = 0

    def __init__(self):
        self.input = 0
        self.output = 0
        self.weight = random.random()
        self.innovation_number = Connection.innovation_number
        Connection.innovation_number += 1
        self.from_layer = 0

    def SetConnection(self, input, output, layer):
        self.input = input
        self.output = output
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
        self.Net = None  # representação da rede neural
        self.connections = [[]]
        """
        As conexões são formadas por listas, cada elemento da lista é um layer da rede.
        Cada layer possui uma lista de conexões
        """

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
                    i, self.inputs + j, 0)
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
        LinearizedGenome = self.ReturnLinearizedGenome()
        connection_index = random.randint(0, len(LinearizedGenome) - 1)
        connection = LinearizedGenome[connection_index]
        newNode_layer = connection.from_layer + 1

        if connection.to_layer == newNode_layer:
            # Insere nova layer se necessário
            self.InsertLayer(newNode_layer)

        Con1 = Connection()
        Con1.SetConnection(connection.input, self.CromIndex,
                           connection.from_layer)
        Con1.SetWeight(connection.weight)
        self.connections[connection.from_layer].append(Con1)

        Con2 = Connection()
        Con2.SetConnection(self.CromIndex, connection.output, newNode_layer)
        Con2.SetWeight(1)
        self.connections[newNode_layer].append(Con2)

        # Alocação de espaço para o novo nó
        self.CromIndex += 1
        self.WeightedSums += [0]
        self.Activations += [0]

        self.DelConnection(connection)

    def ReturnLinearizedGenome(self):
        LinearizedGenome = []
        for layer in self.connections:
            LinearizedGenome += layer

        return LinearizedGenome

    def DelConnection(self, Con_to_del):
        layer_del = 0
        con_del = 0
        layer_index = 0
        delete = False
        for layer in self.connections:
            con_index = 0
            for connection in layer:
                if connection == Con_to_del:
                    delete = True
                    layer_del = layer_index
                    con_del = con_index
                    break
                con_index += 1
            layer_index += 1

        if delete:
            self.connections[layer_del].__delitem__(con_del)

    def InsertLayer(self, layer_index):
        for layer in self.connections:
            for connection in layer:
                if connection.from_layer >= layer_index:
                    connection.from_layer += 1
                if connection.to_layer >= layer_index:
                    connection.to_layer += 1

        self.connections.insert(layer_index, [])

    def AddConection(self):
        AvailableConnections = []
        self.NetRepresentation()
        net = self.Net
        jmax = len(net) - 2

        j = 0
        for layer in net:
            next_layer_neurons = net[j + 1].ReturnNeurons()
            for neuron in layer.neurons:
                neuron_avb_con = neuron.AvailableConnections(
                    next_layer_neurons)
                if neuron_avb_con == []:
                    pass
                else:
                    AvailableConnections.append([neuron.ID, neuron_avb_con])

            j += 1
            if j > jmax:
                break

        if len(AvailableConnections) != 0:
            neurons_pairs = []

            for element in AvailableConnections:
                source = element[0]
                for target in element[1]:
                    neurons_pairs.append([source, target])

            pair_index = random.randint(0, len(neurons_pairs) - 1)
            pair = neurons_pairs[pair_index]
            layer = self.ReturnOwnerLayer(pair[0])
            new_connection = Connection()
            new_connection.SetConnection(pair[0], pair[1], layer)
            new_connection.SetWeight(random.random())
            self.connections[layer].append(new_connection)

    def ReturnOwnerLayer(self, neuronID):
        for layer in self.connections:
            for connection in layer:
                if connection.input == neuronID:
                    return connection.from_layer

        return None

    def NetRepresentation(self):
        if self.Net == None:
            i = 1
            net = []
            for layer in self.connections:
                rep_layer = Layer(i)
                for connection in layer:
                    rep_layer.AddConection(connection)

                net.append(rep_layer)
                i += 1

            output_layer = Layer(i)
            output_layer.neuronsIDs = range(
                self.inputs, self.inputs + self.outputs)
            net.append(output_layer)

            self.Net = net

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

nodes = 5
for i in range(0, nodes):
    player.AddNode()

connections = 5
for i in range(0, connections):
    player.AddConection()

print(player)
player.InputData([2.5, 3.6])
player.FeedForward()
result = player.ReturnOutput()

player.ClearNet()

print(result)
