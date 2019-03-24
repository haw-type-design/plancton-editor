outputtemplate := "%j%c.svg"; % output format
u = 40pt;
ux = 1*u; 
uy = 1*u;

height = 40;
grid = 1;

vardef cadratin(expr width)=
	draw (0 * ux, 0 * uy)--(width * ux, 0 * uy)--(width * ux, height * uy)--(0 * ux, height * uy);
enddef;

def beginchar(expr keycode, width)=
  beginfig(keycode);
	pickup pencircle scaled 1.2;

	draw (0 * ux, 0 * uy) -- (width * ux, 0 * uy) -- (width * ux, height * uy) -- (0 * ux, height * uy) -- cycle scaled .05 withcolor red;
	height = 40;
	if grid = 1:
		for i=0 upto width:
			draw (i*ux, height*uy) -- (i*ux, 0*uy) withcolor blue;
		endfor;
		for i=0 upto height:
			draw (width*ux, i*uy) -- (0*ux, i*uy) withcolor blue;
		endfor;
	fi;

	pickup pencircle xscaled 1ux yscaled 1uy rotated -20;
enddef;

def endchar(expr lenDots)=
    defaultscale :=7;
	for i=1 upto lenDots:
	  dotlabels.top([i]) withcolor red;
	endfor;
	endfig;
enddef;


