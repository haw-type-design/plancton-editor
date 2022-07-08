% rebase('templates/base.tpl')
<link rel="stylesheet" href="/static/css/{{ project }}.css" type="text/css">
<style>
@font-face {
	font-family: 'current-font';
	src: url('../static/fonts/exports/{{ project }}.otf');
}
/* .page{ */
/* 	display: flex; */
/* }  */

body{
	padding : 1rem;
}
p {
	font-size: 10em;
	line-height: 1em;
}
h1 {
	font-weight: normal;
	font-size: 14px;
	color :blue;
	display:inline-block;
}

#specimenOptions{
	font-size : 14px;
	color:blue;
	display:inline-flex;
}
#specimenOptions div{
	display:inline-block;
}
.small {
	font-size: 4em;
}
</style>

<section id="specimen">
<div id="pages">
<h1>{{ project }}</h1>
	<div id="specimenOptions">
		<div id="set_size">size
		<input class="size" type="range" step="0.1" value="1" min="0.5" max="5" />
			<span class="zoom_value"> 1 </span>
			</div>
		<div id="btn_print">print</div>
		<a href="../static/fonts/exports/{{ project }}.otf">download {{ project }}</a>
	</div>
	
	<div class="page" style="font-family: 'current-font'">

		<p class="small" spellcheck="false" contenteditable>
		Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. 01234567890</p>
		<p class="medium" spellcheck="false" contenteditable>Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. 01234567890</p>
	</div>
</div>


<div id="editorBox">
	<div id="editor_css">
	</div></div>

</section>


<script>
	document.addEventListener('DOMContentLoaded', function(){

		if(window.location.hash){
			var page = document.querySelector('.page')
			var vall = window.location.hash.substr(1)
			page.style.transform = 'scale('+vall+')'
		} else {
		}

		let editor_css = document.getElementById('editor_css')
		console.log(editor_css)

		cssEditor = ace.edit(editor_css);
		cssEditor.getSession().setMode("ace/mode/javascript");
		loadCss(cssEditor, editor_css)
		
		shortcuts()
	
	

	})
</script>
