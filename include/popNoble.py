#!/opt/local/bin/python3

import sys
import tkinter as tk
from tkinter import messagebox


GEOMETRY = '400x500+20+20'
WIDTH=15
HEIGHT=8

class PopBuild(object):
	"""docstring for PopBuild"""
	def __init__(self, master):
		top=self.top=tk.Toplevel(master)
		top.title("Build Molecular Dynamical Model")
		self.boxFont = ('Georgia', 14)
		self.labelFont = ('Georgia', 10)
		self.butFont = ('Georgia', 12)
		top.geometry(GEOMETRY)


		self.type=tk.IntVar()
		self.type.set(1)

		self.name={1:"He", 2:"Ar", 3:"Ne", 4:"Xe"}


		self.Typevalue=1
		self.Framevalue=100
		self.Tempvalue=300
		self.Numvalue=10
		self.Submit=False
		self.output="output.txt"
		self.Typename=self.name[self.Typevalue]




		frame1 = tk.Frame(top)
		frame1.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5',width=50)
		frame1.pack(side=tk.TOP)

		Boxsize=tk.Label(frame1, text="Number of Frames")
		Boxsize.pack(side=tk.LEFT, anchor=tk.W)
		Boxsize.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0', width=15)
		Boxsize.config(font=self.labelFont)

		self.SizeBox = tk.Entry(frame1, font=self.boxFont, width=15)
		self.SizeBox.bind('<Return>', (lambda event: self.getFramesize()))
		self.SizeBox.pack(side=tk.LEFT, padx=5)
		self.SizeBox.config(relief=tk.SUNKEN, bd=5)
		self.SizeBox.focus()
		
		#enter1=tk.Button(frame1, text="Enter",width=5, command=self.Enter1)
		#enter1.pack(side=tk.LEFT, anchor=tk.W)
		#enter1.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0')
		#enter1.config(font=self.butFont, state=tk.NORMAL)

		frame2 = tk.Frame(top)
		frame2.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5',width=50)
		frame2.pack(side=tk.TOP)

		NumAtom=tk.Label(frame2, text="Number of Molecules")
		NumAtom.pack(side=tk.LEFT, anchor=tk.W)
		NumAtom.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0', width=15)
		NumAtom.config(font=self.labelFont)

		self.NumBox = tk.Entry(frame2, font=self.boxFont, width=15)
		self.NumBox.bind('<Return>', (lambda event: self.getNum()))
		self.NumBox.pack(side=tk.LEFT, padx=5)
		self.NumBox.config(relief=tk.SUNKEN, bd=5)
		self.NumBox.focus()
			

		frame3 = tk.Frame(top)
		frame3.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5',width=50)
		frame3.pack(side=tk.TOP)


		Temper=tk.Label(frame3, text="Temperature (K)")
		Temper.pack(side=tk.LEFT, anchor=tk.W)
		Temper.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0', width=15)
		Temper.config(font=self.labelFont)

		self.TempBox = tk.Entry(frame3, font=self.boxFont, width=15)
		self.TempBox.bind('<Return>', (lambda event: self.getTemp()))
		self.TempBox.pack(side=tk.LEFT, padx=5)
		self.TempBox.config(relief=tk.SUNKEN, bd=5)
		self.TempBox.focus()


		frame3 = tk.Frame(top)
		frame3.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5', width=50)
		frame3.pack(side=tk.LEFT)
		

		self.atomtype=[("He",1),("Ar",2),("Ne",3),("Xe",4)]
		Atom=tk.Label(frame3, text="Type of Atom")
		Atom.pack(side=tk.TOP, anchor=tk.W)
		Atom.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#E0E0E0', width=10)
		Atom.config(font=self.labelFont)
		for atom, val in self.atomtype:
			Radio=tk.Radiobutton(frame3, text=atom, padx=5, variable=self.type, command=self.getType, value=val)
			Radio.config(indicatoron=0, width=10,padx=5, pady=5, bd=5, relief=tk.RAISED)
			Radio.pack(side=tk.TOP)


		submit=tk.Button(frame3, text="Submit",width=8, command=self.SubVal)
		submit.pack(side=tk.TOP, anchor=tk.W)
		submit.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#f44248')
		submit.config(font=self.butFont, state=tk.NORMAL)


		frame4 = tk.Frame(top)
		frame4.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#FFCCE5',width=30)
		frame4.pack(side=tk.LEFT)

		scrollbar = tk.Scrollbar(frame4)

		scrollbar2 = tk.Scrollbar(frame4)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		scrollbar2.pack(side=tk.BOTTOM,fill="both")

		self.listBox = tk.Listbox(frame4)
		self.listBox.pack( side = tk.TOP, fill = tk.Y)
		self.listBox.config( bg='white', bd=5, font=self.boxFont )
		self.listBox.config(width=WIDTH, height=HEIGHT)
		self.listBox.bind('<Double-1>', self.Display)
		self.listBox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.listBox.yview)
		self.listBox.config(xscrollcommand=scrollbar2.set)
		scrollbar2.config(command=self.listBox.xview, orient=tk.HORIZONTAL)
			

		#print(self.value)



	def getType(self):
		self.Typevalue=self.type.get()
		self.Typename=self.name[self.Typevalue]
		#print(self.type.get())
		self.listBox.insert(tk.END,"Atom type set to:"+str(self.Typename))

	#def Enter1(self):
		#self.Numvalue=self.NumBox.get()
		#self.listBox.insert(tk.END,"The boxsize set to:"+self.Numvalue)
		#print(self.Numvalue)



	
	def getNum(self):
		try:
			if self.NumBox.get().isdigit():
				self.Numvalue=int(self.NumBox.get())
				if (self.Numvalue > 50 or self.Numvalue<3):
					self.outrangeWarning(self.NumBox,(3,50))
					#self.NumBox.delete(0,tk.END)
				else:
					self.listBox.insert(tk.END,"Num set to:"+str(self.Numvalue))
			else:
				self.noInterWarning(self.NumBox)

		except:
			self.noInterWarning(self.NumBox)
			#self.NumBox.delete(0,tk.END)

		

	def getTemp(self):
		try:
			if self.TempBox.get().isdigit():
				self.Tempvalue=int(self.TempBox.get())
				if (self.Tempvalue<0 or self.Tempvalue>1000):
					self.outrangeWarning(self.TempBox,(0,1000))
				else:
					self.listBox.insert(tk.END,"Temp set to:"+str(self.Tempvalue)+" K")
			else:
				self.noInterWarning(self.TempBox)

		except:
			self.noInterWarning(self.TempBox)

	

	def getFramesize(self):
		try:
			if self.SizeBox.get().isdigit():
				self.Framevalue=int(self.SizeBox.get())
				if(self.Framevalue<3 or self.Framevalue>4000):
					self.outrangeWarning(self.SizeBox,(3,4000))
				else:
					self.listBox.insert(tk.END,"Frame number:"+str(self.Framevalue))
			else:
				self.noInterWarning(self.SizeBox)

		except:
			self.noInterWarning(self.SizeBox)
		

	
	def SubVal(self):
		if messagebox.askyesno('Submit', "Do you want to submit your parameter?\nFrame Number is:"+str(self.Framevalue)
			+"\nThe Number of Molecules is: "+str(self.Numvalue)+"\nThe Temperature is: "+str(self.Tempvalue)+"\nThe Atom type is: "+self.Typename):
		    messagebox.showwarning('Yes', 'Submit')
		    self.Submit=True
		    self.top.destroy()
		else:
			messagebox.showinfo('No', 'I want reset the parameter')
		

	def Display(self):
		index = self.listBox.curselection()
		label = self.listBox.get(index)
		self.listBox.delete(index)
   
   ##enter the range in a tuple,widget is name of enterbox
	def outrangeWarning(self,widget,range):
		messagebox.showwarning('Out of range', 'Please enter the number in range of '+str(range[0])+" to "+str(range[1]))
		widget.delete(0,tk.END)

  ##widget is name of enterbox
	def noInterWarning(self, widget):
		messagebox.showwarning('Oops', 'Input is not Integer!')
		widget.delete(0,tk.END)




if __name__ == "__main__":
  pop = PopBuild(tk.Tk())
  tk.mainloop()
