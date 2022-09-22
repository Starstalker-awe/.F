import sys, os, re, shutil, datetime, math, re

DIR, AVGS = os.getcwd(), []

def getsize(bytes_):
	return f'{round(bytes_ / math.pow(1024, (i := int(math.floor(math.log(bytes_, 1024))))), 2)}{("B","KB","MB","GB","TB","PB","EB","ZB","YB")[i]}' if bytes_ else '0B'

def main():
	if len(sys.argv) < 3:
		print('Usage: python filefilter.py [extract_to] [type1, {type2, {type_n}}]')
		sys.exit(1)
	if not os.path.exists(f'{DIR}/{(fn := sys.argv[1])}'):
		os.mkdir(f'{DIR}/{fn}')
		print(f'Created folder "{fn}"')
	for _d, _, fs in os.walk('.'):
		for f in [x for x in fs if re.match(f'.+\.({"|".join(sys.argv[2:])})', x)]:
			if not os.path.exists(f'{DIR}/{fn}/{f}'):
				begin = datetime.datetime.now()
				print(f'Copying "{f}"', end='\r')
				shutil.copy2(f'{DIR}/{_d}/{f}', f'{DIR}/{fn}/{f}')
				AVGS.append({'time': datetime.datetime.now() - begin, 'size': os.path.getsize(f'{DIR}/{_d}/{f}')})
				print(f"\x1b[2KTook {round(AVGS[-1]['time'].total_seconds(), 2)} seconds to copy {getsize(AVGS[-1]['size'])}")
	print(f'Average rate: {round(sum([x["time"].total_seconds() for x in AVGS]) / (sum([x["size"] for x in AVGS])) / 1048576, 2)}MB/s')

if __name__ == '__main__':
	main()