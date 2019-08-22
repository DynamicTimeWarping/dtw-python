/* 
 * Compute global cost matrix - companion
 * to the dtw R package
 * (c) Toni Giorgino  2007-2012
 * Distributed under GPL-2 with NO WARRANTY.
 *
 * $Id: computeCM.c 436 2018-05-17 14:23:15Z tonig $
 *  
 */


#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#if !defined(R_VERSION) || defined(TEST_UNIT)
#define STANDALONE 1
#endif


#ifndef R_VERSION
// Define R-like functions - a bad idea
     #include <limits.h>
     #define R_NaInt INT_MIN
     #define R_alloc(n,size) alloca((n)*(size))
     #define error(...) { fprintf (stderr, __VA_ARGS__); exit(-1); }
     #define EXPORT_FLAG
#else
     #include <R.h>
     #define EXPORT_FLAG static
#endif




#ifndef NAN
#error "This code requires native IEEE NAN support. Possible solutions: 1) verify you are using gcc with -std=gnu99; 2) use the fallback interpreted DTW version (should happen automatically); 3) ask the author"
#endif


/* undo R indexing */
#define EP(ii,jj) ((jj)*nsteps+(ii))
#define EM(ii,jj) ((jj)*n+(ii))

#define CLEARCLIST { \
  for(int z=0; z<npats; z++) \
    clist[z]=NAN; }




/*
 * Auxiliary function: return the arg min, ignoring NANs, -1 if all NANs
 * TODO: remove isnan and explain, check, time
*/
static inline
int argmin(const double *list, int n) {
  int ii=-1;
  double vv=INFINITY;
  for(int i=0; i<n; i++) {
      /* The following is a faster equivalent to
       *    if(!isnan(list[i]) && list[i]<vv) 
       * because   (NAN < x) is false 
       */
    if(list[i]<vv) {
      ii=i;
      vv=list[i];
    }
  }
  return ii;
}



/* 
 *  Compute cumulative cost matrix: replaces kernel in globalCostMatrix.R
 */

/* For now, this code is also valid outside R, as a test unit (the
   STANDALONE will be defined). This means that we have to refrain to
   use R-specific functions, such as R_malloc, or conditionally
   provide replacements when STANDALONE is defined */

/* R matrix fastest index is row */

EXPORT_FLAG void computeCM(			/* IN */
	       const int *s,		/* mtrx dimensions, int */
	       const int *wm,		/* windowing matrix, logical=int */
	       const double *lm,	/* local cost mtrx, numeric */
	       const int *nstepsp,	/* no of steps in stepPattern, int */
	       const double *dir,	/* stepPattern description, numeric */
				/* IN+OUT */
	       double *cm,		/* cost matrix, numeric */
    	                        /* OUT */
	       int *sm			/* direction mtrx, int */
				) {

  /* recover matrix dim */
  int n=s[0],m=s[1];		/* query,template as usual*/
  int nsteps=*nstepsp;


  /* copy steppattern description to ints,
     so we'll do indexing arithmetic on ints 
  */
  int *pn,*di,*dj;
  double *sc;

  pn=(int*) R_alloc((size_t)nsteps,sizeof(int)); /* pattern id */
  di=(int*) R_alloc((size_t)nsteps,sizeof(int)); /* delta i */
  dj=(int*) R_alloc((size_t)nsteps,sizeof(int)); /* delta j */
  sc=(double*) R_alloc((size_t)nsteps,sizeof(double)); /* step cost */

  for(int i=0; i<nsteps; i++) {
    pn[i]=(int)dir[EP(i,0)]-1;	/* Indexing C-way */
    di[i]=(int)dir[EP(i,1)];
    dj[i]=(int)dir[EP(i,2)];
    sc[i]=dir[EP(i,3)];

    if(pn[i]<0 || pn[i]>=nsteps) {
      error("Error on pattern row %d, pattern number %d out of bounds\n",
	      i,pn[i]+1);
    }
  }

  /* assuming pattern ids are in ascending order */
  int npats=pn[nsteps-1]+1;

  /* prepare a cost list per pattern */
  double *clist=(double*)
    R_alloc((size_t)npats,sizeof(double));

  /* we do not initialize the seed - the caller is supposed
     to do so
     cm[0]=lm[0];
   */

  /* clear the direction matrix */
  for(int i=0; i<m*n; i++) 
    sm[i]=R_NaInt;			/* should be NA_INTEGER? */


  /* lets go */
  for(int j=0; j<m; j++) {
    for(int i=0; i<n; i++) {

      /* out of window? */
      if(!wm[EM(i,j)])
	continue;

      /* already initialized? */
      if(!isnan(cm[EM(i,j)]))
	  continue;

      CLEARCLIST;
      for(int s=0; s<nsteps; s++) {
	int p=pn[s];		/* indexing C-way */

	int ii=i-di[s];
	int jj=j-dj[s];
	if(ii>=0 && jj>=0) {	/* address ok? C convention */
	  double cc=sc[s];
	  if(cc==-1.0) {
	    clist[p]=cm[EM(ii,jj)];
	  } else {		/* we rely on NAN to propagate */
	    clist[p] += cc*lm[EM(ii,jj)];
	  }
	}
      }

      int minc=argmin(clist,npats);
      if(minc>-1) {
	cm[EM(i,j)]=clist[minc];
	sm[EM(i,j)]=minc+1;	/* convert to 1-based  */
      }
    }
  }
  /* Memory alloc'd by R_alloc is automatically freed */
}



/* --------------------------------------------------
 *
 * Wrapper for .Call, avoids several copies. Returns a list with names
 * "costMatrix" and "directionMatrix"
 */
#ifdef R_VERSION
#include <Rdefines.h>
#include <Rinternals.h>

SEXP computeCM_Call(SEXP wm, 	/* logical */
		    SEXP lm,	/* double */
		    SEXP cm,	/* double */
		    SEXP dir) {	/* double */

  /* Get problem size */
  SEXP lm_dim;
  PROTECT(lm_dim = GET_DIM(lm)); /* ---- 1 */
  int *p_lm_dim = INTEGER_POINTER(lm_dim);

  /* Get pattern size */
  SEXP dir_dim;
  PROTECT(dir_dim = GET_DIM(dir)); /* ---- 2 */
  int nsteps=INTEGER_POINTER(dir_dim)[0];

  /* Cost matrix (input+output 1).  */
  SEXP cmo;
  PROTECT(cmo=duplicate(cm)); /* ---- 3 */

  /* Output 2: smo, INTEGER */
  SEXP smo;
  PROTECT(smo=allocMatrix(INTSXP,p_lm_dim[0],p_lm_dim[1]));  /* ---- 4 */

  /* Dispatch to C */
  computeCM(p_lm_dim,
	    LOGICAL_POINTER(wm),
	    NUMERIC_POINTER(lm),
	    &nsteps,
	    NUMERIC_POINTER(dir),
	    NUMERIC_POINTER(cmo),
	    INTEGER_POINTER(smo));
	    
  /* cmo and smo are now set. Put them in a list. From S. Blay,
     http://www.sfu.ca/~sblay/R-C-interface.ppt */
  SEXP list_names;
  PROTECT(list_names = allocVector(STRSXP,2)); /* ---- 5 */
  SET_STRING_ELT(list_names,0,mkChar("costMatrix")); 
  SET_STRING_ELT(list_names,1,mkChar("directionMatrix")); 

  // Creating a list with 2 vector elements:
  SEXP list;
  PROTECT(list = allocVector(VECSXP, 2)); /* ---- 6 */
  SET_VECTOR_ELT(list, 0, cmo); 
  SET_VECTOR_ELT(list, 1, smo); 
  // and attaching the vector names:
  setAttrib(list, R_NamesSymbol, list_names); 

  UNPROTECT(6);
  return list;
}

#endif




/* Test as follows:

   R CMD SHLIB -d computeCM.c

    dyn.load("computeCM.so")
    lm <- matrix(nrow = 6, ncol = 6, byrow = TRUE, c(
      1, 1, 2, 2, 3, 3, 
      1, 1, 1, 2, 2, 2, 
      3, 1, 2, 2, 3, 3, 
      3, 1, 2, 1, 1, 2, 
      3, 2, 1, 2, 1, 2, 
      3, 3, 3, 2, 1, 2
    ))
    step.matrix <- as.matrix(structure(c(1, 1, 2, 2, 3, 3, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2,
     0, -1, 1, -1, 1, -1, 1), .Dim = c(6L, 4L), class = "stepPattern", npat = 3, norm = "N"))
    nsteps<-dim(step.matrix)[1]
    wm <- matrix(TRUE,6,6)
    cm <- matrix(NA,6,6)
    cm[1,1] <- lm[1,1];
    sm <- matrix(NA,6,6)

    out<-.C("computeCM",NAOK=TRUE,
       as.integer(dim(cm)),
       as.logical(wm),
       as.double(lm),
       as.integer(nsteps),
       as.double(step.matrix),
       cmo=as.double(cm),
       smo=as.integer(sm))

    cmoo<-matrix(out$cmo,6,6)
    smoo<-matrix(out$smo,6,6)
    
    storage.mode(wm) <- "logical"
    storage.mode(lm) <- "double"
    storage.mode(cm) <- "double"
    storage.mode(step.matrix) <- "double"
    
    out2<-.Call("computeCM_Call", wm, lm, cm, step.matrix)

*/








#ifdef TEST_UNIT
/* --------------------------------------------------
 * Unit test - for debugging
 */




/*
 * Printout a matrix. 
 * int *s: s[0] - no. of rows
 *         s[1] - no. of columns
 * double *mm: matrix to print
 * double *r: return value
 */

void tm_print(int *s, double *mm, double *r) {
  int i,j;
  int n=s[0],m=s[1];
  FILE *f=stdout;

  for(i=0;i<n;i++) {
    for(j=0;j<m;j++) {
      double val=mm[j*n+i];
      if(isnan(val)) {
	  printf("NAN %d %d\n",i,j);
      }
      fprintf(f,"[%2d,%2d] = %4.2lf    ",i,j,val);
    }
    fprintf(f,"\n");
  }
  *r=-1;
  // fclose(f);
  printf("** tm dump end **\n");
}


/* test  equivalent to the following
   mylm<-outer(1:10,1:10)
   globalCostNative(mylm)->myg2
*/

#define TS 5000
#define TSS (TS*TS)

void test_computeCM() {
  int ts[]={TS,TS};
  int *twm;
  double *tlm;
  int tnstepsp[]={6};
  double tdir[]={1, 1, 2, 2, 3, 3, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0,-1, 1,-1, 1,-1, 1};
  double *tcm;
  int *tsm;

  int i,j;

  twm=malloc(TSS*sizeof(int));
   for( i=0;i<TSS;i++)
    twm[i]=1;

  tlm=malloc(TSS*sizeof(double));
  for( i=0;i<TS;i++)
    for( j=0;j<TS;j++)
      tlm[i*TS+j]=(i+1)*(j+1);


  tcm=malloc(TSS*sizeof(double));
  for( i=0;i<TS;i++)
    for( j=0;j<TS;j++)
      tcm[i*TS+j]=NAN;
  tcm[0]=tlm[0];

  tsm=malloc(TSS*sizeof(int));


  double r=-2;

//  tm_print(ts,tlm,&r);

  /* pretend we'r R */
  computeCM(ts,twm,tlm,tnstepsp,
	    tdir,tcm,tsm);

//  tm_print(ts,tcm,&r);

  free(twm);
  free(tlm);
  free(tcm);
  free(tsm);

}


# include <assert.h>

void test_argmin() {
    int n=5;

    double t1[]={10,-2,NAN,2,NAN};
    double t2[]={10,-2,-3,2,-4};
    double t3[]={10,INFINITY,-3,2,-4};
    double t4[]={NAN,NAN,NAN,NAN,NAN};

    printf("argmin(t1,n)==%d, should be 1\n",argmin(t1,n));
    printf("argmin(t2,n)==%d, should be 4\n",argmin(t2,n));
    printf("argmin(t3,n)==%d, should be 4\n",argmin(t3,n));
    printf("argmin(t4,n)==%d, should be -1\n",argmin(t4,n));
    
}
 


int main(int argc,char **argv) {
    test_argmin();
    test_computeCM();
}

#endif

