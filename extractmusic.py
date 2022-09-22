import os, sys, zipfile, shutil, re

DIR, USE, DEL = os.path.join(os.getcwd(), sys.argv[1]).replace('\\', '/'), [], True if len(sys.argv) > 2 and sys.argv[2] == '--delete' else False

def zipname(name):
	name = name.split('/')[-1].split('\\')[-1]
	for index, piece in enumerate(name.split('-')):
		if piece.isnumeric():
			if len(piece) != 4:
				continue
			return ' '.join(name.split('-')[0:index]).title()

def main():
	if not os.path.exists(f"{DIR}/.extracted"):
		os.mkdir(f"{DIR}/.extracted")
		print('Created .extracted folder!')
	print('Extracting zips!')
	for f1 in os.listdir(DIR):
		if f1.endswith('.zip'):
			with zipfile.ZipFile(f"{DIR}/{f1}", 'r') as zipped:
				znamd, znam = zipname(zipped.filename), zipped.filename
				if znamd in USE:
					if DEL or input(f'Delete duplicate "{znam.split("/")[-1]}"? [y/n]: ').lower() == 'y':
						zipped.close()
						os.remove(znam)
						continue
				print(list(filter(lambda x:re.match(r".*\.(mp3|wav)", x), zipped.namelist())))
				options = sorted(filter(lambda x:re.match(r".*\.(mp3|wav)", x), zipped.namelist()), key=lambda x:os.stat(f"{DIR}/{f1}/{x}").st_size)
				print(options)
				mp3s = list(filter(lambda x:x.endswith('.mp3'), options))
				print(mp3s)
				name = mp3s[-1] if mp3s else list(filter(lambda x:x.endswith('.wav'), options))[-1]
				orig = f"{DIR}/.extracted/{name.split('/')[-1]}"
				try:
					shutil.copy2(f"{DIR}/{f1}/{name}", f"{DIR}/.extracted/")
					os.rename(orig, f"{DIR}/.extracted/{znamd}.mp3")
					USE.append(znamd)
				except:
					os.remove(orig)
					print(f'Failed to extract and rename "{name}"')
					continue
	print('All files extracted!')
	print(f'Deleting temporary folders!')
	for piece in os.listdir(DIR):
		if piece != '.extracted':
			pname = f"{DIR}/{piece}"
			if not os.path.isfile(pname):
				shutil.rmtree(pname)
	if DEL:
		print('Deleting zips!')
		for zipf in [y for y in os.listdir(f"{CWD}/{genre}") if os.path.isfile(f"{CWD}/{genre}/{y}")]:
			os.remove(f"{CWD}/{genre}/{zipf}")
	print('Process complete!', end='')
	return True

if __name__ == '__main__':
	main()