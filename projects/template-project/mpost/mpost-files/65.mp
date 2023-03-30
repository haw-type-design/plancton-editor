%A
 input ../def; 

beginchar(65,9);
    x1 := 2 * ux;
	bot y1 := 0 * uy;
	x2 := 4.5 * ux - (strokeX);
	top y2 := capHeight * uy;
	x3 := 4.5 * ux + (strokeX);
	top y3 := capHeight * uy;
	x4 := 7 * ux;
	bot y4 := 0 * uy;
	z5 := .15[z1,z2];
	z6 := .15[z4,z3];

	draw z1 -- z2 -- z3 -- z4 withcolor col;
    pickup pencircle scaled (strokeY/2);
	draw z5 -- z6 withcolor col;
endchar(6);
