def fib1(n):                      # Funktion berechnet die n-te Fibonacci-Zahl
    if n <= 1: 
        return n                 # Rekursionsabschluss
    return fib1(n-1) + fib1(n-2)  # Baumrekursion

def fib3(n):
    f1, f2 = fib3Impl(n)    # Hilfsfunktion, f1 ist die Fibonacci-Zahl von (n+1) und f2 ist die Fibonacci-Zahl von n
    return f2

def fib3Impl(n):
    if n == 0: 
        return 1, 0         # gebe die Fibonacci-Zahl von 1 und die davor zurück
    else:                          # rekursiver Aufruf
       f1, f2 = fib3Impl(n-1)      # f1 ist Fibonacci-Zahl von n, f2 die von (n-1)
       return f1 + f2, f1          # gebe neue Fibonacci-Zahl fn+1 = f1+f2 und die vorherige (fn = f1) zurück.

def fib5(n):
    f1, f2 = 1, 0                # f1 ist die Fibonaccizahl für n=1, f2 die für n=0
    while n > 0:
        f1, f2 = f1 + f2, f1     # berechne die nächste Fibonaccizahl in f1 und speichere die letzte in f2
        n -= 1
    return f2

def fib6(n):
	if n==0:
		return 0
	elif n==1:
		return 1
	else:
		fibonacci = [1, 1, 1, 0] # initialisiere mit der Einheitsmatrix für n==0
		matrix = mul2x2(fibonacci, fibonacci)
		n=n-1
		while n>0:
			matrix = mul2x2(matrix, fibonacci) # berechne die n-te Potenz der Matrix
			n-=1
		return matrix[1]

def mul2x2(matrix, matrix2): 
	new11 = matrix[0]*matrix2[0] + matrix[1]*matrix2[2]
	new12 = matrix[0]*matrix2[1] + matrix[1]*matrix2[3]
	new21 = matrix[2]*matrix2[0] + matrix[3]*matrix2[2]
	new22 = matrix[2]*matrix2[1] * matrix[3]*matrix2[3]
	matrix[3] = new22
	matrix[1] = new12
	matrix[0] = new11
	matrix[2] = new21
	return matrix

def fib7(n):
	if n==0:
		return 0
	elif n==1:
		return 1
	elif n%2==0:
		quadrat = [2,1,1,1]
		matrix = [2,1,1,1]
		n = n/2
		while n > 0:
			matrix = mul2x2(matrix, quadrat)
			print(matrix)
			n-=1
		return matrix[2]
	else:
		quadrat = mul2x2([1,1,1,0],[1,1,1,0])
		matrix = quadrat
		n = (n-1)/2
		while n > 0:
			matrix = mul2x2(matrix, quadrat)
			n-=1
		matrix = mul2x2([1,1,1,0], matrix)
		return matrix[1]

import timeit
import unittest

# print(timeit.timeit('fib1(7)', globals=globals()))
# print(timeit.timeit('fib1(8)', globals=globals()))

# print(timeit.timeit('fib3(32)', globals=globals()))
# print(timeit.timeit('fib3(33)', globals=globals()))

# print(timeit.timeit('fib5(81)', globals=globals()))
# print(timeit.timeit('fib5(82)', globals=globals()))

# print(timeit.timeit('fib6(17)', globals=globals()))
# print(timeit.timeit('fib6(18)', globals=globals()))

print(fib7(10))
print(fib6(10))
print(fib5(10))
# print(timeit.timeit('fib7(32)', globals=globals()))
# print(timeit.timeit('fib7(33)', globals=globals()))


class testFibonacci(unittest.TestCase):
	def testDefinitions(self):
		self.assertTrue(fib7(10)==fib5(10))

#if __name__ == '__main__':
	unittest.main()
# a) Die Unterschiede der Algorithmen liegen zum Einen in der mehrfachen Berechnung der gleichen Zahlen innerhalb einer Folge (fib1). Die Algorithmen 3 und 5 haben dieses Mehraufwand nicht mehr. Funktion 5 laeuft nicht rekursiv, sondern iterativ und das ist für den Python Compiler besser zu handhaben, da hier nicht n Funktionen aufgerufen werden muessen, sondern nur eine while Schleife. Das kostet deutlich weniger Speicher und Hashing Zeit.



