class GaulNum:
	log = []
	pow = []

	N = 0

	def __init__(self, v):
		if isinstance(v, int):
			self.value = v
		else:
			raise TypeError("Ожидается число, а получено " + str(type(v)))

	def __eq__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError

		return self.value == other.value

	def __add__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError("Невозможно сложить с " + str(type(other)))

		return GaulNum(self.value ^ other.value)

	def __sub__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError("Невозможно сложить с " + str(type(other)))

		return GaulNum(self.value ^ other.value)

	def __mul__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError("Невозможно умножить на " + str(type(other)))

		if self.value == 0 or other.value == 0:
			return GaulNum(0)

		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] + GaulNum.log[other.value]) % GaulNum.N])

	def __truediv__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError("Невозможно разделить на " + str(type(other)))

		if other.value == 0:
			raise ZeroDivisionError

		if self.value == 0:
			return GaulNum(0)

		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] + GaulNum.N - GaulNum.log[other.value]) % GaulNum.N])

	def __pow__(self, power, modulo=None):
		powe = power
		if isinstance(power, GaulNum):
			powe = power.num
		elif not isinstance(power, int):
			raise TypeError
		if self.value == 0:
			return GaulNum(0)
		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] * powe) % GaulNum.N])


	def __str__(self):
		return str(self.value)


if __name__ == "__main__":
	for i in range(10):
		print(GaulNum(i)*GaulNum(i))

