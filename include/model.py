#!/opt/local/bin/python3

import random
import sys
sys.path.append('include')
import para
import random,math



SIGMA=para.SIGMA
EPSkb=para.EPSkb
mHe=para.mHe

Limit=0.8*SIGMA

class Model(object): 
	"""docstring for MD, Npart: number of particles"""
	def __init__(self):
		self.dt=1
		self.precoor=[]
		self.newcoor=[]
		self.V=[]
		##totoal energy
		self.TEnergy=[]
		##Kinetical energy
		self.KEnergy=[]


	def acceleration(self, Npart,coor,boxsize, para,mass):

		#epsilon*kb kb=1.38e-23 Jk^-1

		EPSkb=para[0]*1.38e-23
		SIGMA=para[1]
		mass=mass/6.0221409e+26
		gap=0.8*SIGMA
		boxsizeX=(math.floor(math.sqrt(Npart))+1)*gap
		boxsizeY=(math.ceil(math.sqrt(Npart))+1)*gap

		###kinetic energy

		kinetic=0.0
		for i in range(0, Npart):
			#print(self.V[i][0])
			kinetic+=0.5*mass*(self.V[i][0]*self.V[i][0]+self.V[i][1]*self.V[i][1])
			#print(kinetic)
		self.KEnergy.append(kinetic)

		#print(kinetic)

		acc=[]

		potential=0.0


		for i in range(0, Npart):
			acc.append([0,0])
			
		for i in range(0,Npart-1):
			for j in range(i+1, Npart):
				#print(coor[i], coor[j])

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
				#print(rij2)
				tp2=SIGMA*SIGMA/rij2
				tp6=tp2*tp2*tp2		
				#force 
				#( (24*EPSILON*A)/r^2 ) * (SIGMA/r)^6 * ( 2*(SIGMA/r^2)^6 -1  )

				#if rij2 < 9*SIGMA*SIGMA:

				Ffactor=24*EPSkb*tp6*(2*tp6-1)/rij2
				accel=Ffactor/(mass*1e10)

				acc[i][0]+=accel*xij
				acc[i][1]+=accel*yij

				acc[j][0]-=accel*xij
				acc[j][0]-=accel*yij

				potential+=4*(1.0/rij12-1.0/rij6)


		self.TEnergy.append(potential)


		return acc

	###boxsize is the size for periodic box, para:(EPSILON, SIGMA), mass: mass of atom


	def Verlet(self,Npart, coor, boxsize,para,mass):

		acc=self.acceleration(Npart,coor,boxsize,para, mass)

		newcoor=self.newcoor
		precoor=self.precoor

		#calc v(t+0.5dt)
		#print("acc ", acc)


		for i in range(0,Npart):
			#self.newcoor[i][0]=2*coor[i][0]-self.precoor[i][0]+acc[i][0]*self.dt*self.dt
			#self.newcoor[i][1]=2*coor[i][1]-self.precoor[i][1]+acc[i][1]*self.dt*self.dt
			newcoor[i][0]=2*coor[i][0]-precoor[i][0]+acc[i][0]*self.dt*self.dt
			newcoor[i][1]=2*coor[i][1]-precoor[i][1]+acc[i][1]*self.dt*self.dt

			#self.V[i][0]=(self.newcoor[i][0]-self.precoor[i][0])/(2*self.dt)
			#self.V[i][1]=(self.newcoor[i][1]-self.precoor[i][1])/(2*self.dt)
			self.V[i][0]=(newcoor[i][0]-precoor[i][0])/(2*self.dt)
			self.V[i][1]=(newcoor[i][1]-precoor[i][1])/(2*self.dt)

		self.precoor=precoor
		self.newcoor=newcoor
		coor=newcoor


		return coor




    ##initialize velocity

	def InitVelo(self, Npart,boxsize,temp,para):
		coord=self.Lattice(Npart, boxsize,para)
		precoor=[]
		#print("coor in Lattice ", coor)
		self.V=[]
		speed_scale=1.0
		sumv=[0,0]
		sumv2=0

		for i in range(0,Npart):
			vx=speed_scale*(2*random.random()-1)
			vy=speed_scale*(2*random.random()-1)
			self.V.append([vx,vy])
			sumv[0]+=vx
			sumv[1]+=vy
			sumv2+=vx*vx+vy*vy
			#print("sumv2 is ",sumv2)

		sumv[0]=sumv[0]/Npart
		sumv[1]=sumv[1]/Npart
		fs=math.sqrt(3*temp/sumv2)
		#print("coor in Lattice ", coord)

		for i in range(0,len(self.V)):
			self.V[i][0]=(self.V[i][0]-sumv[0])*fs
			self.V[i][1]=(self.V[i][1]-sumv[1])*fs
			#print("coor in loop 1 ", coord[i][0])
			tpx=coord[i][0]-self.V[i][0]*self.dt
			#self.precoor[i][0]=tpx
			#print("coor in loop 2 ", coord[i][0])
			tpy=coord[i][1]-self.V[i][1]*self.dt
			#print("coor in loop 3 ", coord[i])
			precoor.append([tpx,tpy])


		return precoor



	def Lattice(self, Npart,boxsize, para):
		L=[]
		SIGMA=para[1]
		#print(SIGMA)
		gap=0.8*SIGMA

		n=int(math.sqrt(Npart))
		tpx=0
		tpy=0
		
		for i in range(0,n):
			tpx+=gap
			tpy=0
			for j in range(0,n):
				tpy+=gap
				L.append([tpx,tpy])
		extr=Npart-n*n
		tpx+=gap
		tpy=0

		for i in range(0,extr):
			tpy+=gap
			L.append([tpx,tpy])
			
		self.precoor=self.newcoor=L
		#print("The first coor",L)
		return L



	def GetEnergy(self):
		return (self.TEnergy, self.KEnergy)


		
if __name__=="__main__":
	view=Model()
	coor=view.Lattice(2, 20, (10.22, 2.556))
	view.InitVelo(2,20,300, (10.22, 2.556))

	for i in range(1,10):
		#coor=view.Verlet(2,coor,5)
		coor=view.Verlet(2,coor,20,(10.22, 2.556),4.0026)
		print(coor)


	

		