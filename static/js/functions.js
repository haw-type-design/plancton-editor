
let section = document.getElementById('content')
let editor = document.getElementById('editor')
let inputsRange = document.getElementsByClassName('input_range')
let globalNav = document.getElementById('global_nav')
let btn_inkscapce = document.getElementsByClassName('cadratin'); 
var sentence = editor.value

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
	xhr.open("GET", "files/output-svg/" + key + ".svg", false)
	xhr.overrideMimeType("image/svg+xml")
	xhr.send("")
	p = '<span data-key="' + key + '" class="cadratin" >' + xhr.responseXML.documentElement.outerHTML + '</span>'
	console.log(p)
	section.innerHTML += p	
}

function inputBuild(glob, i) {
	if(glob[i].type) {
		var input = document.createElement("input")
		input.type = glob[i].type;
		input.className = "input_" + glob[i].type 
		input.id = "input_" + i
		input.setAttribute('title', glob[i].description)
		input.setAttribute('data-var', i)
		if (glob[i].type == 'range') {
			input.setAttribute('min', glob[i].range[0])
			input.setAttribute('max', glob[i].range[1])
			input.setAttribute('step', glob[i].range[2])
			input.setAttribute('value', glob[i].value)
		}
		globalNav.innerHTML += '<div class="block_input" ><label>' + glob[i].description + ' | <span id="span_' + i + '" class="valueBox">' + glob[i].value + '</span></label>' + input.outerHTML + '</div>'
	}
}

function buildNav(data) {
	var glob = data.global_variables
	for (i in glob){
		inputBuild(glob, i)
	}
}

function writeJson(data){
	section.className = "loading"
	var xmlhttp = new XMLHttpRequest();
	var sentence = editor.value
	xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState == 4)
		{
			var sentence = editor.value
			writeValue(sentence)	
			section.classList.remove("loading")
		}
	}
	xmlhttp.open('POST', 'http://localhost:8080/write', true);
	xmlhttp.send('json=' + JSON.stringify(data,  null, 4) + '&set=' + sentence);
}


function changeValue(data){
	for(i in inputsRange) {
		inputsRange[i].addEventListener('change', function(evt) {
			var val = this.value
			var vari = this.getAttribute('data-var')
			sp = document.getElementById('span_' + vari)
			sp.innerHTML = val
			data.global_variables[vari].value = val
			writeJson(data)
		});
	}
}

function writeValue(stn) {
	section.innerHTML = ""
	stn = sentence.split('')
	stn.forEach(function(entry) {
		code = entry.charCodeAt(0)
		loadSvg(code)
	});
}

window.addEventListener('DOMContentLoaded', function(){
	readJson("files/global-1.json", function(text){
		var data = JSON.parse(text)
		buildNav(data)
		changeValue(data)
	})

	writeValue(sentence);
	editor.addEventListener('input', function() {
		sentence = this.value
		writeValue(sentence)	
	}) 
	
	btn_inkscapce.addEventListener('click', function(evt) {
		alert('saut')	
	})


})

