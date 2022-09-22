import sys,os,re,shutil,datetime,math,re;AS=[]
def main():
	if len(sys.argv)<3:print('Usage: ./filefilter.py [extract_to] [type, {type2, {type_n}}]');sys.exit(1)
	if not os.path.exists(fn:=sys.argv[1]):os.mkdir(fn);print(f'Created folder "{fn}"')
	for _d,_,fs in os.walk('.'):
		for f in [x for x in fs if re.match(f'.+\.({"|".join(sys.argv[2:])})',x)]:
			if not os.path.exists(fn+f):b=datetime.datetime.now();print(f'Copying {f}',end='\r');shutil.copy2(_d+f,fn+f);AVGS.append({'t':datetime.datetime.now()-b,'s':os.path.getsize(_d+f)});print('\x1b[2KTook '+round(AS[-1]['t'].total_seconds(),2)+' secs to copy '+(lambda b:f'{round(b/math.pow(1024,(i:=int(math.floor(math.log(b,1024))))),2)}{("B","KB","MB","GB","TB","PB","EB","ZB","YB")[i]}'if b else'0B')(AS[-1]['s']))
	print(f"Average: {round(sum([x['t'].total_seconds()for x in AS])/sum([x['s']for x in AS])/1048576,2)}MB/s")
if __name__=='__main__':main()