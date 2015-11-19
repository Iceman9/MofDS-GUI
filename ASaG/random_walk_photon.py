import numpy as np
import matplotlib.pyplot as plt
from time import sleep

class Random_Walk_Photon():
	N=10000
	Orig_num = 10000
	def __init__(self):
		self.f = plt.figure()
		self.ax, self.ax_2 = self.f.add_subplot(121), self.f.add_subplot(122)
		x=np.linspace(0,2*np.pi, 1000)
		self.ax.grid(which='both')

		#self.ax.plot(np.sin(x), np.cos(x))
		self.pos_x = [0.0 for i in range(self.N)]
		self.pos_y = [0.0 for i in range(self.N)]

		self.ax_2.plot(0.0, 0,'o')

		self.counter=1.0
		self._to_be_removed=[]
		self._start()
	def _start(self):
		#Random distribution with angle.
		self.ax.clear()
		x=np.linspace(0,2*np.pi, 100)

		self.ax.plot(np.sin(x), np.cos(x))
		self.ax.plot(0.3*np.sin(x), 0.3*np.cos(x))
		povprečje = 0.0
		for i in range(self.N):
			rand_angle = np.random.random()*2*np.pi
			length = self.free_path(self.pos_x[i], self.pos_y[i])
			self.pos_x[i] = self.pos_x[i] + np.cos(rand_angle)*length
			self.pos_y[i] = self.pos_y[i] + np.sin(rand_angle)*length
			velikost = np.sqrt(self.pos_x[i]*self.pos_x[i] + self.pos_y[i]*self.pos_y[i])
			if velikost >= 1:
				#The reason not normally append is that the lower indexes comes first
				#Deleting the element at the normal index first cause the array to move
				#left, thus making deleting at a higher index lead to index out of bounds.
				self._to_be_removed=[i]+self._to_be_removed 

			else:
				povprečje += velikost
		povprečje/=(self.N - len(self._to_be_removed))
		self._remove()
		self.ax.plot(self.pos_x, self.pos_y,'o', ms=1)
		self.ax_2.plot(np.sqrt(self.counter), povprečje, 'o', color='b')
		#self.ax_2.plot(self.counter, len(self.pos_x)/self.Orig_num, 'o-', color='r')
		self.counter+=1
		self.f.canvas.draw()
		plt.pause(0.01)
		self._start()

	def free_path(self, x, y):
		if x**2 + y**2>0.09: _free_path = np.float64(1/20)
		else: _free_path = np.float64(1/25)
		return _free_path
	def _remove(self):
		for el in self._to_be_removed:
			self.pos_x.remove(self.pos_x[el])
			self.pos_y.remove(self.pos_y[el])
			self.pos_x.append(0)
			self.pos_y.append(0)
		self.N-=len(self._to_be_removed)
		self._to_be_removed=[]
		return None

if __name__ == '__main__':
	DO_THE_MONKEY=Random_Walk_Photon()
	plt.show()
