import numpy as np
import math
import random
import matplotlib.pyplot as plt
'''
Converting Hari's script from MATLAB to python.
'''

#fracture network construction using modified Levy-Lee model
D=1.5 #exponent in power law distribution
beta=0.5 #parameter in length distribution
nfrac=512 #number of fractures

#  x = np.zeros((1,nfrac+1))
#  y = np.zeros((1,nfrac+1))
#  idir = np.zeros((1,nfrac+1))
#  lenth = np.zeros((1,nfrac+1))
x = np.zeros(nfrac+1)
y = np.zeros(nfrac+1)
idir = np.zeros(nfrac+1)
lenth = np.zeros(nfrac+1)

#initial seed location in unit square
x[0]=random.uniform(0,1);y[0]=random.uniform(0,1);idir[0]=1;lenth[0]=0.002

for ifrac in np.arange(0,nfrac):
    #draw distance from inverse power law distribution
    ucent=random.uniform(0,1)
    L=ucent**(-1/D)
    #draw angle from uniform dist. on a circle
    theta=random.uniform(0,1)*2.*np.pi
    #assign coordinates of center of next fracture
    #  x(ifrac+1)=x(ifrac)+L*cos(theta);
    #  y(ifrac+1)=y(ifrac)+L*sin(theta);
    x[ifrac+1]=x[ifrac]+L*np.cos(theta)
    y[ifrac+1]=y[ifrac]+L*np.sin(theta)
    #relocate inside -1 to +1 if outside
    #  if(abs(x(ifrac+1))>1)
        #  x(ifrac+1)=-1+2*rand(1,1);
    #  end
    #  if(abs(y(ifrac+1))>1)
        #  y(ifrac+1)=-1+2*rand(1,1);
    #  end
    if (abs(x[ifrac+1])>1):
        x[ifrac+1]=-1+2*random.uniform(0,1)
    if (abs(y[ifrac+1])>1):
        y[ifrac+1]=-1+2*random.uniform(0,1)
    #calculate distance from previous center
    #  L=sqrt((x(ifrac+1)-x(ifrac))^2+(y(ifrac+1)-y(ifrac))^2);
    L=np.sqrt((x[ifrac+1]-x[ifrac])**2.+(y[ifrac+1]-y[ifrac])**2.)
    #assign a length for the next fracture
    ulen=random.uniform(0,1)
    #  len=-log(1-ulen)*beta*L; lenth(ifrac+1)=len;
    #(had to change name 'len' to 'leng')
    leng=-np.log(1-ulen)*beta*L; lenth[ifrac+1]=leng
    #pick orientation x or y
    udir=random.uniform(0,1)
    if (udir <= 0.5):
        idir[ifrac+1]=1 #x direction
    else:
        idir[ifrac+1]=0 #y direction

#at this stage, we have fracture center coordinates, directions and lengths
#now we are going to check for fractures that are overlapping and delete
#the smaller ones - start with x-direction fractures
xfracsx=x[idir==1];xfracsy=y[idir==1];lenx=lenth[idir==1]
#  [xfy,inx]=np.sort(xfracsy);#(DIDN't WORK) sort by y coordinates of centers
xfy = np.sort(xfracsy); inx = np.argsort(xfracsy)
xfx=xfracsx[inx];lenx=lenx[inx]
#now all the x-direction fractures are sorted by the y-coordinates of their
#centers.  Need to check if centers are too close for overlapping fractures
#  flagx=np.zeros((len(xfy),1));thresh=0.1;
flagx=np.zeros(len(xfy));thresh=0.1;
#we will set flagx = 1 for fractures to be deleted

for i in np.arange(0,len(xfy)-1):
    #if y coordinates are too close
    if abs(xfy[i+1]-xfy[i]) < thresh:
        #determine end points
        s1=xfx[i]-lenx[i]/2
        s2=xfx[i+1]-lenx[i+1]/2
        e1=xfx[i]+lenx[i]/2
        e2=xfx[i+1]+lenx[i]/2
        #check for overlap and delete smaller fracture
    if (e1 > e2 and s1 < e2):
        if lenx[i] > lenx[i+1]:
            flagx[i+1]=1
        else:
            flagx[i]=1
    if (e2 > e1 and s2 < e1):
        if lenx[i] > lenx[i+1]:
            flagx[i+1]=1
        else:
            flagx[i]=1
    if (e1 > e2 and s2 > s1):
        flagx[i+1]=1
    if (e2 > e1 and s1 > s2):
        flagx[i]=1

#now delete fractures with flag=1
#  xfx[flagx==1]=[];xfy[flagx==1]=[];lenx[flagx==1]=[]
xfx = np.delete(xfx,np.where(flagx==1))
xfy = np.delete(xfy,np.where(flagx==1))
lenx = np.delete(lenx,np.where(flagx==1))


#now work on the y-direction fractures
yfracsx=x[idir==0];yfracsy=y[idir==0];leny=lenth[idir==0]
#  [yfx,iny]=sort(yfracsx);#(DIDN'T WORK) sort by x coordinates of centers
yfx = np.sort(yfracsx); iny = np.argsort(yfracsx)
yfy=yfracsy[iny];leny=leny[iny]
#now all the y-direction fractures are sorted by the x-coordinates of their
#centers.  Need to check if centers are too close for overlapping fractures
flagy=np.zeros(len(yfx));thresh=0.1
#we will set flagy = 1 for fractures to be deleted

for i in np.arange(0,len(yfx)-1):
    #if x coordinates are too close
    if abs(yfx[i+1]-yfx[i]) < thresh:
        #determine end points
        s1=yfy[i]-leny[i]/2
        s2=yfy[i+1]-leny[i+1]/2
        e1=yfy[i]+leny[i]/2
        e2=yfy[i+1]+leny[i]/2
        #check for overlap and delete smaller fracture
    if (e1 > e2 and s1 < e2):
        if leny[i] > leny[i+1]:
            flagy[i+1]=1
        else:
            flagy[i]=1
    if (e2 > e1 and s2 < e1):
        if leny[i] > leny[i+1]:
            flagy[i+1]=1
        else:
            flagy[i]=1
    if (e1 > e2 and s2 > s1):
        flagy[i+1]=1
    if (e2 > e1 and s1 > s2):
        flagy[i]=1

#now delete fractures with flagy=1
#  yfx(flagy==1)=[];yfy(flagy==1)=[];leny(flagy==1)=[];
yfx = np.delete(yfx,np.where(flagy==1))
yfy = np.delete(yfy,np.where(flagy==1))
leny = np.delete(leny,np.where(flagy==1))

#now we have all fractures - next step is to determine ends (again) and plot
xstart=np.zeros(len(xfx)+len(yfy)); xend=np.zeros(len(xfx)+len(yfy))
ystart=np.zeros(len(xfx)+len(yfy)); yend=np.zeros(len(xfx)+len(yfy))
for i in np.arange(0,len(xfx)):
    xstart[i]=xfx[i]-lenx[i]/2
    xend[i]=xfx[i]+lenx[i]/2
    ystart[i]=xfy[i]
    yend[i]=xfy[i]
for i in np.arange(0,len(yfx)):
    j=len(xfx)+i
    xstart[j]=yfx[i]
    xend[j]=yfx[i]
    ystart[j]=yfy[i]-leny[i]/2
    yend[j]=yfy[i]+leny[i]/2
xstart[xstart>1]=1
xstart[xstart<-1]=-1
xend[xend>1]=1
xend[xend<-1]=-1
ystart[ystart>1]=1
ystart[ystart<-1]=-1
yend[yend>1]=1
yend[yend<-1]=-1

#censoring out very small fractures (likely disconnected)
#lcens=0.2;
#x(lenth<lcens)=[];xstart(lenth<lcens)=[];xend(lenth<lcens)=[];idir(lenth<lcens)=[];
#y(lenth<lcens)=[];ystart(lenth<lcens)=[];yend(lenth<lcens)=[];
#now to plot
#plot(x,y,'r.','MarkerSize',5)

lw = 0.5 #line width
ms = 2   #marker size
fig, ax = plt.subplots(1,figsize=(10,10))
#  ax = plot(xfx,xfy,'r.',ms=5)
#  ax = plot(yfx,yfy,'r.',ms=5)
ax.plot(xfx,xfy,'r.',ms=2)
ax.plot(yfx,yfy,'r.',ms=2)
for ifrac in np.arange(0,len(xstart)):
    ax.plot([xstart[ifrac],xend[ifrac]],[ystart[ifrac],yend[ifrac]],color='gray',lw=lw)

fig.show()


