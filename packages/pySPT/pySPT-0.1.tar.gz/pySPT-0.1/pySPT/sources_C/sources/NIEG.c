#include <math.h>

/* Function: deflection_angle
 * -------------------
 * args[0]: b
 * args[1]: q
 * args[2]: s
 * args[3]: theta_e
 * args[4]: g
 * args[5]: theta_g
 *
 * The parameters b, q and s are related to b', e and s' through:
 * b' = b * q * sqrt(2 / (1+q**2))
 * s' = s * q * sqrt(2 / (1+q**2))
 * e = 1 - q
 *
 * The parameters b', e, theta_e and s' corresponds to the ones defined in
 * "gravlens 1.06: Software for Gravitational Lensing" by C. Keeton, Eq.(3.25) p23.
 * URL: http://www.physics.rutgers.edu/~keeton/gravlens/manual.pdf
 *
 * The parameters of the gravlens code are:
 * [p[1], p[4], p[5], p[8]] = [b', e, theta_e, s']
 *
 */
void deflection_angle(double theta1, double theta2,
                      int n, double args[n],
                      double *alpha1, double *alpha2){
    
    double alpha1_nie, alpha2_nie, alpha1_shear, alpha2_shear;
    
    double qpow2 = pow(args[1],2);
    double qp = sqrt(1 - qpow2);
    double theta1_new, theta2_new, xi, alpha1_derot, alpha2_derot;
    
    // NIS
    theta1_new = theta1*cos(args[3]) + theta2*sin(args[3]);
    theta2_new = theta2*cos(args[3]) - theta1*sin(args[3]);
    
    xi = sqrt(qpow2 * (pow(args[2],2)+pow(theta2_new,2)) + pow(theta1_new,2));
    
    alpha1_derot = args[0]*args[1]/qp * atanh((theta1_new * qp)/(xi + qpow2*args[2]));
    alpha2_derot = args[0]*args[1]/qp * atan((theta2_new * qp)/(xi + args[2]));
    
    alpha1_nie = alpha1_derot * cos(args[3]) - alpha2_derot * sin(args[3]);
    alpha2_nie = alpha1_derot * sin(args[3]) + alpha2_derot * cos(args[3]);
    
    // SHEAR
    if (args[4] == 0.0)
    {
        alpha1_shear = 0.0;
        alpha2_shear = 0.0;
    }
    else if (args[5] == 0.0)
    {
        alpha1_shear =  args[4] * theta1;
        alpha2_shear = -args[4] * theta2;
    }
    else
    {
        double r = hypot(theta1,theta2);
        double phi = atan2(theta2, theta1);
        alpha1_shear =  args[4] * r * cos(phi - 2.0 * args[5]);
        alpha2_shear = -args[4] * r * sin(phi - 2.0 * args[5]);
    }
    
    // OUTPUT
    *alpha1 = alpha1_nie + alpha1_shear;
    *alpha2 = alpha2_nie + alpha2_shear;
}


/* Function: jacobi_matrix_deflection_mapping
 * ------------------------------------------
 * args[0]: b
 * args[1]: q
 * args[2]: s
 * args[3]: theta_e
 * args[4]: g
 * args[5]: theta_g
 *
 */
void jacobi_matrix_deflection_mapping(double theta1, double theta2,
                                      int n, double args[n],
                                      double *j00, double *j01, double *j10, double *j11){
    
    double j00_nie, j01_nie, j10_nie, j11_nie;
    double j00_shear, j01_shear, j10_shear, j11_shear;
    double theta1_new, theta2_new;
    
    double b=args[0], q=args[1], s=args[2], theta_e=args[3];
    double g=args[4], theta_g=args[5];
    
    double qpow2 = pow(q,2);
    double spow2 = pow(s,2);
    double coste = cos(theta_e), sinte = sin(theta_e);
    
    theta1_new = theta1*coste + theta2*sinte;
    theta2_new = theta2*coste - theta1*sinte;
    
    // NIE
    double numerator1, numerator2, denominator;
    double split1;
    
    split1 = sqrt(qpow2 * spow2
                  + (pow(theta1,2) + qpow2 * pow(theta2,2)) * pow(cos(theta_e),2)
                  + (qpow2 * pow(theta1,2) + pow(theta2,2)) * pow(sin(theta_e),2)
                  - (-1 + qpow2) * theta1 * theta2 * sin(2*theta_e));
    
    denominator = 2*sqrt(pow(theta1_new,2) + qpow2*(spow2 + pow(theta2_new,2)))*pow((1 + qpow2)*spow2 + pow(theta1,2) + pow(theta2,2) + 2*s*sqrt(pow(theta1_new,2) + qpow2*(spow2 + pow(theta2_new,2))),2);
    
    numerator1 = b * q * ((1 + 6 * qpow2 + pow(q,4)) * pow(s,4)
                          + 2 * pow(theta2,2) * (pow(theta1,2) + pow(theta2,2))
                          + (1 + qpow2) * spow2 * (3*pow(theta1,2) + 5*pow(theta2,2))
                          + s * (-4 * (-1 + qpow2) * s * theta1 * theta2 * sin(2*theta_e)
                                 + 2 * (2 * (1 + qpow2) * spow2 + pow(theta1,2) + 3 * pow(theta2,2)) * split1
                                 - (-1 + qpow2) * s * cos(2*theta_e) * (3 * pow(theta1,2) - pow(theta2,2) + s * (s + qpow2*s + 2*split1))
                                 )
                          );
    
    numerator2 = b * q * ((1 + 6 * qpow2 + pow(q,4)) * pow(s,4)
                          + 2 * pow(theta1,2) * (pow(theta1,2) + pow(theta2,2))
                          + (1 + qpow2) * spow2 * (5*pow(theta1,2) + 3*pow(theta2,2))
                          + s * (-4 * (-1 + qpow2) * s * theta1 * theta2 * sin(2*theta_e)
                                 + 2 * (2 * (1 + qpow2) * spow2 + pow(theta2,2) + 3 * pow(theta1,2)) * split1
                                 + (-1 + qpow2) * s * cos(2*theta_e) * (3 * pow(theta2,2) - pow(theta1,2) + s * (s + qpow2*s + 2*split1))
                                 )
                          );
    
    j00_nie = numerator1 / denominator;
    j01_nie = -((b * q * (theta1*theta2 + (-1 + qpow2) * spow2 * coste * sinte))/
                (sqrt(pow(theta1_new,2) + qpow2 * (spow2 + pow(theta2_new,2)))*
                 ((1 + qpow2)*spow2 + pow(theta1,2) + pow(theta2,2) +
                  2 * s * sqrt(pow(theta1_new,2) + qpow2 * (spow2 + pow(theta2_new,2))))));
    j10_nie = j01_nie;
    j11_nie = numerator2 / denominator;
    
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
    *j00 = j00_nie + j00_shear;
    *j01 = j01_nie + j01_shear;
    *j10 = j10_nie + j10_shear;
    *j11 = j11_nie + j11_shear;
}



