#include <math.h>
//#include "SHEAR.c" // Required only for the old implementation

// NEW IMPLEMENTATION
/* Function: deflection_angle
 * --------------------------
 * Model parameters:
 * args[0] : theta_c (the core radius)
 * args[1] : theta_E (angular radius of the Einstein ring)
 * args[2] : external shear intensity
 * args[3] : external shear orientation
 */
void deflection_angle(double theta1, double theta2,
                      int n, double args[n],
                      double *alpha1, double *alpha2){
    
    double alpha1_nis, alpha2_nis, alpha1_shear, alpha2_shear;
    
    double t1pow2 = pow(theta1,2), t2pow2 = pow(theta2, 2);
    double tcpow2 = pow(args[0],2), K0;
    
    
    // NIS
    K0 = tcpow2 + t1pow2 + t2pow2;
    
    alpha1_nis = args[1] / sqrt(K0) * theta1;
    alpha2_nis = args[1] / sqrt(K0) * theta2;
    
    // SHEAR
    if (args[3] == 0.0)
    {
        alpha1_shear =  args[2] * theta1;
        alpha2_shear = -args[2] * theta2;
    }
    else
    {
        double r = hypot(theta1,theta2);
        double phi = atan2(theta2, theta1);
        alpha1_shear =  args[2] * r * cos(phi - 2.0 * args[3]);
        alpha2_shear = -args[2] * r * sin(phi - 2.0 * args[3]);
    }
    
    // OUTPUT
    *alpha1 = alpha1_nis + alpha1_shear;
    *alpha2 = alpha2_nis + alpha2_shear;
}

void jacobi_matrix_deflection_mapping(double theta1, double theta2,
                                      int n, double args[n],
                                      double *j00, double *j01, double *j10, double *j11){
    
    double j00_nis, j01_nis, j10_nis, j11_nis;
    double j00_shear, j01_shear, j10_shear, j11_shear;
    
    double t1pow2 = pow(theta1,2), t2pow2 = pow(theta2, 2);
    double tcpow2 = pow(args[0],2), K0;
    
    K0 = tcpow2 + t1pow2 + t2pow2;
    
    // NIS
    j00_nis = args[1] / pow(K0, 1.5) * (t2pow2 + tcpow2);
    j11_nis = args[1] / pow(K0, 1.5) * (t1pow2 + tcpow2);
    j01_nis = - args[1] / pow(K0, 1.5) * theta1 * theta2;
    j10_nis = j01_nis;
    
    // SHEAR
    if (args[3] == 0.0)
    {
        j00_shear = args[2];
        j11_shear = -args[2];
        j01_shear = 0.0;
        j10_shear = 0.0;
    }
    else
    {
        j00_shear =  args[2] * cos(2.0 * args[3]);
        j11_shear = -j00_shear;
        j01_shear =  args[2] * sin(2.0 * args[3]);
        j10_shear = j01_shear;
    }

    // OUTPUT
    *j00 = j00_nis + j00_shear;
    *j01 = j01_nis + j01_shear;
    *j10 = j10_nis + j10_shear;
    *j11 = j11_nis + j11_shear;
}

// #############################################################################
// OLD IMPLEMENTATION
/*
void nis(double theta1, double theta2,
         double tc, double te,
         double *alpha1, double *alpha2,
         double *j00, double *j01, double *j10, double *j11){
    
    double t1pow2 = pow(theta1,2), t2pow2 = pow(theta2, 2);
    double tcpow2 = pow(tc,2), K0;
    
    K0 = tcpow2 + t1pow2 + t2pow2;
    
    *alpha1 = te / sqrt(K0) * theta1;
    *alpha2 = te / sqrt(K0) * theta2;
    
    *j00 = te / pow(K0, 1.5) * (t2pow2 + tcpow2);
    *j11 = te / pow(K0, 1.5) * (t1pow2 + tcpow2);
    *j01 = - te / pow(K0, 1.5) * theta1 * theta2;
    *j10 = *j01;
}

void nisg(double theta1, double theta2,
          int n, double args[n],
          double *alpha1, double *alpha2,
          double *j00, double *j01, double *j10, double *j11){
    
    double a1_nis, a2_nis, j00_nis, j01_nis, j10_nis, j11_nis;
    double a1_g, a2_g, j00_g, j01_g, j10_g, j11_g;
    
    nis(theta1, theta2, args[0], args[1], &a1_nis, &a2_nis, &j00_nis, &j01_nis, &j10_nis, &j11_nis);
    shear(theta1, theta2, args[2], args[3], &a1_g, &a2_g, &j00_g, &j01_g, &j10_g, &j11_g);
    
    *alpha1 = a1_nis + a1_g;
    *alpha2 = a2_nis + a2_g;
    
    *j00 = j00_nis + j00_g;
    *j01 = j01_nis + j01_g;
    *j10 = j10_nis + j10_g;
    *j11 = j11_nis + j11_g;
}
 */


