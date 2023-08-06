#include <math.h>
#include <gsl/gsl_sf_hyperg.h>

#define DBL_EPSILON        2.2204460492503131e-16

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

/* hyperg_2F1_series
 * Code inspired by the open-source GSL (GNU Scientific Library)
 * (https://github.com/ampl/gsl/blob/master/specfunc/hyperg_2F1.c)
 */

double hyperg_2F1_series(const double a, const double b, const double c, const double x)
{
    if(x >= 1) {
        return 0.0;
    }
    else {
        return gsl_sf_hyperg_2F1(a,b,c,x);
    }
}

/*
double hyperg_2F1_series(const double a, const double b, const double c, const double x)
{
    double sum_pos = 1.0;
    double sum_neg = 0.0;
    double del_pos = 1.0;
    double del_neg = 0.0;
    double del = 1.0;
    double del_prev;
    double k = 0.0;
    int i = 0;
    
    if(fabs(c) < DBL_EPSILON) {
        return 0.0;
    }
    
    do {
        if(++i > 30000) {
            return sum_pos - sum_neg;
        }
        
        del_prev = del;
        del *= (a+k)*(b+k) * x / ((c+k) * (k+1.0));  // Gauss series
        
        if(del > 0.0) {
            del_pos  =  del;
            sum_pos +=  del;
        }
        else if(del == 0.0) {
            // Exact termination (a or b was a negative integer).
            del_pos = 0.0;
            del_neg = 0.0;
            break;
        }
        else {
            del_neg  = -del;
            sum_neg -=  del;
        }
        //
        // This stopping criteria is taken from the thesis
        // "Computation of Hypergeometic Functions" by J. Pearson, pg. 31
        // (http://people.maths.ox.ac.uk/porterm/research/pearson_final.pdf)
        //
 
        if (fabs(del_prev / (sum_pos - sum_neg)) < DBL_EPSILON &&
            fabs(del / (sum_pos - sum_neg)) < DBL_EPSILON)
            break;
        
        k += 1.0;
    } while(fabs((del_pos + del_neg)/(sum_pos-sum_neg)) > DBL_EPSILON);
    
    return sum_pos - sum_neg;
}
*/


void deflection_angle(double theta1, double theta2,
                      int n, double args[n],
                      double *alpha1, double *alpha2){
    
    double alpha1_hern, alpha2_hern, alpha1_gnfw, alpha2_gnfw;
    double alpha1_shear, alpha2_shear;
    double alphar_hern, alphar_gnfw;
    double T1, T2, T3;
    
    double rsHern=args[0], ksHern=args[1];
    double rsNFW=args[2], ksNFW=args[3], ga=args[4];
    double g=args[5], theta_g=args[6];
    
    double r = sqrt(pow(theta1,2) + pow(theta2,2));
    double xHern = r / rsHern;
    double xNFW = r / rsNFW;
    double xNFWsq = pow(xNFW,2);
    
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
    *alpha1 = alpha1_hern + alpha1_gnfw + alpha1_shear;
    *alpha2 = alpha2_hern + alpha2_gnfw + alpha2_shear;
}


void jacobi_matrix_deflection_mapping(double theta1, double theta2,
                                      int n, double args[n],
                                      double *j00, double *j01, double *j10, double *j11){
    
    double j00_hern, j01_hern, j10_hern, j11_hern;
    double j00_gnfw, j01_gnfw, j10_gnfw, j11_gnfw;
    double j00_shear, j01_shear, j10_shear, j11_shear;
    double K, Q, T, H2F1;
    double _args[n], _alpha1, _alpha2, _alphar;
    
    double rsHern=args[0], ksHern=args[1];
    double rsNFW=args[2], ksNFW=args[3], ga=args[4];
    double g=args[5], theta_g=args[6];
    
    double rsq = pow(theta1,2) + pow(theta2,2);
    double r = sqrt(rsq);
    
    double xHern = r / rsHern;
    double rsHernsq = pow(rsHern,2);
    double xNFW = r / rsNFW;
    double rsNFWsq = pow(rsNFW,2);
    
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
    *j00 = j00_hern + j00_gnfw + j00_shear;
    *j01 = j01_hern + j01_gnfw + j01_shear;
    *j10 = j10_hern + j10_gnfw + j10_shear;
    *j11 = j11_hern + j11_gnfw + j11_shear;
}
