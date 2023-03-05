import ReedSolomon
import hemming
from table_generator import *
from GaulNum import GaulNum
from GaulPoly import GaulPoly
from math import ceil

from random import randint


GaulNum.log, GaulNum.pow = init_tables(0b10011) # 2**4

N = n - 1
K = N - 2 * 3 # размер блока(в байтах)

GaulNum.N = N

g = ReedSolomon.G_polynom_generator(N-K+1)


f = open("data.bin", "rb")
data = ''.join([bin(i)[2:].zfill(8) for i in list(f.read())])
f.close()


#data = ''.join([bin(i)[2:].zfill(8) for i in range(32)])


for _ in range(0,len(data),K*bits):
	p = data[_:_+K*bits]
	p += "0" * (K*bits-len(p))

	p = GaulPoly([int(p[i:i+bits],2) for i in range(0,len(p),bits)])

	#print(p)

	mess = ReedSolomon.encode(p, g, N, K)

	mess = ''.join([bin(i.value)[2:].zfill(bits) for i in mess])
	mess = hemming.encode(mess)

	mess += "0" * (ceil(len(mess)/8)*8 - len(mess))

	mess = [int(mess[i:i+8],2) for i in range(0,len(mess),8)]

	# передаём, совершая ошибки

	mess = list(''.join([bin(i)[2:].zfill(8) for i in mess]))

	for i in range(1):
		id = randint(0,len(mess)-1)
		mess[id] = str(1 - int(mess[id]))

	mess = ''.join(mess)

	mess = [int(mess[i:i+8],2) for i in range(0,len(mess),8)]

	# приняли

	mess = ''.join([bin(i)[2:].zfill(8) for i in mess])[:60]

	mess = hemming.decode(mess)


	mess = GaulPoly([int(mess[i:i+bits],2) for i in range(0,len(mess),bits)])

	#print(ReedSolomon.decode(mess, g, N, K))

	#print()
