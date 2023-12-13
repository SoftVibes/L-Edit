import pickle

with open("data.dat", "rb") as f:
	try:
		while True:
			print(pickle.load(f))
	except EOFError:
		pass
