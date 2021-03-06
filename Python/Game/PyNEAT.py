import random
import numpy as np
import matplotlib.pyplot as plt
import copy
from pyvis.network import Network


class neuron:
    """
    Classe para representar um neurônio da rede e suas conexões seguintes
    Esta classe é usada para a criação das representações e para a mutação de adição de conexão
    """

    def __init__(self, ID):
        self.ID = ID
        self.forward_connections = []
        self.weights = []

    def AddNetConnection(self, ID, weight):
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
        self.NeuronYPosition = []

    def AddNetConnection(self, Connection):
        try:
            # Neurônio já existe, apenas a conexão será inserida
            index = self.neuronsIDs.index(Connection.input)
            selected_neuron = self.neurons[index]
            selected_neuron.AddNetConnection(
                Connection.output, Connection.weight)
        except ValueError:
            # Neurônio não existe, será criado e adicionado
            self.neuronsIDs.append(Connection.input)
            new_neuron = neuron(Connection.input)
            new_neuron.AddNetConnection(Connection.output, Connection.weight)
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
        self.weight = RandSim()
        self.innovation_number = Connection.innovation_number
        Connection.innovation_number += 1
        self.from_layer = 0
        self.enable = True
        self.recurrent = False

    def SetConnection(self, input, output, layer, recurrent):
        self.input = input
        self.output = output
        self.from_layer = layer
        self.to_layer = layer + 1
        self.recurrent = recurrent

    def SetOutLayer(self, OutLayer):
        self.to_layer = OutLayer

    def SetWeight(self, weight):
        self.weight = weight

    def __str__(self):
        text = "Do nó " + str(self.input) + " (L: " + str(self.from_layer) + ") ao nó " + str(self.output) + " (L: " + str(self.to_layer) + ") com peso " + \
            str(round(self.weight, 2)) + " - IN: " + \
            str(self.innovation_number)

        if self.recurrent:
            text += " recorrente"

        if not self.enable:
            text += " DISABLED"
        return text


class Genome:

    ID = 0

    def __init__(self):
        self.Net = None  # representação da rede neural
        self.connections = [[], []]
        """
        As conexões são formadas por listas, cada elemento da lista é um layer da rede.
        Cada layer possui uma lista de conexões
        """
        self.OwnerSpecie = None
        self.score = 0
        self.ID = Genome.ID
        Genome.ID += 1

    def InitGenome(self, inputs, outputs):
        self.inputs = inputs + 1  # Bias neuron
        self.outputs = outputs
        self.CromIndex = inputs + 1 + outputs
        self.WeightedSums = [0] * (self.inputs + self.outputs)
        self.Activations = [0] * (self.inputs + self.outputs)
        self.LastActivations = [0] * (self.inputs + self.outputs)
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
                    i, self.inputs + j, 0, False)
                first_connections.append(new_connection)

        self.connections[0] = first_connections

    def InputData(self, data):
        data += [1]  # Bias neuron
        if len(data) == self.inputs:
            self.Activations[0:self.inputs] = data
        else:
            print("Número de inputs inadequado")

    def FeedForward(self):
        RecurrentConnections = self.ReturnRecurrent()

        # Relações recorrentes
        for connection in RecurrentConnections:
            a = self.LastActivations[connection.input]
            w = connection.weight
            self.WeightedSums[connection.output] += a * w

        # Relações diretas
        for layer in self.connections:
            for connection in layer:
                if connection.enable and not connection.recurrent:
                    if connection.from_layer > 0:
                        # Para o input layer não é preciso calcular as ativações
                        ws = self.WeightedSums[connection.input]
                        a = self.ActivateFunction(ws)
                        self.Activations[connection.input] = a

                    if connection.recurrent:
                        a = self.LastActivations[connection.input]
                    else:
                        a = self.Activations[connection.input]
                    w = connection.weight
                    self.WeightedSums[connection.output] += a * w

        for k in range(0, self.outputs):  # Ativaçoes da output Layer
            ws = self.WeightedSums[k + self.inputs]
            a = self.ActivateFunction(ws)
            self.Activations[k + self.inputs] = a

        # Armazenamento das ativaçõe na memória
        self.LastActivations = self.Activations[:]

    def ReturnOutput(self):
        output = self.Activations[self.inputs:self.inputs + self.outputs]
        return output

    def ClearNet(self):
        size = len(self.WeightedSums)
        self.WeightedSums = [0] * size
        self.Activations = [0] * size

    def RandomNode(self):
        self.Net = None
        LinearizedGenome = self.ReturnLinearizedGenome()
        valid = False
        while not valid:
            connection_index = random.randint(0, len(LinearizedGenome) - 1)
            connection = LinearizedGenome[connection_index]
            valid = connection.enable and not connection.recurrent

        newNode_layer = connection.from_layer + 1

        if connection.to_layer == newNode_layer:
            # Insere nova layer se necessário
            self.InsertLayer(newNode_layer)

        Con1 = Connection()
        Con1.SetConnection(connection.input, self.CromIndex,
                           connection.from_layer, False)
        Con1.SetWeight(connection.weight)
        self.connections[connection.from_layer].append(Con1)

        Con2 = Connection()
        Con2.SetConnection(self.CromIndex, connection.output,
                           newNode_layer, False)
        Con2.SetWeight(1)
        self.connections[newNode_layer].append(Con2)

        # Alocação de espaço para o novo nó
        self.CromIndex += 1
        self.WeightedSums += [0]
        self.Activations += [0]
        self.LastActivations += [0]

        self.DisableConnection(connection)

    def ReturnLinearizedGenome(self):
        LinearizedGenome = []
        for layer in self.connections:
            LinearizedGenome += layer

        return LinearizedGenome

    def ReturnRecurrent(self):
        RecurrentConnections = []
        for layer in self.connections:
            for connection in layer:
                if connection.recurrent:
                    RecurrentConnections.append(connection)

        return RecurrentConnections

    def DisableConnection(self, con_to_disable):
        layer_del = 0
        con_del = 0
        layer_index = 0
        delete = False
        for layer in self.connections:
            con_index = 0
            for connection in layer:
                if connection == con_to_disable:
                    delete = True
                    layer_del = layer_index
                    con_del = con_index
                    break
                con_index += 1
            layer_index += 1

        if delete:
            self.connections[layer_del][con_del].enable = False

    def InsertLayer(self, layer_index):
        for layer in self.connections:
            for connection in layer:
                if connection.from_layer >= layer_index:
                    connection.from_layer += 1
                if connection.to_layer >= layer_index:
                    connection.to_layer += 1

        self.connections.insert(layer_index, [])

    def RandomConnection(self):
        self.__NetRepresentation()
        net = self.Net
        self.Net = None
        genome = self.ReturnLinearizedGenome()
        NeuronsIDs = []

        for layer in net:
            neurons = layer.ReturnNeurons()
            NeuronsIDs += neurons

        maxConnections = (len(NeuronsIDs) - self.inputs)**2 + \
            2 * self.inputs * (len(NeuronsIDs) - self.inputs)
        if len(genome) < maxConnections:
            size = len(NeuronsIDs)
            valid = False
            j = 0
            while not valid:
                j += 1
                source = NeuronsIDs[random.randint(0, size - 1)]
                target = NeuronsIDs[random.randint(self.inputs, size - 1)]
                source_layer = self.ReturnOwnerLayer(source)
                target_layer = self.ReturnOwnerLayer(target)
                if source_layer >= target_layer:
                    recurrent = True
                else:
                    recurrent = random.randint(0, 1) == 1

                for connection in genome:
                    if source == connection.input and target == connection.output and recurrent == connection.recurrent:
                        valid = False
                        break
                    else:
                        valid = True

                if j > 1000:
                    print("Desisto")
                    break

            if valid:
                new_connection = Connection()
                new_connection.SetConnection(
                    source, target, source_layer, recurrent)
                new_connection.SetOutLayer(target_layer)
                new_connection.SetWeight(RandSim())
                self.connections[source_layer].append(new_connection)

        else:
            print("Rede cheia!")

    def RandonWeightVariation(self, prob, alpha):
        for layer in self.connections:
            for con in layer:
                if con.enable:
                    if random.random() < prob:
                        con.weight += alpha * RandSim()

    def ReturnOwnerLayer(self, neuronID):
        Ownerlayer = None
        if neuronID >= self.inputs and neuronID < (self.inputs + 1 + self.outputs):
            Ownerlayer = len(self.connections) - 1

        for layer in self.connections:
            for connection in layer:
                if connection.input == neuronID:
                    Ownerlayer = connection.from_layer

        return Ownerlayer

    def __NetRepresentation(self):
        if self.Net == None:
            i = 1
            net = []
            for layer in self.connections:
                rep_layer = Layer(i)
                for connection in layer:
                    if connection.enable:
                        rep_layer.AddNetConnection(connection)

                net.append(rep_layer)
                i += 1

            output_layer = Layer(i - 1)
            output_layer.neuronsIDs = range(
                self.inputs, self.inputs + self.outputs)
            net.append(output_layer)

            self.Net = net

    def ActivateFunction(self, ws):
        sigmoid = 1 / (1 + np.exp(-ws))
        return sigmoid

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

    def GenomeRepresentation(self, name):
        self.__NetRepresentation()
        net = self.Net
        LinGen = self.ReturnLinearizedGenome()
        display = NetDisplay(net, LinGen, name)
        display.nodesPlot()

    def SetScore(self, score):
        SharedScore = score / self.OwnerSpecie.SpeciePopulation()
        self.score = SharedScore

    def MemberDeath(self):
        self.OwnerSpecie.RemoveMember(self.ID)

    def SetSpecie(self, specie):
        self.OwnerSpecie = specie


class NetDisplay:
    def __init__(self, net, LinGen, name):
        self.net = net
        self.LinGen = LinGen
        self.Grafo = Network(height="600px", width="1000px")
        self.name = name

        self.Grafo.toggle_physics(False)
        self.Grafo.inherit_edge_colors_from(False)

    def nodesPlot(self):
        self.CalcNeuronsYpositions()
        for layer in self.net:
            neurons = layer.ReturnNeurons()
            y_positions = layer.NeuronYPosition
            for neuron, y_pos in zip(neurons, y_positions):
                self.Grafo.add_node(
                    neuron, x=layer.number * 100, y=y_pos * 100)

        i = 0
        for con in self.LinGen:
            if con.enable:
                if con.weight >= 0:
                    color = 'blue'
                else:
                    color = 'red'

                if con.recurrent:
                    dashes = 'true'
                else:
                    dashes = 'false'

                try:
                    self.Grafo.add_edge(
                        con.input, con.output, value=abs(con.weight))
                    self.Grafo.edges[i].update(
                        {'color': color, 'arrows': 'to', 'arrowStrikethrough': 'false',
                         'title': 'IN: ' + str(con.innovation_number), 'dashes': dashes, 'shadow': dashes})
                    i += 1
                except:
                    pass

        self.Grafo.show_buttons()
        self.Grafo.set_edge_smooth('dynamic')
        self.Grafo.show(self.name + ".html")

    def CalcNeuronsYpositions(self):
        for layer in self.net:
            neuronsYposition = []
            size = len(layer.ReturnNeurons())
            if size % 2 == 0:
                for i in range(0, size // 2):
                    neuronsYposition += [i + 0.5, -i - 0.5]
            else:
                neuronsYposition = [0]
                for i in range(1, size // 2 + 1):
                    neuronsYposition += [i, -i]
            layer.NeuronYPosition = neuronsYposition


class Specie:

    ID = 0

    def __init__(self, RepresentationMember, NEAT):
        self.RepresentationMember = RepresentationMember
        self.members = [RepresentationMember]
        self.NEAT = NEAT
        self.ID = Specie.ID
        Specie.ID += 1

    def addMember(self, newMember):
        distance = self.NEAT.CalcDistance(self.RepresentationMember, newMember)
        if distance < self.NEAT.DeltaTHR:
            newMember.SetSpecie(self)
            self.members.append(newMember)
            return True
        else:
            return False

    def GetMember(self, ID):
        for member in self.members:
            if member.ID == ID:
                return member

        return None

    def SpeciePopulation(self):
        return len(self.members)

    def RemoveMember(self, ID):
        if len(self.members) == 1:
            self.Extinction()
        else:
            member = self.GetMember(ID)
            try:
                index = self.members.index(member)
                self.members.__delitem__(index)
                if member == self.RepresentationMember:
                    ranIndex = random.randint(0, len(self.members) - 1)
                    self.RepresentationMember = self.members[ranIndex]
            except:
                #print("Membro não encontrado")
                pass

    def Extinction(self):
        self.NEAT.removeSpecie(self)
        print("Extinção da espécie " + str(self.ID))

    def RevalidateMembers(self):
        for member in self.members:
            distance = self.NEAT.CalcDistance(
                self.RepresentationMember, member)
            if distance > self.NEAT.DeltaTHR:
                member.MemberDeath()
                self.NEAT.addMember(member)

    def Reproduction(self, proportion):
        numberOfNewMembers = round(self.SpeciePopulation() * proportion)
        for i in range(0, numberOfNewMembers):
            pass  # CONTINUAR


class NEAT:
    """
    Classe para fornecer as funcionalidades esperadas num algoritmo de NEAT
    """

    def __init__(self):
        self.c1 = 1
        self.c2 = 1
        self.c3 = 0.6
        self.DeltaTHR = 3
        self.probRandomNode = 0.3
        self.probRandomConnection = 0.3
        self.probRandomWeightVariation = 0.7
        self.probMemberMutation = 0.3
        self.initialPopulation = 5

    def CalcDistance(self, gen1, gen2):
        """Cálculo da distância entre duas topologias diferentes        
        Arguments:
            gen1 {[genome]} -- [genoma 1]
            gen2 {[genome]} -- [genoma 2]
        """
        gen1 = gen1.ReturnLinearizedGenome()
        gen2 = gen2.ReturnLinearizedGenome()
        lastIN1 = self.returnLastInnovation(gen1)
        lastIN2 = self.returnLastInnovation(gen2)
        N = np.max([len(gen1), len(gen2)])

        if lastIN1 > lastIN2:
            newer = gen1
            older = gen2
        else:
            newer = gen2
            older = gen1

        disjoint = 0
        weight_distance = 0
        for con_old in older:
            IN = con_old.innovation_number
            match = False
            for con_new in newer:
                if con_new.innovation_number == IN:
                    match = True
                    weight_distance += (con_new.weight - con_old.weight)**2
                    break

            if match:
                pass
            else:
                disjoint += 1

        weight_distance = np.sqrt(weight_distance)

        excess = 0
        olderLastIN = np.min([lastIN1, lastIN2])
        for connection in newer:
            if connection.innovation_number > olderLastIN:
                excess += 1

        distance = self.c1 * excess / N + self.c2 * \
            disjoint / N + self.c3 * weight_distance

        """
        print("Disjoint: " + str(disjoint) + " excess: " +
              str(excess) + " weight: " + str(round(weight_distance, 2)))
        """
        return distance

    def returnLastInnovation(self, gen):
        lastIN = 0
        for connection in gen:
            if connection.innovation_number > lastIN:
                lastIN = connection.innovation_number

        return lastIN

    def SetInitialTopology(self, inputs, outputs):
        firstMember = Genome()
        firstMember.InitGenome(inputs, outputs)
        firstSpecie = Specie(firstMember, self)
        firstMember.SetSpecie(firstSpecie)
        self.species = [firstSpecie]

        for i in range(1, self.initialPopulation):
            member = copy.deepcopy(firstMember)
            # Mudança completas dos pesos da rede inicial
            member.RandonWeightVariation(1, 1)
            member.ID = Genome.ID
            Genome.ID += 1  # Mudança do ID do Genoma
            self.addMember(member)

    def GetAllMembers(self):
        members = []  # Os membros são objetos do tipo Genome
        for specie in self.species:
            members += specie.members

        return members

    def addMember(self, member):
        match = False
        # Verifica se existe alguma espécie que comporte o novo membro
        for specie in self.species:
            added = specie.addMember(member)
            if added:
                match = True
                break
        # Se não existir uma espécie adequada, é criada uma nova espécie
        if not match:
            newSpecie = Specie(member, self)
            self.species.append(newSpecie)

    def removeSpecie(self, specie_to_del):
        try:
            index = self.species.index(specie_to_del)
            self.species.__delitem__(index)
        except:
            pass

    def RandomUpdate(self):
        for member in self.GetAllMembers():
            if random.random() <= self.probMemberMutation:
                # Variação aleatória dos pesos
                member.RandonWeightVariation(self.probRandomWeightVariation, 1)
                # Se o membro for o representante da espécie, os outros membros devem ser reavaliados
                if member == member.OwnerSpecie.RepresentationMember:
                    member.OwnerSpecie.RevalidateMembers()
                else:
                    # Analisando se o membro ainda pertence a mesma espécie
                    if self.CalcDistance(member, member.OwnerSpecie.RepresentationMember) >= self.DeltaTHR:
                        member.MemberDeath()
                        member.ID = Genome.ID
                        self.addMember(member)
                        Genome.ID += 1

            newMember = copy.deepcopy(member)
            new = False
            # Criação de nó aleatórios
            if random.random() < self.probRandomNode:
                member.RandomNode()
                new = True

            # Criação de conexões aleatórias
            if random.random() < self.probRandomConnection:
                member.RandomConnection()
                new = True

            if new:
                newMember.ID = Genome.ID
                Genome.ID += 1  # Mudança do ID do Genoma
                self.addMember(newMember)

    def PrintSpecies(self):
        for specie in self.species:
            text = "Espécie " + str(specie.ID) + " com " + \
                str(specie.SpeciePopulation()) + " membros"

            membros = ""
            scores = []
            for member in specie.members:
                membros += ", " + str(member.ID)
                scores.append(member.score)
            print(text + " " + membros[2:] + ' | Melhos score: ' + str(round(np.max(scores), 2)))

    def Selection(self, survivors):
        if survivors >= len(self.GetAllMembers()):
            pass
        else:
            scores = []
            for member in self.GetAllMembers():
                scores.append(member.score)

            scores.sort(reverse=True)
            thr = scores[survivors]

            for member in self.GetAllMembers():
                if member.score <= thr and len(self.GetAllMembers()) >= survivors:
                    member.MemberDeath()

# Definição de algumas funções úteis


def RandSim():
    rand = 2 * (random.random() - 0.5)
    return rand
