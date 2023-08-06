#include <math.h>

/*
 t1, t2 = r * cos(varphi), r * sin(varphi)
 dotprod = self._ct1*t1 + self._ct2*t2
 return (1./(4.*pi)) * log(1. - 2.*dotprod/self._R**2 + self._ctheta**2 * r**2 / self._R**4)
 */

double gf_1(double theta1, double theta2, double ctheta1, double ctheta2, double R){

    double norm;
    
    norm = pow(ctheta1 - theta1, 2) + pow(ctheta2 - theta2, 2);
    return log(norm / pow(R,2)) / (4.0*M_PI);
}

double gf_2(double theta1, double theta2, double ctheta1, double ctheta2, double R){
    
    double tpow2 = pow(theta1,2) + pow(theta2,2);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);

    return (ctpow2 + tpow2) / (-4.0 * M_PI * pow(R,2));
}

double gf_3(double theta1, double theta2, double ctheta1, double ctheta2, double R){
    
    double dotprod = theta1*ctheta1 + theta2*ctheta2;
    double tpow2 = pow(theta1,2) + pow(theta2,2);
    double ctpow2 = pow(ctheta1,2) + pow(ctheta2,2);
    double norm = pow(ctheta1 - theta1, 2) + pow(ctheta2 - theta2, 2);
    
    return log(1.0 - 2.0*dotprod/pow(R,2) + ctpow2*tpow2/pow(R,4)) / (4.0*M_PI);
}
