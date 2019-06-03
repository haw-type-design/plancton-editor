% rebase('templates/base.tpl')
<section id="content" class="specimen">
	<nav>
		<h1>P L A N C T O N</h1>
		<hr>
		<div id="listArchive" >
			<ul>
				% for item in archiveList:
				<li>
					<span class="delete">X</span>
					<span class="version"><a>{{ item }}</a></span>
					<span class="compare"><-></span>
				</li>
				% end
			</ul>
		</div>
	</nav>
	<div id="typewriter">
		<style>
		@font-face{
			font-family:'{{ elem }}';
			src: url('files/fonts/archive/{{ elem }}/{{ elem }}.otf');	
		}
		</style>
		<div class="page" style="font-family: {{ elem }}, times;" >
			<h1>Hello world {{ elem }}</h1>
		</div>
	</div>
	% include('templates/form-glyph.tpl')
</section>
