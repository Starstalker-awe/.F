import os, sys

CWD = os.getcwd()

def cleanall():
	for genre in [x for x in os.listdir() if not os.path.isfile(x)]:
		for zipf in [y for y in os.listdir(f"{CWD}/{genre}") if os.path.isfile(f"{CWD}/{genre}/{y}")]:
			os.remove(f"{CWD}/{genre}/{zipf}")

def cleansingle(genre):
	for zipf in [y for y in os.listdir(f"{CWD}/{genre}") if os.path.isfile(f"{CWD}/{genre}/{y}")]:
		os.remove(f"{CWD}/{genre}/{zipf}")


def main():
	if sys.argv[1] == 'single':
		print(f'Deleting all zips in ./{sys.argv[2]}!')
		cleansingle(sys.argv[2])
	elif sys.argv[1] == 'all':
		print('Deleting all zips!')
		cleanall()

if __name__ == '__main__':
	main()