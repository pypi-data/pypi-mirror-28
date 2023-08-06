/*-----------------------------------------------------------------*/
/*! 
  \file calcephspkseg13.c 
  \brief perform I/O on SPICE KERNEL ephemeris data file 
         for the segments of type 13
         interpolate SPICE KERNEL Ephemeris data.
         for the segments of type 13
         compute position and velocity from SPICE KERNEL ephemeris file
         for the segments of type 13.

  \author  M. Gastineau 
           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 

   Copyright, 2016, 2017, CNRS
   email of the author : Mickael.Gastineau@obspm.fr

  History:
*/
/*-----------------------------------------------------------------*/

/*-----------------------------------------------------------------*/
/* License  of this file :
 This file is "triple-licensed", you have to choose one  of the three licenses 
 below to apply on this file.
 
    CeCILL-C
    	The CeCILL-C license is close to the GNU LGPL.
    	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
   
 or CeCILL-B
        The CeCILL-B license is close to the BSD.
        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
  
 or CeCILL v2.1
      The CeCILL license is compatible with the GNU GPL.
      ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
 

This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
French law and abiding by the rules of distribution of free software.  
You can  use, modify and/ or redistribute the software under the terms 
of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
at the following URL "http://www.cecill.info". 

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability. 

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or 
data to be ensured and,  more generally, to use and operate it in the 
same conditions as regards security. 

The fact that you are presently reading this means that you have had
knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
*/
/*-----------------------------------------------------------------*/

#include "calcephconfig.h"
#if HAVE_STDIO_H
#include <stdio.h>
#endif
#if HAVE_STDLIB_H
#include <stdlib.h>
#endif
#if HAVE_STRING_H
#include <string.h>
#endif
#if HAVE_ERRNO_H
#include <errno.h>
#endif
#if HAVE_MATH_H
#include <math.h>
#endif
#if HAVE_SYS_TYPES_H
#include <sys/types.h>
#endif

#include "calcephdebug.h"
#include "real.h"
#define __CALCEPH_WITHIN_CALCEPH 1
#include "calceph.h"
#include "calcephspice.h"
#include "util.h"
#include "calcephinternal.h"

/*--------------------------------------------------------------------------*/
/* private types */
/*--------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------*/
/* private functions */
/*--------------------------------------------------------------------------*/
static void calceph_spk_interpol_Hermite_an(int m, const double *y, const double *x, double *a);

/*--------------------------------------------------------------------------*/
/*!  This function performs the Hermite Interpolation.
 
 @param m (in) degree of the polynomial.
 @param y (in) array of m+1 points
 @param x (in) array of m+1 times
 @param a (out) array of the coefficients of the polynomial of degree m
 */
/*--------------------------------------------------------------------------*/
static void calceph_spk_interpol_Hermite_an(int m, const double *x, const double *y, double *a)
{
    int i, k;

    double t, fact;

    double travail[1000];

    int nr[1000];

    k = 0;
    t = y[0];
    travail[0] = t;
    nr[k] = 0;
    for (i = 1; i <= m; i++)
    {
        if (x[i] == x[i - 1])
        {
            nr[i] = k;
            travail[i] = t;
        }
        else
        {
            k = i;
            nr[i] = i;
            t = y[i];
            travail[i] = t;
        }
    }
    /* compute the coefficients */
    a[0] = travail[0];
    fact = 1.E0;
    for (k = 1; k <= m; k++)
    {
        fact = fact * k;
        for (i = 0; i <= m - k; i++)
        {
            if (x[i] == x[i + k])
                travail[i] = y[nr[i] + k] / fact;
            else
                travail[i] = (travail[i] - travail[i + 1]) / (x[i] - x[i + k]);

        }
        a[k] = travail[0];
    }
}

/*--------------------------------------------------------------------------*/
/*!  This function computes position and velocity vectors
     using the Hermite Interpolation.                                      
                                          
 @param S (in) number of valid points in drecord .
 It assumes that S <1000/2 .                                                                        
 @param drecord (in) array of 6*S points: (x,y,z, dx/dt, dy/dt, dz/dt), (x,y,z , ...), (x, y, z,....)              
 @param depoch (in) array of S times              
 @param TimeJD0  (in) Time in seconds from J2000 for which position is desired (Julian Date)
 @param Timediff  (in) offset time from TimeJD0 for which position is desired (Julian Date)
 @param Planet (out) Pointer to external array to receive the position/velocity.
   Planet has position in ephemerides units                                 
   Planet has velocity in ephemerides units                                 
*/
/*--------------------------------------------------------------------------*/
void calceph_spk_interpol_Hermite(int S, const double *drecord, const double *depoch,
                                  double TimeJD0, double Timediff, stateType * Planet)
{
    int i, j, k, q, r, s;

    double a[1000], x[1000], y[1000];

    for (i = 0; i < 3; i++)
    {
        double P_Sum, V_Sum;

        for (k = 0; k < S; k++)
        {
            x[2 * k] = depoch[k];
            x[2 * k + 1] = depoch[k];
            y[2 * k] = drecord[6 * k + i];  /* position */
            y[2 * k + 1] = drecord[6 * k + i + 3];  /* derivative */
        }
        /* compute the coefficients of the Hermite interpolation polynomial  */
        calceph_spk_interpol_Hermite_an(2 * S - 1, x, y, a);

        /* evaluate the polynomial at time tp  : position */
        P_Sum = a[2 * S - 1];
        for (k = 2 * S - 2; k >= 0; k--)
        {
            double delta = ((TimeJD0 - x[k]) + Timediff);

            P_Sum = P_Sum * delta + a[k];
        }
        Planet->Position[i] = P_Sum;

        /* evaluate the derivative of the polynomial at time tp  : velocity */
        if (Planet->order>=1)
        {
            V_Sum = 0.E0;
            for (k = 0; k <= 2 * S - 1; k++)
            {
                double sumdelta = 0.E0;
                
                for (q = 0; q < k; q++)
                {
                    double proddelta = 1.E0;
                    
                    for (j = 0; j < k; j++)
                    {
                        if (j != q)
                            proddelta *= ((TimeJD0 - x[j]) + Timediff);
                    }
                    sumdelta += proddelta;
                }
                V_Sum = V_Sum + a[k] * sumdelta;
            }
           Planet->Velocity[i] = V_Sum;
        }

        /* evaluate the second derivative of the polynomial at time tp  : acceleration */
        if (Planet->order>=2)
        {
            double A_Sum = 0.E0;
            for (k = 0; k <= 2 * S - 1; k++)
            {
                double sumdelta = 0.E0;
                
                for (q = 0; q < k; q++)
                {
                    for (r = 0; r < k; r++)
                    {
                        double proddelta = 1.E0;
                        
                        if (q != r)
                        {
                        for (j = 0; j < k; j++)
                        {
                            if (j != r && j!=q)
                                proddelta *= ((TimeJD0 - x[j]) + Timediff);
                        }
                        sumdelta += proddelta;
                        }
                    }
                }
                A_Sum = A_Sum + a[k] * sumdelta;
            }
            Planet->Acceleration[i] = A_Sum;
        }

        /* evaluate the second derivative of the polynomial at time tp  : acceleration */
        if (Planet->order>=3)
        {
            double J_Sum = 0.E0;
            for (k = 0; k <= 2 * S - 1; k++)
            {
                double sumdelta = 0.E0;
                
                for (q = 0; q < k; q++)
                {
                    for (r = 0; r < k; r++)
                    {
                        if (q != r)
                        {
                            for (s = 0; s < k; s++)
                            {
                                double proddelta = 1.E0;
                                
                                if (s != r && s != q)
                                {
                                    for (j = 0; j < k; j++)
                                    {
                                        if (j != r && j!=q && j!=s)
                                            proddelta *= ((TimeJD0 - x[j]) + Timediff);
                                    }
                                    sumdelta += proddelta;
                                }
                            }
                        }
                    }
                }
                J_Sum = J_Sum + a[k] * sumdelta;
            }
            Planet->Jerk[i] = J_Sum;
        }
    }
}

/*--------------------------------------------------------------------------*/
/*!                                                      
     This function read the data block corresponding to the specified Time
     if this block isn't already in memory.
     
     This function works only over the specified segment.
     The segment must be of type 13.
     
     It computes position and velocity vectors for a selected  
     planetary body from Chebyshev coefficients.          

                                                                          
  @param pspk (inout) SPK file  
  @param seg (in) segment where is located TimeJD0+timediff 
  @param cache (inout) cache for the object
  @param TimeJD0  (in) Time for which position is desired (Julian Date)
  @param Timediff  (in) offset time from TimeJD0 for which position is desired (Julian Date)
  @param Planet (out) position and veloticity                                                                        
         Planet has position in km                                                
         Planet has velocity in km/sec
*/
/*--------------------------------------------------------------------------*/
int calceph_spk_interpol_PV_segment_13(struct SPKfile *pspk, struct SPKSegmentHeader *seg, struct SPICEcache *cache,
                                       treal TimeJD0, treal Timediff, stateType * Planet)
{
#if DEBUG
    int j;
#endif
    int p;

    const double Timesec = ((TimeJD0 - 2.451545E+06) + Timediff) * 86400E0;

    int recT;                   /* record where is located Timesec */

    const double *drecord;

    int nrecord;

    int subdir = 0;

    int wordbegin, wordend;

    int interpbegin, interpend;

    int S;

    double depoch[1000];

    /* read all the epoch */
    int nreadepoch = seg->seginfo.data13.count_record;

    if (nreadepoch > 100)
    {
        /* locate the correct nepoch slot using the fast directory */
        while (subdir < seg->seginfo.data13.count_directory && seg->seginfo.data13.directory[subdir] < Timesec)
        {
            subdir++;
        }
        subdir *= 100;
        /* load the subdirectory */
        wordbegin = seg->rec_begin + 6 * nreadepoch;
        wordend = wordbegin + nreadepoch - 1;

        if (calceph_spk_fastreadword(pspk, seg, cache, "", wordbegin, wordend, &drecord) == 0)
        {
            return 0;
        }
        drecord += subdir;
        nrecord = 100;
        if (subdir + nrecord >= nreadepoch)
            nrecord = nreadepoch - subdir;
    }
    else
    {                           /* less than 100 epochs */
        drecord = seg->seginfo.data13.directory;
        nrecord = nreadepoch;
    }

    /* find the record */
    recT = 0;
    while (recT < nrecord - 1 && drecord[recT] < Timesec)
        recT++;
    recT += subdir;

    /* compute the bound for the interpolation */
    S = seg->seginfo.data13.window_sizem1 + 1;
    if (S % 2 == 0)
    {
        interpbegin = recT - S / 2;
        interpend = recT + (S / 2 - 1);
    }
    else
    {
        interpbegin = recT - (S - 1) / 2;
        interpend = recT + (S - 1) / 2;
    }
    /* check if the bound are outside the records */
    if (interpbegin < 0)
    {
        interpbegin = 0;
        interpend = S - 1;
    }
    if (interpend >= nreadepoch)
    {
        interpend = nreadepoch - 1;
        interpbegin = interpend - S + 1;
    }

    /* load the record */
    for (p = 0; p < S; p++)
        depoch[p] = drecord[interpbegin + p - subdir];
    if (calceph_spk_fastreadword
        (pspk, seg, cache, "", seg->rec_begin + 6 * interpbegin, seg->rec_begin + 6 * interpend + 5, &drecord) == 0)
    {
        return 0;
    }

    calceph_spk_interpol_Hermite(S, drecord, depoch, (TimeJD0 - 2.451545E+06) * 86400E0, Timediff * 86400E0, Planet);

#if DEBUG
    /* print the record */
    printf("S=%d %d\n", S, seg->seginfo.data13.window_sizem1 + 1);
    printf("S2=%d %d\n", S, (interpend - interpbegin + 1));
    printf("Timesec=%23.16E\n", Timesec);
    printf("seg->seginfo.data13.count_record : %d\n", seg->seginfo.data13.count_record);
    printf("interpbegin=%d interpend=%d\n", interpbegin, interpend);
    printf("subdir=%d\n", subdir);
    printf("read : %d %d\n", wordbegin, wordend);
    for (p = 0; p < 6 * S; p++)
        printf("internal %d [%23.16E(=%23.16E)] %23.16E\n", p, depoch[p / 6] / 86400E0, depoch[p / 6], drecord[p]);
    printf("recT=%d\n", recT);
    if (interpbegin < 0)
        fatalerror("calceph_spk_interpol_PV_segment_13 cas 2 : %d %d\n", recT, nrecord);
    if (interpend >= seg->seginfo.data13.count_record)
        fatalerror("calceph_spk_interpol_PV_segment_13 cas 2 : %d %d\n", recT, nrecord);
    if (recT >= seg->seginfo.data13.count_record)
        fatalerror("calceph_spk_interpol_PV_segment_13 cas 2 : %d %d\n", recT, nrecord);
    if (subdir >= seg->seginfo.data13.count_record)
        fatalerror("calceph_spk_interpol_PV_segment_13 cas 1 : %d %d\n", subdir, nrecord);

    calceph_stateType_debug(Planet);
#endif

    return 1;
}
