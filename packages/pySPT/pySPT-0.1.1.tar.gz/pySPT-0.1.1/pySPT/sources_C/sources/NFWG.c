#include <math.h>
#include <gsl/gsl_sf_hyperg.h>

double Gfunction(double b, double c, double z){
    double Niter = 1, Nmax = 100;
    double step = INFINITY;
    double result = 0.0, iteration = 0.0;
    
    while ((Niter < Nmax) && (step > 1.0e-16))
    {
        iteration = (tgamma(b+Niter)/tgamma(b)) / (tgamma(c+Niter)/tgamma(c)) * pow(z,Niter)/Niter;
        
        if (fabs(iteration) < fabs(step))
        {
            step = iteration;
        }
        result = result + iteration;
        Niter ++;
    }
    return result;
}

double hyperg_2F1_series(const double a, const double b, const double c, const double x)
{
    if(x >= 1) {
        return 0.0;
    }
    else {
        return gsl_sf_hyperg_2F1(a,b,c,x);
    }
}

void deflection_angle(double theta1, double theta2,
                      int n, double args[n],
                      double *alpha1, double *alpha2){
    
    double alpha1_gnfw, alpha2_gnfw;
    double alpha1_shear, alpha2_shear;
    double alphar_gnfw;
    double T1, T2, T3;
    
    double rsNFW=args[0], ksNFW=args[1], ga=args[2];
    double g=args[3], theta_g=args[4];
    
    double r = sqrt(pow(theta1,2) + pow(theta2,2));
    double xNFW = r / rsNFW;
    double xNFWsq = pow(xNFW,2);
    
    // gNFW
    T1 = log(1.0 + xNFWsq);
    
    if (rsNFW == -1.0 && ksNFW == -1.0)  // manual criteria to not account for the gNFW model.
    {
        alphar_gnfw = 0.0;
    }
    else if (xNFW <= 1.0)
    {
        T2 = Gfunction(ga/2.0, (ga-1.0)/2.0, xNFWsq/(1.0+xNFWsq));
        T3 = pow(xNFWsq/(1.0+xNFWsq),(3.0-ga)/2.0) * (tgamma((ga-3.0)/2.0)*tgamma(1.5)/tgamma((ga-3.0)/2.0 + 1.5)) * hyperg_2F1_series(1.5, (3.0-ga)/2.0, (5.0-ga)/2.0, xNFWsq/(1.0+xNFWsq));
        alphar_gnfw = 2.0 * ksNFW / xNFW * (T1 - T2 - T3);
    }
    else if (xNFW > 1.0)
    {
        alphar_gnfw = 0.0;
    }
    
    alpha1_gnfw= alphar_gnfw / r * theta1;
    alpha2_gnfw = alphar_gnfw / r * theta2;
    
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
    *alpha1 = alpha1_gnfw + alpha1_shear;
    *alpha2 = alpha2_gnfw + alpha2_shear;
}


void jacobi_matrix_deflection_mapping(double theta1, double theta2,
                                      int n, double args[n],
                                      double *j00, double *j01, double *j10, double *j11){
    
    double j00_gnfw, j01_gnfw, j10_gnfw, j11_gnfw;
    double j00_shear, j01_shear, j10_shear, j11_shear;
    double K, Q, T, H2F1;
    double _args[n], _alpha1, _alpha2, _alphar;
    
    double rsNFW=args[0], ksNFW=args[1], ga=args[2];
    double g=args[3], theta_g=args[4];
    
    double rsq = pow(theta1,2) + pow(theta2,2);
    double r = sqrt(rsq);
    
    double xNFW = r / rsNFW;
    double rsNFWsq = pow(rsNFW,2);

    // gNFW
    T = 4.0 * rsNFW * ksNFW / (rsq * (rsq + rsNFWsq));
    H2F1 = hyperg_2F1_series(1.0, ga/2.0, 1.5, 1.0/(1.0+pow(xNFW,2)));
    _args[0]=-1, _args[1]=-1, _args[2]=args[2], _args[3]=args[3], _args[4]=args[4], _args[5]=0.0, _args[6]=0.0;
    deflection_angle(theta1, theta2, n, _args, &_alpha1, &_alpha2);
    _alphar = sqrt(pow(_alpha1,2) + pow(_alpha2,2));
    
    if (rsNFW == -1.0 && ksNFW == -1.0) // manual criteria to not account for the gNFW model.
    {
        j00_gnfw = 0.0, j11_gnfw = 0.0, j01_gnfw = 0.0, j10_gnfw = 0.0;
    }
    else
    {
        j00_gnfw = (pow(theta2,2)-pow(theta1,2)) / rsq * _alphar/r + pow(theta1,2) * T * H2F1;
        j11_gnfw = (pow(theta1,2)-pow(theta2,2)) / rsq * _alphar/r + pow(theta2,2) * T * H2F1;
        j01_gnfw = (theta1*theta2) * (-2.0 * _alphar/r / rsq +  T * H2F1);
        j10_gnfw = j01_gnfw;
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
    *j00 = j00_gnfw + j00_shear;
    *j01 = j01_gnfw + j01_shear;
    *j10 = j10_gnfw + j10_shear;
    *j11 = j11_gnfw + j11_shear;
}
