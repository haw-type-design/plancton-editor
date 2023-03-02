function shortcuts() {
	document.onkeydown = keydown 
	function keydown (evt) { 
		if (!evt) evt = event; 

		if (evt.ctrlKey == true) {
			console.log(evt)
			switch(evt.keyCode){
				case 77: // Press M
					write('write_file', aceEditor[2], _KEY_)
					write('write_mp', aceEditor[1], _KEY_)
					break
				case 191: // Press : Focus Zoom
					inputWrite.value = ':'
					inputWrite.focus()
					break
				case 37: // Press LeftKey 
					content.classList.toggle('hide_left')
					window.focus()
					break
				case 39: // Press rightKey 
					content.classList.toggle('hide_right')
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
