"""
拉法尔喷管的一维等熵流动解析解（包括亚音速—超音速和全亚音速喷管）
@author: 许韶光
@date: 2020.12.26
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from function.plotCanvas import PlotCanvas_left

# plt.rcParams.update({'font.sans-serif': "SimHei",
#                      'mathtext.fontset': 'custom',
#                      'mathtext.rm': 'Arial',
#                      })  # 用来正常显示中文标签和负号


def shapeA(x, laval_type):
    """
    定义喷管形状，假设喷管的长度为0<=x<=3，type变量为1即亚声速-超声速喷管，type变量为2即全亚声速喷管。
    :param x:
    :param laval_type:
    :return: A
    """
    "亚声速-超声速喷管"
    if laval_type == 1:
        A = 1 + 2.2 * (x - 1.5) ** 2
    " 全亚声速喷管 "
    if laval_type == 2:
        if type(x) == np.ndarray:
            A = np.empty(x.shape[0])
            for i in range(x.shape[0]):
                if x[i] <= 1.5:
                    A[i] = 1 + 2.2 * (x[i] - 1.5) ** 2
                else:
                    A[i] = 1 + 0.2223 * (x[i] - 1.5) ** 2
        else:
            if x <= 1.5:
                A = 1 + 2.2 * (x - 1.5) ** 2
            else:
                A = 1 + 0.2223 * (x - 1.5) ** 2

    return A


def initial(x, laval_type):
    """
    定义初始条件，t=0时密度rho，温度T，速度V沿喷管沿程的初始值，type值同shape()函数
    :param x:
    :param laval_type:
    :return: rho,T,V
    """
    "亚声速-超声速喷管"
    if laval_type == 1:
        rho = 1 - 0.314 * x
        T = 1 - 0.2314 * x
        V = (0.1 + 1.09 * x) * np.sqrt(T)
    " 全亚声速喷管 "
    if laval_type == 2:
        rho = 1 - 0.023 * x
        T = 1 - 0.009333 * x
        V = 0.05 + 0.11 * x
    return rho, T, V


def Mach_and_A(Ma, A):
    """
    Mach和A的解析解公式，和analysis_compute关联。
    :param Ma:
    :param A:
    :return:
    """
    return (5 / 6 * (1 + 0.2 * Ma ** 2)) ** 3 - A * Ma  # A=A/A_Star，以gamma=1.4直接求得的方程


def analysis_compute(laval_type, Discrete=31):
    """
    数值解的主计算函数，以gamma=1.4直接求得。  #全亚音速管中设压力比pe/p0=0.93
    :param laval_type: type变量为1即亚声速-超声速喷管，type变量为2即全亚声速喷管。
    :param Discrete: 要画的点数，值越大画的点越密集，相对的dx就越小
    :return: Ma, rho, T, p, x
    """
    x_max = 3
    dx = x_max / (Discrete - 1)
    x = np.arange(0, x_max + dx, dx)  # arange函数不包括终点所以需要多加一个dx
    A = shapeA(x, laval_type)
    if laval_type == 2:
        Mach_e = np.sqrt((0.93 ** (-0.4 / 1.4) - 1) / 0.2)  # pe/p0=0.93,你可以再多写一个改变这个比值的接口，我比较懒哈哈哈哈
        A_e = shapeA(3, laval_type)  # 出口处面积
        A_star = A_e * Mach_e * (2 / 2.4 * (1 + 0.2 * Mach_e ** 2)) ** (-1.2 / 0.4)  # 解析解的推导
        print(A_star)
    if laval_type == 1:
        A_star = 1

    Ma = np.zeros(A.shape[0])
    for i in range(A.shape[0]):
        Mach_root = fsolve(Mach_and_A, [0, 10], args=A[i] / A_star)
        '''scipy的fsolve函数用来求根，Mach关于A的数值解有两个根。
        第一个变量是求根的方程，第二个变量是解可能存在的区间，第三个变量是需要输入求根方程的其他参数'''
        if laval_type == 1:
            if x[i] < 1.5:
                Ma[i] = min(Mach_root)
            elif x[i] >= 1.5:
                Ma[i] = max(Mach_root)
        else:
            Ma[i] = min(Mach_root)
    p = (1 + 0.4 / 2 * Ma ** 2) ** (-1.4 / 0.4)
    rho = (1 + 0.4 / 2 * Ma ** 2) ** (-1 / 0.4)
    T = (1 + 0.4 / 2 * Ma ** 2) ** (-1)

    all = [rho, T, p, Ma]
    all_name = ["rho/rho0", "T/T0", "p/p0", "Ma"] 
    return all, all_name, x

# all, all_name, x = analysis_compute(laval_type=1)
# PlotCanvas_left(parent=None,iterations=x,all=all,all_name=all_name)


