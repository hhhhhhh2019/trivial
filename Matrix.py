from GaulNum import GaulNum
from GaulPoly import GaulPoly
from itertools import combinations



class Matrix:
	def __init__(self, t, data):
		self.data = [[None] * t for i in range(t)]

		for r in range(t): # строка
			for c in range(t): # столбец
				self.data[r][c] = data[-(t+r-c)]

	def __len__(self):
		return len(self.data)

	def __str__(self):
		return '\n'.join([' '.join([str(self.data[i][j]) for j in range(len(self))]) for i in range(len(self))])

	def row(self, y):
		return self.data[y]

	def col(self, x):
		return [self.data[i][x] for i in range(len(self))]


	def __mul__(self, other):
		if isinstance(other, Matrix):
			zip_b = zip(*other.data)
			# uncomment next line if python 3 :
			# zip_b = list(zip_b)
			res = Matrix([GaulNum(0)] * len(self.data[0]) * 2, len(self.data[0]))
			for i in range(0, len(self.data)):
				for j in range(0, len(other.data[0])):
					for k in range(0, len(self.data[0])):
						res.data[i][j] += self.data[i][k] * other.data[k][j]
			return res
		elif isinstance(other, GaulPoly):
			if len(self.data[0]) != len(other):
				raise Exception('Размеры матриц не соответствуют!')

			res = [GaulNum(0)] * len(other)

			for x in range(len(self)):
				a = self.col(x)
				b = other
				res[x] = sum([a[i] * b[i] for i in range(len(self))], GaulNum(0))

			return GaulPoly(res)
		else:
			raise TypeError


	def det(self, A, size):
		if size == 1:
			return A[0][0]
		detA = GaulNum(0)
		for itr, a in enumerate(A[0]):
			detA += a * self.det(
				[[A[i][j] for j in range(size) if j != itr] for i in range(1, size)],
				size - 1)
		return detA

	def minor(self, A, a, b, size):
		return self.det([[A[i][j] for j in range(size) if j != b] for i in range(size) if i != a], size - 1)

	def reverse_data(self):
		if len(self) == 1:
			return

		detA = self.det(self.data, len(self))

		B = [[GaulNum(0) for i in range(len(self))] for j in range(len(self))]
		for i in range(len(self)):
			for j in range(len(self)):
				B[j][i] = self.minor(self.data, i, j, len(self)) / detA

		self.data = B

	def reversed(self):
		m = Matrix(0, [])
		m.data = self.data[::]

		m.reverse_data()
		return m


	def chekLinearFunction(self):
		for k in range(2, len(self.data) + 1):
			for B in combinations(self.data, k):
				if sum([GaulNum(sum(i, GaulNum(0)).value % 2) for i in B], GaulNum(0)) == GaulNum(0) or sum(
						[GaulNum(sum([B[j][i] for j in range(len(B))], GaulNum(0)).value % 2) for i in range(len(B[0]))],
						GaulNum(0)) == GaulNum(0):
					return True
		return False


if __name__ == "__main__":
	a = Matrix(2, [GaulNum(1),GaulNum(2),GaulNum(3),GaulNum(4)])
	b = a.reversed()

	print(a)
	print(b)
	print(a*b)
