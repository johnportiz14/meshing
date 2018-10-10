#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <math.h>
/***** this code merges two stor files into one (for tet and tri ) ***/
/*****  without summ of volume values and area values for concident nodes (keeping duplicate nodes)*******/  

int main(void)
{
printf("\n----- Merging two stor files into one. --------- \n");
printf(" Format of stor files is ascii, no compression. \n");
printf(" Geometric area coefficients are scalar values (NUM_AREA_COEF = 1). \n");
printf(" This stor file includes all the duplicate nodes. To run FEHM MDnode list is required.\n"); 
FILE *mesh1;
FILE *mesh2;
if ((mesh1 = fopen ("plane.stor","r")) == NULL)
{
      printf ("\n First stor file could not be opened\n");
      exit(1);
}

if ((mesh2 = fopen ("cylinder.stor","r")) == NULL)
{
      printf ("\n Second stor file could not be opened\n");
      exit(1);
}

FILE *fm;
if ((fm = fopen ("cyl_plane.stor","w")) == NULL)
{
      printf ("\n File final_mesh could not be opened\n");
      exit(1);
}


int i,j=0,count=0, numb_com=0;
char cs, ms;

/***** ASCII Header  of stor files*******/
   for (i=0; i<2; i++)
  {
    do 
{
      cs=fgetc(mesh1);
      fprintf(fm,"%c", cs);
      ms=fgetc(mesh2); 
 }     
    while (cs!='\n');

    }
/****Matrix Parameters in stor files*******/
   int nnodes1, nedges1, node_edge1, area_coef1, max_neighb1,snode_edge1;
   int nnodes2, nedges2, node_edge2, area_coef2, max_neighb2,snode_edge2;

   fscanf (mesh1," %d %d %d %d %d \n", &nedges1, &nnodes1, &snode_edge1, &area_coef1, &max_neighb1 );
   fscanf (mesh2," %d %d %d %d %d \n", &nedges2, &nnodes2, &snode_edge2, &area_coef2, &max_neighb2 );



int final_number=0;
final_number=nnodes1+nnodes2;
 int fin_nedge=0;
fin_nedge=nedges1+nedges2;
int fin_snode;
fin_snode=1+fin_nedge+final_number; 
int finmax=0;
if (max_neighb1>max_neighb2)
   finmax=max_neighb1;
else
   finmax=max_neighb2;

fprintf(fm," %15d  %15d  %15d  %10d  %10d \n",  fin_nedge, final_number, fin_snode, 1, finmax);
/***** Voronoi Volumes *****/


double voronoi=0;
 for (i=0; i<nnodes1; i++)
{
fscanf(mesh1," %lf ", &voronoi);
     if (((i+1) % 5)==0)
     fprintf(fm, " %15.12E \n", voronoi);
     else
     fprintf(fm, " %15.12E ", voronoi);
}
for (i=0; i<nnodes2; i++)
{
fscanf(mesh2," %lf ", &voronoi);
     if (((i+1+nnodes1) % 5)==0)
     fprintf(fm, " %15.12E \n", voronoi);
     else
     fprintf(fm, " %15.12E ", voronoi);
}
printf("\n ----- Done with writing Voronoi polygon's volumes  -------\n");
/**** writing number of nodes and connectivity list ****/
if ((final_number % 5)!=0)
    fprintf(fm,"\n");


 int c=0, coef=0, coef1=0,coef2=0, coef3=0;
for (i=0; i<nnodes1+1; i++)
{ 
fscanf(mesh1," %d ", &coef);  
  c++;
  coef1=coef-nnodes1+final_number;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef1);
     else
      fprintf(fm, " %10d ", coef1);
  }
coef3=coef1;
fscanf(mesh2," %d ", &coef);  
for (i=0; i<nnodes2; i++)
{
fscanf(mesh2," %d ", &coef2);
coef1=(coef2-coef)+coef3;  
coef3=coef1;
  c++;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef1);
     else
      fprintf(fm, " %10d ", coef1);
coef=coef2; 
}

if ((c % 5) !=0)   
fprintf(fm,"\n");
//matrix entries
c=0;
coef=0;
for (i=0; i<nedges1; i++)
{
fscanf(mesh1," %d ", &coef);  
  c++;
  
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef);
     else
      fprintf(fm, " %10d ", coef);
}
for (i=0; i<nedges2; i++)
{
fscanf(mesh2," %d ", &coef);  
  c++;
  coef1=coef+nnodes1;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef1);
     else
      fprintf(fm, " %10d ", coef1);
}

printf("\n ----- Done with writing connectivity list  -------\n");

int nf=0;

if ((c % 5) !=0)   
fprintf(fm,"\n");
c=0;
for (i=0; i<nedges1; i++)
   {
fscanf(mesh1," %d ", &nf);  
     c++;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", nf);
     else
      fprintf(fm, " %10d ", nf);
    }
for (i=0; i<nedges2; i++)
   {
fscanf(mesh2," %d ", &nf);  
     c++;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", nf+nedges1);
     else
      fprintf(fm, " %10d ", nf+nedges1);
    }

if ((c % 5) !=0)   
fprintf(fm,"\n");
c=0;

for (i=0; i<nnodes1+1; i++)
   {
fscanf(mesh1," %d ", &nf);  
     c++;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", 0);
     else
      fprintf(fm, " %10d ", 0);
    }
for (i=0; i<nnodes2+1; i++)
   {
fscanf(mesh2," %d ", &nf);  
     c++;
    if (((c) % 5)==0)
      fprintf(fm, " %10d \n", 0);
     else
      fprintf(fm, " %10d ", 0);
    }
//diagonal elements
int diel=final_number+1;
if ((c % 5) !=0)   
fprintf(fm,"\n"); 
c=0;
for (i=0; i<nnodes1; i++)
 {
fscanf(mesh1," %d ", &nf);

        c++;
     if (((c) % 5)==0)
      fprintf(fm, " %10d \n", nf+nnodes2);
     else
      fprintf(fm, " %10d ", nf+nnodes2);
coef=nf+nnodes2+1;
}
fscanf(mesh2," %d ", &nf);
coef1=coef-nf;
for (i=0; i<nnodes2-1; i++)
 {

        c++;
     if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef);
     else
      fprintf(fm, " %10d ", coef);
fscanf(mesh2," %d ", &nf);
coef=nf+coef1;
}
   c++;
     if (((c) % 5)==0)
      fprintf(fm, " %10d \n", coef);
     else
      fprintf(fm, " %10d ", coef);

printf("\n ----- Done with writing diagonal elements of matrix  --------\n");
/**** writing area coefficients *****/
double areas;
if ((c % 5) !=0)   
fprintf(fm,"\n");
c=0;
for (i=0; i<nedges1; i++)
 {
fscanf(mesh1," %lf ", &areas);
        c++;
     if (((c) % 5)==0)
      fprintf(fm, " %15.12E\n", areas);
     else
      fprintf(fm, " %15.12E", areas);
 }
  for (i=0; i<nedges2; i++)
 {
fscanf(mesh2," %lf ", &areas);
        c++;
     if (((c) % 5)==0)
      fprintf(fm, " %15.12E\n", areas);
     else
      fprintf(fm, " %15.12E", areas);
 }  

printf("\n ----- Done with writing area coefficients  -------\n");
fprintf(fm, "\n");

/***********************************/
 
  fclose(mesh1);
fclose(mesh2);


fclose(fm);
   printf(" \n New stor file: cyl_plane.stor \n");
/*************************************/
 

   printf("\n ----- DONE-------\n");   
return 0;
}
