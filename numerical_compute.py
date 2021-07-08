import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import prettytable as pt
import re


#---------------------------------------------- 主程序 -----------------------------------------------------------#
class Main_Function(object):
    def __init__(self):
        table_array, iterations = self.implement_function()
    def implement_function(self):
        # 理想气体比热比  gamma = cp/cv
        gamma = 1.4
        delta_x = 0.1
        x_num = int(3 / delta_x + 1)  # 0=<x<=3
        x = np.linspace(0, 3, x_num)

        # 设置最大迭代步数
        max_Iteration = 1500

        iterations,table_array = [],[]
        self.rho_eachIter, self.T_eachIter, self.Ma_eachIter, self.p_eachIter, \
        self.Partial_rho_t_all, self.Partial_V_t_all = [],[],[],[],[],[]

        # -------------初始化，无量纲量,并列出喷管形状和初始值----------------#
        A = self.pipeline_shape(x)
        rho, T, V = self.initial_condition(x)
        Ma = V / np.sqrt(T)
        # 初始值
        all_value_initial = [x, A, rho, V, T]
        table_title, data = self.iter_table(0, all_value_initial)
        table_array.append(data)

        C = 0.5  # 柯朗数,小于等于 1;从精度考虑，尽可能接近 1
        for i in range(max_Iteration):
            # 绘制 喉口处 无量纲温度 和 无量纲密度
            iterations.append(i)

            a = np.sqrt(T)  # 无量纲的音速
            delta_t = min(C * delta_x / (np.abs(V) + a))  # 计算最大允许时间推进步长

        #-------------------------------------1st:预测步,采用向前差分 forward_partial  -----------------------------------------------------------------------
            Partial_rho_t = - rho[1:-1] * self.forward_partial(V, delta_x) - rho[1:-1] * V[1:-1] * self.forward_partial(
                    np.log(A), delta_x) - V[1:-1] * self.forward_partial(rho, delta_x)
            Partial_V_t = -V[1:-1] * self.forward_partial(V, delta_x) - (1.0 / gamma) * (
                    self.forward_partial(T, delta_x) + (T[1:-1] / rho[1:-1]) * self.forward_partial(rho, delta_x))
            Partial_T_t = -V[1:-1] * self.forward_partial(T, delta_x) - (gamma - 1.0) * T[1:-1] * (
                    self.forward_partial(V, delta_x) + V[1:-1] * self.forward_partial(np.log(A), delta_x))

            # 得到的预测量
            rho_pred = self.final_rho_or_T(rho, Partial_rho_t, delta_t)
            V_pred = self.final_V(V, Partial_V_t, delta_t)
            T_pred = self.final_rho_or_T(T, Partial_T_t, delta_t)

        #-----------------------------------2nd: 修正步 采用后向差分 backward_partial ------------------------------------------------------------------------
            Partial_rho_t_pred = (-V_pred[1:-1] * self.backward_partial(rho_pred, delta_x)
                                  - rho_pred[1:-1] * self.backward_partial(V_pred, delta_x)
                                  - rho_pred[1:-1] * V_pred[1:-1] * self.backward_partial(np.log(A), delta_x))
            Partial_V_t_pred = (-V_pred[1:-1] * self.backward_partial(V_pred, delta_x)
                                - 1.0 / gamma * self.backward_partial(T_pred, delta_x)
                                - 1.0 / gamma * T_pred[1:-1] / rho_pred[1:-1] * self.backward_partial(rho_pred, delta_x))
            Partial_T_t_pred = (-V_pred[1:-1] * self.backward_partial(T_pred, delta_x)
                                - (gamma - 1.0) * T_pred[1:-1] * self.backward_partial(V_pred, delta_x)
                                - (gamma - 1.0) * T_pred[1:-1] * V_pred[1:-1] * self.backward_partial(np.log(A), delta_x))

            # 平均值
            # 注意:此处得到的_mean shape:29  而原初始值 shape:31   猜想:因为首尾不进行前后向差分,所以在最后修正值需要首尾补0
            Partial_rho_t_mean = 0.5 * (Partial_rho_t_pred + Partial_rho_t)
            Partial_V_t_mean = 0.5 * (Partial_V_t_pred + Partial_V_t)
            Partial_T_t_mean = 0.5 * (Partial_T_t_pred + Partial_T_t)

            # t+delta_t时刻的流动参数的修正值
            rho = self.final_rho_or_T(rho, Partial_rho_t_mean, delta_t)
            V = self.final_V(V, Partial_V_t_mean, delta_t)
            T = self.final_rho_or_T(T, Partial_T_t_mean, delta_t)


            Ma = V / np.sqrt(T)
            p = rho * T
            all_value = [x,A,rho,V,T,p,Ma]

            table_title, data = self.iter_table(i + 1, all_value)
            table_array.append(data)

            # 注意名称对应i=16的位置显示,但是编成是以0开始的,所以代号用15
            self.rho_eachIter.append(rho)
            self.T_eachIter.append(T)
            self. Ma_eachIter.append(Ma)
            self.p_eachIter.append(p)
            # mean的shape是29,因为把首尾去掉了,作前后差分操作,所以对应i=16的代号为14
            self.Partial_rho_t_all.append(np.abs(Partial_rho_t_mean))
            self.Partial_V_t_all.append(np.abs(Partial_V_t_mean))

        return table_array, iterations

    # 喷管截面形状
    def pipeline_shape(self,x):
        return 1 + 2.2 * (x - 1.5) ** 2

    # 初始条件
    def initial_condition(self,x):
        rho = 1 - 0.3146 * x
        T = 1 - 0.2314 * x
        V = (0.1 + 1.09 * x) * np.sqrt(T)
        return rho, T, V


    # 绘制表格
    def iter_table(self, num, all_value):
        tb = pt.PrettyTable()
        if num == 0:
            tb.field_names = ["x/l", "A/A*", "rho/rho0", "V/a0", "T/T0"]
            table_title = "######### 喷管条件和初始条件: ########\n"
            for i in range(31):
                a_temp = []
                x_temp = format(all_value[0][i], '.1f')
                A_temp = format(all_value[1][i], '.3f')
                rho_temp = format(all_value[2][i], '.3f')
                V_temp = format(all_value[3][i], '.3f')
                T_temp = format(all_value[4][i], '.3f')
                a_temp = [x_temp, A_temp, rho_temp, V_temp, T_temp]
                tb.add_row(a_temp)
                data = tb.get_string()
        else:
            tb.field_names = ["x/l", "A/A*", "rho/rho0", "V/a0", "T/T0", "P", "Ma"]
            table_title = "\n######## {}个时间步后的流场参数: ########\n".format(num)
            for i in range(31):
                x_temp = format(all_value[0][i], '.1f')
                A_temp = format(all_value[1][i], '.3f')
                rho_temp = format(all_value[2][i], '.3f')
                V_temp = format(all_value[3][i], '.3f')
                T_temp = format(all_value[4][i], '.3f')
                p_temp = format(all_value[5][i], '.3f')
                Ma_temp = format(all_value[6][i], '.3f')
                # a_temp = np.around([A[i],rho[i],V[i],T[i]],decimals=3)
                a_temp = [x_temp,A_temp,rho_temp,V_temp,T_temp,p_temp,Ma_temp]
                tb.add_row(a_temp)
            # todo 改格式
            data = tb.get_string()
            # data = re.sub("P", ' P ',data)
            # data = re.sub('Ma', '  Ma  ',data)
        return table_title,data

    def eachIter_value(self, num):
        rho_i_eachIter, T_i_eachIter, Ma_i_eachIter, p_i_eachIter, \
        Partial_rho_t_i_all, Partial_V_t_i_all = [], [], [], [], [], []
        for i in range(1500):
            rho_i_eachIter.append(self.rho_eachIter[i][num-1])
            T_i_eachIter.append(self.T_eachIter[i][num-1])
            Ma_i_eachIter.append(self.Ma_eachIter[i][num-1])
            p_i_eachIter.append(self.p_eachIter[i][num-1])
            if num != 0 and num != 31:
                Partial_rho_t_i_all.append(self.Partial_rho_t_all[i][num-2])
                Partial_V_t_i_all.append(self.Partial_V_t_all[i][num-2])
            else:
                Partial_rho_t_i_all.append(0)
                Partial_V_t_i_all.append(0)

        all = [rho_i_eachIter, T_i_eachIter, p_i_eachIter, Ma_i_eachIter]
        all_name = ["rho/rho0", "T/T0", "p/p0", "Ma"]
        Partial = [Partial_rho_t_i_all, Partial_V_t_i_all]
        return all,all_name,Partial


    #---------------------- MacCormack 方法 ------------------------#
    # 向前，向后差分计算，输入 N 个数据，输出 N-2 个偏导数(i=0和i=31不带入计算了,没有i=-1,i=32)
    def forward_partial(self,y, delta_x):

        return (y[2:] - y[1:-1]) / delta_x


    def backward_partial(self, y, delta_x):

        return (y[1:-1] - y[:-2]) / delta_x


    def final_rho_or_T(self, original, partial, delta_t):              # (rho, Partial_rho_t_mean, delta_t)
        # 修正
        final_value = original + np.hstack([0, partial, 0]) * delta_t  # 关于补0问题,看下述

        #
        final_value[-1] = 2 * final_value[-2] - final_value[-3]  # 出口处又外插值确定，入口处保持不变
        return final_value


    def final_V(self, V, P_V_t, delta_t):
        final_V = V + np.hstack([0, P_V_t, 0]) * delta_t
        final_V[0] = 2 * final_V[1] - final_V[2]  # 入口的速度可变，外插值确定
        final_V[-1] = 2 * final_V[-2] - final_V[-3]
        return final_V

# if __name__ == '__main__':
#     table_array, iterations, all, all_name, Partial = Main_Function().implement_function()
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())


