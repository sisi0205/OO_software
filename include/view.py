#!/opt/local/bin/python3

import sys,os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
from pygame.locals import *
sys.path.append('include')
import popNoble
#import controller
import model
import para

###matplot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


GEOMETRY = '700x400+2+2'
WIDTH=120
HEIGHT=19

PWIDTH=400
PHEIGHT=400


class Controller(object):
  def __init__(self):
   pass
  def pos(self):
  	pass
  def getcwd(self):
  	pass

class View(object):
	"""docstring for View"""
	def __init__(self, controller):
		
		self.root=tk.Tk()
		root=self.root
		root.bind('<Escape>', lambda event: sys.exit())
		root.title("Molecular Dynamic simulation")
		root.geometry(GEOMETRY)
		self.controller = controller


		self.labelFont = ('Georgia', 10)
		self.boxFont = ('Georgia', 14)
		self.butFont = ('Georgia', 12)
		self.colormap=para.colormap

		self.Tempvalue=300
		self.Numvalue=20
		self.Sizevalue=10
		self.Framevalue=500
		self.Typevalue=1
		self.Typename='He'
		self.Para=para.Paramap["He"]
		self.Mass=para.Massmap["He"]
		self.Color=para.colormap["He"]
		self.Coord=[]
		self.output="output.txt"
		self.stop=False



		self.fileOpt = {}
		self.fileOpt['defaultextension'] = '' 
		self.fileOpt['filetypes'] = [('all files', '.*'), ('text files', '.txt'),("python files","*.py")]
		self.fileOpt['initialdir'] = self.controller.getcwd()
		self.fileOpt['initialfile'] = '*.txt'
		self.fileOpt['parent'] = self.root


		frame1 = tk.Frame(root)
		frame1.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#fda9b2')
		frame1.pack(side=tk.TOP)

		File=tk.Menubutton(frame1, text="File",width=10)
		File.pack(side=tk.LEFT, anchor=tk.W)
		File.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0')
		File.config(font=self.butFont, state=tk.NORMAL)
		File.menu=tk.Menu(File, tearoff = 0)
		File["menu"]=File.menu
		File.menu.add_command(label="Directory", command =self.askdiretory)
		File.menu.add_command(label="Open file", command =self.askopenfile)
		File.menu.add_command(label="Save Current Energy", command =self.saveEnergy)
		File.menu.add_command(label="Save Current Coord", command =self.saveCoord)
		File.menu.add_command(label="Load simulation", command =self.LoadTraj)


		self.build=tk.Button(frame1, text="Build",width=10, command=self.popNoble)
		self.build.pack(side=tk.LEFT, anchor=tk.W)
		self.build.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0')
		self.build.config(font=self.butFont, state=tk.NORMAL)


		Analy=tk.Menubutton(frame1, text="Analysis",width=10)
		Analy.pack(side=tk.LEFT, anchor=tk.W)
		Analy.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0')
		Analy.config(font=self.butFont, state=tk.NORMAL)
		Analy.menu=tk.Menu(Analy, tearoff = 0)
		Analy["menu"]=Analy.menu
		Analy.menu.add_command(label="Display Potential Curve", command =self.Potential)
		Analy.menu.add_command(label="Energy of Current running simulation", command =self.TEnergy)
		Analy.menu.add_command(label="Plot Energy from file", command =self.ReadEnergy)


		start=tk.Button(frame1, text="Start",width=5, command=self.Start)
		start.pack(side=tk.LEFT, anchor=tk.W)
		start.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#f44248')
		start.config(font=self.butFont, state=tk.NORMAL)


		stop=tk.Button(frame1, text="Stop",width=5, command=self.Stop)
		stop.pack(side=tk.LEFT, anchor=tk.W)
		stop.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#f44248')
		stop.config(font=self.butFont, state=tk.NORMAL)

		Continue=tk.Button(frame1, text="Continue",width=6, command=self.Continue)
		Continue.pack(side=tk.LEFT, anchor=tk.W)
		Continue.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#f44248')
		Continue.config(font=self.butFont, state=tk.NORMAL)



		frame2 = tk.Frame(root)
		frame2.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5')
		frame2.pack(side=tk.BOTTOM)

		scrollbar = tk.Scrollbar(frame2)
		scrollbar2 = tk.Scrollbar(frame2)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		scrollbar2.pack(side=tk.BOTTOM,fill="both")

		self.listBox = tk.Listbox(frame2)
		self.listBox.pack( side = tk.TOP, fill = tk.BOTH)
		self.listBox.config( bg='white', bd=5, font=self.boxFont )
		self.listBox.config(width=WIDTH, height=HEIGHT)
		self.listBox.bind('<Double-1>', self.displayItem)
		self.listBox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.listBox.yview)
		self.listBox.config(xscrollcommand=scrollbar2.set)
		scrollbar2.config(command=self.listBox.xview, orient=tk.HORIZONTAL)



		####pygame
		#os.environ['SDL_WINDOWID'] = str(root.winfo_id())
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,200)
		root.update()
		

		pygame.init()
		self.FPS = 30 # frames per second setting
		self.fpsClock = pygame.time.Clock()
		self.DISPLAYSURF = pygame.display.set_mode((PWIDTH, PHEIGHT), 0, 32)
		pygame.display.set_caption('Animation')
		


		self.WHITE = (255, 255, 255)

		self.DISPLAYSURF.fill(self.WHITE)

		while True:
			#frame1.update()		
			for event in pygame.event.get():
				
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
		
			pygame.display.update()
			self.root.update()
			self.fpsClock.tick(self.FPS)


		#self.file.close()	


		#tk.mainloop()

	def askdiretory(self):
		cwd=self.controller.getcwd()
		dirOpt = {}
		dirOpt['initialdir'] = cwd
		dirOpt['mustexist'] = False
		dirOpt['parent'] = self.root
		dirOpt['title'] = 'Select Directory'

		directory = tk.filedialog.askdirectory(**dirOpt)
		print( "askdirectory is:", directory )
		return directory

	def askopenfile(self):

		cwd=self.controller.getcwd()
		self.fileOpt['title'] = 'Select File'
		filename=filedialog.askopenfilename(**self.fileOpt)
		#print( "askopenfilename is:", filename )
		if filename:
			self.openfile(filename)
			return open(filename, 'r')

	
	def openfile(self, filename):
		popup=tk.Toplevel(self.root)
		popup.geometry(GEOMETRY)
		popup.title(filename)

		scrollbar = tk.Scrollbar(popup)
		scrollbar2 = tk.Scrollbar(popup)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		scrollbar2.pack(side=tk.BOTTOM,fill="both")

		listBox = tk.Listbox(popup)
		listBox.pack( side = tk.TOP, fill = tk.BOTH)
		listBox.config( bg='white', bd=5, font=self.boxFont )
		listBox.config(width=WIDTH, height=HEIGHT)
		listBox.bind('<Double-1>', self.displayItem)
		listBox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=listBox.yview)
		self.listBox.config(xscrollcommand=scrollbar2.set)
		scrollbar2.config(command=listBox.xview, orient=tk.HORIZONTAL)

		f=open(filename, 'r')

		f1=f.readlines()
		for x in f1:
			rmbreaker=x[:-1]
			listBox.insert(tk.END,rmbreaker)
		f.close()


	def saveEnergy(self):

		self.fileOpt['title'] = 'Save Energy File'
		f = tk.filedialog.asksaveasfile(**self.fileOpt)
		if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
		    return
		Energy=self.controller.GetEnergy()[0]
		for x in Energy:
			f.write("%f\n"%x)
		f.close()


	def saveCoord(self):
		self.fileOpt['title'] = 'Save Coordinate File'
		f = tk.filedialog.asksaveasfile(**self.fileOpt)
		if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
		    return
		Coord=self.Coord
		#print(self.Coord)
		for coor in Coord:
			for i in range(0,len(coor)):
				f.write(str(coor[i][0])+" "+str(coor[i][1])+",")
			f.write("\n")
			
		f.close()



	def LoadTraj(self):

		self.fileOpt['title'] = 'Select Trajectory File'
		filename = tk.filedialog.askopenfilename(**self.fileOpt)
		coord=[]
		coorxy=[]	

		if filename:
		    openfile=open(filename,"r")
		    line=openfile.readlines()
		    for coor in line:
		    	strip1=coor.split(",")

		    	self.DISPLAYSURF.fill(self.WHITE)

		    	for xy in strip1:
		    		strip2=list(xy.split())
		    		if strip2==[]:
		    			try:
			    			for x in coorxy:
			    				pygame.draw.circle(self.DISPLAYSURF,self.Color, x,10,0)
			    		except:
			    			self.formatwarning()
			    			return

		    			coord.append(coorxy)
		    			coorxy=[]

		    		else:
		    			#print(strip2)
		    			try:
			    			x=int(strip2[0])
			    			y=int(strip2[1])
			    			coorxy.append([x,y])
			    		except:
			    			self.formatwarning()
			    			return

		    	pygame.display.update()
		    	self.root.update()
		    	self.fpsClock.tick(self.FPS)
		    openfile.close()


		#print(coord)
	
	def ReadEnergy(self):

		self.fileOpt['title'] = 'Select Potential File'
		filename = tk.filedialog.askopenfilename(**self.fileOpt)

		Energy=[]

		if filename:
			openfile=open(filename,"r")
			line=openfile.readlines()
			for x in line:
				rmbreaker=x[:-1]
				try: 
					if float(rmbreaker):
						Energy.append(float(rmbreaker))

				except:
					self.formatwarning()
					return



		if len(Energy)!=0:
			popup=tk.Toplevel(self.root)

			f = Figure(figsize=(5,5), dpi=100)
			a = f.add_subplot(111)
			#print(self.Para[0],self.Para[1])
			x=np.arange(0.5,len(Energy),1)

			a.plot(x,Energy)
			a.set_title ("Potential Energy", fontsize=16)
			a.set_ylabel("Energy(J/mol)", fontsize=14)
			a.set_xlabel("Time Step", fontsize=14)
			
			self.Canvasformat(popup, f)

		else:
			messagebox.showwarning('Oops', 'The input file is empty')
		
				
					
	
	def Start(self):

		self.Coord=[]

		#self.file=open(self.output,"w")	
		self.stop=False		
		self.L=self.controller.Lattice(self.Numvalue,self.Sizevalue,self.Para)
		self.controller.InitVelo(self.Numvalue,self.Sizevalue, self.Tempvalue,self.Para)
		coor=self.Zoom(self.Numvalue)
		self.Coord.append(coor)


		for x in coor:
				pygame.draw.circle(self.DISPLAYSURF,self.Color, x,10,0)
        
		
		for i in range(1,self.Framevalue):

			for event in pygame.event.get():
				
				if event.type==QUIT:
					pygame.quit()

			if self.stop==False:

				self.DISPLAYSURF.fill(self.WHITE)

			    #print("self.L", self.L)
				for j in range(1,200):
					#Verlet(self,Npart, coor, boxsize,para,mass):
					self.L=self.controller.Verlet(self.Numvalue,self.L,self.Sizevalue, self.Para, self.Mass)

				coor=self.Zoom(self.Numvalue)
				self.Coord.append(coor)
				#print("self.Color",self.Color)				
				for x in coor:
					pygame.draw.circle(self.DISPLAYSURF,self.Color, x,10,0)	
				#frame1.update()
			while self.stop==True:
				for x in coor:
					pygame.draw.circle(self.DISPLAYSURF,self.Color, x,10,0)
				pygame.display.update()
				self.root.update()
				self.fpsClock.tick(5)

			pygame.display.update()
			self.root.update()
			self.fpsClock.tick(self.FPS)

		



	def popNoble(self):
		self.wbuild=popNoble.PopBuild(self.root)
		self.build["state"]="disabled"
		self.root.wait_window(self.wbuild.top)
		self.build["state"] = "normal"

		if self.wbuild.Submit==True:

			self.Framevalue=self.wbuild.Framevalue
			self.Tempvalue=self.wbuild.Tempvalue
			self.Numvalue=self.wbuild.Numvalue
			self.Typename=self.wbuild.Typename
			self.Typevalue=self.wbuild.Typevalue
			self.Color=self.colormap[self.Typename]
			self.Para=para.Paramap[self.Typename]
			self.Mass=para.Massmap[self.Typename]
			self.output=self.wbuild.output
			self.listBox.insert(tk.END,"Frame number:"+str(self.Framevalue))
			self.listBox.insert(tk.END,"Temperature:"+str(self.Tempvalue)+" K")
			self.listBox.insert(tk.END,"Number of Atom:"+str(self.Numvalue))
			self.listBox.insert(tk.END,"Atom type:"+str(self.Typename))
			self.Start()
	
	
	def Potential(self):


		popup=tk.Toplevel(self.root)
		f = Figure(figsize=(5,5), dpi=100)
		a = f.add_subplot(111)
		#print(self.Para[0],self.Para[1])
		x=np.arange(0.5,1.0,0.0001)
		#a.set_ylim(-0.5,2)
		vLJ=np.vectorize(self.LJ)
		#vLJ=self.LJ
		a.plot(x,vLJ(x))
		a.set_title ("Potential", fontsize=16)
		a.set_ylabel("U(r)", fontsize=14)
		a.set_xlabel("r", fontsize=14)	
		#a.set_xlim([0.7,2])
		self.Canvasformat(popup, f)


	def LJ(self,x):
		if x>0.0:
			tp=self.Para[1]/x
			return self.Para[0]*(tp**12-2*tp**6)


	def TEnergy(self):
		Energy=self.controller.GetEnergy()[0]

		if len(Energy)!=0:
			popup=tk.Toplevel(self.root)

			f = Figure(figsize=(5,5), dpi=100)
			a = f.add_subplot(111)
			#print(self.Para[0],self.Para[1])
			x=np.arange(0.5,len(Energy),1)

			a.plot(x,Energy)
			a.set_title ("Potential Energy", fontsize=16)
			a.set_ylabel("Energy(J/mol)", fontsize=14)
			a.set_xlabel("Time Step", fontsize=14)
			
			self.Canvasformat(popup, f)

		else:
			messagebox.showwarning('Oops', 'No simulaitons, please set up simulaitons')



	
	def Canvasformat(self, master, figure):

		canvas = FigureCanvasTkAgg(figure, master)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		toolbar = NavigationToolbar2Tk(canvas, master)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




	def displayItem(self, event):
		index = self.listBox.curselection()
		label = self.listBox.get(index)
		self.listBox.delete(index)					


	def Zoom(self, Npart):
		sumx=0
		sumy=0
		coor=[]

		for i in range(0,len(self.L)):
			coor.append([10*self.L[i][0],10*self.L[i][1]])

		for i in range(0,len(self.L)):
			sumx+=coor[i][0]
			sumy+=coor[i][1]
		sumx/=Npart
		sumy/=Npart
		deltax=PWIDTH/2-sumx
		deltay=PHEIGHT/2-sumy

		for i in range(0,len(self.L)):
			coor[i][0]+=deltax
			coor[i][1]+=deltay
			coor[i][0]=int(coor[i][0])
			coor[i][1]=int(coor[i][1])
			#self.file.write(str(coor[i][0])+" "+str(coor[i][1])+",")
			if (abs(coor[i][0])>PWIDTH or abs(coor[i][1])>PHEIGHT):
				messagebox.showwarning('Oops', 'The parameter setting is not correct, please reset the parameters')
				self.stop=True
		#self.file.write("\n")

		#print("coor", coor)
		#print("self.L", self.L)
		return coor


	def formatwarning(self):
		messagebox.showwarning('Oops', 'The format is not correct')

	def Stop(self):
		self.stop=True

	def Continue(self):
		self.stop=False


		

		
if __name__ == "__main__":
  view = View(Controller() )
  #tk.mainloop()
  