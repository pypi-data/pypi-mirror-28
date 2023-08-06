/*
 The original model implementation (here NISG.c) must implement 2 specific functions:
    (1) ``deflection_angle``
    (2) ``jacobi_matrix_deflection_mapping``
 These functions are used into ``hat_kappa``.
 
 The SPT implementation (here isotropic_stretching_1.c) must implement 2 specific functions:
    (1) ``jacobi_matrix_source_mapping``
    (2) ``modified_source_position``
    The (1) function is used into ``hat_kappa`` and (2) into hat_alpha_dot_n
 
 Meeting these two criteria ensures to have a generic code implementation, namely which
 is valid for any model and SPT. No fine-tuning of this implementation is required to make
 it run. The only signature of the model and SPT occurs in the pre-processing part through 
 the #include lines.
*/

#include <math.h>
#include <string.h>

#include "gradient_green_functions.c"

// Original lens model
/* Here must be included the C implementation of the original lens model. The code must
 * implement both the ``deflection_angle`` and ``jacobi_matrix_deflection_mapping``.
 * For instance,
 * #include "NISG.c"
 */
#include "HERNG.c"
 
// SPT
/* Here must be included the C implementation of the SPT source mapping. The code must
 * implement both the ``jacobi_matrix_source_mapping`` and ``modified_source_position``.
 * For instance,
 * #include "isotropic_stretching_1.c"
 */
#include "isotropic_stretching_1.c"


/* Function: hat_kappa
 * -------------------
 * Generic wrapping of the modified mass distribution.
 *
 * To calculate hat_kappa, we need informations about the original model and the SPT.
 * (1) the modified model quantities are call through ``deflection_angle`` and ``jacobi_matrix_deflection_mapping``
 * (2) the jacobi matrix of the SPT is called through ``jacobi_matrix_source_mapping``
 * Therefore, the shape of this function implementation doesn't depend on the modified
 * model quantities, the number of parameters, the source mapping ...
 * Its implementation is valid in all situations.
 *
 * Parameters:
 * theta1, theta2 : double, double
 *      Position in the lens plane where hat_kappa is evaluated.
 * n0 : int
 *      Number of model arguments.
 * model_args : array of n0 double
 *      Model arguments. For instance, a NIS model requires 2 arguments, the radius of the core and
 *      the angular radius of the Einstein ring.
 * n1 : int
 *      Number of spt arguments.
 * spt_args : array of double
 *      Source mapping arguments. For instance, the isotropic stretching (1 + f0 + f2/2 *|beta|**2) beta 
 *       2 arguments, f0 and f2.
 *
 * Returns: the modified mass distribution hat_kappa evaluated in (theta1, theta2), according to 
 *          Eq.(30) in Schneider & Sluse,2014, A&A 564, A103.
 *
 */
double hat_kappa(double theta1, double theta2, int n0, double model_args[n0], int n1, double spt_args[n1]){
    
    double model_alpha1, model_alpha2, model_j00, model_j11, model_j01, model_j10;
    double spt_j00, spt_j11, spt_j01, spt_j10;
    double beta1, beta2;
    double hatA00, hatA11;
    
    deflection_angle(theta1, theta2, n0, model_args, &model_alpha1, &model_alpha2);
    jacobi_matrix_deflection_mapping(theta1, theta2, n0, model_args, &model_j00, &model_j01, &model_j10, &model_j11);
    
    beta1 = theta1 - model_alpha1;
    beta2 = theta2 - model_alpha2;
    
    jacobi_matrix_source_mapping(beta1, beta2, n1, spt_args, &spt_j00, &spt_j01, &spt_j10, &spt_j11);
    
    hatA00 = spt_j00 * (1.0 - (model_j00)) + spt_j01 * (-(model_j10));
    hatA11 = spt_j10 * (-(model_j01)) + spt_j11 * (1.0 - (model_j11));
    
    return 1.0 - 0.5 * (hatA00 + hatA11);
}


/* Function: hat_alpha_dot_n
 * -------------------------
 */
double hat_alpha_dot_n(double R, double varphi, int n0, double model_args[n0], int n1, double spt_args[n1]){
    double model_alpha1, model_alpha2, beta1, beta2, hatbeta1, hatbeta2, hatalpha1, hatalpha2;
    
    double cvarphi = cos(varphi), svarphi = sin(varphi);
    double theta1 = R * cvarphi, theta2 = R * svarphi;
    
    deflection_angle(theta1, theta2, n0, model_args, &model_alpha1, &model_alpha2);
    beta1 = theta1 - model_alpha1;
    beta2 = theta2 - model_alpha2;
    
    modified_source_position(beta1, beta2, n1, spt_args, &hatbeta1, &hatbeta2);
    
    hatalpha1 = theta1 - hatbeta1;
    hatalpha2 = theta2 - hatbeta2;
    
    return hatalpha1 * cvarphi + hatalpha2 * svarphi;
}

/* Function:
 * ---------
 * The integrand of integral I1.
 */
double integrand_i1_comp_0(double x, double delta,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){

    double hkappa, dotprod, p1, p2, p3, p, denominator, cm_t1, cm_t2;
    
    double x1 = x*cos(delta), x2 = x*sin(delta);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);
    double ctpow2m = pow(ctheta1,2) - pow(ctheta2,2);
    double Rpow2 = pow(R,2);
    
    // grad[GreenFunc_1] * CM-Jacobian, in CM-coordinates
    dotprod = ctheta1*x1 + ctheta2*x2;
    p1 = Rpow2 * (ctpow2 - Rpow2);
    p2 = R*x1/pow(x,2) + ctheta1;
    p3 = pow(Rpow2 + 2*R*dotprod + ctpow2*pow(x,2),2);
    p = p1*p2/p3;
    
    // Position in the lens plane from the position in the CM-plane
    denominator = 1.0 + 2.0*dotprod/R + ctpow2*pow(x,2)/Rpow2;
    cm_t1 = (R*x1 + ctheta1*(1.0+pow(x,2)) + (x1 * ctpow2m + 2.0 * ctheta1*ctheta2 * x2) / R) / denominator;
    cm_t2 = (R*x2 + ctheta2*(1.0+pow(x,2)) + (-x2 * ctpow2m + 2.0 * ctheta1*ctheta2 * x1) / R) / denominator;
    
    // Modified mass distribution
    hkappa = hat_kappa(cm_t1, cm_t2, n0, model_args, n1, spt_args);
    
    return hkappa * x * p / M_PI;
}

double integrand_i1_comp_1(double x, double delta,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){
    
    double hkappa, dotprod, p1, p2, p3, p, denominator, cm_t1, cm_t2;
    
    double x1 = x*cos(delta), x2 = x*sin(delta);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);
    double ctpow2m = pow(ctheta1,2) - pow(ctheta2,2);
    double Rpow2 = pow(R,2);
    
    // grad[GreenFunc_1] * CM-Jacobian, in CM-coordinates
    dotprod = ctheta1*x1 + ctheta2*x2;
    p1 = Rpow2 * (ctpow2 - Rpow2);
    p2 = R*x2/pow(x,2) + ctheta2;
    p3 = pow(Rpow2 + 2*R*dotprod + ctpow2*pow(x,2),2);
    p = p1*p2/p3;
    
    // Position in the lens plane from the position in the CM-plane
    denominator = 1.0 + 2.0*dotprod/R + ctpow2*pow(x,2)/Rpow2;
    cm_t1 = (R*x1 + ctheta1*(1.0+pow(x,2)) + (x1 * ctpow2m + 2.0 * ctheta1*ctheta2 * x2) / R) / denominator;
    cm_t2 = (R*x2 + ctheta2*(1.0+pow(x,2)) + (-x2 * ctpow2m + 2.0 * ctheta1*ctheta2 * x1) / R) / denominator;
    
    // Modified mass distribution
    hkappa = hat_kappa(cm_t1, cm_t2, n0, model_args, n1, spt_args);
    
    return hkappa * x * p / M_PI;
}

/* Function:
 * ---------
 * The integrand of integral I3.
 */
double integrand_i3_comp_0(double theta, double varphi,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){
    
    double hkappa, ggf30;
    double t1 = theta*cos(varphi), t2 = theta*sin(varphi);
    
    ggf30 = grad_gf_3_comp_0(t1, t2, ctheta1, ctheta2, R);
    hkappa = hat_kappa(t1, t2, n0, model_args, n1, spt_args);
    
    return hkappa * theta * ggf30 / M_PI;
}

double integrand_i3_comp_1(double theta, double varphi,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){
    
    double ggf31, hkappa;
    double t1 = theta*cos(varphi), t2 = theta*sin(varphi);
    
    ggf31 = grad_gf_3_comp_1(t1, t2, ctheta1, ctheta2, R);
    hkappa = hat_kappa(t1, t2, n0, model_args, n1, spt_args);
    
    return hkappa * theta * ggf31 / M_PI;
}

/* Function:
 * ---------
 * The integrand of J1
 */
double integrand_j1_comp_0(double varphi,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){

    double ggf10, dotprod;
    double t1 = R * cos(varphi), t2 = R * sin(varphi);
    
    dotprod = hat_alpha_dot_n(R, varphi, n0, model_args, n1, spt_args);
    ggf10 = grad_gf_1_comp_0(t1, t2, ctheta1, ctheta2);
    
    return R * dotprod * ggf10 / (2.0 * M_PI);
}

double integrand_j1_comp_1(double varphi,
                           double ctheta1, double ctheta2, double R,
                           int n0, double model_args[n0], int n1, double spt_args[n1]){
    
    double ggf11, dotprod;
    double t1 = R * cos(varphi), t2 = R * sin(varphi);
    
    dotprod = hat_alpha_dot_n(R, varphi, n0, model_args, n1, spt_args);
    ggf11 = grad_gf_1_comp_1(t1, t2, ctheta1, ctheta2);
    
    return R * dotprod * ggf11 / (2.0 * M_PI);
}

/* Function:
 * ---------
 * The functions wrapped in the form required by scipy.integrate.nquad()
 *
 * For I1:
 * x, delta,
 * ctheta1, ctheta2, R,
 * n0, n1,
 * model_args[0], ..., model_args[n0-1],
 * spt_args[0], ..., spt_args[n1-1]
 *
 * For I3:
 * theta, varphi,
 * ctheta1, ctheta2, R,
 * n0, n1,
 * model_args[0], ..., model_args[n0-1],
 * spt_args[0], ..., spt_args[n1-1]
 *
 * For J1:
 * varphi
 * ctheta1, ctheta2, R,
 * n0, n1,
 * model_args[0], ..., model_args[n0-1],
 * spt_args[0], ..., spt_args[n1-1]
 *
 * For NISG, model_args[4] = {tc, te, g, theta_g}.
 * For Isotropic stretching 1, spt_args[2] = {f0, f2}.
 *
 */

double integrand_I1_0(int n, double args[n]){
    int n0 = args[5], n1 = args[6];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[7], n0*sizeof(*args));
    memcpy(&spt_args, &args[7+n0], n1*sizeof(*args));
    return integrand_i1_comp_0(args[0], args[1], args[2], args[3], args[4], n0, model_args, n1, spt_args);
}

double integrand_I1_1(int n, double args[n]){
    int n0 = args[5], n1 = args[6];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[7], n0*sizeof(*args));
    memcpy(&spt_args, &args[7+n0], n1*sizeof(*args));
    return integrand_i1_comp_1(args[0], args[1], args[2], args[3], args[4], n0, model_args, n1, spt_args);
}

double integrand_I3_0(int n, double args[n]){
    int n0 = args[5], n1 = args[6];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[7], n0*sizeof(*args));
    memcpy(&spt_args, &args[7+n0], n1*sizeof(*args));
    return integrand_i3_comp_0(args[0], args[1], args[2], args[3], args[4], n0, model_args, n1, spt_args);
}

double integrand_I3_1(int n, double args[n]){
    int n0 = args[5], n1 = args[6];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[7], n0*sizeof(*args));
    memcpy(&spt_args, &args[7+n0], n1*sizeof(*args));
    return integrand_i3_comp_1(args[0], args[1], args[2], args[3], args[4], n0, model_args, n1, spt_args);
}

double integrand_J1_0(int n, double args[n]){
    int n0 = args[4], n1 = args[5];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[6], n0*sizeof(*args));
    memcpy(&spt_args, &args[6+n0], n1*sizeof(*args));
    return integrand_j1_comp_0(args[0], args[1], args[2], args[3], n0, model_args, n1, spt_args);
}

double integrand_J1_1(int n, double args[n]){
    int n0 = args[4], n1 = args[5];
    double model_args[n0], spt_args[n1];
    memcpy(&model_args, &args[6], n0*sizeof(*args));
    memcpy(&spt_args, &args[6+n0], n1*sizeof(*args));
    return integrand_j1_comp_1(args[0], args[1], args[2], args[3], n0, model_args, n1, spt_args);
}
