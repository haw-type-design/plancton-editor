let content = document.getElementById('content')
let projectName = content.getAttribute('data-project')
let typewriter = document.querySelector('.typewriter')
let svgContainer = document.getElementById('svgContainer')
let setchart = document.getElementById('setchart')
let editors = document.getElementsByClassName('editor')
let editor_mp = document.getElementById('editor_mp')
let run = document.getElementById('run')
let inputWrite= document.getElementById('inputWrite')
let inputsRange = document.getElementsByClassName('input_range')
let globalNav = document.getElementById('global_nav')
let infoNav = document.getElementById('info_nav')
let btn_inkscape = document.getElementById('inkscape')
let btn_refresh = document.getElementById('refresh')
let btn_all = document.getElementById('btn_all')
let btn_tab = document.getElementsByClassName('tab')
let imgs = document.getElementsByClassName('imgChar')	
let aceEditor = []
let toggleNav = document.getElementsByClassName('toggleNav')	
let inputZoom = document.querySelector('.zoom input')	
let log = document.querySelector('.log')	


if (content.className !== 'set ') {
	var sentence = inputWrite.value
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function pingServer(url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url, true);
	svgContainer.className = "loading"
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status == "200") {
			callback(xhr.responseText);
			svgContainer.classList.remove("loading")
		}
	}
	xhr.send(null);
}

function readJson(file, callback) {
	var rawFile = new XMLHttpRequest();
	rawFile.overrideMimeType("application/json");
	rawFile.open("GET", file, true);
	rawFile.onreadystatechange = function() {
		if (rawFile.readyState === 4 && rawFile.status == "200") {
			callback(rawFile.responseText)
		}
	}
	rawFile.send(null);
}

function writeJson(data){

	if (data == false) {
		var sentence = '-all'
	}else {
		var sentence = inputWrite.value
		svgContainer.innerHTML = ''
		svgContainer.className = "loading"
	}

	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			if (data == false) {
				for(img in imgs) {
					var re = imgs[img].src
					imgs[img].src = re + '2'
				}
			} else {	
				var sentence = inputWrite.value
				writeValue(sentence)	
				writeJson(false)
			}
			svgContainer.classList.remove("loading")
		}
	}

	xmlhttp.open('POST', '/write-json' , true);
	console.log(JSON.stringify(data,  null, 4))
	xmlhttp.send('project=' + projectName + '&json=' + JSON.stringify(data,  null, 4) + '&set=' + sentence);
}

function loadSvg(key) {
	var l = String.fromCharCode(key);
	xhr = new XMLHttpRequest()
	xhr.overrideMimeType("image/svg+xml")
	xhr.open("GET", "/projects/" + projectName + "/output-svg/" + key + ".svg?random=" + getRandomInt(3000), false)
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status == "200") {
		p = '<span data-key="' + key + '" id="i_' + key + '" class="cadratin" ><a class="link_cadratin" href="/type/' + projectName + '/' + key + '#editor_mp" >' + xhr.responseXML.documentElement.outerHTML + '<span class="ref">'+l+' | '+key+'.mp</span></a></span>'
		}else {
			p = ''

		}
	}
	xhr.send("")	
	
	svgContainer.innerHTML += p	
}

function inputBuild(variablesTable, i) {
	var table = variablesTable[i]

	var p = []
	for (u in table){
		if(table[u].type) {
			var input = document.createElement("input")
			input.type = table[u].type;
			input.className = "input_" + table[u].type 
			input.id = "input_" + u
			input.setAttribute('title', table[u].description)
			input.setAttribute('data-var', u)
			if (table[u].type == 'range') {
				input.setAttribute('min', table[u].range[0])
				input.setAttribute('max', table[u].range[1])
				input.setAttribute('step', table[u].range[2])
				input.setAttribute('value', table[u].value)
			}
			p += '<li class="block_input" ><label><div title="'+table[u].description+'"class="description">'+table[u].description+'</div><span id="span_'+u+'" class="valueBox">| '+table[u].value+'</span></label>'+input.outerHTML+'</li>'
		}
	}
	globalNav.innerHTML += '<ul class="items" id="' + i + '" ><li><h1>' + i + '</h1></li>' + p + '</ul>'

}

function buildNav(data) {
	var glob = data.variables

	for (i in glob){
		inputBuild(glob, i)
	}

	var info = data.font_info
	var p = []
	for (i in info){
		p += '<label>' + i + '| <span class="valueBox" >' + info[i] + '</span></label>'
	}
	infoNav.innerHTML += p
}


function changeValue(data){
	for (var i = 0, len = inputsRange.length; i < len; i++) {
		inputsRange[i].addEventListener('change', function() {
			var val = this.value
			var vari = this.getAttribute('data-var')
			var cat = this.closest('.items').id
			sp = document.getElementById('span_' + vari)
			sp.innerHTML = '| ' + val
			data.variables[cat][vari].value = val
			writeJson(data, false)
		});
	}
}


function writeValue(stn) {
	svgContainer.innerHTML = ""
	var out = []
	
	if(stn.charAt(0) == ':') {
		switch(true) {
			case /:add _[0-9]+_/.test(stn): // test de :add _65_
				var k = stn.match(/[0-9]+/)
				var l = String.fromCharCode(k)
				log.innerHTML = `<span style="color: green">
				Do you want add the glyph ` + l + ` ? </span>
				<input type="button" value="Yes"/>
				<input type="button" value="No"/>
				`
				break
			case /:del(ete)? _[0-9]+_/.test(stn): // test de :del _65_
				var k = stn.match(/[0-9]+/)
				var l = String.fromCharCode(k)
				log.innerHTML = `<span style="color: green">
				Do you want delete the glyph ` + l + ` ? </span>
				<input type="button" value="Yes"/>
				<input type="button" value="No"/>
				`
				break
			case /:generate font/.test(stn): // test de :add _65_
				alert('on genère la font' + stn.match(/[0-9]+/))
				break
			case /:set/.test(stn): // test de :add _65_
				pingServer('/set/meta-old-french', function(cb){
					out = cb.split('|')
					out.forEach(function(entry) {
						loadSvg(entry)
					});
				})	
				if(!typewriter.classList.contains('set')){
					typewriter.classList.add('set')
				}
			default:
				log.innerHTML = ''

			// case (stn == ':help'):
			// 	alert('on voit apparaitre l\'aide de commandes')
			// 	break
			// case (stn == ':set'):
			// 	alert('on voit apparaitre tout le glyphs set')
			// 	break
			// case (stn == ':add'):	
			// 	console.log(stn.split(' '))
			// 	// if(stn.split(' ').length == 2) {
			// 	// 	alert('on ajoute un glyph')
			// 	// }
			// 	break
			// case ':delete':
			// 	alert('on suprime un glyph')
			// 	break
		}
	}else{
		out= stn.split('')
		out.forEach(function(entry) {
			code = entry.charCodeAt(0)
			loadSvg(code)
		});
		if(typewriter.classList.contains('set')){
			typewriter.classList.remove('set')
		}
	}
}

function activeInks() {
		btn_inkscape.addEventListener('click', function(){
			var key = this.closest('.tools_bar').getAttribute('data-key')
			var xmlhttp = new XMLHttpRequest()
			xmlhttp.onreadystatechange = function()
			{
				if (xmlhttp.readyState == 4)
				{
					console.log('yes')
				}
			}
			xmlhttp.open('POST', '/inkscape', true)
			xmlhttp.send('project=' + projectName + '&key=' + key)
			this.parentElement.classList.add('activeInks')
		}, false)
}

function refreshInks(editor) {
		btn_refresh.addEventListener('click', function(){

			var key = this.closest('.tools_bar').getAttribute('data-key')
			var xmlhttp = new XMLHttpRequest()
			xmlhttp.onreadystatechange = function()
			{
				if (xmlhttp.readyState == 4)
				{
					sentence = inputWrite.value
					writeValue(sentence)
					loadMp(editor)
				}
			}
			xmlhttp.open('POST', '/updateMp', true)
			xmlhttp.send('project=' + projectName + '&key=' + key)
		}, false)
}

function loadMp(editor, edi) {
	var key = edi.getAttribute('data-key')
	xhr = new XMLHttpRequest()
	xhr.open("GET", "/projects/" + projectName + "/mpost/" + key + ".mp?random=" + getRandomInt(3000), false)
	xhr.send("")
	editor.setValue(xhr.responseText)
}

function write(type, editor, key) {
	console.log(editor)
	var contentMp = editor.getValue()
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			sentence = inputWrite.value
			writeValue(sentence)

		}
	}
	xmlhttp.open('POST', '/' + type, true);
	contentMp = contentMp.replace(/;/g, '#59');
	contentMp = contentMp.replace(/\+/g, '#45');
	xmlhttp.send('project=' + projectName + '&mp=' + contentMp + '&key=' + key);
}

/* INTERFACE */

function toogle(elem, classN) {
	let elems = document.querySelectorAll(elem)

	for (var i = 0, len = elems.length; i < len; i++) {
		elems[i].addEventListener('click', function(){
			var e = document.querySelector(elem + '.' + classN[0])
			e.classList.remove(classN[0])
			e.classList.add(classN[1])
			this.classList.add(classN[0])
		})
	}
} 



