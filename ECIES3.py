# ECIES3.py
# 1st November 2015
# Mohit  Bhura 11CS30019
# Yash Shrivastava 13CS10054
# Souvik Sonar 15CS91S01

from sage.all import *
from random import randint
from math import *

#input : 3 integers - base, exp, modulus
# output : (base^exp)%modulus
def mod_pow(base, exp ,modulus):

	base%=modulus;
	result = 1;
	while ( exp > 0):
		if ( exp & 1 > 0 ):
			result = (result*base)%modulus
		base = (base*base)%modulus;
		exp/=2;
	return result;



#input : a point belonging to the elliptic curve
#return : a point 
def point_double(P):
	p1 = map(int,P.xy());
	q1 = map(int,P.xy());
	lam = 3*p1[0]*p1[0]+a;
	# lam/=(2*p1[1]);
	inv = mod_pow(2*p1[1],p-2,p);
	lam = lam*inv;
	# print 'inv : ',inv
	# print 'yp = ',2*p1[1];
	# print 'lam = ',lam;
	xr = (lam*lam - p1[0] - q1[0])%p;
	yr = lam*(p1[0]-xr)-p1[1];
	yr = yr%p
	R = E(xr,yr);
	return R;

#input : 2 points belonging to the elliptic curve
#return : a point 
def point_addition(P,Q):
	p1 = map(int,P.xy());
	q1 = map(int,Q.xy());
	if(p1 == q1):
		return point_double(P);
	lam = (q1[1]-p1[1]);
	inv = mod_pow(q1[0]-p1[0],p-2,p);
	lam = lam*inv;
	# print 'inv : ',inv
	# print 'den : ', q1[0]-p1[0];
	# print 'lam = ',lam;
	xr = lam*lam - p1[0] - q1[0];
	yr = lam*(p1[0]-xr)-p1[1];
	xr %= p;
	yr %= p;
	R = E(xr,yr);
	return R;

#input : an integer, a point belonging to the elliptic curve
#return : a point 
def point_multiply(d,P):
	p1 = map(int,P.xy());
	m = log(d,2)+1;
	d = bin(d)[2:]
	d = list(d)
	d.reverse()
	# print 'd : ',d;
	# d = d[1:];
	# Q  = E(0,0);
	# Q = P
	Q  = 0;
	d = map(int,d)
	for i in (d):
		# print i,Q;
		if i :
			if Q == 0 :
				Q = P;
			else:
				Q = point_addition(P,Q);
		P = point_double(P);
	return Q


def point_compress(P):

	l = P.xy();
	return [int(l[0]),int(l[1])%2];


# input : a tuple consisiting of the return of point_compress
# return : a tuple [x0/m,y0/m]
def point_decompress(x,i):

	z = (x**3 + a*x + b)%p;
	if power_mod(z,(p-1)/2,p) == -1 :
		return "failure";
	y = int(Mod(z,p).sqrt());
	if y%2 == i:
		return [x,y];
	else:
		return [x,p-y];


#encryption
def encrypt(x):

	encryption = [point_compress(l),(x*int(R.xy()[0]))%p];
	return encryption;

#decryption
def decrypt(encryption):

	y1 = encryption[0];
	y2 = encryption[1];
	alpha = point_decompress(y1[0],y1[1]);
	S = E(int(alpha[0]),int(alpha[1]));
	# S = m*S;
	S = point_multiply(m, S);
	x0 = int(S.xy()[0])
	decryption = (y2*mod_pow(x0,p-2,p))%p;
	return decryption;


def main():

	encryption = [];
	arr = [];
	x = int(raw_input("Please enter your number : "));	
	while x > 0 :	
		arr.append(x%p);	
		encryption.append(encrypt(x%p));
		x/=p;
	print 'encryption : ', encryption;
	encryption.reverse();
	decryption = 0;
	for a,i in enumerate(encryption) :
		d = decrypt(i);
		# print '\t\t',arr[a],d;
		decryption*=p;
		decryption+=d;
	print 'decryption : ',decryption;

# a = 1;
# b = 6;
a = 0;
b = 3;
x = 6917529027641089837;
p = 36*(x**4)+36*(x**3)+24*(x**2)+6*(x)+1;
# p = 11
E = EllipticCurve(GF(p),[a,b]);
n = 36*(x**4)+36*(x**3)+18*(x**2)+6*(x)+1;
# n = 10;
P = E(1,2);
# P = E(2,7);
m = randint(1,n);
# m = 7;
k = randint(1,n);
# k = 6;
# Q = m*P;
Q = point_multiply(m, P)
print 'Q : ',Q[0],Q[1];
# R = k*Q;
R = point_multiply(k, Q)
print 'R : ',R[0],R[1];
# l = k*P;
l = point_multiply(k, P)
print 'l : ',l[0],l[1];
print ' Prime : ',p;
main();

