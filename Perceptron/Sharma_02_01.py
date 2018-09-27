# Sharma, Roopam
# 1001-559-960
# 2018-09-24
# Assignment-02-01
import Sharma_02_02
import sys

if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from matplotlib import colors as c
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.backends.tkagg as tkagg
import random

class MainWindow(tk.Tk):
	# This class creates and controls the main window frames and widgets
	def __init__(self, debug_print_flag=False):
		tk.Tk.__init__(self)
		self.debug_print_flag = debug_print_flag
		self.rowconfigure(0,weight=1)
		self.columnconfigure(0,weight=1)
		self.master_frame = tk.Frame(self)
		self.master_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		# set the properties of the row and columns in the master frame
		self.master_frame.rowconfigure(0, weight=15,uniform='xx')
		self.master_frame.columnconfigure(0, weight=1, minsize=200, uniform='xx')
		# create the frame for placing plot and controls
		self.model_frame = tk.Frame(self.master_frame)
		# Arrange the widgets
		self.model_frame.grid(row=0, pady=(0,40),sticky=tk.N + tk.E + tk.S + tk.W)
		# Create an object for plotting graphs in the left frame
		self.display_activation_functions = ModelFrame(self, self.model_frame, debug_print_flag=self.debug_print_flag)

class ModelFrame:
	"""
	This class creates the plot frame and sliders and buttons
	"""
	def __init__(self, root, master, debug_print_flag=False):
		self.master = master
		self.root = root
		#########################################################################
		#  Set up the constants and default values
		#########################################################################
		self.xmin = -10
		self.xmax = 10
		self.ymin = -10
		self.ymax = 10
		self.input_weights = [1,1]
		self.bias = 0.0
		self.data = []
		self.activation_type = "SymmetricHardLimit"
		#########################################################################
		#  Set up the plotting frame and controls frame
		#########################################################################
		# row widget size
		master.rowconfigure(0, weight=1)
		#column widget size
		master.columnconfigure(0, weight=1)
		master.columnconfigure(1, weight=1)
		self.plot_frame = tk.Frame(self.master)
		self.plot_frame.grid(row=0,columnspan =2,sticky=tk.N+tk.S+tk.E+tk.W)
		# stretch the figure to cover full row and column
		self.plot_frame.grid_columnconfigure(0,weight=1)
		self.plot_frame.grid_rowconfigure(0, weight=1)
		self.figure = plt.figure()
		self.axes = self.figure.gca()
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
		self.plot_widget = self.canvas.get_tk_widget()
		self.plot_widget.grid(row=0,sticky=tk.N+tk.S+tk.E+tk.W)
		# Create a frame to contain all the controls such as sliders, buttons, ...
		self.controls_frame1 = tk.Frame(self.master)
		self.controls_frame2 = tk.Frame(self.master)
		self.controls_frame1.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.controls_frame2.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
		#########################################################################
		#  Set up the control widgets such as sliders and selection boxes
		#########################################################################
		self.controls_frame1.rowconfigure(0, weight=1)
		self.controls_frame1.rowconfigure(1, weight=1)
		self.controls_frame1.rowconfigure(2, weight=1)
		self.controls_frame2.rowconfigure(0, weight=1)
		self.controls_frame2.rowconfigure(1, weight=1)
		self.controls_frame2.rowconfigure(2, weight=1)
		self.controls_frame2.rowconfigure(3, weight=1)
		self.controls_frame1.columnconfigure(0, weight=2)
		self.controls_frame1.columnconfigure(1, weight=2)
		self.controls_frame2.columnconfigure(0, weight=2)
		self.controls_frame2.columnconfigure(1, weight=2)
		self.controls_frame2.columnconfigure(2, weight=2)
		self.input_weight_slider1 = tk.Scale(self.controls_frame1, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
		                                    from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
		                                    activebackground="#FF0000", highlightcolor="#00FFFF", label="Weight 1",
		                                    command=lambda event: self.input_weight_slider1_callback())
		self.input_weight_slider1.set(self.input_weights[0])
		self.input_weight_slider1.bind("<ButtonRelease-1>", lambda event: self.input_weight_slider1_callback())
		self.input_weight_slider1.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

		self.input_weight_slider2 = tk.Scale(self.controls_frame1, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
											 from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
											 activebackground="#FF0000", highlightcolor="#00FFFF", label="Weight 2",
											 command=lambda event: self.input_weight_slider2_callback())
		self.input_weight_slider2.set(self.input_weights[1])
		self.input_weight_slider2.bind("<ButtonRelease-1>", lambda event: self.input_weight_slider2_callback())
		self.input_weight_slider2.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

		self.bias_slider = tk.Scale(self.controls_frame1, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=-10.0,
		                            to_=10.0, resolution=0.01, bg="#DDDDDD", activebackground="#FF0000",
		                            highlightcolor="#00FFFF", label="Bias",
		                            command=lambda event: self.bias_slider_callback())
		self.bias_slider.set(self.bias)
		self.bias_slider.bind("<ButtonRelease-1>", lambda event: self.bias_slider_callback())
		self.bias_slider.grid(row=2, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
		#########################################################################
		#  Set up the frame for drop down selection
		#########################################################################
		self.label_for_activation_function = tk.Label(self.controls_frame2, text="Activation Function Type:",
		                                              justify="left")
		self.label_for_activation_function.grid(row=2, column=1, sticky=tk.S)
		self.activation_function_variable = tk.StringVar()
		self.activation_function_dropdown = tk.OptionMenu(self.controls_frame2, self.activation_function_variable,
		                                                  "SymmetricHardLimit", "Linear","tanh", command=lambda
				event: self.activation_function_dropdown_callback())
		self.activation_function_variable.set("SymmetricHardLimit")
		self.activation_function_dropdown.grid(row=3, column=1,sticky=tk.N)
		self.random_data = tk.Button(self.controls_frame2, text="Create Random Data", command=self.create_random_data)
		self.random_data.grid(row=0, column=1,sticky=tk.S)
		self.train_model = tk.Button(self.controls_frame2, text="Train", command=self.train_model)
		self.train_model.grid(row=1, column=1,sticky=tk.N)

	def create_random_data(self):
		random_values = []
		for i in range(2):
			random_values.append((random.randint(-10,10),random.randint(-10,10),1))
		for i in range(2):
			random_values.append((random.randint(-10,10),random.randint(-10,10),-1))
		self.data = pd.DataFrame(random_values)
		print("Random_data: ")
		print(self.data)
		self.displayMesh()

	def display_random_data(self):
		self.axes.scatter(self.data.iloc[:2, 0], self.data.iloc[:2, 1], marker="s", color="yellow")
		self.axes.scatter(self.data.iloc[2:, 0], self.data.iloc[2:, 1], marker="^", color="blue")
		plt.title(self.activation_type)

	def displayMesh(self):
		self.axes.cla()
		resolution = 100
		xs = np.linspace(-10., 10., resolution)
		ys = np.linspace(-10., 10., resolution)
		xx, yy = np.meshgrid(xs, ys)
		zz = Sharma_02_02.calculate_activation_function(self.input_weights, self.bias, np.array([xx,yy]),self.activation_type)
		if self.activation_type=="SymmetricHardLimit":
			color = c.ListedColormap(['r', 'g'])
			self.axes.pcolormesh(xs, ys, zz,cmap=color)
		else:
			self.axes.pcolormesh(xs, ys, zz)
		plt.xlim(self.xmin, self.xmax)
		plt.ylim(self.ymin, self.ymax)
		ys = self.plotline(xs, self.input_weights, self.bias)
		self.axes.plot(xs, ys)
		if len(self.data)>0:
			self.display_random_data()
		self.canvas.draw()

	def plotline(self,x,w,b):
		y = -b/w[1] - w[0]*x/w[1]
		return y

	def train_model(self):
		if len(self.data)>0:
			for i in range(100):
				t = self.data.iloc[:,2]
				self.input_weights,self.bias = Sharma_02_02.calculate_error(self.input_weights,self.bias,self.data,self.activation_type)
				self.displayMesh()
				# for reflecting the learnt weights and bias in main window but can have value out of range of -10 to 10
				#self.input_weight_slider1.set(self.input_weights[0])
				#self.input_weight_slider2.set(self.input_weights[1])
				#self.bias_slider.set(self.bias)
			print("Learned Weights:", self.input_weights)
			print("Learned Bias:", self.bias)
			print("Random_data: ")
			print(self.data)

	def input_weight_slider1_callback(self):
		self.input_weights[0] = np.float(self.input_weight_slider1.get())
		self.displayMesh()

	def input_weight_slider2_callback(self):
		self.input_weights[1] = np.float(self.input_weight_slider2.get())
		self.displayMesh()

	def bias_slider_callback(self):
		self.bias = np.float(self.bias_slider.get())
		self.displayMesh()

	def activation_function_dropdown_callback(self):
		self.activation_type = self.activation_function_variable.get()
		self.displayMesh()

# confirm function
def close_window_callback(root):
	if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()

main_window = MainWindow(debug_print_flag=False)
# main_window.geometry("500x500")
# set the state of the main window
main_window.wm_state('normal')
# window title
main_window.title('Assignment_02 --  Sharma')
# window size
main_window.minsize(600, 600)
# function for closing the window and calls confirm function before closing
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
# to keep window running
main_window.mainloop()