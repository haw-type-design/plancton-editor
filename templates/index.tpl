
% rebase('templates/base.tpl')
<section id="content" class="" >
	<nav>
		<h1>P L A N C T O N</h1>

		<p>Plancton est un environnement de développement destiné à réaliser des typographies numériques par le biais du langage de construction de figures <a href="https://fr.wikipedia.org/wiki/MetaPost"> Metapost </a></p>

		
		<p id='projects'>Projets :
		% for project in projectsjson:
		<a href="/type/{{ project['font-id'] }}">{{ project['font-name'] }}</a>
			
		% end

		<p>Documentation par <a href="">ici</a></p>

</section>
