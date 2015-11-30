# ECIES5.py
# 21st November 2015
# Mohit  Bhura 11CS30019
# Yash Shrivastava 13CS10054
# Souvik Sonar 15CS91S01
# Nadeem Shaik 11CS30033 

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

# The jacobian function
def jacobi(a, n):
	t = 1
	while a != 0:
		while a % 2 == 0:
			a >>= 1
			if n % 8 == 3 or n % 8 == 5: t = -t
		if a < n:
			a, n = n, a
			if a % 4 == 3 and n % 4 == 3: t = -t
		a = (a - n) >> 1
		if n % 8 == 3 or n % 8 == 5: t = -t
	if n == 1: return t
	else: return 0

# calculates sqrt(a)mod(p) where p is a prime

def mod_sqrt(a, p):
	a = a % p

	if p % 8 == 3 or p % 8 == 7:
		return mod_pow(a, (p+1)/4, p)

	elif p % 8 == 5:
		x = mod_pow(a, (p+3)/8, p)
		c = (x*x) % p
		if a == c:
			return x
		return (x * mod_pow(2, (p-1)/4, p)) % p

	else:
		
		# find a quadratic non-residue d
		d = 2
		while jacobi(d, p) > -1:
			d += 1

		# set p-1 = 2^s * t with t odd
		t = p - 1
		s = 0
		while t % 2 == 0:
			t /= 2
			s += 1

		at = mod_pow(a, t, p)
		dt = mod_pow(d, t, p)

		m = 0
		for i in xrange(0, s):
			if mod_pow(at * pow(dt, m), pow(2, s-1-i), p) == (p-1):
				m = m + pow(2, i)

		return (pow(a, (t+1)/2) * pow(dt, m/2)) % p


#input : a point belonging to the elliptic curve
#return : a point 
def point_double(P):
	p1 = P;
	q1 = P;
	lam = 3*p1[0]*p1[0]+a;
	inv = mod_pow(2*p1[1],p-2,p);
	lam = lam*inv;

	xr = (lam*lam - p1[0] - q1[0])%p;
	yr = lam*(p1[0]-xr)-p1[1];
	yr = yr%p
	R = (xr,yr);
	return R;

#input : 2 points belonging to the elliptic curve
#return : a point 
def point_addition(P,Q):
	p1 = P;
	q1 = Q;
	if(p1 == q1):
		return point_double(P);
	lam = (q1[1]-p1[1]);
	inv = mod_pow(q1[0]-p1[0],p-2,p);
	lam = lam*inv;

	xr = lam*lam - p1[0] - q1[0];
	yr = lam*(p1[0]-xr)-p1[1];
	xr %= p;
	yr %= p;
	R = (xr,yr);
	return R;

#input : an integer, a point belonging to the elliptic curve
#return : a point 
def point_multiply(d,P):
	m = log(d,2)+1;
	d = bin(d)[2:]
	d = list(d)
	d.reverse()
	Q  = 0;
	d = map(int,d)
	for i in (d):
		if i :
			if Q == 0 :
				Q = P;
			else:
				Q = point_addition(P,Q);
		P = point_double(P);
	return Q


def point_compress(P):

	l = P;
	return [int(l[0]),int(l[1])%2];


# input : a tuple consisiting of the return of point_compress
# return : a tuple [x0/m,y0/m]
def point_decompress(x,i):

	z = (x**3 + a*x + b)%p;
	if mod_pow(z,(p-1)/2,p) == -1 :
		return "failure";
	y = mod_sqrt(z, p)
	if y%2 == i:
		return [x,y];
	else:
		return [x,p-y];


#encryption
def encrypt(x):

	encryption = [point_compress(l),(x*int(R[0]))%p];
	return encryption;

#decryption
def decrypt(encryption):

	y1 = encryption[0];
	y2 = encryption[1];
	alpha = point_decompress(y1[0],y1[1]);
	# S = E(int(alpha[0]),int(alpha[1]));
	S = (alpha[0], alpha[1]);
	# S = m*S;
	S = point_multiply(m, S);
	x0 = int(S[0])
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
		decryption*=p;
		decryption+=d;
	print 'decryption : ',decryption;

a = 0;
b = 3;
x = 6917529027641089837;
p = 36*(x**4)+36*(x**3)+24*(x**2)+6*(x)+1;
print 'Elliptic Curve : y^2 = x^3 + ', a, 'x + ', b, ' over ';
print 'Prime : ',p;
n = 36*(x**4)+36*(x**3)+18*(x**2)+6*(x)+1;
P = (1,2);
print 'P (generator point for the elliptic curve, Public parameter) : ', P
print '<P> = n  (P is having a prime order) : ', n
m = randint(1,n);
print 'm (Private key) : ', m
k = randint(1,n);
print 'k (Secret Random Number) : ', k;
Q = point_multiply(m, P)
print 'Q ( = mP , Public parameter) : ',Q[0],Q[1];
R = point_multiply(k, Q)
print 'R (= kQ = kmP): ',R[0],R[1];
l = point_multiply(k, P)
print 'l ( = kP, used for point compression): ',l[0],l[1];
main();