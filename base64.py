import sys
from array import array

Base64Index = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def encode(byteArray):
	output = ""
	i=0
	while(i < len(byteArray)):
		b = (int(byteArray[i]) & 0xFC) >> 2
		output += Base64Index[b]
		b = (int(byteArray[i]) & 0x03) << 4
		if i+1 < len(byteArray):
			b |= (int(byteArray[i+1]) & 0xF0) >> 4
			output += (Base64Index[b])
			b = (int(byteArray[i+1]) & 0x0F) << 2
			if i+2 < len(byteArray):
				b |= (int(byteArray[i+2]) & 0xC0) >> 6
				output += (Base64Index[b])
				b = int(byteArray[i+2]) & 0x3F
				output += (Base64Index[b])
			else:
				output += (Base64Index[b])
				output += ("=")
		else:
			output += (Base64Index[b])
			output += ("==")

		i += 3

	return output

def decode(string):
	outputByteArray = []
	b = ['','','','']
	if len(string) % 4 == 0:
		i = 0
		while( i<len(string) ):
			for j in range(0,4):
				b[j] = Base64Index.index(string[i+j]) 
			outputByteArray.append( ((b[0] << 2) | (b[1] >> 4)) & 0xff )
			if b[2] < 64:
				outputByteArray.append( ((b[1] << 4) | (b[2] >> 2)) & 0xff )
				if b[3] < 64:
					outputByteArray.append( ((b[2] << 6) | b[3]) & 0xff )
			i += 4
	else:
		return "Error" 
	
	output = ""
	for t in outputByteArray:
		output += chr(t)

	return output

f = open(sys.argv[1], 'r')
w = open("output.txt", 'w')

N = int(f.readline())
for i in range(0, N):
	inputString = f.readline().rstrip('\n')
	inputString = inputString.split(' ')
	if len(inputString) <= 1:
		print("Input arg err")
		sys.exit(1)

	funcType = inputString[0]
	targetString = ""
	for t in range(1, len(inputString)):
		targetString += " " + inputString[t]
	targetString = targetString[1:]

	if funcType == "e":
		byteArray = array("B", targetString)
		output = encode(byteArray)
		w.write(output + "\n")
	elif funcType == "d":
		output = decode(targetString)
		w.write(output + "\n")
	else:
		print("Input Error")

f.close()
w.close()
