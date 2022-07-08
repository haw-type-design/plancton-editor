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
		case /:clean [0-9]+/.test(stn): // test de :del _65_
			var k = stn.match(/[0-9]+/)
			var l = String.fromCharCode(k)
			LOG('IN', 'Do you want clean the metapost file of '+l+' ?', true, function(result){
				if(result === true){	
					pingServer('/clean/'+k, function(cb){
						LOG('OUT', cb, false)
						window.location.reload(false);
					})
				}
			})
			break
		case /:generate font/.test(stn): // test de :add _65_
			alert('on genère la fonte ' + stn.match(/[0-9]+/))
			pingServer('/testing/metabise', function(cb){
						LOG('OUT', cb, false)
						window.location.reload(false);
					})
			break
		case /:specimen/.test(stn): // test de :add _65_
			pingServer('/testing/metabise', function(cb){
						LOG('OUT', cb, false)
						window.location.assign('/testing/metabise');
					})
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
			nav.classList.add('editing')
			loadJson(aceEditor[0])


			
			// data = data.replace(/;/g, '#59');
			// data = data.replace(/\+/g, '#45');
			//writeJson(aceEditor[0].getValue())
			// loadJson(editor_global);

			// LOG('IN', 'Do you want add the glyph '+l+' ?', true, function(result){
			// 	if(result === true){	
			// 		var contenu = aceEditor[0].getValue()
			// 		write('write_file', aceEditor[2], _KEY_, function(cb){
			// 			LOG('OUT', cb, false)
			// 		})
			// 	}
			// })

			LOG('IN', 'Do you want to edit global', true, function(result){
				if(result === true){

					


					
				}
			})

			//fonction bricolée car requete impossible dans log 

			if (document.querySelector('input[type="button"][value="yes"]')){
				document.querySelector('input[type="button"][value="yes"]').addEventListener('click', function(){

					write('write_json', aceEditor[0], _KEY_)
					inputWrite.value = ''
					write_sentence('')	
					log_elem.innerHTML = ""
					nav.classList.remove('editing')
					readJson("/projects/" + projectName + "/current.json?rand=" + getRandomInt(3000), function(text){
					var data = JSON.parse(text)
					buildNav(data)
					changeValue(data)
				})

				})

				document.querySelector('input[type="button"][value="no"]').addEventListener('click', function(){
				
					inputWrite.value = ''
					write_sentence('')	
					log_elem.innerHTML = ""
					nav.classList.remove('editing')
					

				})
			}
			break


		default:
			log_elem.innerHTML = ""

	}
}
