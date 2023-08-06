#include <math.h>

// NEW IMPLEMENTATION
void jacobi_matrix_source_mapping(double beta1, double beta2,
                                  int n, double spt_args[n],
                                  double *j00, double *j01, double *j10, double *j11){
    
    double K;
    K = 1.0 + (spt_args[0] + spt_args[1] * 0.5 * (pow(beta1,2) + pow(beta2,2)));
    
    *j00 = K + beta1 * (spt_args[1] * beta1);
    *j01 = beta1 * (spt_args[1] * beta2);
    *j10 = beta2 * (spt_args[1] * beta1);
    *j11 = K + beta2 * (spt_args[1] * beta2);
}

void modified_source_position(double beta1, double beta2,
                              int n, double spt_args[n],
                              double *hb1, double *hb2){
    
    double K = 1.0 + spt_args[0] + spt_args[1] * 0.5 * (pow(beta1,2) + pow(beta2,2));
    
    *hb1 = K * beta1;
    *hb2 = K * beta2;
}

// OLD IMPLEMENTATION
/*
void jacobi_matrix(double beta1, double beta2,
                   int n, double spt_args[n],
                   double *j00, double *j01, double *j10, double *j11){
    double K;
    K = 1.0 + (spt_args[0] + spt_args[1] * 0.5 * (pow(beta1,2) + pow(beta2,2)));
    
    *j00 = K + beta1 * (spt_args[1] * beta1);
    *j01 = beta1 * (spt_args[1] * beta2);
    *j10 = beta2 * (spt_args[1] * beta1);
    *j11 = K + beta2 * (spt_args[1] * beta2);
}
 */
