clear all; close all;

%Fracture network construction using modified Levy-Lee model
D=1.3;      %Exponent in power law distribution
beta=0.2;   %Parameter in length distribution
nfrac=500;  %Number of fractures
bp=0.01;    %Model fracture width

%Initial seed location in unit square
x(1)=rand(1,1);y(1)=rand(1,1);idir(1)=1;lenth(1)=0.002;

% NOT NAMED LENGTH BECUASE THAT IS ALREADY A MATLAB FUNCTION NAME

for ifrac=1:nfrac-1
    
    %Draw distance from inverse power law distribution
    ucent=rand(1,1);
    L=ucent^(-1/D);
    
    %Draw angle from uniform dist. on a circle
    theta=rand(1,1)*2*pi;
    
    %Assign coordinates of center of next fracture
    x(ifrac+1)=x(ifrac)+L*cos(theta);
    y(ifrac+1)=y(ifrac)+L*sin(theta);
    
    %Relocate inside -(1-bp) to +(1-bp) if outside
    if(abs(x(ifrac+1))>(1-bp)) 
    
        x(ifrac+1)=-(1-bp)+2*(1-bp)*rand(1,1);
    
    end
    
    if(abs(y(ifrac+1))>(1-bp))
    
        y(ifrac+1)=-(1-bp)+2*(1-bp)*rand(1,1);
    
    end
    
    %Calculate distance from previous center
    L=sqrt((x(ifrac+1)-x(ifrac))^2+(y(ifrac+1)-y(ifrac))^2);
    
    %Assign a length for the next fracture
    ulen=rand(1,1);
    len=-log(1-ulen)*beta*L; lenth(ifrac+1)=len;
    
    %Pick orientation x or y
    udir=rand(1,1);
    
    if (udir <= 0.5)
    
        idir(ifrac+1)=1;%x direction
    
    else
        
        idir(ifrac+1)=0;%y direction
    
    end
    
end

%At this stage, we have fracture center coordinates, directions and lengths
%now we are going to check for fractures that are overlapping and delete
%the smaller ones - start with x-direction fractures.
%Here, overlapping means same direction fractures that have centers too
%close to each other. 
%This line works because the x, y, and length vectors are in the same order
xfracsx=x(idir==1);xfracsy=y(idir==1);lenx=lenth(idir==1);

%Sort by y coordinates of centers
[xfy,inx]=sort(xfracsy);
xfx=xfracsx(inx);lenx=lenx(inx);

%Now all the x-direction fractures are sorted by the y-coordinates of their
%centers.  Need to check if centers are too close for overlapping fractures
flagx=zeros(length(xfy),1);thresh=0.05;

%We will set flagx = 1 for fractures to be deleted
for i=1:length(xfy)

    %Compare each fracture to each other y-direction fracture in network
    for j=1:length(xfy)
        
        if abs(xfy(i)-xfy(j)) < thresh && i ~= j

            %Determine end points
            s1=xfx(i)-lenx(i)/2;
            s2=xfx(j)-lenx(j)/2;
            e1=xfx(i)+lenx(i)/2;
            e2=xfx(j)+lenx(j)/2;

            %Check for overlap and delete smaller fracture
            if (e1 > e2 && s1 < e2)
                if lenx(i) > lenx(j)
                    flagx(j)=1;
                else
                    flagx(i)=1;
                end
            end
            if (e2 > e1 && s2 < e1)
                if lenx(i) > lenx(j)
                    flagx(j)=1;
                else
                    flagx(i)=1;
                end
            end
            if (e1 > e2 && s2 > s1)
                flagx(j)=1;
            end
            if (e2 > e1 && s1 > s2)
                flagx(i)=1;
            end
        end
    end
end

%Now delete fractures with flag=1
xfx(flagx==1)=[];xfy(flagx==1)=[];lenx(flagx==1)=[];

%Now work on the y-direction fractures
yfracsx=x(idir==0);yfracsy=y(idir==0);leny=lenth(idir==0);

%Sort by x coordinates of centers
[yfx,iny]=sort(yfracsx);
yfy=yfracsy(iny);leny=leny(iny);

%Now all the y-direction fractures are sorted by the x-coordinates of their
%centers.  Need to check if centers are too close for overlapping fractures
flagy=zeros(length(yfx),1);

%We will set flagy = 1 for fractures to be deleted
for i=1:length(yfx)
    
    %Compare each fracture to each other y-direction fracture in network
    for j=1:length(yfx)
    
        %If x coordinates are too close
        if abs(yfx(j)-yfx(i)) < thresh && i ~= j

            %Determine end points
            s1=yfy(i)-leny(i)/2;
            s2=yfy(j)-leny(j)/2;
            e1=yfy(i)+leny(i)/2;
            e2=yfy(j)+leny(j)/2;

            %Check for overlap and delete smaller fracture
            if (e1 > e2 && s1 < e2)
                if leny(i) > leny(j)
                    flagy(j)=1;
                else
                    flagy(i)=1;
                end
            end
            if (e2 > e1 && s2 < e1)
                if leny(i) > leny(j)
                    flagy(j)=1;
                else
                    flagy(i)=1;
                end
            end
            if (e1 > e2 && s2 > s1)
                flagy(j)=1;
            end
            if (e2 > e1 && s1 > s2)
                flagy(i)=1;
            end
        end
    end
end

%Now delete fractures with flagy=1
yfx(flagy==1)=[];yfy(flagy==1)=[];leny(flagy==1)=[];

%Censoring out very small fractures (likely disconnected)
lcens=0.1;
xfx(lenx<lcens)=[];xfy(lenx<lcens)=[];lenx(lenx<lcens)=[];
yfx(leny<lcens)=[];yfy(leny<lcens)=[];leny(leny<lcens)=[];

%Now we have all fractures - next step is to determine ends
%Also create rectangles around fractures for model subdomains

%Each fracture will now have four points to track. 
%x1,y1 - bottom left
%x2,y2 - bottom right
%x3,y3 - top right
%x4,y4 - top left

for i=1:length(xfx)
        xstart(i)=xfx(i)-lenx(i)/2;
        xend(i)=xfx(i)+lenx(i)/2;
        ystart(i)=xfy(i);
        yend(i)=xfy(i);
        
        x1(i) = xstart(i);
        x2(i) = xend(i);
        x3(i) = xend(i);
        x4(i) = xstart(i);
        y1(i) = ystart(i)-bp/2;
        y2(i) = yend(i)-bp/2;
        y3(i) = yend(i)+bp/2;
        y4(i) = ystart(i)+bp/2;
end

for i=1:length(yfx)
    j=length(xfx)+i;
        xstart(j)=yfx(i);
        xend(j)=yfx(i);
        ystart(j)=yfy(i)-leny(i)/2;
        yend(j)=yfy(i)+leny(i)/2;
        
        x1(j) = xstart(j)-bp/2;
        x2(j) = xstart(j)+bp/2;
        x3(j) = xend(j)+bp/2;
        x4(j) = xend(j)-bp/2;
        y1(j) = ystart(j);
        y2(j) = ystart(j);
        y3(j) = yend(j);
        y4(j) = yend(j);
end

%Clip the fractures to the unit square
xstart(xstart>1)=1;
xstart(xstart<-1)=-1;
xend(xend>1)=1;
xend(xend<-1)=-1;
ystart(ystart>1)=1;
ystart(ystart<-1)=-1;
yend(yend>1)=1;
yend(yend<-1)=-1;

x1(x1>1)=1;
x1(x1<-1)=-1;
x2(x2>1)=1;
x2(x2<-1)=-1;
x3(x3>1)=1;
x3(x3<-1)=-1;
x4(x4>1)=1;
x4(x4<-1)=-1;
y1(y1>1)=1;
y1(y1<-1)=-1;
y2(y2>1)=1;
y2(y2<-1)=-1;
y3(y3>1)=1;
y3(y3<-1)=-1;
y4(y4>1)=1;
y4(y4<-1)=-1;

%Create the "untrimmed" network too
for i=1:length(x)
    
    if idir(i) == 0 %y-direction
        xstart_full(i)=x(i);
        xend_full(i)=x(i);
        ystart_full(i)=y(i)-lenth(i)/2;
        yend_full(i)=y(i)+lenth(i)/2;
        
    else
        xstart_full(i)=x(i)-lenth(i)/2;
        xend_full(i)=x(i)+lenth(i)/2;
        ystart_full(i)=y(i);
        yend_full(i)=y(i);
    end

end

%Clip fractures to the unit square
xstart_full(xstart_full>1)=1;
xstart_full(xstart_full<-1)=-1;
xend_full(xend_full>1)=1;
xend_full(xend_full<-1)=-1;
ystart_full(ystart_full>1)=1;
ystart_full(ystart_full<-1)=-1;
yend_full(yend_full>1)=1;
yend_full(yend_full<-1)=-1;

figure
hold on

%Plot "untrimmed" fracture network
% for ifrac=1:length(xstart_full)
% plot([xstart_full(ifrac) xend_full(ifrac)], [ystart_full(ifrac) yend_full(ifrac)],'r');
% end

%Plot trimmed fracture network
for ifrac=1:length(xstart)
plot([xstart(ifrac) xend(ifrac)], [ystart(ifrac) yend(ifrac)],'k');
end

%Plot model fracture rectangles
for ifrac=1:length(x1)
    plot([x1(ifrac) x2(ifrac) x3(ifrac) x4(ifrac) x1(ifrac)],[y1(ifrac) y2(ifrac) y3(ifrac) y4(ifrac) y1(ifrac)],'r')
end

%Save model rectangles to text file
model_fracs = [x1',y1',x2',y2',x3',y3',x4',y4'];

save('model_fracs.txt','model_fracs','-ascii')
