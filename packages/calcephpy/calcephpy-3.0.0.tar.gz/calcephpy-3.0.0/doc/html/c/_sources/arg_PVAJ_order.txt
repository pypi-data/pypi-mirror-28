| An array to receive the cartesian position (x,y,z) and the derivatives. 
| This array must be large enough to store the results.
|  - PVAJ[1:3] contain the position (x,y,z) and is always valid.
|  - PVAJ[4:6] contain the velocity  (dx/dt,dy/dt,dz/dt) and is only valid if *order* is greater or equal to 1.
|  - PVAJ[7:9] contain the acceleration (d^2x/dt^2,d^2y/dt^2,d^2z/dt^2) and is only valid if *order* is greater or equal to 2.
|  - PVAJ[10:12] contain the jerk (d^3x/dt^3,d^3y/dt^3,d^3z/dt^3) and is only valid if *order* is equal to 3.
| The position, velocity, acceleration and jerk are expressed in Astronomical Unit (au) if unit contains |CALCEPH_UNIT_AU|.
| The position, velocity, acceleration and jerk are expressed in kilometers if unit contains |CALCEPH_UNIT_KM|.
| The velocity, acceleration, jerk, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
| The velocity, acceleration, jerk, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
| The angles of the librations of the Moon are expressed in radians if unit contains |CALCEPH_UNIT_RAD|.
| For example, to get the positions, velocities, accelerations and jerks expressed in kilometers and kilometers/seconds, the unit must be set to |CALCEPH_UNIT_KM| + |CALCEPH_UNIT_SEC|. 

