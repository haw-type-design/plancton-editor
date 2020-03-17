
<section id="content" class="" >
	<nav>
		<h1>P L A N C T O N /</h1>
		<hr>
		% for project in projectsjson:
			<a href="/set/{{ project['font-id'] }}">{{ project['font-name'] }}</a>
			<br>
		% end
</section>

