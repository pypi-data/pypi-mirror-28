| An array to receive the euler angles and their different order of the derivatives for the orientation of the body. 
| This array must be large enough to store the results. 
| -  PVAJ[1:3] contain the angles  and is always valid.
| -  PVAJ[4:6] contain the first derivative and is only valid if *order* is greater or equal to 1.
| -  PVAJ[7:9] contain the second derivative and is only valid if *order* is greater or equal to 2.
| -  PVAJ[10:12]  contain the third derivative and is only valid if *order* is equal to 3.
| The derivatives of the angles are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
| The derivatives of the angles are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
| The angles of the orientation are expressed in radians if unit contains |CALCEPH_UNIT_RAD|.
