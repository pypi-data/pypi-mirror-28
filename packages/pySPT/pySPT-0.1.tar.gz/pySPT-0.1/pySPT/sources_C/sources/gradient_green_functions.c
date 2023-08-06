#include <math.h>

double grad_gf_1_comp_0(double theta1, double theta2, double ctheta1, double ctheta2){
    double numerator, denominator;
    
    numerator = ctheta1 - theta1;
    denominator = pow(ctheta1 - theta1,2) + pow(ctheta2 - theta2,2);
    
    return numerator/denominator;
}

double grad_gf_1_comp_1(double theta1, double theta2, double ctheta1, double ctheta2){
    double numerator, denominator;
    
    numerator = ctheta2 - theta2;
    denominator = pow(ctheta1 - theta1,2) + pow(ctheta2 - theta2,2);
    
    return numerator/denominator;
}

double grad_gf_3_comp_0(double theta1, double theta2, double ctheta1, double ctheta2, double R){
    double numerator, denominator, dotprod;
    
    double thetapow2 = pow(theta1,2) + pow(theta2,2);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);
    double Rpow2 = pow(R,2);
    
    dotprod = ctheta1*theta1 + ctheta2*theta2;
    
    numerator = thetapow2 * ctheta1 - Rpow2 * theta1;
    denominator = pow(R,4) - 2.0 * Rpow2 * dotprod + ctpow2 * thetapow2;
    
    return numerator/denominator;
}

double grad_gf_3_comp_1(double theta1, double theta2, double ctheta1, double ctheta2, double R){
    double numerator, denominator, dotprod;
    
    double thetapow2 = pow(theta1,2) + pow(theta2,2);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);
    double Rpow2 = pow(R,2);
    
    dotprod = ctheta1*theta1 + ctheta2*theta2;
    
    numerator = thetapow2 * ctheta2 - Rpow2 * theta2;
    denominator = pow(R,4) - 2.0 * Rpow2 * dotprod + ctpow2 * thetapow2;
    
    return numerator/denominator;
}
