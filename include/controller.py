#!/opt/local/bin/python3

import os
import sys
import tkinter as tk
sys.path.append('include')
import model
import view

class Controller():
	def __init__(self):	
		self.model =model.Model()
		self.view = view.View(self)

	def Lattice(self, Npart, boxsize,para):
		return self.model.Lattice(Npart,boxsize,para)


	def InitVelo(self,Npart,boxsize,temp, para):
		self.model.InitVelo(Npart,boxsize,temp,para)

	def Verlet(self,Npart, coor, boxsize, para,mass):
		return self.model.Verlet(Npart, coor, boxsize, para, mass)

	def GetEnergy(self):
		return self.model.GetEnergy()

	def getcwd(self):
		return os.getcwd()



if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()

