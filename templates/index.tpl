<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title></title>
	<link rel="stylesheet" href="/static/css/style.css" title="" type="text/css">
</head>
<body>

	<section id="content" class="{{ mode }}">
		<nav>
			<h1>P L A N C T O N</h1>
			<hr>
			
			<div id="interface_nav">
			</div>
			<div id="global_nav">
			</div>
		</nav>
		%if mode == 'type':
		<div id="editorBox">
			<div class="options">
				<h1>char : {{ key[1] }} | key : {{key[0] }}</h1>
			    <div class="tools_bar"  data-key="{{key[0]}}" >
					<input type="button" class="btn" id="run" value="<<< Run Mpost" >
					<span class="inks" >
						<span class="btn" id="refresh" >mpost <<< </span>
						<span id="inkscape" class="btn" > inkscape</span>
					</span>
				</div>
			</div>
			<div id="editor_mp" data-key="{{ key[0] }}">test</div>
		</div>
		%end
		<div id="typewriter">
			%if mode == 'type':
				<input type="text" name="" id="inputWrite" value="{{ key[1] }}">
			%end
			<div id="svgContainer"></div>
		</div>
		<div id="setchart">
			<input type="button" onclick="writeJson(false);" class="btn" name="" id="btn_all" value="refresh all">
		% for chart in setchart:
		<a href="/type/{{ chart }}">
			<div class="chart">	
				<div class="info">
					<span class="key">
					%if mode == 'set':
						key :
					%end
					{{ chart }}</span>
				</div>
				<div class="imgBox">
					<img class="imgChar" src="/files/output-svg/{{ chart }}.svg?random={{ rand }}" />
				</div>
			</div>
		</a>

		% end
		<div class="chart addChart">
				<span class="key">+</span>
		</div>
	</section>
</body>
	<script charset="utf-8" src="/static/js/functions.js" ></script>
	<script charset="utf-8" src="/static/js/main.js" ></script>
	<script charset="utf-8" src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.01/ace.js" ></script>
	<script>
	</script>
</html>
