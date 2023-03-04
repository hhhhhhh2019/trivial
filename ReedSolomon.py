from Matrix import Matrix
from GaulNum import GaulNum
from GaulPoly import GaulPoly


def encode(p, N, K):
	g = GaulPoly([1,7,9,3,12,10,12])

	p1 = GaulPoly([*p, *([GaulNum(0)]*(N-K))])

	c = p1 + p1 % g

	return c


def decode(c, N, K):
	g = GaulPoly([1,7,9,3,12,10,12])

	if len(c % g) == 0:
		return GaulPoly(p[:K])
	else:
		e = c % g

		t = (N-K)//2

		S = []

		for i in range(len(e)-1,-1,-1):
			S.append(e.solve(GaulNum(2)**(len(e)-i)))

		S = GaulPoly(S[::-1])

		M = Matrix(t, S)
		V = GaulPoly(S[::-1][t:2*t])

		while M.linear_check():
			t -= 1

			M = Matrix(t, S)
			V = GaulPoly(S[::-1][t:2*t])

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
		for i in range(1,16):
			if L.solve(GaulNum(i)).value == 0:
				X.append(GaulNum(i))
		X = GaulPoly(X)

		Y = []
		for i in range(len(X)):
			#if L1.solve(X[i]).value != 0:
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
	N = 15
	K = 9

	p = GaulPoly([9,1,1,1,9,0,10,5,7])

	encoded = encode(p, N, K)

	encoded[0] = GaulNum(1)

	decoded = decode(encoded, N, K)

	ok = True
	for i in range(len(p)):
		if decoded[i].value != p[i].value:
			ok = False
			break

	print(ok)
