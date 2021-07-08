###################################################
###########  拟一维亚声速-超声速喷管流动数值解  #########
###########       @author: 张文睿          #########
###########       @date: 2020.12.25      ##########
###################################################

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from function.numerical_compute import Main_Function
from PyQt5.QtGui import QIntValidator
from function.plotCanvas import PlotCanvas_left,PlotCanvas_right
from function.analysis_compute import analysis_compute

# -------------------- 布局 -----------------------#
def hBoxLayout(button1,button2,button3=None):
    hbox = QHBoxLayout()
    hbox.setContentsMargins(200,0,200,0)
    hbox.addWidget(button1,stretch=1)
    hbox.addWidget(button2,stretch=1)
    if button3 != None:hbox.addWidget(button3, stretch=1)
    return hbox

def vBoxLayout(figure=None ,hbox=None, line=None,figure_box=None):
    vbox = QVBoxLayout()
    if line != None : vbox.addWidget(line, stretch=1)
    if figure!= None : vbox.addWidget(figure,stretch=5)
    if figure_box != None : vbox.addLayout(figure_box,stretch=20)
    if hbox != None : vbox.addLayout(hbox,stretch=1)

    return vbox
# -----------------------------------------------#


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(720, 750)
        self.center()
        self.setWindowTitle('CFD')

        self.title = QLabel(self)
        self.title.setText('拟一维亚声速-超声速喷管流动\n(柯朗数C=0.5)')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color:black")
        self.title.setFont(QFont("Roman times", 20, QFont.Bold))

        question_1 = QLabel(self)
        question_1.setText('请输入网格点 i 值,查看喷管处相应变化图: ')
        question_1.setStyleSheet("color:black")
        question_1.setFont(QFont("Roman times", 12, QFont.Bold))
        question_1_pix = QPixmap('fig.png')
        question_1_label = QLabel(self)
        question_1_label.setMaximumSize(280,80)
        question_1_label.setPixmap(question_1_pix)
        question_1_label.setScaledContents(True)

        question_2 = QLabel(self)
        question_2.setText('请输入时间步数 iter ,查看对应时间步数的流场变量:')
        question_2.setStyleSheet("color:black")
        question_2.setFont(QFont("Roman times", 12, QFont.Bold))
        question_2_pix = QPixmap('table.png')
        question_2_label = QLabel(self)
        question_2_label.setMaximumSize(280,80)
        question_2_label.setPixmap(question_2_pix)
        question_2_label.setScaledContents(True)

        self.input_1 = QLineEdit(self)
        self.input_2 = QLineEdit(self)
        self.input_1_button = QPushButton("查看对应曲线")
        self.input_2_button = QPushButton("查看对应表格")

        ana_label = QLabel(self)
        ana_label.setText('亚声速-超声速等熵流动解析解')
        ana_label.setStyleSheet("color:black")
        ana_label.setFont(QFont("Roman times", 12, QFont.Bold))
        self.ana_button = QPushButton(self)
        self.ana_button.setText('查看解析解')
        ana_box = QHBoxLayout()
        ana_box.addWidget(ana_label,stretch=2)
        ana_box.addWidget(self.ana_button,stretch=1)
        ana_box.setContentsMargins(0,0,200,50)

        # 布局
        question_1_hbox = hBoxLayout(question_1,question_1_label)
        question_1_hbox.setContentsMargins(0,0,20,20)
        question_2_hbox = hBoxLayout(question_2, question_2_label)
        question_2_hbox.setContentsMargins(0, 0, 20, 20)
        h_box_1 = hBoxLayout(self.input_1,self.input_1_button)
        h_box_2 = hBoxLayout(self.input_2, self.input_2_button)
        v_box_final = QVBoxLayout(self)
        v_box_final.addWidget(self.title,stretch=1)
        v_box_final.addLayout(ana_box,stretch=1)
        v_box_final.addLayout(question_1_hbox,stretch=1)
        v_box_final.addLayout(h_box_1,stretch=1)
        v_box_final.addLayout(question_2_hbox,stretch=1)
        v_box_final.addLayout(h_box_2,stretch=1)
        self.setLayout(v_box_final)


    def center(self):
        # 获得窗口
        frame = self.frameGeometry()

        # 此处加括号要说明一下,正常我们调用函数如: def data(x):
        #   c = data   // 打印的是函数体或者说函数的地址;
        # 而c = data() // 打印的是函数运行的结果;
        # 此处我的理解是应该找到窗口坐标,要层层递进地运行函数,找到中心点
        center_point = QDesktopWidget().availableGeometry().center()

        # 窗口显示到中心
        frame.moveCenter(center_point)
        # 将窗口赋值到self,qt以topleft为坐标原点,所以移动到窗口
        self.move(frame.topLeft())

    def error(self):
        self.title.setText("Error")

    # 处理切换窗口信号
    def handle_click(self):
        if not self.isVisible(): self.show()

    def figure_plot(self):
        print("图已绘制:\n")


    def num_table(self):
        try:
            point_table = self.input_2.text()
            self.title.setText('拟一维超声速和亚声速熵')
            return point_table
        except:
            self.title.setText('请重新输入数字:')

    def num_fig(self):
        try:
            point_fig = self.input_1.text()
            self.title.setText('拟一维超声速和亚声速熵')
            return point_fig
        except:
            self.title.setText('请重新输入数字:')

################################ 子窗口 ########################################
class SubWidget(QWidget):

# -------------  窗口主程序定义 -----------------------#
    def __init__(self,flag):
        super(SubWidget, self).__init__()
        # self.resize(720, 600)
        # self.center()
        self.flag =flag

        self.back_button = QPushButton(self)
        self.back_button.setText('返回到主界面')
        if self.flag == 0:
            self.resize(1900, 1100)
            self.center()
            self.setWindowTitle('亚声速-超音速等熵流动的数值解曲线图')
            # 定义按钮
            self.page_value = QLineEdit(self)
            self.toPages = QPushButton(self)
            self.toPages.setText('跳转到相应时间步长的流程图')

            self.title_fig = QLabel(self)
            self.title_fig.setAlignment(Qt.AlignCenter)

            # todo 显示图像
            self.little_lable_1 = QLabel(self)
            self.little_lable_2 = QLabel(self)


            self.label_box = QHBoxLayout()
            self.label_box.addWidget(self.little_lable_1,stretch=10)
            self.label_box.addWidget(self.little_lable_2, stretch=10)
            h_box = hBoxLayout(self.page_value, self.toPages,self.back_button)
            h_box.setContentsMargins(500, 50, 500, 50)
            v_box = vBoxLayout(figure=None,hbox=h_box,line=self.title_fig,figure_box=self.label_box)


        else:
            self.resize(720, 720)
            self.setWindowTitle('亚声速-超音速等熵流动的数值解表格图')
            self.center()
            self.page_value = QLineEdit(self)
            self.toPages = QPushButton(self)
            self.toPages.setText('跳转到相应i值的表格')

            self.title = QLabel(self)
            self.title.setAlignment(Qt.AlignCenter)

            self.little_lable = QLabel(self)
            self.little_lable.setAlignment(Qt.AlignCenter)

            h_box = hBoxLayout(self.page_value, self.toPages,self.back_button)
            v_box = vBoxLayout(self.little_lable, h_box, self.title)
        self.setLayout(v_box)
# -------------------------------------------------#

    def fig2label(self):
        m_1 = PlotCanvas_left(self.little_lable_1, iterations, self.all, self.all_name)
        m_2 = PlotCanvas_right(self.little_lable_2, iterations, self.Partial)

# ------------------ 确定窗口位置 -----------------#
    def center(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
# -----------------------------------------------#

# ------------------ 窗口切换信号 -----------------#
    def sub_win_show(self):
        if not self.isVisible(): self.show()

############################################## Fig曲线窗口系列的处理事件 #######################################################
    def handle_click_fig(self):
        # int() 强制转换失败的原因,是因为初始值为空,无法进行转换,需要进行输入数字才能再转换,所以这个功能不能默认开启,需要先输入值,然后按钮来实现打开获取值,再int
        point = main_win.num_fig()
        num = int(point)
        if num == 0:
            fig_title = "\n######### i={}所对应的图 ########\n".format(num)
        elif num != 0:
            fig_title = "\n######### i={}所对应的图 ########\n".format(num)
        else:
            self.title_fig.setText("请返回上一层输入数字")
        return num, fig_title


    def fig_init_page(self):
        try:
            num,fig_title = self.handle_click_fig()
            self.title_fig.setText(fig_title)
            self.title_fig.setStyleSheet("color:black")
            self.title_fig.setFont(QFont("Roman times", 12, QFont.Bold))
            main_win.title.setStyleSheet("color:black")
            self.toPages.clicked.connect(self.change_page_fig)
            self.all, self.all_name, self.Partial = Main_Function().eachIter_value(num)
            self.fig2label()
        except:
            main_win.title.setText('请检查输入格式是否错误:(1 =< i <= 31):')
            main_win.title.setStyleSheet("color:red")
            main_win.title.setFont(QFont("Roman times", 16, QFont.Bold))
            self.title_fig.setText('请返回上一界面检查输入格式是否错误:(1 =< i <= 31):')
            self.title_fig.setStyleSheet("color:red")
            self.title_fig.setFont(QFont("Roman times", 16, QFont.Bold))

    def change_page_fig(self):
        try:
            page_temp = self.page_value.text()
            page = int(page_temp)
            self.title_fig.setText("\n######### i={}所对应的图 ########\n".format(page))
            self.title_fig.setStyleSheet("color:black")
            main_win.title.setText('拟一维亚声速-超声速喷管流动\n(柯朗数C=0.5)')
            main_win.title.setStyleSheet("color:black")
            main_win.title.setFont(QFont("Roman times", 20, QFont.Bold))
            self.all, self.all_name, self.Partial = Main_Function().eachIter_value(page)
            self.fig2label()

        except:
            self.title_fig.setText('请检查输入格式是否错误:(1 =< i <= 31):')
            self.title_fig.setStyleSheet("color:red")
            self.title_fig.setFont(QFont("Roman times", 16, QFont.Bold))

#############################################################################################################################


############################################## table表格窗口系列的处理事件 #######################################################
    def handle_click_table(self):
        # int() 强制转换失败的原因,是因为初始值为空,无法进行转换,需要进行输入数字才能再转换,所以这个功能不能默认开启,需要先输入值,然后按钮来实现打开获取值,再int
        point = main_win.num_table()
        num = int(point)
        if num == 0:
            table_title = "\n######### 喷管条件和初始条件 ########\n"
        elif num != 0:
            table_title = "\n######## {}个时间步后的流场参数 ########\n".format(num)
        else:
            self.title.setText("请返回上一层输入数字")
        return num, table_title

    def table_init_page(self):
        try:
            num, table_title = self.handle_click_table()
            self.title.setText(table_title)
            self.title.setStyleSheet("color:black")
            self.title.setFont(QFont("Roman times", 12, QFont.Bold))
            main_win.title.setStyleSheet("color:black")
            self.little_lable.setText(table_array[num])
            self.toPages.clicked.connect(self.change_page_table)
        except:
            main_win.title.setText('请检查输入格式是否错误:(1 =< iter <= 1500):')
            main_win.title.setStyleSheet("color:red")
            main_win.title.setFont(QFont("Roman times", 16, QFont.Bold))
            self.title.setText('请返回上一界面检查输入格式是否错误:(1 =< iter <= 1500):')
            self.title.setStyleSheet("color:red")
            self.title.setFont(QFont("Roman times", 16, QFont.Bold))
            self.little_lable.setText('Error')


    def change_page_table(self):
        try:
            page_temp = self.page_value.text()
            page = int(page_temp)
            self.little_lable.setText(table_array[page])
            self.title.setText("\n######## {}个时间步后的流场参数 ########\n".format(page))
            self.title.setStyleSheet("color:black")
            main_win.title.setText('拟一维亚声速-超声速喷管流动\n(柯朗数C=0.5)')
            main_win.title.setStyleSheet("color:black")
            main_win.title.setFont(QFont("Roman times", 20, QFont.Bold))
        except:
            self.title.setText('请检查输入格式是否错误:(0 =< iter <= 1500)')
            self.title.setStyleSheet("color:red")
            self.title.setFont(QFont("Roman times", 16, QFont.Bold))
            self.little_lable.setText('Error')

    def error(self):
        self.title.setText("Error")




################################ 子窗口2222222 ########################################
class SubWidget_2(QWidget):

# -------------  窗口主程序定义 -----------------------#
    def __init__(self):
        super(SubWidget_2, self).__init__()
        self.resize(1080, 1000)
        # self.resize(1440, 800)
        self.back_button = QPushButton(self)
        self.back_button.setText('返回到主界面')
        back_box = QHBoxLayout()
        back_box.addWidget(self.back_button,stretch=1)
        back_box.setContentsMargins(320,3,320,10)
        self.center()
        self.setWindowTitle('亚声速-超音速等熵流动的解析解曲线图')

        self.title_fig = QLabel(self)
        self.title_fig.setAlignment(Qt.AlignCenter)
        self.title_fig.setText('亚声速-超音速等熵流动的解析解')
        self.title_fig.setStyleSheet("color:black")
        self.title_fig.setFont(QFont("Roman times", 16, QFont.Bold))

        # todo 显示图像
        self.fig = QLabel(self)
        self.fig.setScaledContents(True)
        # fig_box = QHBoxLayout()
        # fig_box.addWidget(self.fig, stretch=1)
        # fig_box.setContentsMargins(20,0,20,0)

        label_box = QVBoxLayout(self)
        label_box.addWidget(self.title_fig,stretch=1)
        label_box.addWidget(self.fig, stretch=8)
        # label_box.addLayout(fig_box, stretch=10)
        label_box.addLayout(back_box,stretch=1)
        self.setLayout(label_box)
# -------------------------------------------------#

    # ------------------ 确定窗口位置 -----------------#
    def center(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    # ------------------ 窗口切换信号 -----------------#
    def sub_win_show(self):
        if not self.isVisible(): self.show()

    def fig_init_page(self):
        self.title_fig.setStyleSheet("color:black")
        main_win.title.setText('拟一维亚声速-超声速喷管流动\n(柯朗数C=0.5)')
        main_win.title.setStyleSheet("color:black")
        main_win.title.setFont(QFont("Roman times", 20, QFont.Bold))
        all, all_name, x = analysis_compute(laval_type=1)
        PlotCanvas_left(parent=self.fig, iterations=x, all=all, all_name=all_name)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWidget()

    table_array, iterations  = Main_Function().implement_function()

    sub_figure_win = SubWidget(flag=0)
    sub_table_win = SubWidget(flag=1)
    sub_ana_win = SubWidget_2()

    # 主窗口 切换到 1
    try:
        main_win.input_1_button.clicked.connect(main_win.hide)
        main_win.input_1_button.clicked.connect(sub_figure_win.sub_win_show)
        main_win.input_1_button.clicked.connect(sub_figure_win.fig_init_page)
    except:
        main_win.error()

    # 主窗口 切换到 2
    try:
        main_win.input_2_button.clicked.connect(main_win.hide)
        main_win.input_2_button.clicked.connect(sub_table_win.sub_win_show)
        main_win.input_2_button.clicked.connect(sub_table_win.table_init_page)
    except:
        main_win.error()

    # 子窗口2 切回
    try:
        sub_table_win.back_button.clicked.connect(sub_table_win.hide)
        sub_table_win.back_button.clicked.connect(main_win.handle_click)

    except:
        sub_table_win.error()

    # 子窗口1 切回
    try:
        sub_figure_win.back_button.clicked.connect(sub_figure_win.hide)
        sub_figure_win.back_button.clicked.connect(main_win.handle_click)
    except:
        sub_figure_win.error()


    # 主窗口 切换到 ana
    main_win.ana_button.clicked.connect(main_win.hide)
    main_win.ana_button.clicked.connect(sub_ana_win.sub_win_show)
    main_win.ana_button.clicked.connect(sub_ana_win.fig_init_page)

    # ana 切回
    sub_ana_win.back_button.clicked.connect(sub_ana_win.hide)
    sub_ana_win.back_button.clicked.connect(main_win.handle_click)



    main_win.show()
    sys.exit(app.exec_())