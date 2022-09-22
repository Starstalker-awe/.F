import os, exif, re, struct, datetime as dt

CWD = os.getcwd()

def timecreated(d, f):
	path = f'{d}/{f}'
	if (type_ := f.split('.')[-1].lower()) == 'jpg':
		return ''.join(exif.Image(path).get('datetime_original').split(':'))[0:8]
	elif type_ == 'mov':
		with open(path, 'rb') as fil:
			while not (ah := fil.read(8))[4:8] == b'moov':
				fil.seek(struct.unpack('>I', ah[0:4])[0] - 8, 1)
			if (ah := fil.read(8))[4:8] == b'mvhd':
				fil.seek(4, 1)
				return dt.datetime.fromtimestamp(struct.unpack('>I', fil.read(4))[0] - 2082844800).strftime('%Y%m%d')
	elif type_ == 'mp4':
		c, m = os.path.getctime(path), os.path.getmtime(path)
		return dt.datetime.fromtimestamp(c if m > c else m)

def main():
	for _d, _, fs in os.walk('.'):
		print(f"{os.getcwd()}\\{_d[2:]}")
		for f in fs:
			if not str(list(f)[0]) in list('0123456789') and re.match(r"(mov|jpg|mp4)", f.split('.')[-1].lower()):
				if (t := timecreated(_d, f)):
					os.rename(f"{CWD}/{_d[2:]}/{f}".replace('\\', '/'), f"{CWD}/{_d[2:]}/{t}__{f.split('.')[0]}.{f.split('.')[-1]}".replace('\\', '/'))
					print(f"{f} --> {t}__{f.split('.')[0]}.{f.split('.')[-1]}")
				else:
					print(f'Failed {f}')
					continue

if __name__ == '__main__':
	main()
	print('Done!', end='')