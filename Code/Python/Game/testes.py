import matplotlib.pyplot as plt
from DynamicGraphs import Chart
import random
import time

MyGraph = plt.subplots()
plt.xlabel("Amostra")
plt.ylabel("Valor")

MyChart = Chart()
MyChart.setPlot(MyGraph)
MyChart.setXaxisType("absolute_time")

x = range(0, 200)
y = []
for i in x:
    MyChart.appendData(random.random())
    MyChart.plot()
    time.sleep(0.01)
