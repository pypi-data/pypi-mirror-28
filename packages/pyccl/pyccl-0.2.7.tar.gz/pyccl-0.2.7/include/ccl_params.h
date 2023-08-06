/** @file */
#ifdef __cplusplus
extern "C" {
#endif

#pragma once

/** 
 * Struct that contains all the parameters needed to create certain splines.
 * This includes splines for the scale factor, masses, and power spectra.
 */
typedef struct ccl_spline_params {
   //Scale factor splines
  int  A_SPLINE_NA;
  double A_SPLINE_MIN;
  double A_SPLINE_MIN_PK;
  double  A_SPLINE_MAX;
  double A_SPLINE_MINLOG;
  int A_SPLINE_NLOG;
  
  //Mass splines
  double LOGM_SPLINE_DELTA;
  int LOGM_SPLINE_NM;
  double LOGM_SPLINE_MIN;
  double LOGM_SPLINE_MAX;
  
  //PS a and k spline
  int A_SPLINE_NA_PK;

  //k-splines and integrals
  double K_MAX_SPLINE;
  double K_MAX;
  double K_MIN_DEFAULT;
  int N_K;
  
} ccl_spline_params;

extern ccl_spline_params * ccl_splines;

#ifdef __cplusplus
}
#endif
