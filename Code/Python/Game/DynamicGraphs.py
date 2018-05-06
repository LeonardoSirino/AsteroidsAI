import matplotlib.pyplot as plt
import time

class Chart:
    def __init__(self):
        import matplotlib.pyplot as plt
        import time
        plt.ion()
        self.lastX = 0
        self.x = []
        self.y = []
        self.Xaxis = "sample"
        self.__xTypes = ["sample", "relative_time", "absolute_time"]
        """
        sample - numeração sequencial dos valores no eixo X
        relative_time - numeração com base no tempo relativo de chegada da amostra em y
        absolute_time - numeração com base no tempo absoluto de chegada da amostra em y
        """

    def setPlot(self, PlotAndAxis):
        self.figure, self.ax = PlotAndAxis
        self.lines, = self.ax.plot([], [], '-')
        self.ax.set_autoscaley_on(True)

    def appendData(self, data):
        self.y.append(data)

        if self.Xaxis == "sample":
            x = self.lastX + 1
            self.x.append(x)
            self.lastX += 1
        elif self.Xaxis == "relative_time":
            if self.lastX == 0:
                self.lastX == time.time()
                self.x.append(0)
            else:
                x = time.time() - self.lastX
                self.x.append(x)
        elif self.Xaxis == "absolute_time":
            self.x.append(time.time())

    def setXaxisType(self, type):
        valid = False
        for valid_type in self.__xTypes:
            if type == valid_type:
                valid = True
                break

        if valid:
            self.Xaxis = type
        else:
            print("Este tipo de eixo X não existe")

    def plot(self):
        self.lines.set_xdata(self.x)
        self.lines.set_ydata(self.y)

        self.ax.relim()
        self.ax.autoscale_view()

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        plt.show()
