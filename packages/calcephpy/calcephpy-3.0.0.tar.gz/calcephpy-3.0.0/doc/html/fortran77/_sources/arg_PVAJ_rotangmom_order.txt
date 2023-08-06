| An array to receive the angular momentum due to its rotation, divided by the product of the mass and of the square of the radius, and their different order of the derivatives, of the body.
| This array must be large enough to store the results. 
| -  PVAJ[1:3] contain the angular momentum  and is always valid.
| -  PVAJ[4:6] contain the first derivative and is only valid if *order* is greater or equal to 1.
| -  PVAJ[7:9] contain the second derivative and is only valid if *order* is greater or equal to 2.
| -  PVAJ[10:12]  contain the third derivative and is only valid if *order* is equal to 3.
| The angular momentum and its derivatives are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
| The angular momentum and its derivatives are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
