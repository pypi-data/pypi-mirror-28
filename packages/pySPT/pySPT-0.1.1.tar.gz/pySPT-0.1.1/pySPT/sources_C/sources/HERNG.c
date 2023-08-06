#include <math.h>

double F(double a){
    if (a == 1.0)
    {
        return 1.0;
    }
    else if (fabs(a) < 1.0e-08)
    {
        return 0.0;
    }
    else if (a > 1)
    {
        return atan(sqrt(pow(a,2) - 1.0)) / sqrt(pow(a,2) - 1.0);
    }
    else if (a < 1)
    {
        return atanh(sqrt(1.0 - pow(a,2))) / sqrt(1.0 - pow(a,2));
    }
    else
    {
        return 0.0;
    }
}

double Fr(double a){
    if (a == 1.0)
    {
        return -2.0/3.0;
    }
    else
    {
        return (1.0 - pow(a,2) * F(a)) / (a * (pow(a,2)-1.0));
    }
}

void deflection_angle(double theta1, double theta2,
                      int n, double args[n],
                      double *alpha1, double *alpha2){
    
    double alpha1_hern, alpha2_hern;
    double alpha1_shear, alpha2_shear;
    double alphar_hern;
    
    double rsHern=args[0], ksHern=args[1];
    double g=args[2], theta_g=args[3];
    
    double r = sqrt(pow(theta1,2) + pow(theta2,2));
    double xHern = r / rsHern;
    
    // HERNQUIST
    if (rsHern == -1.0 && ksHern == -1.0) // manual criteria to not account for the Hernquist model.
    {
        alphar_hern = 0.0;
    }
    else if (xHern == 1.0)
    {
        alphar_hern = 2.0/3.0 * rsHern * ksHern;
    }
    else
    {
        alphar_hern = 2.0 * rsHern * ksHern * (xHern * (1 - F(xHern))) / (pow(xHern,2) - 1);
    }
    
    alpha1_hern = alphar_hern / r * theta1;
    alpha2_hern = alphar_hern / r * theta2;
    
    // SHEAR
    if (g == 0.0)
    {
        alpha1_shear = 0.0;
        alpha2_shear = 0.0;
    }
    else if (theta_g == 0.0)
    {
        alpha1_shear =  g * theta1;
        alpha2_shear = -g * theta2;
    }
    else
    {
        double r = hypot(theta1,theta2);
        double phi = atan2(theta2, theta1);
        alpha1_shear =  g * r * cos(phi - 2.0 * theta_g);
        alpha2_shear = -g * r * sin(phi - 2.0 * theta_g);
    }
    
    // OUTPUT
    *alpha1 = alpha1_hern + alpha1_shear;
    *alpha2 = alpha2_hern + alpha2_shear;
}


void jacobi_matrix_deflection_mapping(double theta1, double theta2,
                                      int n, double args[n],
                                      double *j00, double *j01, double *j10, double *j11){
    
    double j00_hern, j01_hern, j10_hern, j11_hern;
    double j00_shear, j01_shear, j10_shear, j11_shear;
    double K, Q;
    
    double rsHern=args[0], ksHern=args[1];
    double g=args[2], theta_g=args[3];
    
    double rsq = pow(theta1,2) + pow(theta2,2);
    double r = sqrt(rsq);
    
    double xHern = r / rsHern;
    double rsHernsq = pow(rsHern,2);
    
    // HERNQUIST
    if (rsHern == -1.0 && ksHern == -1.0) // manual criteria to not account for the Hernquist model.
    {
        j00_hern = 0.0, j11_hern = 0.0, j01_hern = 0.0, j10_hern = 0.0;
    }
    else if (xHern == 1.0)
    {
        j00_hern = 2.0/15.0 * ksHern * (-1.0 + 6.0 * pow(theta2/rsHern,2));
        j11_hern = 2.0/15.0 * ksHern * ( 5.0 - 6.0 * pow(theta2/rsHern,2));
        j01_hern = -4.0 * theta1 * theta2 * ksHern / (5.0 * rsHernsq);
        j10_hern = j01_hern;
    }
    else
    {
        K = 2.0 * ksHern * rsHern / (r * pow(rsq-rsHernsq,2));
        Q = 2.0 * ksHern * rsHernsq / pow(rsq-rsHernsq,2);
        
        j00_hern = K * (r * rsHern * (rsHernsq + pow(theta1,2) - pow(theta2,2)) * (F(xHern)-1.0) - pow(theta1,2) * (rsq-rsHernsq) * Fr(xHern));
        j11_hern =-K * (r * rsHern * (rsHernsq - pow(theta1,2) + pow(theta2,2)) * (1.0-F(xHern)) + pow(theta2,2) * (rsq-rsHernsq) * Fr(xHern));
        j01_hern = Q * theta1 * theta2 * (2.0 * (F(xHern)-1.0) - rsHern/r * (pow(r/rsHern,2)-1.0) * Fr(xHern));
        j10_hern = j01_hern;
    }
    
    // SHEAR
    if (theta_g == 0.0)
    {
        j00_shear = g;
        j11_shear = -g;
        j01_shear = 0.0;
        j10_shear = 0.0;
    }
    else
    {
        j00_shear =  g * cos(2.0 * theta_g);
        j11_shear = -j00_shear;
        j01_shear =  g * sin(2.0 * theta_g);
        j10_shear = j01_shear;
    }
    
    // OUTPUT
    *j00 = j00_hern + j00_shear;
    *j01 = j01_hern + j01_shear;
    *j10 = j10_hern + j10_shear;
    *j11 = j11_hern + j11_shear;
}
