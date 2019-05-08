% rebase('templates/base.tpl')

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
		<div id="info_nav"></div>
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
				<input type="button" class="btn_file tab active" data-btn="{{ key[0] }}" value="char : {{ key[1] }} | key : {{key[0] }}" >
				<input type="button" class="btn_file tab" data-btn="def.mp" value="def.mp" >
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
		<div class="editor" id="editor_mp" data-key="mpost-files/{{ key[0] }}"></div>
		<div class="editor" id="editor_def" data-key="def"></div>
	</div>
	%end
	<div id="typewriter">
		%if mode == 'type':
			<input type="text" name="" id="inputWrite" value="{{ key[1] }}">
		%end
		<div id="svgContainer"></div>
	</div>

	%if mode == 'set':
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
	% end
</section>
