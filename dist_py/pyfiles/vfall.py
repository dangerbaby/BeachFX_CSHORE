from __future__ import division
import numpy as np

"""
vfall calculation from Brad's matlab code (originally Jarrell Smith). 
comments starting with "%" are directly from this code

	%VFALL is a function to estimate fall velocity based on Soulsby's (1997)
	%      optimization.
	%      w = kvis/d* [sqrt(10.36^2 + 1.049 D^3) - 10.36]
	%
	% SYNTAX:  w=vfall(d,T,S)
	%  where w = sediment fall speed (m/s)
	%        d = grain diameter (mm)
	%        T = temperature (deg C)
	%        S = Salinity (ppt)
	%
	% Jarrell Smith
	% Coastal and Hydraulics Laboratory
	% Engineer Research and Development Center
	% Vicksburg, MS

"""

class vfall_calc(object):
	def __init__(self):
		temp = {}

	def init(self, d, T, S):
		self.d = d
		self.T = T
		self.S = S
		return self.vfall_calc()

	def vfall_calc(self):
		g = 9.81
		rho = self.denfun(self.T, self.S)
		kvis = self.kvisfun(self.T)
		rhos = 2650
		self.d = self.d/1000 											# %convert mm to m
		s=rhos/rho
		D=(g*(s-1)/kvis**2)**(1/3)*self.d
		return kvis/self.d*(np.sqrt(10.36**2+1.049*D**3)-10.36) 		# %settling speed

	def denfun(self, T, S):
		"""
		%DENFUN estimates water density from temperature and salinity
		%Approximation from VanRijn, L.C. (1993) Handbook for Sediment Transport 
		%                     by Currents and Waves
		%
		%SYNTAX:  rho=denfun(T,S)
		%  where  rho = density of water (kg/m^3)
		%           T = temperature (C)
		%           S = salinity (o/oo)
		%
		"""
		CL=(S-0.03)/1.805 								# %VanRijn
		rho=1000 + 1.455*CL - 6.5e-3* (T-4+0.4*CL)**2  	# %from VanRijn (1993)
		return rho

	def kvisfun(self, T):
		"""
		%KVISFUN estimates kinematic viscosity of water
		%Approximation from VanRijn, L.C. (1989) Handbook of Sediment Transport
		%
		%SYNTAX:  kvis=kvisfun(T)
		%  where  kvis = kinematic viscosity (m^2/sec)
		%            T = temperature (C)
		%
		"""
		kvis=1e-6*(1.14 - 0.031*(T-15) + 6.8E-4*(T-15)**2)
		return kvis
