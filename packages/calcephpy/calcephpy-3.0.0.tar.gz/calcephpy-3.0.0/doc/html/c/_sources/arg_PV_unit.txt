| An array to receive the cartesian position (x,y,z) and the velocity (xdot, ydot, zdot). 
| The position and velocity are expressed in Astronomical Unit (au) if unit contains |CALCEPH_UNIT_AU|.
| The position and velocity are expressed in kilometers if unit contains |CALCEPH_UNIT_KM|.
| The velocity, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
| The velocity, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
| The angles of the librations of the Moon are expressed in radians if unit contains |CALCEPH_UNIT_RAD|.
| For example, to get the position and velocities expressed in kilometers and kilometers/seconds, the unit must be set to |CALCEPH_UNIT_KM| + |CALCEPH_UNIT_SEC|. 

