from PyQt5.QtWidgets import QSizePolicy,QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class PlotCanvas_left(FigureCanvas):
    def __init__(self, parent= QLabel, iterations=[], all=[], all_name=[]):
        fig = Figure(figsize=(10,8),dpi=100)
        fig.clear()
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(iterations, all, all_name)

    def plot(self,iterations,all,all_name):
        ax = self.figure.add_subplot(2,2,1)
        self.plt_figure(ax,iterations, 0, all_name, all)

        ax1 = self.figure.add_subplot(2, 2, 2)
        self.plt_figure(ax1,iterations, 1, all_name, all)

        ax2 = self.figure.add_subplot(2, 2, 3)
        self.plt_figure(ax2,iterations, 2, all_name, all)

        ax3 = self.figure.add_subplot(2, 2, 4)
        self.plt_figure(ax3,iterations, 3, all_name, all)

        self.show()

    # 画图
    def plt_figure(self, ax, iterations, i, all_name, all):
        new_ticks = np.arange(0, 1400, 200)
        ax.set_xticks(new_ticks)
        if len(iterations) == 31:ax.set_xlabel("x")
        else:ax.set_xlabel("Iterations")
        ax.set_ylabel(all_name[i])
        ax.plot(iterations, all[i])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

class PlotCanvas_right(FigureCanvas):
    def __init__(self, parent=QLabel, iterations=[], Partial=[]):
        fig = Figure(figsize=(10, 8), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(iterations,Partial)

    def plot(self,iterations,Partial):
        ax = self.figure.add_subplot(1,1,1)
        # plt.title("time derivatives of nondimensional density and velocity(i=16)")
        ax.set_ylim(10 ** (-7), 1)
        ax.set_yscale('log')
        l1, = ax.plot(iterations, Partial[0], linestyle='-', color='blue')
        l2, = ax.plot(iterations, Partial[1], linestyle='--', color='red')
        ax.legend(handles=[l1, l2], labels=['Partial_rho_t', 'Partial_V_t'], loc='best')

        self.show()

    # 画图
    def plt_figure(self,ax,iterations,i, all_name, all):
        new_ticks = np.arange(0, 1400, 200)
        ax.set_xticks(new_ticks)
        ax.set_xlabel("Iterations")
        ax.set_ylabel(all_name[i])
        ax.plot(iterations, all[i])

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # axis = ax.gca()
        # axis.spines['top'].set_color('none')
        # axis.spines['right'].set_color('none')
        # #
        # axis.xaxis.set_ticks_position('bottom')
        # axis.yaxis.set_ticks_position('left')
        # # axis.spines['bottom'].set_position(('data',0))
        # axis.spines['left'].set_position(('data', 0))

