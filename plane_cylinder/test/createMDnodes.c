#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <math.h>
/***** the code creates a file with MDnodes in fehm format ***/
/***** MD nodes are coincident nodes *****/
/***** Also adds connectivity list of elements into fehmn file ****/

int main(void)
{
printf("\n ----- Create MD nodes list --------- \n");

FILE *mt1;

if ((mt1 = fopen ("common_pts1.table","r")) == NULL)
{
      printf ("\n First pts1table file could not be opened\n");
      exit(1);
}

FILE *md;
if ((md = fopen ("MDnodes","w")) == NULL)
{
      printf ("\n MDnodes file could not be opened\n");
      exit(1);
}

fprintf(md,"mdnode\n");
fprintf(md," 123   2     0   10.     \n   ");


FILE *inp;
if ((inp = fopen ("cyl_plane.inp","r")) == NULL)
{
      printf ("\n avs file could not be opened\n");
      exit(1);
}

int nnodes=0, nelem=0, nf=0, i=0;
fscanf(inp,"%d  %d  %d  %d  %d \n", &nnodes, &nelem, &nf, &nf, &nf); 
printf("  Total number of nodes %d \n", nnodes);
printf("  Total number of elements %d \n", nelem);
/**** reading the table with common set of nodes ********/
char line[6], line1[64];
int res1, n1=0,itp=0, nme=0, nm1=0, nm2=0, ptg=0, numb_com=0;
double coord[3]={0.0, 0.0, 0.0}; 
  do 
{
 fscanf(mt1, " %s  \n", &line);
 
 res1=strncmp(line,"pt_gtg,",7);
  }   
while (res1!=0);
  fscanf(mt1, " %s \n", &line1);
  
 for (i=0; i<nnodes; i++)
 { 

 fscanf(mt1," %d  %d  %d  %d  %d  %d \n", &n1, &itp, &nme, &nm1, &nm2, &ptg); 
 fscanf(inp, "%d  %lf  %lf  %lf \n", &nf, &coord[0], &coord[1], &coord[2]); 
  if ((itp==21) && ((nme==2)||(nme==12)) 
      {
    numb_com++;
     fprintf(md,"\n %5d  %5d  %5d",n1, 0, ptg);
      }
  }

rewind(md);
fprintf(md,"mdnode");
fprintf(md," \n %5d   %5d   %5d  10. ", numb_com, 2, 0);
fclose(mt1);
fclose(md);
printf("\n ----- There are %d MD nodes----------\n", numb_com);
printf("\n ----- MDnode file is created  -------\n");   


/*************************************/
int el1, el2, el3, el4, nelements;
double cr;
  printf("  \n Adding connectivity list to fehmn file \n");
FILE *fe;
if ((fe = fopen ("cyl_plane.fehmn","r+")) == NULL)
{
      printf ("\n fehmn file could not be opened\n");
      exit(1);
}
nelements=nelem;
 do 
{
 fscanf(fe, " %s \n ", &line);
 
 res1=strncmp(line,"elem",4);

  }   
while (res1!=0);
fseek(fe,-1,SEEK_CUR);
fprintf(fe,"     4   %10d  \n",nelements); 

   for (i=0; i<nelements; i++)
{
 fscanf(inp, " %d  %d  %s ", &nf, &nf, &line); 
  res1=strncmp(line,"tri",3);
  if (res1==0)
    {
     fscanf(inp," %d %d %d \n", &el1, &el2, &el3);
     fprintf(fe,"  %5d %5d %5d %5d %5d\n",i+1, el1, el2, el3, 0);
    }
   else
   {
  res1=strncmp(line,"tet",3);
  if (res1==0)
    {
     fscanf(inp," %d %d %d %d\n", &el1, &el2, &el3, &el4);
     fprintf(fe,"  %5d %5d %5d %5d %5d\n",i+1, el1, el2, el3, el4);
    }
   else

     printf(" The type of element is not 'tri' and not 'tet'.\n");
    }
}   
fprintf(fe, "\nstop");

printf("\n ----- Done with writing connectivity list into fehmn file  -------\n");


fclose(fe);
fclose(inp);


   printf("\n ----- DONE-------\n");   
   
   printf(" \n check for MD nodes \n");
   
   
   
return 0;
}
