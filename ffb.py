import os, sys, zipfile, shutil, re, time, math

def getvals():
	if len(sys.argv) < 8:
		if len(sys.argv) == 2 and sys.argv[1] == '--defaults':
			return ['.extracted', '*', 1, True, '.*', False, 0, '.*']
		print('Defaults: ".extracted", "*", "copy", "yes", ".*" (all names), "no", "0", ".*" (all types)')
		return (
			input('Name the extract folder: ') or '.extracted',
			input('Do you want the smallest (<), largest (>), or all files (*)? ') or '*',
			int((input('Do you want to copy or move files? ') or 'c').lower()[0] == 'c'),
			i.lower()[0] == 'y' if (i := input('Do you want to extract from zips? [Y/n] ')) else True,
			input('(Advanced) Regex string to match filename: ') or '.*',
			i.lower()[0] == 'y' if (i := input('Do you want to retain depth? [y/N] ')) else False,
			int(input('Minimum depth of files: ') or 0),
			input('What file types do you want? (no . plz) ').split(' ') or '.*',
		)
	return (sys.argv[1], sys.argv[2], bool(sys.argv[3]), bool(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8:])

[FOLDER, GET, METHOD, ZIPS, STRING, DEPTH, MDEPTH, TYPES, AVG] = [*getvals(), []]; MATCH = f'({STRING})\.({TYPES if len(TYPES) == 1 else "|".join(TYPES)})'


def getsize(bytes_):
	return f'{round(bytes_ / math.pow(1024, (i := int(math.floor(math.log(bytes_, 1024))))), 2)}{("B","KB","MB","GB","TB","PB","EB","ZB","YB")[i]}' if bytes_ else '0B'

def deeep(fn):
	if not DEPTH:
		return None
	d = '/'.join(fn.split('/')[:-1])
	if not os.path.exists(f'./{FOLDER}/{d}'):
		os.mkdir(f'./{FOLDER}/{d}')
	return d

def transfer(_d, f, d2=None, zn=None, sz=None):
	from_ = f'./{_d}/{f"{zn}/{f}" if zn else f}', to_ = f'{f"./{FOLDER}/{d2}" if d2 else f"./{FOLDER}"}/{f"{zn}/{f}" if zn else f}'
	print(f'{"Copying" if METHOD else "Moving"} "{f}" from "{from_}" to "{to_}"', end='\r')
	b1, b2 = time.time(), time.process_time()
	shutil.copy2(from_, to_) if METHOD else shutil.move(from_, to_)
	AVG.append({'w': time.time() - b1, 'c': time.process_time() - b2, 's': sz})
	print(f'\x1b[2K{"Copied" if METHOD else "Moved"} {getsize(sz)} in {round(AVG[-1]["w"], 3)}s real-time & {round(AVG[-1]["c"], 3)}s CPU-time')
	return True

def handle(_d, f):
	if ZIPS and f.endswith('.zip'):
		with zipfile.ZipFile(f'./{_d}/{f}') as zipped:
			cmprsd = [{'fn': f, 'sz': s} for f, s in [(x.filename, x.file_size) for x in zipped.infolist() if not x.is_dir()]]
			if GET == '<':
				transfer(_d, (st := [v for v in sorted(cmprsd, key='sz') if re.match(MATCH, v)][0])['fn'], deeep(st['fn']), zipped.name, st['sz'])
				if ZIPS and st.endswith('.zip'):
					handle(f'{_d}/{zipped.name}', st)
			elif GET == '>':
				transfer(_d, (st := [v for v in sorted(cmprsd, key='sz', reverse=True) if re.match(MATCH, v)][0])['fn'], deeep(st['fn']), zipped.name, st['sz'])
				if ZIPS and st.endswith('.zip'):
					handle(f'{_d}/{zipped.name}', st)
			elif GET == '*':
				for v in cmprsd:
					transfer(_d, v['fn'], deeep(v['fn']), zipped.name, v['sz'])
					if ZIPS and st.endswith('.zip'):
						handle(f'{_d}/{zipped.name}', st)
	else:
		transfer(_d, f)

def main():
	if not os.path.exists(f'./{FOLDER}'):
		os.mkdir(f := f'./{FOLDER}')
		print(f'Created folder "{f}"')
	for _d, _, fs in os.walk('.'):
		for f in fs:
			if (re.match(MATCH, x) and len(_d.split('/')) > MDEPTH) or (ZIPS and x.endswith('.zip')):
				handle(_d, f)
	print(f'Average rate: {round(sum([x["w"] for x in AVG]) / (sum([x["s"] for x in AVG]) / 1048576), 2)}MB/s real-time & {round(sum([x["c"] for x in AVG]) / (sum([x["s"] for x in AVG]) / 1048576), 2)}MB/s CPU-time') if METHOD else print('Done!')

if __name__ == '__main__':
	main()