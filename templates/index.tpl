<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title></title>
	<link rel="stylesheet" href="/static/css/style.css" title="" type="text/css">
</head>
<body>
	<nav>
		<div id="interface_nav">
			<input type="text" data-sentence="Aabcdefghy" name="" id="editor" value="Aa">
			<input type="button" onclick="writeJson(false);" name="" id="btn_all" value="all">
		</div>
		<div id="global_nav">

		</div>
	</nav>
	<section id="editor_mp">def draww(suffix data) = </section>
	<section id="content"></section>
</body>
	<script charset="utf-8" src="static/js/functions.js" ></script>
	<script charset="utf-8" src="static/js/main.js" ></script>
	<script charset="utf-8" src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.01/ace.js" ></script>
<script>
	var editor_mp = ace.edit("editor_mp");
		editor_mp.getSession().setMode("ace/mode/Tex");
		// editor_mp.getSession().setMode("ace/theme/ambiance");

</script>
</html>
