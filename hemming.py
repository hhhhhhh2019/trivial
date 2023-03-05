from math import log2, ceil


def encode(data):
	data = list(data)

	N = 0

	while (1<<N) < N + len(data) + 1:
		N += 1

	ids = [1<<i for i in range(N)]

	for i in ids:
		data.insert(i - 1, '0')

	for i in ids:
		s = 0
		for j in range(i-1,len(data),i<<1):
			s += sum([int(k) for k in data[j:j+i]])
		data[i-1] = str(s % 2)

	return ''.join(data)


def decode(data):
	data = list(data)

	N = 0

	for i in range(len(data),0,-1):
		if i & (i - 1) == 0:
			N = int(log2(i)) + 1
			break

	ids = [1<<i for i in range(N)]

	party = []

	for i in ids:
		party.append(data[i-1])
		data[i-1] = 0

	error = 0

	for n,i in enumerate(ids):
		s = 0
		for j in range(i-1,len(data),i<<1):
			s += sum([int(k) for k in data[j:j+i]])

		if int(party[n]) != s % 2:
			error += i

	if error not in ids and error < len(data):
		data[error - 1] = str(1 - int(data[error - 1]))

	result = ""

	for i,v in enumerate(data):
		if i & (i + 1) != 0:
			result += v

	return result


if __name__ == "__main__":
	from random import randint

	size = 30

	f = open("data.bin", "rb")
	all_data = list(f.read())
	f.close()

	for _ in range(ceil(len(all_data)/size)):
		data = ''.join([bin(i)[2:].zfill(8) for i in all_data[_*size:_*size+size]])

		encoded = encode(data)

		id = randint(0,len(encoded)-1)

		encoded = encoded[:id] + str(1 - int(encoded[id])) + encoded[id + 1:]

		decoded = decode(encoded)

		print(data == decoded, len(encoded) / 8)
