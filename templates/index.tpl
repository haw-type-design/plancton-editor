
% rebase('templates/base.tpl')
<section id="content" class="" >
	<nav>
		<h1>P L A N C T O N</h1>

		<p>Plancton is a development environment for making digital typography. It’s built on <a href="https://www.tug.org/docs/metapost/mpman.pdf" target="_blank">Metapost</a></p>

		
		<p id='projects' class='projects-grid'>Projets:
		% for project in projectsjson:
		<a class= 'grid-item' href="/type/{{ project['font-id'] }}">{{ project['font-name'] }}</a>
			
		% end
            
        <a class= 'grid-item' href="">+ New Project</a>

		<p>Documentation <a href="https://github.com/simonthi/plancton-editor/" target="_blank">here</a></p>

</section>
