let content = document.getElementById('content')
let projectName = content.getAttribute('data-project')
let typewriter = document.querySelector('.typewriter')
let svgContainer = document.getElementById('svgContainer')
let setchart = document.getElementById('setchart')
let editors = document.getElementsByClassName('editor')
let editor_mp = document.getElementById('editor_mp')
let editor_css = document.getElementById('editor_css')
let run = document.getElementById('run')
let inputWrite = document.getElementById('inputWrite')
let inputsRange = document.getElementsByClassName('input_range')
let nav = document. getElementsByTagName('nav')[0]
let globalNav = document.getElementById('global_nav')
let editGlobal = document.getElementById('editor_global')
let infoNav = document.getElementById('info_nav')
let btn_inkscape = document.getElementById('inkscape')
let btn_refresh = document.getElementById('refresh')
let btn_all = document.getElementById('btn_all')
let btn_tab = document.getElementsByClassName('tab')

let imgs = document.getElementsByClassName('imgChar')	
var aceEditor = []
var cssEditor = []
let toggleNav = document.getElementsByClassName('toggleNav')	
let inputZoom = document.querySelector('.zoom input')	
var log_elem = document.getElementById('log')	


let inputGitCheckout = document.querySelector('input#input_git_checkout')	
let inputGitCheckoutSelect = document.getElementById('select_version')	


if (content.className !== 'set ') {
    var sentence = inputWrite.value
    }

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function get_session(key){
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


function writeGlobal(){
    var editor = aceEditor[0]

    var sentence = inputWrite.value
    svgContainer.innerHTML = ''
    svgContainer.className = "loading"

    var contentMp = editor.getValue()
    contentMp = contentMp.replace(/;/g, '#59');
    contentMp = contentMp.replace(/\+/g, '#45');


    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4)
        {

            var sentence = inputWrite.value
            write_sentence(sentence)	
            svgContainer.classList.remove("loading")
        }
    }

    xmlhttp.open('POST', '/write_global' , true);
    xmlhttp.send('project=' + projectName + '&data=' + contentMp  + '&set=' + sentence);
    //xmlhttp.send('project=' + projectName + '&json=' + data + '&set=' + sentence);

}

function loadSvg(key) {

    var l = String.fromCharCode(key);
    xhr = new XMLHttpRequest()
    xhr.overrideMimeType("image/svg+xml")
    try {
        xhr.open("GET", "/projects/" + projectName + "/output-svg/" + key + ".svg?random=" + getRandomInt(3000), false)
        xhr.onreadystatechange = function() {

            if (xhr.readyState === 4 && xhr.status == "200") {

                p = '<span data-key="' + key + '" id="i_' + key + '" class="cadratin" ><a class="link_cadratin" href="/type/' + projectName + '/' + key + '#editor_mp" >' + xhr.responseXML.documentElement.outerHTML + '<span class="ref">'+l+' | '+key+'.mp</span></a></span>'
            }
        }
        xhr.send("")	
        svgContainer.innerHTML += p	
        delete p
    } catch {
        console.log("Glyph "+l+" not in font")
    }
}

function inputBuild(variablesTable, i) {
    var t = variablesTable[i]
    var p = []

    for (u in t){
        if(t[u].type) {
            var input = document.createElement("input")
            input.type = t[u].type;
            input.className = "input_" + t[u].type 
            input.id = "input_" + u
            input.setAttribute('title', t[u].description)
            input.setAttribute('data-var', u)
            if (t[u].type == 'range') {
                input.setAttribute('min', t[u].range[0])
                input.setAttribute('max', t[u].range[1])
                input.setAttribute('step', t[u].range[2])
                input.setAttribute('value', t[u].value)
            }
            p += '<li class="block_input" ><label data-unity="'+t[u].unity+'" ><div data-name="'+t[u].name+'"  title="'+t[u].description+' \n name: '+t[u].name+'"class="description">'+t[u].description+'</div><span id="span_'+u+'" class="valueBox">| '+t[u].value+'</span><span class="unity">'+t[u].unity+'</span></label>'+input.outerHTML+'</li>'
        }
    }
    globalNav.innerHTML += '<ul class="items" id="' + i + '" ><li><h1>' + i + '</h1></li>' + p + '</ul>'

    var inputs = document.querySelectorAll('.block_input > label > div')
    inputs.forEach(function(item,i){
        item.addEventListener('mouseenter', function(){
            var name = this.getAttribute('data-name')
            var elms = document.querySelectorAll('label[data-unity='+name+']')
            // elms.forEach((el)=>{el.classList.add('ligth')} ) 
            elms.forEach(function(el){ el.classList.add('ligth') }) 
        })
        item.addEventListener('mouseleave', function(){
            var name = this.getAttribute('data-name')
            var elms = document.querySelectorAll('label[data-unity='+name+']')
            elms.forEach(function(el){el.classList.remove('ligth')} ) 
        })
    })

}

function buildNav(data) {
    var glob = data.variables
    console.log(glob);

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

function loadJson(editor){

    xhr = new XMLHttpRequest()
    xhr.open("GET", "/projects/" + projectName + "/global.json?random=" + getRandomInt(3000), false)
    xhr.send("")
    // editor.setValue(xhr.responseText)
    editor.setValue(xhr.responseText)

}

function write_sentence(stn) {

    if(stn.charAt(0) == ':') {
        commands(stn)
    }else{
        var out = []
        svgContainer.innerHTML = ""
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


function loadCss(editor, edi) {

    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/static/css/metabise.css", true)


    xhr.onload = function () {
        if (xhr.readyState == 4) {

            console.log(xhr.response);
            //console.log(xhr.responseText);


        }
        editor.setValue(xhr.response)
    };



    xhr.send("")

}

function writeCss(editor){
    // var contentCss = cssEditor;
    var contentCss = editor.getValue();
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4)
        {

        }
    }


    xmlhttp.open('POST', '/write_css', true);

    xmlhttp.send('&css=' + contentCss);



}

function write(type, editor, file, key) {

    var data1, data2
    //var fileMp = editor.getAttribute('href')

    var contentMp = editor.getValue()
    //console.log("c moi" + editor.getValue())


    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState == 4 )
        {
            console.log('yes')

        }
    }

    data1 = 'mp'
    data2 = 'file'
    data3 = 'key'
    contentMp = contentMp.replace(/;/g, '#59');
    contentMp = contentMp.replace(/\+/g, '#45');


    console.log(file)
    xmlhttp.open('POST', '/write_file', true);
    xmlhttp.send('project=' + projectName + '&mp='+ contentMp + '&file=' + file + '&key=' + key );

    //console.log(fileMp + "," + data2)
}

// function writejkon(type, editor, key) {
// 	var contentMp = editor.getValue()
// 	var xmlhttp = new XMLHttpRequest();
// 	xmlhttp.onreadystatechange = function()
// 	{
// 		if (xmlhttp.readyState == 4)
// 		{
// 			sentence = inputWrite.value
// 			write_sentence(sentence)
// 		}
// 	}


// 	xmlhttp.open('POST', '/write_jkon', true);
// 	contentMp = contentMp.replace(/;/g, '#59');
// 	contentMp = contentMp.replace(/\+/g, '#45');
// 	xmlhttp.send('project=' + projectName + '&json=' + contentMp + '&key=' + key);


// }

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

/* BIDOUILLE */
var tabs = document.querySelectorAll(".tabs > a");
for (var i = 0, len = tabs.length; i < len; i++) {

    tabs[i].addEventListener('click', function(){
        for (var j = 0, len = tabs.length; j < len; j++) {
            console.log(tabs[j]);

        }


        for (var j=0; j<len; j++){

            document.querySelector(tabs[j].getAttribute("href")).style.display='none';

        }
        var href= this.getAttribute("href");
        console.log(href);
        console.log(document.querySelector(href));
        document.querySelector(href).style.display='block';
    });
}


// TERMINAL
function git_action_checkout(new_branch){
    pingServer('/git/checkout/'+new_branch+'/none', function(cb){
        alert(cb)
    })
}
