let content = document.getElementById('content')
let typewriter = document.getElementById('svgContainer')
let setchart = document.getElementById('setchart')
let editor_mp = document.getElementById('editor_mp')
let run = document.getElementById('run')
let inputWrite= document.getElementById('inputWrite')
let inputsRange = document.getElementsByClassName('input_range')
let globalNav = document.getElementById('global_nav')
let btn_inkscape = document.getElementById('inkscape'); 
let btn_refresh = document.getElementById('refresh'); 
let btn_all = document.getElementById('btn_all'); 
let imgs = document.getElementsByClassName('imgChar')	


if (content.className !== 'set') {
	var sentence = inputWrite.value
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function readJson(file, callback) {
	var rawFile = new XMLHttpRequest();
	rawFile.overrideMimeType("application/json");
	rawFile.open("GET", file, true);
	rawFile.onreadystatechange = function() {
		if (rawFile.readyState === 4 && rawFile.status == "200") {
			callback(rawFile.responseText);
		}
	}
	rawFile.send(null);
}

function loadSvg(key) {
	xhr = new XMLHttpRequest()
	xhr.open("GET", "/files/output-svg/" + key + ".svg?random=" + getRandomInt(3000), false)
	xhr.overrideMimeType("image/svg+xml")
	xhr.send("")
	p = '<span data-key="' + key + '" id="i_' + key + '" class="cadratin" ><a href="/type/' + key + '" >' + xhr.responseXML.documentElement.outerHTML + '</a></span>'
	typewriter.innerHTML += p	
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
			p += '<div class="block_input" ><label>' + table[u].description + ' | <span id="span_' + u + '" class="valueBox">' + table[u].value + '</span></label>' + input.outerHTML + '</div>'
		}
	}
	globalNav.innerHTML += '<div class="items" id="' + i + '" ><h1>' + i + '</h1>' + p + '</div>'

}

function buildNav(data) {
	var glob = data.variables
	for (i in glob){
		inputBuild(glob, i)
	}
}

function writeJson(data){

	if (data == false) {
		var sentence = '-all'
	}else {
		var sentence = inputWrite.value
		typewriter.innerHTML = ''
		typewriter.className = "loading"
	}
	
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			if (data == false) {
				console.log('test')
				for(img in imgs) {
					var re = imgs[img].src
					imgs[img].src = re + '2'
				}
			} else {	
				var sentence = inputWrite.value
				writeValue(sentence)	
				writeJson(false)
			}
			typewriter.classList.remove("loading")
		}
	}

	xmlhttp.open('POST', '/write', true);
	xmlhttp.send('json=' + JSON.stringify(data,  null, 4) + '&set=' + sentence);
}

function changeValue(data){
	for (var i = 0, len = inputsRange.length; i < len; i++) {
		inputsRange[i].addEventListener('change', function() {
			var val = this.value
			var vari = this.getAttribute('data-var')
			var cat = this.closest('.items').id
			sp = document.getElementById('span_' + vari)
			sp.innerHTML = val
			data.variables[cat][vari].value = val
			console.log(data)
			writeJson(data, false)
		});
	}
}

function writeValue(stn) {
	typewriter.innerHTML = ""
	stn = sentence.split('')
	stn.forEach(function(entry) {
		code = entry.charCodeAt(0)
		loadSvg(code)
	});

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
			xmlhttp.send('key=' + key)
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
			xmlhttp.send('key=' + key)
		}, false)
}


function loadMp(editor) {
	var key = editor_mp.getAttribute('data-key')
	xhr = new XMLHttpRequest()
	xhr.open("GET", "/files/mpost/mpost-files/" + key + ".mp?random=" + getRandomInt(3000), false)
	xhr.send("")
	console.log(xhr)
	editor.setValue(xhr.responseText)
}

function writeMp(editor, key) {
	var contentMp = editor.getValue()
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			sentence = inputWrite.value
			writeValue(sentence)
			console.log('finish')
		}
	}
	xmlhttp.open('POST', '/writeMp', true);
	contentMp = contentMp.replace(/;/g, '#59');
	xmlhttp.send('mp=' + contentMp + '&key=' + key);
}


window.addEventListener('DOMContentLoaded', function(){
	let editor = ace.edit("editor_mp");
	editor.getSession().setMode("ace/mode/javascript");	
	loadMp(editor)
	readJson("/files/global.json", function(text){
		var data = JSON.parse(text)


		console.log(data)
		buildNav(data)
		changeValue(data)
	})
	
	run.addEventListener('click', function() {
		var key = this.parentElement.getAttribute('data-key')
		writeMp(editor, key)

	})
	
	inputWrite.addEventListener('input', function() {
		sentence = this.value
		writeValue(sentence)
	})

	writeValue(sentence);
	activeInks()
	refreshInks(editor)
	btn_all.addEventListener('click',function(e){	
		writeJson(data, true)
	})

})

