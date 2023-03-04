from GaulNum import GaulNum
from operator import add, sub


class GaulPoly:
	def __init__(self, data):
		if not isinstance(data, list):
			raise TypeError
		elif len(data) == 0:
			self.data = []
		elif isinstance(data[0], int):
			self.data = [GaulNum(i) for i in data]
		elif isinstance(data[0], GaulNum):
			self.data = data
		else:
			raise TypeError

	def __str__(self):
		return '{' + ' '.join([str(i) for i in self.data]) + '}'

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		if type(self.data[0]) != type(value):
			raise TypeError

		self.data[key] = value

	def __len__(self):
		return len(self.data)


	def __add__(self, other):
		if not isinstance(other, GaulPoly):
			raise TypeError("Невозможно сложить с " + str(type(other)))

		a = [GaulNum(0)] * max(0, len(other)-len(self)) + self.data
		b = [GaulNum(0)] * max(0, len(self)-len(other)) + other.data

		return GaulPoly(list(map(add, a, b)))

	def __sub__(self, other):
		if not isinstance(other, GaulPoly):
			raise TypeError("Невозможно вычесть " + str(type(other)))

		a = [GaulNum(0)] * max(0, len(other)-len(self)) + self.data
		b = [GaulNum(0)] * max(0, len(self)-len(other)) + other.data

		return GaulPoly(list(map(sub, a, b)))

	def __mul__(self, other):
		if not isinstance(other, GaulPoly):
			raise TypeError("Невозможно умножить на " + str(type(other)))

		result = GaulPoly([0] * max(len(other), len(self)))

		for i,v in enumerate(other[::-1]):
			s = GaulPoly([*([j*v for j in self]), *([GaulNum(0)]*i)])
			result += s

		return result

	def __floordiv__(self, other):
		if not isinstance(other, GaulPoly):
			raise TypeError("Невозможно разделить на " + str(type(other)))

		result = []

		a = GaulPoly(self[::])
		b = other[::]


		for i in range(len(b)):
			if b[0].value != 0:
				break

			b.pop(0)

		b = GaulPoly(b)


		for i in range(len(a)-1):
			m = a[i] / b[0]

			result.append(m)

			s = GaulPoly([*([j*m for j in b]), *([GaulNum(0)] * (len(b)-i))])

			a -= s

		return GaulPoly(result)

	def __mod__(self, other):
		if not isinstance(other, GaulPoly):
			raise TypeError("Невозможно разделить на " + str(type(other)))

		result = []

		a = GaulPoly(self[::])
		b = other[::]


		for i in range(len(b)):
			if b[0].value != 0:
				break

			b.pop(0)

		b = GaulPoly(b)


		for i in range(len(a)-1):
			m = a[i] / b[0]

			result.append(m)

			s = GaulPoly([*([j*m for j in b]), *([GaulNum(0)] * (len(b)-i))])

			a -= s


		result = a[::]

		for i in range(len(result)):
			if result[0].value != 0:
				break

			result.pop(0)

		return GaulPoly(result)


if __name__ == "__main__":
	N = 15
	K = 9

	g = GaulPoly([1,7,9,3,12,10,12])
	p = GaulPoly([0,0,0,0,0,0,0,0,1])

	p1 = GaulPoly([*p, *([GaulNum(0)]*(N-K))])

	c = p1 + p1 % g

	c[6] = GaulNum(1)

	print(c % g)
