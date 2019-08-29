#!/opt/local/bin/python3

import unittest
import sys
sys.path.append('include')
import model
import math
import random



class Testmodel(unittest.TestCase):
	"""docstring for Testmodel"""

	def setUp(self):
		self.model=model.Model()
		self.Npart=2
		self.temp=300
		self.boxsize=20
		self.para=(10.22, 2.556)
		self.mass=4.0026
		self.dt=1
	


	def testAcceleration(self):
		boxsizeX=4.0896
		boxsizeY=6.134399999999999
		EPSkb=self.para[0]*1.38e-23
		SIGMA=self.para[1]
		mass=self.mass/6.0221409e+26
		self.model.InitVelo(self.Npart,self.boxsize,self.temp, self.para)

		def coorgen():
			coor1=[random.uniform(0,10),random.uniform(0,10)]
			coor2=[random.uniform(0,10),random.uniform(0,10)]
			while coor1==coor2:
				coor1=[random.uniform(0,10),random.uniform(0,10)]
				coor2=[random.uniform(0,10),random.uniform(0,10)]
			return [coor1,coor2]
					
		
		for i in range(1,1000):
			coor=coorgen()
			tacc=self.model.acceleration(2,coor,self.boxsize,self.para, self.mass)
			acc=[]

			for i in range(0,2):
				acc.append([0,0])

			for i in range(0,1):
				for j in range(i+1, 2):

					xij=coor[i][0]-coor[j][0]
					yij=coor[i][1]-coor[j][1]
					

					if xij>=0.5*boxsizeX:
						xij-=boxsizeX
					if xij<-0.5*boxsizeX:
						xij+=boxsizeX
					if yij>=0.5*boxsizeY:
						yij-=boxsizeY
					if yij<-0.5*boxsizeY:
						yij+=boxsizeY

					rij2=xij*xij+yij*yij
					rij6=rij2*rij2*rij2
					rij12=rij6*rij6
		
					tp2=SIGMA*SIGMA/rij2
					tp6=tp2*tp2*tp2		

					Ffactor=24*EPSkb*tp6*(2*tp6-1)/rij2
					accel=Ffactor/(mass*1e10)

					acc[i][0]+=accel*xij
					acc[i][1]+=accel*yij

					acc[j][0]-=accel*xij
					acc[j][0]-=accel*yij
			

			self.assertEqual(acc,tacc)




	def testVerlet(self):

		coor=self.model.Lattice(self.Npart, self.boxsize, self.para)
		precoor=self.model.InitVelo(self.Npart,self.boxsize,self.temp, self.para)
		newcoor=coor
		#print(coor)    
		for i in range(1,1000):
			

			acc=self.model.acceleration(self.Npart,coor,self.boxsize,self.para, self.mass)
		
			for i in range(0,self.Npart):
				newcoor[i][0]=2*coor[i][0]-precoor[i][0]+acc[i][0]*self.dt*self.dt
				newcoor[i][1]=2*coor[i][1]-precoor[i][1]+acc[i][1]*self.dt*self.dt

			tcoor=self.model.Verlet(self.Npart, coor, self.boxsize,self.para,self.mass)
			self.assertEqual(len(tcoor),len(newcoor))
			precoor=coor
			coor=newcoor


	def testInitVelo(self):
		###InitVelo() will get the random velocity, it is hard the test the random number, i just tested the size of the return list. 

		for i in range(1,100):
			precoor=self.model.InitVelo(i, self.boxsize,self.temp, self.para)
			self.assertEqual(i,len(precoor))
		
	
	def testLattice(self):

		for i in range(2,1000):
			coor=self.model.Lattice(i, self.boxsize, self.para)
			L=[]

			num=int(math.sqrt(i))
			tpx=0
			tpy=0
			gap=0.8*2.556

			for k in range(0,num):
				tpx+=gap
				tpy=0
			
				for j in range(0,num):
					tpy+=gap
					L.append([tpx,tpy])
			extr=i-num*num
			tpx+=gap
			tpy=0

			for k in range(0,extr):
				tpy+=gap
				L.append([tpx,tpy])

			#print(coor)
			self.assertEqual(L,coor)
			
		
		

if __name__=="__main__":
	unittest.main()
		