bits = 4
n = 1<<bits

gf_exp = [0] * n*2
gf_log = [0] * n


def gf_mult_noLUT(x, y, prim=0):
	def cl_mult(x, y):
		z = 0
		i = 0
		while (y >> i) > 0:
			if y & (1 << i):
				z ^= x << i
			i += 1
		return z

	def bit_length(n):
		bits = 0
		while n >> bits: bits += 1
		return bits

	def cl_div(dividend, divisor=None):
		dl1 = bit_length(dividend)
		dl2 = bit_length(divisor)

		if dl1 < dl2:
			return dividend

		for i in range(dl1 - dl2, -1, -1):
			if dividend & (1 << i + dl2 - 1):
				dividend ^= divisor << i
		return dividend

	result = cl_mult(x, y)

	if prim > 0:
		result = cl_div(result, prim)

	return result

def init_tables(prim):
	global gf_exp, gf_log
	gf_exp = [0] * n*2
	gf_log = [0] * n

	x = 1
	for i in range(0, n-1):
		gf_exp[i] = x
		gf_log[x] = i
		x = gf_mult_noLUT(x, 2, prim)

	for i in range(n-1, 2*n):
		gf_exp[i] = gf_exp[i - (n-1)]
	return [gf_log, gf_exp]


if __name__ == "__main__":
	t = init_tables()

	print(','.join([str(i) for i in t[0]]))
	print()
	print(','.join([str(i) for i in t[1]]))
