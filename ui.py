from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import matplotlib.pyplot as plt
from geometry import *

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shape Analysis")
        self.setGeometry(0, 0, 600, 400)

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.central_layout)

        self.main_frame = QFrame(self.central_widget)
        self.main_layout = QVBoxLayout(self.main_frame)

        self.input_frame = QFrame(self.main_frame)
        self.input_layout = QGridLayout(self.input_frame)

        self.x_spinbox = QSpinBox(self.input_frame)
        self.x_spinbox.setPrefix("X: ")
        self.x_spinbox.setMinimum(-16)
        self.x_spinbox.setMaximum(16)
        self.input_layout.addWidget(self.x_spinbox, 1, 1, 1, 1)

        self.y_spinbox = QSpinBox(self.input_frame)
        self.y_spinbox.setPrefix("Y: ")
        self.y_spinbox.setMinimum(-16)
        self.y_spinbox.setMaximum(16)
        self.input_layout.addWidget(self.y_spinbox, 3, 1, 1, 1)

        self.add_button = QPushButton(self.input_frame)
        self.add_button.setText("Add")
        self.add_button.clicked.connect(self.spinbox_add_point)
        self.input_layout.addWidget(self.add_button, 1, 2, 1, 1)

        self.remove_button = QPushButton(self.input_frame)
        self.remove_button.setText("Remove")
        self.remove_button.clicked.connect(self.spinbox_remove_point)
        self.input_layout.addWidget(self.remove_button, 3, 2, 1, 1)

        self.clear_button = QPushButton(self.input_frame)
        self.clear_button.setText("Clear")
        self.clear_button.clicked.connect(self.clear_points)
        self.input_layout.addWidget(self.clear_button, 3, 3, 1, 1)

        self.random_frame = QFrame(self.input_frame)
        self.random_layout = QHBoxLayout(self.random_frame)
        self.random_layout.setContentsMargins(0, 0, 0, 0)

        self.random_button = QPushButton(self.random_frame)
        self.random_button.setText("Random")
        self.random_button.clicked.connect(self.random_point)
        self.random_layout.addWidget(self.random_button)

        self.random_spinbox = QSpinBox(self.random_frame)
        self.random_spinbox.setMinimum(1)
        self.random_spinbox.setMaximum(100)
        self.random_layout.addWidget(self.random_spinbox)

        self.input_layout.addWidget(self.random_frame, 1, 3, 1, 1)
        self.main_layout.addWidget(self.input_frame)

        self.plot_frame = QFrame(self.main_frame)
        self.plot_layout = QHBoxLayout(self.plot_frame)

        self.plot_table = QTableWidget(self.plot_frame)
        self.plot_table.setColumnCount(2)
        self.plot_table.horizontalHeader().setStretchLastSection(True)
        self.plot_table.setHorizontalHeaderLabels(["X","Y"])
        self.plot_layout.addWidget(self.plot_table)

        self.main_layout.addWidget(self.plot_frame)
        self.central_layout.addWidget(self.main_frame)
    
    def get_point(self):
        point = np.array([int(self.x_spinbox.text()[3:]), int(self.y_spinbox.text()[3:])])
        return point

    def spinbox_add_point(self):
        point = self.get_point()
        if not any(np.array_equal(p, point) for p in point_list):
            self.add_point(point)
    
    def spinbox_remove_point(self):
        point = self.get_point()
        if any(np.array_equal(p, point) for p in point_list):
            self.remove_point(point)

    def add_point(self, point):
            point_list.append(point)
            self.update_points()

    def remove_point(self, point):
        global point_list
        new_point_list = []
        update = False
        for p in point_list:
            if not np.array_equal(p, point):  
                new_point_list.append(p)
        point_list = new_point_list.copy()
        self.update_points()
    
    def clear_points(self):
        point_list.clear()
        self.update_plot()

    def random_point(self):
        print("random point")

    def create_plot(self):
        global fig, axes
        fig, axes = plt.subplots()
        self.set_axes()
        fig.canvas.mpl_connect("button_press_event", self.click_plot)
        plt.gca().set_aspect("equal", adjustable = "box")
    
    def set_axes(self):
        axes.set_title("Points")
        axes.set_xlim(-16, 16)
        axes.set_ylim(-16, 16)
        axes.set_xticks(np.arange(-16, 17), minor = True)
        axes.set_yticks(np.arange(-16, 17), minor = True)
        axes.grid(which= "major", alpha = 0.6)
        axes.grid(which= "minor", alpha = 0.3)
    
    def update_points(self):
        self.update_table()
        self.update_plot()

    def update_table(self):
        self.plot_table.setRowCount(len(point_list))

        for n, p in enumerate(point_list):
            self.plot_table.setItem(n, 0, QTableWidgetItem(str(p[0])))
            self.plot_table.setItem(n, 1, QTableWidgetItem(str(p[1])))
    
    def update_plot(self):
        if not plt.fignum_exists(1):
            self.create_plot()
        plt.cla()
        self.set_axes()
        print(point_list)
        for p in point_list:
            axes.plot(p[0], p[1], marker= "o", markersize = 3, color = "blue")
        
        plt.show()

    def click_plot(self, event):
        try:
            x, y = event.xdata, event.ydata
            point = np.array([int(round(x)), int(round(y))])
            if any(np.array_equal(p, point) for p in point_list):
                self.remove_point(point)
            else:
                self.add_point(point)
        except:
            pass