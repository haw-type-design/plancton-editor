% rebase('templates/base.tpl')

% if key[0] == 'free':
	% status = 'free'
% else:
	% status = 'trip'
% end 

<section id="content" class="{{mode}} {{status}}" data-project="{{ PROJECT }}">
	<nav>
		<h1>P L A N C T O N / {{ PROJECT }}</h1>
		<hr>
		<div id="interface_nav"></div>
		<div id="info_nav"></div>
		<div id="global_nav"></div>
		<div class="tabs">
		% if mode == 'type':

				<a id="dip" title="Ctrl+left" class="btn_file toggleNav">dip</a>
				<a id="trip" title="Ctrl+right" class="btn_file toggleNav active">trip</a>
				<br/>
				<br/>
				<a href="/{{ PROJECT }}" class="btn_file" >set</a>
				<a class="btn_file active" >type</a>
		% else:
			<a class="btn_file active" >set</a>
			<a href="/type/{{ PROJECT }}" class="btn_file" >type</a>
		% end
		</div>
	</nav>
	% if mode == 'type':
	<div id="editorBox">
		<div class="options">
			<div class="tabs">
				<a class="btn_file tab active" data-active="false" href="#editor_mp" >char : {{key[1]}} | key : {{key[0]}}</a>
				<a class="btn_file tab" data-active="false" href="#editor_def" >def.mp</a>
				<a href="/type" class="btn_file">X</a>
			</div>
			<div class="tools_bar"  data-key="{{key[0]}}" >
				<input type="button" class="btn" title="Ctrl + m" id="run" value="<<< Run Mpost" >
				<span class="inks" >
					<span class="btn" id="refresh" >mpost <<< </span>
					<span id="inkscape" class="btn" > inkscape</span>
				</span>
			</div>
		</div>
		<div class="editor" id="editor_mp" data-key="mpost-files/{{key[0]}}"></div>
		<div class="editor" id="editor_def" data-key="def"></div>
	</div>
	% end
	<div id="typewriter">
		% if mode == 'type':
			<input type="text" name="" id="inputWrite" value="{{key[1]}}">
		% end
		<div id="svgContainer"></div>
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
				<img class="imgChar" src="/projects/{{ PROJECT  }}/output-svg/{{chart}}.svg?random={{rand}}" />
			</div>
		</div>
	</a>
	% end
		<div class="chart addChart">
			<span class="key">+</span>
		</div>
	</div>
	% end
	% include('templates/form-glyph.tpl')
</section>

