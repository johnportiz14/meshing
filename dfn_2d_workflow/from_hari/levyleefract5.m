clear all; close all;
%fracture network construction using modified Levy-Lee model
D=1.5;%exponent in power law distribution
beta=0.5;%parameter in length distribution
nfrac=512;%number of fractures
%initial seed location in unit square
x(1)=rand(1,1);y(1)=rand(1,1);idir(1)=1;lenth(1)=0.002;
for ifrac=1:nfrac
    %draw distance from inverse power law distribution
    ucent=rand(1,1);
    L=ucent^(-1/D);
    %draw angle from uniform dist. on a circle
    theta=rand(1,1)*2*pi;
    %assign coordinates of center of next fracture
    x(ifrac+1)=x(ifrac)+L*cos(theta);
    y(ifrac+1)=y(ifrac)+L*sin(theta);
    %relocate inside -1 to +1 if outside
    if(abs(x(ifrac+1))>1) 
        x(ifrac+1)=-1+2*rand(1,1);
    end
    if(abs(y(ifrac+1))>1)
        y(ifrac+1)=-1+2*rand(1,1);
    end
    %calculate distance from previous center
    L=sqrt((x(ifrac+1)-x(ifrac))^2+(y(ifrac+1)-y(ifrac))^2);
    %assign a length for the next fracture
    ulen=rand(1,1);
    len=-log(1-ulen)*beta*L; lenth(ifrac+1)=len;
    %pick orientation x or y
    udir=rand(1,1);
    if (udir <= 0.5)
        idir(ifrac+1)=1;%x direction
    else
        idir(ifrac+1)=0;%y direction
    end
end
%at this stage, we have fracture center coordinates, directions and lengths
%now we are going to check for fractures that are overlapping and delete
%the smaller ones - start with x-direction fractures
xfracsx=x(idir==1);xfracsy=y(idir==1);lenx=lenth(idir==1);
[xfy,inx]=sort(xfracsy);%sort by y coordinates of centers
xfx=xfracsx(inx);lenx=lenx(inx);
%now all the x-direction fractures are sorted by the y-coordinates of their
%centers.  Need to check if centers are too close for overlapping fractures
flagx=zeros(length(xfy),1);thresh=0.1;
%we will set flagx = 1 for fractures to be deleted
for i=1:length(xfy)-1
    %if y coordinates are too close
    if abs(xfy(i+1)-xfy(i)) < thresh
        %determine end points
        s1=xfx(i)-lenx(i)/2;
        s2=xfx(i+1)-lenx(i+1)/2;
        e1=xfx(i)+lenx(i)/2;
        e2=xfx(i+1)+lenx(i)/2;
        %check for overlap and delete smaller fracture
    if (e1 > e2 && s1 < e2)
        if lenx(i) > lenx(i+1)
            flagx(i+1)=1;
        else
            flagx(i)=1;
        end
    end
    if (e2 > e1 && s2 < e1)
        if lenx(i) > lenx(i+1)
            flagx(i+1)=1;
        else
            flagx(i)=1;
        end
    end
    if (e1 > e2 && s2 > s1)
        flagx(i+1)=1;
    end
    if (e2 > e1 && s1 > s2)
        flagx(i)=1;
    end
    end
end
%now delete fractures with flag=1
xfx(flagx==1)=[];xfy(flagx==1)=[];lenx(flagx==1)=[];
%now work on the y-direction fractures
yfracsx=x(idir==0);yfracsy=y(idir==0);leny=lenth(idir==0);
[yfx,iny]=sort(yfracsx);%sort by x coordinates of centers
yfy=yfracsy(iny);leny=leny(iny);
%now all the y-direction fractures are sorted by the x-coordinates of their
%centers.  Need to check if centers are too close for overlapping fractures
flagy=zeros(length(yfx),1);thresh=0.1;
%we will set flagy = 1 for fractures to be deleted
for i=1:length(yfx)-1
    %if x coordinates are too close
    if abs(yfx(i+1)-yfx(i)) < thresh
        %determine end points
        s1=yfy(i)-leny(i)/2;
        s2=yfy(i+1)-leny(i+1)/2;
        e1=yfy(i)+leny(i)/2;
        e2=yfy(i+1)+leny(i)/2;
        %check for overlap and delete smaller fracture
    if (e1 > e2 && s1 < e2)
        if leny(i) > leny(i+1)
            flagy(i+1)=1;
        else
            flagy(i)=1;
        end
    end
    if (e2 > e1 && s2 < e1)
        if leny(i) > leny(i+1)
            flagy(i+1)=1;
        else
            flagy(i)=1;
        end
    end
    if (e1 > e2 && s2 > s1)
        flagy(i+1)=1;
    end
    if (e2 > e1 && s1 > s2)
        flagy(i)=1;
    end
    end
end
%now delete fractures with flagy=1
yfx(flagy==1)=[];yfy(flagy==1)=[];leny(flagy==1)=[];
%
%now we have all fractures - next step is to determine ends (again)
%and plot
for i=1:length(xfx)
        xstart(i)=xfx(i)-lenx(i)/2;
        xend(i)=xfx(i)+lenx(i)/2;
        ystart(i)=xfy(i);
        yend(i)=xfy(i);
end
for i=1:length(yfx)
    j=length(xfx)+i;
        xstart(j)=yfx(i);
        xend(j)=yfx(i);
        ystart(j)=yfy(i)-leny(i)/2;
        yend(j)=yfy(i)+leny(i)/2;
end
xstart(xstart>1)=1;
xstart(xstart<-1)=-1;
xend(xend>1)=1;
xend(xend<-1)=-1;
ystart(ystart>1)=1;
ystart(ystart<-1)=-1;
yend(yend>1)=1;
yend(yend<-1)=-1;
%censoring out very small fractures (likely disconnected)
%lcens=0.2;
%x(lenth<lcens)=[];xstart(lenth<lcens)=[];xend(lenth<lcens)=[];idir(lenth<lcens)=[];
%y(lenth<lcens)=[];ystart(lenth<lcens)=[];yend(lenth<lcens)=[];
%now to plot
%plot(x,y,'r.','MarkerSize',5)
%hold on
plot(xfx,xfy,'r.','MarkerSize',5)
plot(yfx,yfy,'r.','MarkerSize',5)
for ifrac=1:length(xstart)
line([xstart(ifrac) xend(ifrac)], [ystart(ifrac) yend(ifrac)]);
end

       

