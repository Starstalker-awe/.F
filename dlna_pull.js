(_=>{let files=[...document.querySelectorAll('a')].slice(1, 51);files.forEach(f=>(f.setAttribute('download',''),f.click()))})()

(_=>{
	const files = [...document.querySelectorAll('a')].slice(1);
	for (let i = 0; i < Math.ceil(files.length / 10); i++){
		files.slice(i * 10, (i + 1) * 10).forEach(e=>(e.setAttribute('download', ''), e.click()));
	}
})()

(_=>{const f=[...document.querySelectorAll('a')].slice(1);for(let i=0;i<Math.ceil(f.length/10);i++){f.slice(i*10,(i+1)*10).forEach(e=>(e.setAttribute('download',''),e.click()))}})()


(_=>{
	const files = [...document.querySelectorAll('a')].slice(1);
	for (let i = 0; i < Math.ceil(files.length / 10); i++){
		setTimeout((_=>{
			files.slice(i, i + 1).forEach(e=>(e.setAttribute('download', ''), e.click()));
		})(), 1000)
	}
})()

(_=>[...document.querySelectorAll('a').slice(1).forEach(e=>window.open(e.href,'_blank'))])()

for (let e of [...document.querySelectorAll('a')].slice(1, 21)){
	setTimeout((_=>{
		let elem = document.createElement('a');
		elem.setAttribute('href', e.href);
		elem.setAttribute('download', '');
		elem.click();
	})(), 2000)
}

(_=>{
	const links = [...document.querySelectorAll('a')].slice(1);
	for (let [i, e] of links.entries()){
		setTimeout((_=>{
			fetch(e.href).then(e=>e.blob()).then(blob=>{
				const bloburl = URL.createObjectURL(blob);
				Object.assign(document.createElement('a'), {href: bloburl, download: links[i].firstChild.innerHTML.split('/').at(-1)}).click();
			})
		})(), 3000)
	}
})()

(_=>{let l=[...document.querySelectorAll('a')].slice(1);for(let[i,e]of l.entries()){fetch(e.href).then(e=>e.blob()).then(b=>Object.assign(document.createElement('a'),{href:URL.createObjectURL(b),download:l[i].firstChild.innerHTML.split('/').at(-1)}).click())}})()

// Not one-liner, the goal of which is to be able to stop and start again, without duplicating files
Promise.resolve(new Promise(resolve=>((s=`a${(Math.random() + 1).toString(36).substring(7)}`)=>{
	const links = [...document.querySelectorAll('a')].slice(1);
	document.body.appendChild(Object.assign(document.createElement('input'), {id: s, type: 'file', multiple: true})).addEventListener('change', _=>run(true));
	document.body.appendChild(Object.assign(document.createElement('button'), {innerHTML: 'Download All'})).addEventListener('click', _=>run(false));
	function run(blacklist){
		const loaded = [...document.querySelector(`#${s}`).files].map(e=>e.name);
		const filtered = blacklist ? links.filter(e=>!loaded.includes(e.firstChild.innerHTML.split('/').at(-1))) : links;
		console.log(`Preparing to download ${filtered.length} items`);
		function download(index, name=null){
			if(index > filtered.length){resolve()}
			try{
				console.log(`Downloading ${name = filtered[index].firstChild.innerHTML.split('/').at(-1)}`)
				Promise.resolve(new Promise(async res=>{
					await fetch(filtered[index].href).then(e=>e.blob()).then(blob=>Object.assign(document.createElement('a'), {
						href: URL.createObjectURL(blob),
						download: name
					}).click());
					res();
				})).then(_=>download(++index));
			}catch(error){}
		}
		download(0);
	}
})())).then(_=>console.log('Done!'));

// Much improved version, not using indexes, but instead slicing "filtered"
((s=`a${(Math.random() + 1).toString(36).substring(7)}`)=>{
	const links = [...document.querySelectorAll('a')].slice(1);
	document.body.appendChild(Object.assign(document.createElement('input'), {id: s, type: 'file', multiple: true})).addEventListener('change', _=>run(true));
	document.body.appendChild(Object.assign(document.createElement('button'), {innerHTML: 'Download All'})).addEventListener('click', _=>run(false));
	async function run(blacklist, name = null){
		const loaded = [...document.querySelector(`#${s}`).files].map(e=>e.name);
		let filtered = blacklist ? links.filter(e=>!loaded.includes(e.firstChild.innerHTML.split('/').at(-1))) : links;
		const logger = setInterval(_=>console.log(`${filtered.length} items remaining!`), 30 * 1e3);
		console.log(`Preparing to download ${filtered.length} items!`);
		do{
			console.log(`Downloading ${name = filtered[0].firstChild.innerHTML.split('/').at(-1)}`);
			await fetch(filtered[0].href).then(e=>(filtered = filtered.slice(1), e.blob())).then(blob=>Object.assign(document.createElement('a'), {
				href: URL.createObjectURL(blob),
				download: name
			}).click());
		}while(filtered.length);
		clearInterval(logger);
		console.log(`All files have been downloaded!`);
	}
})();

((s='a'+~~(Math.random()*10))=>{let l=[...document.querySelectorAll('a')].slice(1);[['input',{id:s,type:'file',multiple:true},'change',true],['button',{innerHTML:'Download All'},'click',false]].forEach(e=>document.body.appendChild(Object.assign(document.createElement(e[0]),e[1])).addEventListener(e[2],_=>(b=>{let f=b?l.filter(e=>![...document.querySelector('#'+s).files].map(x=>x.name).includes(e.firstChild.innerHTML.split('/').at(-1))):l;(d=i=>i<f.length?(_=>{try{Promise.resolve(fetch(f[i].href).then(e=>e.blob()).then(b=>Object.assign(document.createElement('a'),{href:URL.createObjectURL(b),download:f[i].firstChild.innerHTML.split('/').at(-1)}).click())).then(_=>d(++i))}catch(_){}})():null)(0)})(e[3])))})()