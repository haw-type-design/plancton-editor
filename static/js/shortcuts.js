function saveMP(_KEY_){
	for (var i = 0, len = _FILES_.length; i < len; i++) {
		write('write_file', aceEditor[i + 2],_FILES_[i].getAttribute('data-key'), _KEY_)	
	}
	write('write_file', aceEditor[1], _KEY_, _KEY_)
	sentence = inputWrite.value
	write_sentence(sentence)
}
function shortcuts() {
	var section = document.getElementsByTagName('section')[0]
	
	document.onkeydown = keydown 
	function keydown (evt) { 
		if (!evt) evt = event; 

		if (evt.ctrlKey == true) {
			console.log(evt)

			switch(evt.keyCode){
				case 77: // Press M
					saveMP(_KEY_)
				break

				case 71: // PresssaveMP(_KEY_) G
					writeGlobal();
					break

				case 84: // Press T : save CSS specimen
					writeCss(cssEditor)
					break

				case 191: // Press : Focus Zoom
					inputWrite.value = ':'
					inputWrite.focus()
					break
				case 76: // Press ctrl L

						section.classList.toggle('hide_left')
						window.focus()
		
					break
				case 82: // Press ctrl R
					
						section.classList.toggle('hide_right')
						window.focus()
					
					break
				case 40: case 38: // Press up and down
					inputZoom.focus()
					break
			}
		}
		// if (evt.ctrlKey && evt.keyCode === 77) {
		// 	write('write-file', aceEditor[1], key)
		// 	write('write-mp', aceEditor[0], key)
		// } else if (evt.ctrlKey && evt.keyCode === 37){
		// 	content.classList.toggle('dip')
		// 	this.classList.toggle('active')
		// } else if (evt.ctrlKey && evt.keyCode === 39){
		// 	content.classList.remove('dip')
		// 	content.classList.add('trip')
		// 	document.getElementById('dip').classList.remove('active')
		// 	document.getElementById('trip').classList.add('active')
		// } else if (evt.ctrlKey && evt.keyCode === 191){
		// 	inputWrite.value = ':'
		// 	inputWrite.focus()
		// } else if (evt.ctrlKey && /(40|38)/.test(evt.keyCode) === true){
		// 	inputZoom.focus()
		// }
	}
}
