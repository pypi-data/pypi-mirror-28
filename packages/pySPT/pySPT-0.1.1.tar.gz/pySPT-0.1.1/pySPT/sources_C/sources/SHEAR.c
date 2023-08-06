#include <math.h>

void shear_not_oriented(double theta1, double theta2,
                        double g,
                        double *alpha1, double *alpha2,
                        double *j00, double *j01, double *j10, double *j11){
    
    *alpha1 =  g * theta1;
    *alpha2 = -g * theta2;
    
    *j00 = g;
    *j11 = -g;
    *j01 = 0.0;
    *j10 = 0.0;
}

void shear(double theta1, double theta2,
           double g, double theta_g,
           double *alpha1, double *alpha2,
           double *j00, double *j01, double *j10, double *j11){
    
    double r = hypot(theta1,theta2);
    double phi = atan2(theta2, theta1);
    
    *alpha1 =  g * r * cos(phi - 2.0 * theta_g);
    *alpha2 = -g * r * sin(phi - 2.0 * theta_g);
    
    *j00 =  g * cos(2.0 * theta_g);
    *j11 = -g * cos(2.0 * theta_g);
    *j01 = g * sin(2.0 * theta_g);
    *j10 = *j01;
}
