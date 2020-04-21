function LOG(std, message, conf, callback){
	log_elem.className = std
	log_elem.innerHTML = message 

	if(conf == true) {
		var c = []
		var y = document.createElement('INPUT')
		var n = document.createElement('INPUT')
		y.type = n.type = 'button'
		y.value= 'yes'
		n.value= 'no'
		y.onclick = function() {callback(true), stop()}
		n.onclick = function() {callback(false), stop()}
		log_elem.append(y)
		log_elem.append(n)
	}
}

function commands(stn){
	switch(true) {
		case /:add [0-9]+/.test(stn): // test de :add _65_
			var k = stn.match(/[0-9]+/)
			var l = String.fromCharCode(k)
			LOG('IN', 'Do you want add the glyph '+l+' ?', true, function(result){
				if(result === true){	
					pingServer('/add/'+k, function(cb){
						LOG('OUT', cb, false)
						window.location.pathname = '/type/'+projectName+'/'+k
					})
				}
			})
			break
		case /:del(ete)? [0-9]+/.test(stn): // test de :del _65_
			var k = stn.match(/[0-9]+/)
			var l = String.fromCharCode(k)
			LOG('IN', 'Do you want delete the glyph '+l+' ?', true, function(result){
				if(result === true){	
					pingServer('/delete/'+k, function(cb){
						LOG('OUT', cb, false)
					})
				}
			})
			break
		case /:generate font/.test(stn): // test de :add _65_
			alert('on genère la font' + stn.match(/[0-9]+/))
			break
		case /:set/.test(stn): // test de :add _65_
			pingServer('/set/meta-old-french', function(cb){
				out = cb.split('|')
				out.forEach(function(entry) {
					loadSvg(entry)
				})
			})	
			if(!typewriter.classList.contains('set')){
				typewriter.classList.add('set')
			}
			break
		case /:edit global/.test(stn): // test de :add _65_
			LOG('IN', 'Do you want save lobal.json ?', true, function(cb){
				if (cb == true){
					alert(cb)
				} else if (cb == false){
					inputWrite.value = ''
					write_sentence('')	
					log_elem.innerHTML = ""
				}
			})
			break
		default:
			log_elem.innerHTML = ""

	}


}
