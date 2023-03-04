from Matrix import Matrix
from GaulNum import GaulNum
from GaulPoly import GaulPoly


if __name__ == "__main__":
	N = 15
	K = 9

	g = GaulPoly([1,7,9,3,12,10,12])

	# кодирование

	p = GaulPoly([9,1,1,1,9,0,10,5,7])

	p1 = GaulPoly([*p, *([GaulNum(0)]*(N-K))])

	c = p1 + p1 % g

	c[1] = GaulNum(3)
	c[3] = GaulNum(2)
	c[6] = GaulNum(13)

	# декодирование и исправление ошибок

	result = GaulPoly([])

	if len(c % g) == 0:
		print("Ошибок нет")
		result = GaulPoly(p[0:K])
	else:
		print("Есть ошибки")

		e = c % g

		t = (N-K)//2

		S = []

		for i in range(len(e)-1,-1,-1):
			S.append(e.solve(GaulNum(2)**(len(e)-i)))

		S = GaulPoly(S[::-1])

		M = Matrix(t, S)
		V = GaulPoly(S[::-1][t:2*t])

		while M.chekLinearFunction():
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
			if i&1 == 0:
				L1.append(L[2-i])
			else:
				L1.append(GaulNum(0))
		L1 = GaulPoly(L1[::-1])

		X = []
		for i in range(1,16):
			if L.solve(GaulNum(i)).value == 0:
				X.append(GaulNum(i))
		X = GaulPoly(X)

		Y = []
		for i in range(len(X)):
			Y.append(W.solve(X[i])/L1.solve(X[i]))
		Y = GaulPoly(Y)

		E = GaulPoly([0] * len(c))
		for i in range(len(X)):
			pos = GaulNum.log[(GaulNum(1)/X[i]).value]
			E[-(pos+1)] = Y[i]

		result = GaulPoly((c + E)[:K])

		print("p =", p)
		print("C =", c)
		print("e =", e)
		print("S =", S)
		print("L =", L)
		print("W =", W)
		print("L'=", L1)
		print("X =", X)
		print("Y =", Y)
		print("E =", E)
		print("C =", result)


	ok = True
	for i in range(len(p)):
		if result[i].value != p[i].value:
			ok = False
			break

	print(ok)
