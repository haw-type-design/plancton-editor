
let section = document.getElementById('content')
let editor = document.getElementById('editor')
let globalNav = document.getElementById('global_nav')
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
	xhr.open("GET", "../output-svg/" + key +".svg",false)
	xhr.overrideMimeType("image/svg+xml")
	xhr.send("")	
	section.appendChild(xhr.responseXML.documentElement)	
}

function inputBuild(glob, i) {
	if(glob[i].type) {
		var input = document.createElement("input")
		input.type = glob[i].type;
		input.className = "input_" + glob[i].type 
		input.id = "input_" + i
		input.setAttribute('title', glob[i].description)
		if (glob[i].type == 'range') {
			input.setAttribute('min', glob[i].range[0])
			input.setAttribute('max', glob[i].range[1])
			input.setAttribute('value', glob[i].value)
		}
		globalNav.innerHTML += '<div class="block_input" ><label>' + glob[i].description + ' | <span class="valueBox">' + glob[i].value + '</span></label>' + input.outerHTML + '</div>'
	}
}

function buildNav(data) {
	var glob = data.global_variables
	for (i in glob){
		inputBuild(glob, i)
	}
}

readJson("../global.json", function(text){
	var data = JSON.parse(text)
	buildNav(data)
})

function writeValue(stn) {
	section.innerHTML = ""
	stn = sentence.split('')
	stn.forEach(function(entry) {
		code = entry.charCodeAt(0)
		loadSvg(code)
	});
}

writeValue(sentence);		
editor.addEventListener('input', function() {
	sentence = this.value
	writeValue(sentence)		
}) 

