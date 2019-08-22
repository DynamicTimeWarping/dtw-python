
#ifndef _DTW_COMPUTECM_H
#define  _DTW_COMPUTECM_H

void computeCM(			/* IN */
	       const int *s,		/* mtrx dimensions, int */
	       const int *wm,		/* windowing matrix, logical=int */
	       const double *lm,	/* local cost mtrx, numeric */
	       const int *nstepsp,	/* no of steps in stepPattern, int */
	       const double *dir,	/* stepPattern description, numeric */
				/* IN+OUT */
	       double *cm,		/* cost matrix, numeric */
    	                        /* OUT */
	       int *sm			/* direction mtrx, int */
					) ;

#endif
