""" -*- coding: utf-8 -*-
#
==========================================
Interactive 3D scatterplot (GUI)
==========================================

Plotting 3 dimensional (X-Y-Z) data using matplotlib 3D scatter plot. Two datasets are available:
1) randomized data in the range of 0-100 in all axis, which varies on each button pressing [Test Random]
2) iris (flower) dataset from Python scikitLearn package [Test Iris]
With the help of this (fixed window size) GUI 3 dimansional data can be (scatter) plotted and rearranged 
- by limiting the range along one or all axis,
- by rotating the plot with mouse gestures.

Key Features:
    1)  Buttons
        A) The [Test Random] and [Test Iris] buttons load the corresponding dataset and plot it.
        B) Apply Button:
         when clicked, it retrieves the values from the editable fields (see below) and applies them to the plot, updating the axis limits.
         No field should remain empty!
        C) Reset Button:
         the axis limits are reset to their optimal values (which are the minimum and maximum of the actual data points along each corresponding axis).
         This ensures that all points become visible. Use this button if any plot axis range has been changed previously.
        D) Clear button:
         all loaded data is cleared from the plot.
         
    2) Editable Fields:
        Each axis (X, Y, Z) has a pair of fields for the minimum and maximum values to limit the related axis to a certain range.
        These fields are editable, allowing users to input custom values and consequently exclude some parts of the full dataset from the plot.
        Push "Apply" button after limits have been modified.
    
    3) Title (Label): a text indicating the title of the current plot.

Original idea came from a clustered data plot in which a part of the full dataset should have been shown only and verified from different angles. This is not doable with a simple Matplotlib plot.
    
Initialization:
On startup, the editable fields are filled in with the optimal limits (i.e., the min and max of the loaded data values).

Limits Calculation: The get_optimal_limits method in the Plot3DWidget class calculates the min and max values for each axis, which are initially populated in the editable fields.
Dynamic Plot Updates: The set_axes_limits method allows dynamic updates to the axis limits based on user input from the editable fields.

Updating the Title (Label):
Whenever plot_random_data or plot_clusters_data is called ("TEST random", "TEST iris" buttons), a (QT Event) signal is emitted that updates the text in the MainWindow label.

Python modules required:
    - sys
    - random
    - PyQt5
    - matplotlib, mpl_toolkits
    - numpy
    - sklearn

Possible functionality developments:
    - resizable window
    - editable fields value check, user defined number should fall in the min-max range
    - determining clusters for the Iris data using SciKitLearn
    - UX design development (e.g. inactive/active buttons and editable fields)

@author: Data4Every1
Created on Thu Sep  5 20:58:00 2024

"""

import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QLabel, QLineEdit, QHBoxLayout, QFormLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSignal

model = 0
first_run = 1
from sklearn import datasets

iris = datasets.load_iris()
irisX = iris.data
irisy = iris.target
global x_min, x_max, y_min, y_max, z_min, z_max

class Plot3DWidget(FigureCanvas):
    # Signal to update text in MainWindow
    update_text = pyqtSignal(str)
    update_editables = pyqtSignal()
    
    def __init__(self, parent=None):
        
        # Create the figure and 3D axis
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Call the parent constructor
        super().__init__(self.fig)

        # Store the parent window for later use
        self.setParent(parent) # 
        self.main_window = MainWindow  # Store reference to MainWindow
        
        # Initialize the plot with random data
        self.x_data, self.y_data, self.z_data = np.float64(0) , np.float64(0), np.float64(0) #self.generate_random_data()
        
        self.cluster_button = QPushButton('TEST Iris') # Model
        self.cluster_button.setFixedWidth(60)
        self.cluster_button.clicked.connect(self.plot_clusters_data)

        self.clear_button = QPushButton('Clear')
        self.clear_button.setFixedWidth(60)
        self.clear_button.clicked.connect(self.clear_plot)

    def generate_random_data(self):
        # Generate random 3D data
        x = np.random.rand(50) * 100
        y = np.random.rand(50) * 100
        z = np.random.rand(50) * 100
        return x, y, z

    def plot_random_data(self):
        global x_min, x_max, y_min, y_max, z_min, z_max
        model = 1
        # Clear the current plot
        self.ax.clear()
        
        # self.x_data, self.y_data, self.z_data = 
        X,Y,Z = self.generate_random_data()
        
        # Scatter plot the random data
        # self.ax.scatter(self.x_data, self.y_data, self.z_data)
        self.plot_XYZ(X,Y,Z)

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Set the limits for each axis based on the current data
        self.ax.set_xlim([0, self.x_data.max()]) # self.x_data.min()
        self.ax.set_ylim([0, self.y_data.max()]) # self.y_data.min()
        self.ax.set_zlim([0, self.z_data.max()]) # self.z_data.min()

        # Redraw the figure
        self.draw()
        
        # Emit a signal to update the text panel in the main window
        self.update_text.emit('Plot: Random X-Y-Z data - (0-100)')
        self.update_editables.emit()
        
    def plot_clusters_data(self):
        global irisX, first_run, model
        global x_min, x_max, y_min, y_max, z_min, z_max
        # Clear the current plot
        self.ax.clear()

        # Scatter plot the random data
        # self.x_data, self.y_data, self.z_data = 
        self.plot_XYZ(irisX[:, 3], irisX[:, 0], irisX[:, 2])
        self.ax.scatter(self.x_data, self.y_data, self.z_data)

        # Set axis labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        x_min, x_max, y_min, y_max, z_min, z_max = self.get_optimal_limits()
        
        # Set the limits for each axis based on the current data
        self.ax.set_xlim([0, self.x_data.max()]) # self.x_data.min()
        self.ax.set_ylim([0, self.y_data.max()]) # self.y_data.min()
        self.ax.set_zlim([0, self.z_data.max()]) # self.z_data.min()

        # Redraw the figure
        self.draw()
        
        # Emit a signal to update the text panel in the main window
        self.update_text.emit('Plot: SciKitLearn - Iris dataset')
        self.update_editables.emit()
        
    def plot_XYZ(self, X, Y, Z):
        self.x_data, self.y_data, self.z_data = X, Y, Z
        self.ax.scatter(self.x_data, self.y_data, self.z_data)
        
    def clear_plot(self):
        self.ax.clear()
        self.ax.scatter([], [], [])
        self.ax.set_xlim([0, 1]) 
        self.ax.set_ylim([0, 1]) 
        self.ax.set_zlim([0, 1])       

    def set_axes_limits(self, x_min, x_max, y_min, y_max, z_min, z_max):
        #Set the limits for X, Y, Z axes.#
        self.ax.set_xlim([x_min, x_max])
        self.ax.set_ylim([y_min, y_max])
        self.ax.set_zlim([z_min, z_max])
        self.draw()

    def get_optimal_limits(self):
        #Calculate optimal min/max values for each axis based on data.#
        global first_run
        if first_run: # and model:
            x_min = y_min = z_min = 0
            first_run = 0
        else:
            x_min = self.x_data.min()
            y_min = self.y_data.min()
            z_min = self.z_data.min()
        return (x_min, self.x_data.max(),
                y_min, self.y_data.max(),
                z_min, self.z_data.max())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.plot_window = Plot3DWidget() #self)  # Store reference to Plot3DWidget
        # Create the plot widget
        self.plot_widget = Plot3DWidget(self)
        self.plot_widget.setFixedWidth(720)
        
        # Set up the main window
        self.setWindowTitle('3D Scatter Plot - Axis Controls')
        self.setGeometry(100, 100, 900, 600)
        
        # Create the QLabel (Text panel) and set initial text
        self.text_panel = QLabel('Push any TEST button')  # Initial text in the panel
        self.text_panel.setFixedHeight(30)
        # Connect the update_text signal to the method that updates the label
        self.plot_widget.update_text.connect(self.update_text_panel)
        self.plot_widget.update_editables.connect(self.set_optimal_limits_to_fields)
    
        # Create the TEST button (top left)
        self.model_button = QPushButton('TEST Random') # Model
        self.model_button.setFixedWidth(100)
        self.model_button.clicked.connect(self.plot_widget.plot_random_data)
        
        self.cluster_button = QPushButton('TEST Iris') # Model
        self.cluster_button.setFixedWidth(100)
        self.cluster_button.clicked.connect(self.plot_widget.plot_clusters_data)
    
        # Create editable fields for X, Y, Z min/max values
        self.x_min_field = QLineEdit()
        self.x_min_field.setFixedWidth(80)
        self.x_max_field = QLineEdit()
        self.x_max_field.setFixedWidth(80)
        self.y_min_field = QLineEdit()
        self.y_min_field.setFixedWidth(80)
        self.y_max_field = QLineEdit()
        self.y_max_field.setFixedWidth(80)
        self.z_min_field = QLineEdit()
        self.z_min_field.setFixedWidth(80)
        self.z_max_field = QLineEdit()
        self.z_max_field.setFixedWidth(80)
    
        # Create the Apply button
        self.apply_button = QPushButton('Apply')
        self.apply_button.clicked.connect(self.apply_limits)
        self.apply_button.setFixedWidth(80)
        
        # Create the Clear button
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_plot)
        self.clear_button.setFixedWidth(80)
    
        # Create the Reset button
        self.reset_button = QPushButton('Reset XYZ')
        self.reset_button.clicked.connect(self.reset_limits)
        self.reset_button.setFixedWidth(80)
    
        # Create the left-side layout for X, Y, Z editable fields
        form_layout = QFormLayout()
        form_layout.addRow(QLabel('X Min'), self.x_min_field)
        form_layout.addRow(QLabel('X Max'), self.x_max_field)
        form_layout.addRow(QLabel('Y Min'), self.y_min_field)
        form_layout.addRow(QLabel('Y Max'), self.y_max_field)
        form_layout.addRow(QLabel('Z Min'), self.z_min_field)
        form_layout.addRow(QLabel('Z Max'), self.z_max_field)
    
        # Create a vertical layout for the buttons and editable fields
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.model_button)  # Add Model button at the top
        left_layout.addWidget(self.cluster_button)  # Add Clusters button at the top
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.apply_button)
        left_layout.addWidget(self.reset_button)
        left_layout.addWidget(self.clear_button)
    
        # Set initial values for the editable fields based on optimal limits
        self.set_optimal_limits_to_fields()
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.text_panel)  # Add the QLabel to your layout
        right_layout.addWidget(self.plot_widget)
        
        # Create a layout to hold both the plot and the controls
        main_layout = QHBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
    
        main_layout.addWidget(left_widget)  # Add controls on the left
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        # main_layout.addWidget(self.plot_widget)  # Add the plot on the right
        
        main_layout.addWidget(right_widget)  # Add text & plot on the right
        
        # Create a central widget for the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def update_text_panel(self, new_text):
        #Update the text in the label panel.#
        self.text_panel.setText(new_text)
        self.text_panel.repaint()  # Force label refresh

    def set_optimal_limits_to_fields(self):
        global x_min, x_max, y_min, y_max, z_min, z_max
        #Set the optimal axis limits to the editable fields.#
        x_min, x_max, y_min, y_max, z_min, z_max = self.plot_widget.get_optimal_limits()
        
        #round values up to 2 decimals
        self.x_min_field.setText(str(round(x_min,2)))
        self.x_max_field.setText(str(round(x_max,2)))
        self.y_min_field.setText(str(round(y_min,2)))
        self.y_max_field.setText(str(round(y_max,2)))
        self.z_min_field.setText(str(round(z_min,2)))
        self.z_max_field.setText(str(round(z_max,2)))

    def apply_limits(self):
        #Apply the limits from the editable fields to the plot.#
        try:
            x_min = float(self.x_min_field.text())
            x_max = float(self.x_max_field.text())
            y_min = float(self.y_min_field.text())
            y_max = float(self.y_max_field.text())
            z_min = float(self.z_min_field.text())
            z_max = float(self.z_max_field.text())

            # Apply the new limits to the plot
            self.plot_widget.set_axes_limits(x_min, x_max, y_min, y_max, z_min, z_max)
        except ValueError:
            # If the user enters invalid values, handle it (optional)
            print('Invalid input. Please enter valid numbers.')

    def reset_limits(self):
        #Reset the axis limits to the default optimal values.#
        self.set_optimal_limits_to_fields()
        self.apply_limits()  # Reapply the default limits
        
    def plot_random_data(self):
        global x_min, x_max, y_min, y_max, z_min, z_max
        #Calls the plot_random_data method of Plot3DWidget#
        self.plot_widget.plot_random_data()
        self.text_panel.setText('Plot: Random X-Y-Z data - (0-100)')  # Update text in the panel
        # Force the label to refresh in case UI is lagging behind
        self.text_panel.repaint()
        # Emit a signal to update the text panel in the main window
        self.update_text.emit('Plot: Random X-Y-Z data - (0-100)')
        
    def plot_clusters_data(self):
        global x_min, x_max, y_min, y_max, z_min, z_max
        #Calls the plot_random_data method of Plot3DWidget#
        self.plot_widget.plot_clusters_data()
        self.text_panel.setText('Plot: SciKitLearn - Iris dataset')  # Update text in the panel
        self.update_text_panel(self, 'Plot: SciKitLearn - Iris dataset')
        self.set_optimal_limits_to_fields(self)
        # Force the label to refresh in case UI is lagging behind
        self.text_panel.repaint() 
        
    def clear_plot(self):
        self.plot_widget.clear_plot()
        self.apply_limits()  # Reapply the default limits
        # Modify the text on the panel
        self.text_panel.setText('Plot cleared!')  # Update text in the panel
        
    def update_text_panel(self, new_text):
        #Update the text in the label panel.#
        self.text_panel.setText(new_text)
        self.text_panel.repaint()  # Force label refresh

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
