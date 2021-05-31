% rebase('templates/base.tpl')

<style>
@font-face {
	font-family: 'current-font';
	src: url('../static/fonts/exports/{{ project }}.otf');
}
/* .page{ */
/* 	display: flex; */
/* }  */
p {
	font-size: 10em;
	line-height: 1em;
}
h1 {
	font-weight: normal;
	font-size: 6em;
}
.small {
	font-size: 4em;
}
</style>

<div id="pages">
	<div class="page" style="font-family: 'current-font'">
		<h1>{{ project }}</h1>
		<p class="small" spellcheck="false" contenteditable>Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. 01234567890</p>
		<p class="medium" spellcheck="false" contenteditable>Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. 01234567890</p>
	</div>
</div>
<a href="../static/fonts/exports/{{ project }}.otf">download {{ project }}</a>

<script>
	document.addEventListener('DOMContentLoaded', function(){

		if(window.location.hash){
			var page = document.querySelector('.page')
			var vall = window.location.hash.substr(1)
			page.style.transform = 'scale('+vall+')'
		} else {
		}
	})
</script>
