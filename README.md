# ECIES
ECIES.py contains the sage based implementation and ECIES5.py contains pure python based implementation.
Python implementation for Elliptic Curve Integrated Encryption Scheme
To run the code type in shell: python ECIES5.py
(python version 2.7 used)

To use the sage based implementation in sage shell: load("ECIES.py")


1. The elliptic curve used is chosen from Baretto-Naehrig class of curves which are pairing friendly curves. The prime used is of 160 bits. For point with prime order, we have chosen the generator for the curve.
2. The code can be used for any elliptic curve. The curve parameters are defined using variables 'a' and 'b', and a point 'P' having prime order and can be changed according to need. 
3. We have used the equation p = 36*(x^4)+36*(x^3)+24*(x^2)+6*(x)+1, with x = 6917529027641089837 for generating the 160 bit prime. 
reference : (Software Implementation of Pairings 1, Darrel HANKERSON, Alfred MENEZES and Michael SCOTT)
