try:
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.widgets import Slider, Button, RadioButtons
except ImportError:
	raise ImportError('Some of the modules are not installed')
"""
Program: A simple GUI for maps from dynamical systems written purely in python with the 
		 above imported modules.
Date: 21.10.2015
"""

class Maps():
	""" 
	This class contains various maps for (q, p). It does not support many
	pairs of q-s and p-s. Also everything will be as q and p, no phis or
	thetas or sigmas or 
	Goals:
	-map should contain the information on various constants for control
	schematics of the interface.

	"""

	#The slider contains the controlled constants.
	#ADD THE CONSTANTS OF A MAP HERE
	slider={'StandardMap' : ['K',],
			'AdjustedStandardMap': ['K','L',],
			'ArnoldCatMap' : [],
			'HarperMap':['K','L']
	}
	#ADD THE MODUL OF A MAP HERE
	modul= {'StandardMap': 2.0*np.pi,
			'AdjustedStandardMap': 2.0*np.pi,
			'ArnoldCatMap': 1.0,
			'HarperMap':2.0*np.pi,
	}
	steps = 1000
	def __init__(self):
		# REGISTER NEWLY ADDED FUNCTIONS HERE
		self.maps = {'StandardMap':self.Std_map,
		'AdjustedStandardMap':self.Adj_Std_Map,
		'ArnoldCatMap':self.Arnold_Cat_Map,
		'HarperMap':self.Harper_map,
		}
	def Std_map(self, data, *args, **kwargs):
		""" 
		Standard map or Chirikov map:
		q[i+1] = q[i] + p[i] %  mod(2*Pi)
		p[i+1] = p[i] + K * sin(q[i+1]) %  mod(2*Pi)
		"""
		K, q_0, p_0 = data['K'], data['q_0'], data['p_0'] 
		if len(q_0) != len(p_0):
			print('Wrong size of pairs! len(q_0)= ',len(q_0),' len(p_0)= ',len(p_0))
			return None
		else: pass
		N = len(q_0)
		q = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(N)])
		p = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(N)])
		q[:,0] = q_0
		p[:,0] = p_0
		for i in range(N):
			for j in range(self.steps-1):
				q[i][j+1] = (q[i][j] + p[i][j]) % (2.0 * np.pi)
				p[i][j+1] = (p[i][j] + K * np.sin(q[i][j+1])) % (2.0 * np.pi)
		return q,p
	def Adj_Std_Map(self, data, *args, **kwargs):
		""" 
		"Slightly" changed Chirikov map:
		q[i+1] = q[i] - K * np.sin(p[i] %  mod(2*Pi)
		p[i+1] = p[i] + L * sin(q[i+1]) %  mod(2*Pi)
		"""
		K, L, q_0, p_0 = data['K'], data['L'], data['q_0'], data['p_0']
		if len(q_0) != len(p_0):
			print('Wrong size of pairs! len(q_0)= ',len(q_0),' len(p_0)= ',len(p_0))
			return None
		else:
			size_of_0 = len(q_0)
			q = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			p = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			q[:,0] = q_0
			p[:,0] = p_0
			print(data)
			for i in range(size_of_0):
				for j in range(self.steps-1):

					q[i][j+1] = (q[i][j] - K * np.sin(p[i][j])) % (2.0 * np.pi)
					p[i][j+1] = (p[i][j] + L * np.sin(q[i][j+1])) % (2.0 * np.pi)
			#print(q,p)
			return q,p
	def Arnold_Cat_Map(self, data, *args, **kwargs):
		"""The arnold map:
		q[i+1] = 2*q[i] + p[i] %  1
		p[i+1] = q[i] + p[i] %  1
		"""
		q_0, p_0 = data['q_0'], data['p_0']
		if len(q_0) != len(p_0):
			print('Wrong size of pairs! len(q_0)= ',len(q_0),' len(p_0)= ',len(p_0))
			return None
		else:
			size_of_0 = len(q_0)
			q = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			p = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			q[:,0] = q_0
			p[:,0] = p_0
			print(data)
			for i in range(size_of_0):
				for j in range(self.steps-1):

					q[i][j+1] = (2*q[i][j] + p[i][j]) % (1.0)
					p[i][j+1] = (q[i][j] + p[i][j]) % (1.0)
			#print(q,p)
			return q,p
	def Harper_map(self, data, *args, **kwargs):
		"""The Harper map:
		q[i+1] = q[i] - K * sin(p[i]) %  2Pi
		p[i+1] = p[i] + L * sin(q[i] - K * sin(p[i])) %  2Pi
		"""
		K, L, q_0, p_0 = data['K'], data['L'], data['q_0'], data['p_0']
		if len(q_0) != len(p_0):
			print('Wrong size of pairs! len(q_0)= ',len(q_0),' len(p_0)= ',len(p_0))
			return None
		else:
			size_of_0 = len(q_0)
			q = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			p = np.array([np.array([0.0 for i in range(self.steps)]) for j in range(size_of_0)])
			q[:,0] = q_0
			p[:,0] = p_0
			print(data)
			for i in range(size_of_0):
				for j in range(self.steps-1):
					q[i][j+1] = (q[i][j] - K * np.sin(p[i][j])) % (2.0 * np.pi)
					p[i][j+1] = (p[i][j] + L * np.sin(q[i][j] - K * np.sin(p[i][j]))) % (2.0 * np.pi)
			#print(q,p)
			return q,p


class GUI():
	""" 
	This is the Graphical User Interface for maps from Dynamical systems.
	Goals:
	-Draw various maps. Semi-done
	-Accept input new function
	-* maybe save said custom function
	-* maybe create the necessary new bars (tools) for controlling the
	constants in said custom function
	-* maybe make it neat
	"""
	color_pallete = ['b','r','g','c','y','w']
	axcolor = 'lightgoldenrodyellow'
	current_slider_container={}
	default_Map = 'HarperMap'

	def __init__(self):

		self.f = plt.figure()
		plt.subplots_adjust(bottom=0.25)
		self.ax = self.f.add_subplot(111)

		self.maps = Maps() 

		self.cid = self.f.canvas.mpl_connect('button_press_event', self._onclick) # Bind click to canvas
		self.start()

	def start(self):
		#Creating additional buttons
		#Choose installed functions button
		Menu_dim = [0.01, 0.15, 0.1, 0.05] # [Left, Away from bottom, Length, Width]

		"""
		The "menu" buttons options.
		"""
		maps = self.maps.maps.keys()
		self._menu_button_container = {}
		for i, function in enumerate(maps):#Create a button for each function.
			axes = self.f.add_axes([Menu_dim[0], Menu_dim[1]+ (i+1) * 0.05, Menu_dim[2], Menu_dim[3]])
			button = Button(axes, function)
			cid = button.on_clicked(self.selected_function)
			self._menu_button_container[function] = [axes, button, cid]
		self.prepare_interface(self.default_Map)

	def prepare_interface(self, map):

		self.current_map = map
		self.current_constants = self.maps.slider[self.current_map]
		#Create axes or basically the constant slider controls.
		self.create_axes(self.maps.slider[self.current_map])
		self.ax.set_title(self.current_map)
		
	def create_axes(self, list_of_axes):
		"""Creates Axes and attaches Slider widgets to them
		and populates them to the current slider container dictionary.
		"""
		#Default dimensions
		def_dim = [0.17, 0.05, 0.65, 0.03]
		del_bottom = 0.04

		for i in range(len(list_of_axes)):
			name = list_of_axes[i]

			dim = def_dim
			dim[1] += i * del_bottom #Raising axes one above the other

			axes = self.f.add_axes(dim, axisbg = self.axcolor) # Creating the Axes.
			slider = Slider(axes,name, 0, 10, valinit = 1) # Widget need the Axes

			slider.on_changed(self._update) # Bind the widget to update function

			self.current_slider_container[list_of_axes[i]] = [axes, slider]
		return None

	def change_to_new_map(self, name_of_function):
		"""This function changes the interface to the new map."""
		#First clean the current control axes and plot
		self.ax.clear()
		self.clean_axes()
		self.prepare_interface(name_of_function)

	def clean_axes(self):
		"""This cleans the controls when a new map is chosen."""
		for item in self.current_slider_container.items():
			self.f.delaxes(item[1][0])
		self.current_slider_container = {} #Basically deleting the axes and everything.

	def _onclick(self, event):
		if event.xdata==None or event.ydata==None: return None
		if event.inaxes.__str__()!='Axes(0.125,0.25;0.775x0.65)': return None #I know this looks funny, but I don't know how to check on which object you clicked...
		#print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata), event.inaxes)
		#print(event)
		data = {}
		for const in self.current_constants:
			data[const] = np.float(self.current_slider_container[const][1].val)
		data['q_0'] = [event.xdata]
		data['p_0'] = [event.ydata]
		#ax.clear()
		q,p = self.maps.maps[self.current_map](data)		
		self.ax.set_xlim(0, self.maps.modul[self.current_map])
		self.ax.set_ylim(0, self.maps.modul[self.current_map])
		for i in range(len(q)):
			self.ax.plot(q[i],p[i],'o',color = np.random.choice(self.color_pallete), ms=2.0, linewidth=1.2)
		self.f.canvas.draw()

	def _update(self, event):
		"""
		Upon selecting a value on a bar, this function just clears the plot.
		"""
		self.ax.clear()
		self.ax.set_title(self.current_map)
	def selected_function(self, event):
		"""Because, you don't get the name of the Axes... you have to compare the dimensions with the other axes of the
		menu buttons... How funny is that. Yeah, it's not.
		"""
		#First get the name of the function
		for item in self._menu_button_container.items():
			if item[1][0] == event.inaxes: #Comparing the axes dimensions as the only source of identification
				name_of_function = item[0]
		#print(name_of_function)
		self.change_to_new_map(name_of_function)


if __name__ == '__main__':
	x=GUI()
	plt.show()
