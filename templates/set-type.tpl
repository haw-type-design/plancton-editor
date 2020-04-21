% rebase('templates/base.tpl')

% if key[0] == 'free':
	% status = 'free'
% else:
	% status = 'trip'
% end 

<section id="content" class="{{mode}} {{status}}" data-project="{{ PROJECT }}">
	<nav>
		<div class="header">
			P L A N C T O N
			<hr>
		</div>
		<div class="global">
			<div id="interface_nav"></div>
			<div id="info_nav"></div>
			<div id="global_nav"></div>
		</div>

	</nav>
	<div id="editorBox">
		<div class="options">
			<div class="tabs">
				<a class="btn_file tab active" data-active="false" href="#editor_mp" >char : {{key[1]}} | key : {{key[0]}}</a>
				<a class="btn_file tab" data-active="false" href="#editor_def" >def.mp</a>
			</div>
		</div>
		<div class="editor" id="editor_mp" data-key="mpost-files/{{key[0]}}"></div>
		<div class="editor" id="editor_def" data-key="def"></div>
		<div class="tools_bar"  data-key="{{key[0]}}" >
			<input type="button" class="btn" title="Ctrl + m" id="run" value="<<< Run Mpost" >
			<span class="inks" >
				<span class="btn" id="refresh" >mpost <<< </span>
				<span id="inkscape" class="btn" > inkscape</span>
			</span>
		</div>
	</div>
	<div class="typewriter">
		<div class="zoom">
			<input class="zoom" type="range" step="0.1" value="1" min="0.5" max="5" />
			<span class="zoom_value"> 1 </span>
		</div>
		<div id="svgContainer"></div>
		<div class="footer">
			% if mode == 'type':
				<input type="text" name="" id="inputWrite" value="">
				<span id="log" class=""></span>
			% end
		</div>
	</div>

	% if mode == 'set':
	<div id="setchart">
	% for chart in setchart:
	<a href="/type/{{ PROJECT }}/{{chart}}#editor_mp">
		<div class="chart">	
			<div class="info">
				<span class="key">
				% if mode == 'set':
					key :
				% end
				{{chart}}</span>
			</div>
			<div class="imgBox">
				<img class="imgChar" src="/projects/{{PROJECT}}/output-svg/{{chart}}.svg?random={{rand}}" />
			</div>
		</div>
	</a>
	% end
	</div>
	% end
</section>

