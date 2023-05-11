const fs = require('fs');
const express = require('express')
const app = express()

let results = {}

app.get('/',(req, res) => {
	let folders = Object.keys(results)
	let tmp = folders.map(folder =>{
		re =  results[folder]
		return `<li>scrapy crawl flexnews -a domain=${re.folder} -a url=${re.url} :${re.wc}</li>`
	})
	res.send('<ul>'+tmp.join("")+'</ul>')
})

app.get('/feedback', (req,res) => {
	results[req.query.folder] = req.query	
	res.send(req.query)
})

app.get('/reset',(req, res) => {
	results = {}
	res.send('OK')
})

app.get('/export',(req, res) => {
	let stream = fs.createWriteStream('tested.txt')
	stream.once('open', function(rd){
		let folders = Object.keys(results)
        	let tmp = folders.map(folder =>
		{
                	re =  results[folder]
			let name = re.folder.replace('.','_')

			let cmd = `screen -dmS crawl_${name} bash -c`
                	let data=`scrapy crawl flexnews`;
			data += ` -a domain=${re.folder} -a url=${re.url}`;
			stream.write(`${cmd} '${data}'\n`)
        	});
		stream.end();
	})
	let data_s = fs.createWriteStream('data.json')
	data_s.once('open', function(rd){
		let data_str = JSON.stringify(results)
		data_s.write(data_str);
		data_s.end();
	})
	res.redirect('/')
})

app.listen(8080, () => console.log('listen on localhost:8080'))
