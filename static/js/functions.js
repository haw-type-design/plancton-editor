let content = document.getElementById('content')
let projectName = content.getAttribute('data-project')
let typewriter = document.querySelector('.typewriter')
let svgContainer = document.getElementById('svgContainer')
let setchart = document.getElementById('setchart')
let editors = document.getElementsByClassName('editor')
let editor_mp = document.getElementById('editor_mp')
let run = document.getElementById('run')
let inputWrite = document.getElementById('inputWrite')
let inputsRange = document.getElementsByClassName('input_range')
let globalNav = document.getElementById('global_nav')
let infoNav = document.getElementById('info_nav')
let btn_inkscape = document.getElementById('inkscape')
let btn_refresh = document.getElementById('refresh')
let btn_all = document.getElementById('btn_all')
let btn_tab = document.getElementsByClassName('tab')
let imgs = document.getElementsByClassName('imgChar')	
var aceEditor = []
let toggleNav = document.getElementsByClassName('toggleNav')	
let inputZoom = document.querySelector('.zoom input')	
var log_elem = document.getElementById('log')	

if (content.className !== 'set ') {
	var sentence = inputWrite.value
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function get_session(key){
	console.log('set session')
	var xhr = new XMLHttpRequest()
	xhr.open("GET", '/session_get/'+key, false)
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status == "200") {
			console.log(xhr.responseText)
		}
	}
	xhr.send()
	return xhr.responseText
}

function set_session(key, value){
	console.log('get session')
	var xhr = new XMLHttpRequest()
	xhr.open("GET", '/session_set/'+key+'/'+value, false)
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status == "200") {
			console.log(xhr.responseText)
		}
	}
	xhr.send()
}

function pingServer(url, callback) {
	var xhr = new XMLHttpRequest()
	xhr.open("GET", url, false)
	svgContainer.className = "loading"
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4 && xhr.status == "200") {
			callback(xhr.responseText)
			svgContainer.classList.remove("loading")
		}
	}
	xhr.send()
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
				write_sentence(sentence)	
				writeJson(false)
			}
			svgContainer.classList.remove("loading")
		}
	}

	xmlhttp.open('POST', '/write_json' , true);
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

function write_sentence(stn) {
	svgContainer.innerHTML = ""
	var out = []
	
	if(stn.charAt(0) == ':') {
		commands(stn)
	}else{
		out= stn.split('')
		out.forEach(function(entry) {
			code = entry.charCodeAt(0)
			loadSvg(code)
		});
		if(typewriter.classList.contains('set')){
			typewriter.classList.remove('set')
		}
		set_session('sentence', stn)
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
					write_sentence(sentence)
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
	var contentMp = editor.getValue()
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			sentence = inputWrite.value
			write_sentence(sentence)
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



