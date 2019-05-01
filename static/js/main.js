// function tabChange(tab) {
//
// }

window.addEventListener('DOMContentLoaded', function(){

	if (content.className !== 'set ') {
		for (var i = 0, len = editors.length; i < len; i++) {
			aceEditor[i] = ace.edit(editors[i]);
			aceEditor[i].getSession().setMode("ace/mode/javascript");	
			loadMp(aceEditor[i], editors[i])
			refreshInks(aceEditor[i])
		}
		// let editor = ace.edit("editor_mp");
		// editor.getSession().setMode("ace/mode/javascript");	
		// loadMp(editor)
		run.addEventListener('click', function() {
			var key = this.parentElement.getAttribute('data-key')
			console.log(key)
			write('write-mp', aceEditor[0], key)
			write('write-file', aceEditor[1], key)
		})
		writeValue(sentence);
		activeInks()
		for (var i = 0, len = btn_tab.length; i < len; i++) {
			btn_tab[i].addEventListener('click',function(){	
				alert('salut')
			})
		}
	}

	readJson("/files/global.json", function(text){
		var data = JSON.parse(text)
		buildNav(data)
		changeValue(data)
	})


	inputWrite.addEventListener('input', function() {
		sentence = this.value
		writeValue(sentence)
	})

})
