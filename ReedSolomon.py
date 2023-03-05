from Matrix import Matrix
from GaulNum import GaulNum
from GaulPoly import GaulPoly


def G_polynom_generator(D):
	G = GaulPoly([GaulNum(1), GaulNum(2)])
	for itr in range(2, D):
		G *= GaulPoly([GaulNum(1), GaulNum(2) ** itr])
	return G


def encode(p, g, N, K):
	p1 = GaulPoly([*p, *([GaulNum(0)]*(N-K))])

	c = p1 + p1 % g

	return c


def decode(c, g, N, K):
	if len(c % g) == 0:
		return GaulPoly(c[:K])
	else:
		e = c % g

		t = (N-K)//2

		S = []

		for i in range(N-K):
			S.append(e.solve(GaulNum(2)**(i+1)))

		S = GaulPoly(S[::-1])

		M = Matrix(t, S)
		V = GaulPoly(S[::-1][t:t<<1])

		while M.linear_check():
			t -= 1

			M = Matrix(t, S)
			V = GaulPoly(S[::-1][t:t<<1])

		M1 = M.reversed()

		L = GaulPoly((M1 * GaulPoly(V[::-1]))[::]) * GaulPoly([1,0]) + GaulPoly([1])

		W = L * S

		for i in range(N-K):
			W[i] = GaulNum(0)

		L1 = []
		for i in range(len(L)):
			if i&1 == len(L)&1:
				L1.append(L[i])
			else:
				L1.append(GaulNum(0))
		L1 = GaulPoly(L1[:-1])

		X = []
		for i in range(1,N+1):
			if L.solve(GaulNum(i)).value == 0:
				X.append(GaulNum(i))
		X = GaulPoly(X)

		Y = []
		for i in range(len(X)):
			Y.append(W.solve(X[i])/L1.solve(X[i]))
		Y = GaulPoly(Y)

		E = GaulPoly([0] * len(c))
		for i in range(len(Y)):
			pos = GaulNum.log[(GaulNum(1)/X[i]).value]
			E[-(pos+1)] = Y[i]

		result = GaulPoly((c + E)[:K])

		#print("p =", p)
		#pprint("C =", c)
		#pprint("e =", e)
		#pprint("S =", S)
		#pprint("L =", L)
		#pprint("W =", W)
		#pprint("L'=", L1)
		#pprint("X =", X)
		#pprint("Y =", Y)
		#pprint("E =", E)
		#pprint("C =", result)

		return result


if __name__ == "__main__":
	# незабудте изменть n в файле table_generator.py!
	# n = 1 << 6

	from random import randint
	from table_generator import *

	# порождающий полином тоже надо менять
	GaulNum.log, GaulNum.pow = init_tables(0b100101)

	N = 31
	K = N - 2 * 3

	GaulNum.N = N


	g = G_polynom_generator(N-K+1)

	for _ in range(1000):
		p = GaulPoly([randint(0,N) for i in range(K)])

		encoded = encode(p, g, N, K)

		errors = []

		for i in range(3):
			n,v = randint(0,len(encoded)-1), GaulNum(randint(0,N))

			errors.append([n,v.value])

			encoded[n] = v

		decoded = decode(encoded, g, N, K)

		ok = True
		for i in range(len(p)):
			if decoded[i].value != p[i].value:
				ok = False
				break

		if ok == False:
			print("error")
			print(p)
			print(errors)
			print()

		#print(ok)
