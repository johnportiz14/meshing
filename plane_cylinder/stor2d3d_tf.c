#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
/**** the code reads a stor file of DFN *****/
/**** user specifies the thickness (one value for all the fractures )****/
/**** then new stor file is created  ******/ 
int main(void)
{
printf("----- DFN STOR file: recalculating 2D area values to 3D volumes.----- \n"); 
char file2d[128]={0}, file3d[128]={0}, file2dnew[128]={0};
int res;
//printf("\n Please enter the name of STOR file: ");

//scanf("%s", &file2d);

//printf(" \n Please enter the name of new STOR file: ");
//scanf("%s", &file3d);
//strcpy(file2dnew, file2d);
      sprintf(file2d,"tri_fracture.stor");
      sprintf(file3d,"tri_fracture.stor");
      strcpy(file2dnew, file2d);
      
 if (res=strncmp(file2d, file3d, 128)==0)
 {

strcat(file2dnew,"2d");
  if ( 0 == rename(file2d, file2dnew) )
    {
    	printf ("\n Previous stor file %s was renamed to %s.\n", file2d, file2dnew );
    }

   else
     {
     printf ("\n File %s is not found\n", file2d);
      exit(1);
     }
 }
 FILE *f2d;
 
  if ((f2d = fopen (file2dnew,"r")) == NULL)
{
      printf ("\n File %s could not be opened\n", file2dnew);
      exit(1);
}
//printf(" Please enter the name of new STOR file: ");
//scanf("%s", &file3d);
 FILE *f3d;
 
  if ((f3d = fopen (file3d,"w")) == NULL)
{
      printf ("\n File %s could not be opened\n", file3d);
     exit(1);
}
double thickness=0.0;
 printf(" \n Please enter the thickness of fractures in DFN (in meters): ");
 scanf("%lf", &thickness);
 
 
int i,j=0,count=0;
char cs;
/*****1. ASCII Header*******/
   for (i=0; i<2; i++)
  {
    do 
{
      cs=fgetc(f2d);
     fprintf(f3d,"%c", cs);
     
 }     
    while (cs!='\n');

    }

/****2. Matrix Parameters *******/
   int nnodes, nedges, node_edge, area_coef, max_neighb,snode_edge, c=0;
   fscanf (f2d," %d %d %d %d %d \n", &nedges, &nnodes, &snode_edge, &area_coef, &max_neighb );
   fprintf (f3d," %15d  %15d  %15d  %10d  %10d \n", nedges, nnodes,snode_edge, area_coef, max_neighb );       
 double volume2d=0.0, volume3d=0.0 ;

/*****3.Voronoi Volumes *****/
for (i=0; i<nnodes; i++)
     {
     fscanf(f2d,"%lf", &volume2d);
      volume3d=volume2d*thickness;
     
     if ((((i+1) % 5)==0) || (i==nnodes-1))
     fprintf(f3d," %15.12E \n", volume3d);
     
     else
      {
      fprintf(f3d," %15.12E ", volume3d);
      }
      }
 
/****4. Count for Each Row*******/
    c=0; 
for (i=0; i<nnodes+1; i++)
     {
     fscanf(f2d,"%d", &count);
     c++;
     if (((c % 5)==0)|| (i==nnodes))
     fprintf(f3d," %10d \n", count);
     else
      {
      
      fprintf(f3d," %10d ", count);
      }
      }

/***5. Row Entries***********/
    c=0;  
for (i=0; i<nedges; i++)
     {
     fscanf(f2d,"%d", &count);
      c++;
     if (((c % 5)==0)|| (i==nedges-1))
     fprintf(f3d," %10d \n", count);
     else
      {
     
      fprintf(f3d," %10d ", count);
      }
      }
/*****6. Indices into Coefficient List*****/
   c=0; 
for (i=0; i<nedges*area_coef; i++)
     {
     fscanf(f2d,"%d", &count);
      c++;
     if (((c % 5)==0)|| (i==nedges*area_coef-1))
     fprintf(f3d," %10d \n", count);
     else
      {
      
      fprintf(f3d," %10d ", count);
      }
      }

    c=0; 
for (i=0; i<nnodes+1; i++)
     {
     fscanf(f2d,"%d", &count);
      c++;
     if (((c % 5)==0)|| (i==nnodes))
     fprintf(f3d," %10d \n", count);
     else
      {
     
      fprintf(f3d," %10d ", count);
      }
      }

   c=0; 
for (i=0; i<nnodes; i++)
     {
     fscanf(f2d,"%d", &count);
      c++;
       if (((c % 5)==0) || (i==nnodes-1))
     fprintf(f3d," %10d \n", count);
     else
      {
     
      fprintf(f3d," %10d ", count);
      }
      }
   
/***7. Geometric Area Coefficient Values****/
   
for (i=0; i<nedges*area_coef; i++)
     {
     fscanf(f2d,"%lf", &volume2d);
      volume3d=volume2d*thickness;
     
     if ((((i+1) % 5)==0)|| (i==nedges*area_coef-1))
     fprintf(f3d," %15.12E \n", volume3d);
     else
      {
      
      fprintf(f3d," %15.12E ", volume3d);
      }
      }

   fclose(f2d);
   fclose(f3d);
   printf("\n ----- DONE-------\n");   
return 0;
}
