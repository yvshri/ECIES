# ECIES.py
# 1st November 2015
# Mohit  Bhura 11CS30019
# Yash Shrivastava 13CS10054
# Souvik Sonar 15CS91S01

from sage.all import *
from random import randint


#input : a point belonging to the elliptic curve
#return : a tuple 
def point_compress(P):

	l = P.xy();
	return [int(l[0]),int(l[1])%2];


# input : a tuple consisiting of the return of point_compress
# returns : a tuple [x0/m,y0/m]
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
	S = E(alpha[0], alpha[1])
	S = m*S
	x0 = int(S.xy()[0])
	decryption = (y2*pow(x0,p-2,p))%p;
	return decryption;

def main():
	print E
	x = int(raw_input("Please enter your number : "));
	encryption = encrypt(x);
	print 'encryption : ', encryption;
	print 'decryption : ', decrypt(encryption);

x = 6917529027641089837;
p = 36*(x**4)+36*(x**3)+24*(x**2)+6*(x)+1;
a = 0
b = 3
E = EllipticCurve(GF(p),[a,b]);
n = 36*(x**4)+36*(x**3)+18*(x**2)+6*(x)+1;
P = E(1,2);
m = randint(1,n);
k = randint(1,n);
Q = m*P;
R = k*Q;
l = k*P;
main();

