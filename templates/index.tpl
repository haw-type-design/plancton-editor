<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title></title>
	<link rel="stylesheet" href="/static/css/style.css" title="" type="text/css">
</head>
<body>
		%if key[0] == 'free':
			%status = 'free'
		%else:
			%status = ''
		%end 
	

	<section id="content" class="{{mode}} {{status}}">
		<nav>
			<h1>P L A N C T O N</h1>
			<hr>
			
			<div id="interface_nav"></div>
			<div id="global_nav"></div>
			<div class="tabs">
			%if mode == 'type':
				<a href="/index" class="btn_file" >set</a>
				<a class="btn_file active" >type</a>
			%else:
				<a class="btn_file active" >set</a>
				<a href="/type" class="btn_file" >type</a>
			%end
			</div>
		</nav>
		%if mode == 'type':
		<div id="editorBox">
			<div class="options">
				<div class="tabs">
					<input type="button" class="btn_file active" value="char : {{ key[1] }} | key : {{key[0] }}" >
					<input type="button" class="btn_file" value="def.json" >
					<a href="/type" class="btn_file">X</a>
				</div>
			    <div class="tools_bar"  data-key="{{key[0]}}" >
					<input type="button" class="btn" id="run" value="<<< Run Mpost" >
					<span class="inks" >
						<span class="btn" id="refresh" >mpost <<< </span>
						<span id="inkscape" class="btn" > inkscape</span>
					</span>
				</div>
			</div>
			<div id="editor_mp" data-key="{{ key[0] }}"></div>
		</div>
		%end
		<div id="typewriter">
			%if mode == 'type':
				<input type="text" name="" id="inputWrite" value="{{ key[1] }}">
			%end
			<div id="svgContainer"></div>
		</div>
		<div id="setchart">
			<!-- <input type="button" onclick="writeJson(false);" class="btn" name="" id="btn_all" value="refresh all"> -->
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
