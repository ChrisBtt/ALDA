import random
import numpy as np
import matplotlib.pyplot as plt
import unittest

def createData(size):
	a = []
	while len(a) < size:
		x, y = random.uniform(-1,1), random.uniform(-1,1)
		r = np.sqrt(x**2 + y**2)
		if r < 1.0:
			a.append(r)
	return a

def linMap(key, M):
	return int(key*M)

def bucketMap(key, M):
    return int(key**2 * M)

# das Quadrieren der Radien fuehrt zu einer groeßeren Streuung der großen Werte und laesst kleine Werte nahezu gleich.
# Formal gibt es durch die zwei Zufallszahlen im Pythagoras eine Verzerrung der Radien, die durch das Quadrieren rückgängig gemacht wird.

def insertionSort(a):   # sort 'a' in-place
    N = len(a)          # number of elements
    
    for i in range(N):
        current = a[i]  # remember the current element
        # find the position of the gap where 'current' is supposed to go
        j = i       # initial guess: 'current' is already at the correct position
        while j > 0:
            if current < a[j-1]:  # a[j-1] should be on the right of 'current'
                a[j] = a[j-1]     # move a[j-1] to the right
            else:
                break             # gap is at correct position
            j -= 1                # shift gap one index to the left
        a[j] = current            # place 'current' into appropriate gap

    return a

def bucketSort(a, bucketMap, d):
    size = len(a)
    drive = int(size / float(d))  # Anzahl der Buckets festlegen
    print("M:", drive)

    # M leere Buckets erzeugen
    buckets = [[] for k in range(drive)]

    # Daten auf die Buckets verteilen
    for k in range(len(a)):
        index = bucketMap(a[k], drive) # Bucket-Index berechnen
        buckets[index].append(a[k])    # a[k] im passenden Bucket einfügen

    # Daten sortiert wieder in a einfügen
    start = 0                           # Zielindex des aktuellen buckets 
    for k in range(drive):
        end = start + len(buckets[k])  # Bis zu welchem Index wir kopieren wollen
        buckets[k] = insertionSort(buckets[k])      # Daten innerhalb des Buckets sortieren
        a[start:end] = buckets[k]      # Daten an der richtigen Position in a einfügen
        start += len(buckets[k])          # Anfang für den nächsten Bucket

    return a

def deviation(data):
	sampling = []

	size = len(data)
	k,i = 0,0
	for radius in data:
		sampling.append(bucketMap(radius, 100))

	plt.hist(sampling, bins = 100)
	plt.savefig("deviation.pdf")

def chiQuadrat(a, bucketMap, d):

	drive = int(len(a) / float(d))  # Anzahl der Buckets festlegen
	print("M:", drive)

	# M leere Buckets erzeugen
	buckets = [[] for k in range(drive)]

	# Daten auf die Buckets verteilen
	for k in range(len(a)):
	    index = bucketMap(a[k], drive) # Bucket-Index berechnen
	    buckets[index].append(a[k])    # a[k] im passenden Bucket einfügen

	c = len(a)/drive
	chi_square = 0

	for bucket in buckets:
		chi_square += (len(bucket)-c)**2/c

	tau = np.sqrt(2*chi_square)-np.sqrt(2*drive-3)

	if np.abs(tau)<=3:
		return True

	return False

d = 2

data = createData(100000)
sortedData = bucketSort(data, bucketMap, d)
deviation(data)

#######################################################################################
class testBucketSort(unittest.TestCase):

	def setUp(self):
		data = createData(100000)
		self.arrays = [data]
		for i in range(10):
			self.arrays.append(createData(100000))

	def testBucketSort(self):
		for a in self.arrays:
			self.checkBucketSort(a)

	def testDeviation(self):
		for a in self.arrays:
			self.assertTrue(chiQuadrat(a, bucketMap, d))
			self.assertFalse(chiQuadrat(a, linMap, d))

	def checkBucketSort(self, original):
		self.assertEqual(bucketSort(original, bucketMap, 2), sorted(original))
		self.assertEqual(bucketSort(original, bucketMap, 5), sorted(original))
		self.assertEqual(bucketSort(original, bucketMap, 10), sorted(original))
		self.assertEqual(bucketSort(original, bucketMap, 50), sorted(original))

if __name__ == '__main__':
	unittest.main()

