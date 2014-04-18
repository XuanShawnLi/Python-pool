#/usr/bin/python
import math
from math import sqrt

class Solution:
	def SPF500Reading(self,file1):
		f=open(file1);lines=f.read().splitlines();f.close()
		n=len(lines);data=[]
		for l1 in range(n):
			l2=lines[l1].split()
			data.append(float(l2[1]))
		avg=sum(data)/n
		std=sqrt(sum([(x-avg)**2 for x in data])/n)
		print "Spf average rate of return in the last",n/13,'years=',avg
		print "standard deviation=",std
	 	return avg		

	def Preprosessing(self,files,years,months):
		n=len(files)
		lines=[]
		for x in files:
			f=open(x);lines+=[f.read().splitlines()];f.close()
		print "Total of",len(lines),"years"
		bond1=[];bond2=[];bond3=[];bond4=[]
		for year in range(7):
			month=1;i=0
			while(month<=12):
				l3=lines[year][i].split()
				if(l3[0][0]!='Q'):
					j1=3;i1=len(l3[j1]);bond1.append(l3[j1][:i1-1])
					j1=5;i1=len(l3[j1]);bond2.append(l3[j1][:i1-1])
					j1=7;i1=len(l3[j1]);bond3.append(l3[j1][:i1-1])
					j1=9;i1=len(l3[j1]);bond4.append(l3[j1][:i1-1])
					month+=1
				i+=1
		for year in range(7,10):
        		month=1;i=0
        		while(month<=12):
                		l3=lines[year][i].split()
                		if(l3[0][0]!='Q'):
                        		j1=3;i1=len(l3[j1]);bond1.append(l3[j1][:i1-1])
                        		j1=5;i1=len(l3[j1]);bond2.append(l3[j1][:i1-1])
                        		j1=6;i1=len(l3[j1]);bond3.append(l3[j1][:i1-1])
                        		j1=7;i1=len(l3[j1]);bond4.append(l3[j1][:i1-1])
                        		month+=1
                		i+=1
		bond1_new=[];bond2_new=[];bond3_new=[];bond4_new=[]
		i=0
		for year in years:
			for month in months:
				bond1_new.append([year, month,float(bond1[i])])
				bond2_new.append([year, month,float(bond2[i])])
				bond3_new.append([year, month,float(bond3[i])])
				bond4_new.append([year, month,float(bond4[i])])
				i+=1
		return [bond1_new,bond2_new,bond3_new,bond4_new]

	def Analysis(self,bond,names,i):
		print "For ****",names[i],"****"
		#bond2.sort(key=lambda x: x[2])
		n=len(bond)
		avg=sum(x[2] for x in bond)/n
		std=sqrt(sum((x[2]-avg)**2 for x in bond)/n)
		print "Average rate of return is",avg
		print "Standard deviation is",std
		print "Sharp ratio=",(avg-spf500avg)/std
		return (avg,std)

	def Variance(self,bonds,i,j,names,bond_stats):
		n=len(bonds[i])
		var=0
		for index in range(n):
			var+=(bonds[i][index][2]-bond_stats[i][0])*(bonds[j][index][2]-bond_stats[j][0])
		var=var/(n)
		print "variance between ",names[i]," and ",names[j]," is= ",var
		print "correlation is",var/bond_stats[i][1]/bond_stats[j][1]
		return var

	def SharpRatio(self,W1):
		from math import sin
		W2=[x**2 for x in W1]
		norm=sum(W2)
		W=[x/norm for x in W2]
		Ep=0
		for i in range(nbonds):
			Ep+=W[i]*bond_stats[i][0]
		std=0
		for i in range(nbonds):
			for j in range(nbonds):
				std+=W[i]*W[j]*varmatrix[i][j]
		std=sqrt(std)	
		return (Ep-spf500avg)/std
	
	def NegativeSharpRatio(self,W):
		return -self.SharpRatio(W)

	

solution=Solution()
files=["Data2013","Data2012","Data2010","Data2009","Data2008","Data2007","Data2006","Data2005","Data2004","Data2003"]
years=[2013,2012,2010,2009,2008,2007,2006,2005,2004,2003]
months=[x+1 for x in range(12)]
names=["BOND FUND","CANADIAN EQUITY","FOREIGN EQUITY","STIF"]
spf500avg=solution.SPF500Reading("Spf500.txt")
bonds=solution.Preprosessing(files,years,months)
nbonds=len(bonds)
bond_stats=[]
for i in range(nbonds):
	bond_stats.append(solution.Analysis(bonds[i],names,i))
variance={}
for i in range(nbonds):
	for j in range(i,nbonds):
		variance[(i,j)]=solution.Variance(bonds,i,j,names,bond_stats)
varmatrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(nbonds):
	for j in range(i,nbonds):
		varmatrix[i][j]=variance[(i,j)]
		varmatrix[j][i]=variance[(i,j)]
#for x in varmatrix:
#	print x
#print solution.SharpRatio([0.25,0.25,0.25,0.25])
import scipy
from scipy import special, optimize
from scipy.optimize import fmin
result=fmin(solution.NegativeSharpRatio,[0.25,0.25,0.25,0.25])
#result=[ 0.0968895,-0.05848627,0.02914598,0.77631737]
print "result=",result
print "optmized sharp ratio=",solution.SharpRatio(result)
