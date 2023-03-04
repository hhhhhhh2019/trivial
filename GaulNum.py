class GaulNum:
	log = [0,0,1,4,2,8,5,10, 3,14, 9,7, 6,13,11,12]
	pow = [  1,2,4,8,3,6,12,11, 5,10,7,14,15,13, 9]

	def __init__(self, v):
		if isinstance(v, int):
			self.value = v
		else:
			raise TypeError("Ожидается число, а получено " + str(type(v)))


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

		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] + GaulNum.log[other.value]) % 15])

	def __truediv__(self, other):
		if not isinstance(other, GaulNum):
			raise TypeError("Невозможно разделить на " + str(type(other)))

		if other.value == 0:
			raise ZeroDivisionError

		if self.value == 0:
			return GaulNum(0)

		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] + 15 - GaulNum.log[other.value]) % 15])

	def __pow__(self, power, modulo=None):
		powe = power
		if isinstance(power, GaulNum):
			powe = power.num
		elif not isinstance(power, int):
			raise TypeError
		if self.value == 0:
			return GaulNum(0)
		return GaulNum(GaulNum.pow[(GaulNum.log[self.value] * powe) % 15])


	def __str__(self):
		return str(self.value)


if __name__ == "__main__":
	a = GaulNum(8)
	b = a ** -1

	print(a * b)
