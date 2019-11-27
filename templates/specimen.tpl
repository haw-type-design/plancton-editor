% rebase('templates/base.tpl')
<section id="content" class="specimen">
	<style>
		@font-face{
				font-family:'{{ elem }}';
				src: url('/files/fonts/archive/{{ elem }}/temp.otf');	
		}
		[data-version="{{ elem }}"] {
			background: blue !important;
			color: white;
		}
	</style>
	<nav>
		<h1>P L A N C T O N</h1>
		<hr>
		<div id="listArchive" >
			<ul>
				% for item in archiveList:
				<li data-version='{{ item }}'>
					<span class="delete">X</span>
					<span class="version"><a href="/specimen/{{item}}">{{item}}</a></span>
					<span class="compare"><-></span>
				</li>
				% end
			</ul>
		</div>
	</nav>
	<div id="pages">
		<div class="page" style="font-family: {{ elem }}, times;" >
			<h1 spellcheck="false" contenteditable>PUBLIC<br>Guard 8</h1>
			<p spellcheck="false" contenteditable>Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. 01234567890</p>
		</div>
	</div>
	% include('templates/form-glyph.tpl')
</section>
