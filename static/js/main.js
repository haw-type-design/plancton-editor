window.addEventListener('DOMContentLoaded', function(){
	toogle('#editorBox .btn_file', ['active', 'desactive'])
	toogle('nav .btn_file', ['active', 'desactive'])


		var key = document.getElementsByClassName('tools_bar')[0].getAttribute('data-key')
		for (var i = 0, len = editors.length; i < len; i++) {
			aceEditor[i] = ace.edit(editors[i]);
			aceEditor[i].getSession().setMode("ace/mode/javascript");	
			loadMp(aceEditor[i], editors[i])
			refreshInks(aceEditor[i])
		}
		run.addEventListener('click', function() {
			write('write-file', aceEditor[1], key)
			write('write-mp', aceEditor[0], key)
		})

		writeValue(sentence);
		activeInks()

		document.onkeydown = keydown 
		function keydown (evt) { 
			if (!evt) evt = event; 
			if (evt.ctrlKey && evt.keyCode === 77) {
				write('write-file', aceEditor[1], key)
				write('write-mp', aceEditor[0], key)
			} else if (evt.ctrlKey && evt.keyCode === 37){
				content.classList.toggle('dip')
				this.classList.toggle('active')
			} else if (evt.ctrlKey && evt.keyCode === 39){
				content.classList.remove('dip')
				content.classList.add('trip')
				document.getElementById('dip').classList.remove('active')
				document.getElementById('trip').classList.add('active')
			} 
		
		for (var i = 0, len = toggleNav.length; i < len; i++) {
			toggleNav[i].addEventListener('click', function(){
					content.classList.toggle('dip')
					this.classList.toggle('active')
					
			})
		}
	}

	readJson("/projects/" + projectName + "/global.json?rand=" + getRandomInt(3000), function(text){
		var data = JSON.parse(text)
		buildNav(data)
		changeValue(data)
	})

	inputWrite.addEventListener('input', function() {
		sentence = this.value
		writeValue(sentence)
	})

	inputZoom.addEventListener('change', function(i,item){
		svgContainer.style.transform = 'scale('+this.value+')'
	})


})
