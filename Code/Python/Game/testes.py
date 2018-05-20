from pyvis.network import Network
import random

net = Network()
net.inherit_edge_colors_from(False)


nodes = 10
net.add_nodes(range(1, nodes + 1))

cons = 10
for i in range(0, cons):
    nodeFrom = random.randint(1, nodes)
    nodeTo = random.randint(1, nodes)
    weight = random.random() * (-1)**random.randint(0, 1)
    net.add_edge(nodeFrom, nodeTo, value = weight)


net.show_buttons()

net.edges[0].update({'color': 'red'})

print(net.html)

a = net.options.edges
print(a)

net.show("Leo.html")