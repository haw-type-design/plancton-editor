
% B
input ../def;
beginchar(66, 8);
	x1:= 2 * ux;
	bot y1 := baseline * uy;
	x2 :=  2 * ux;
	top y2 := capHeight * uy;
	x3 := 4 * ux;
	top y3 := capHeight * uy;
	x4 := 4 * ux;
	y4 := 5.5 * uy;
	x5 := 4 * ux;
	bot y5 := baseline * uy;
	x6 := 6 * ux;
	y6 := 7.5 * uy;
	x7 := 6 * ux + (strokeX / 2);
	y7 := 3 * uy;
	x8 := 2* ux;
	y8 := 5.5* uy;

	draw z5--z1--z2--z3 withcolor col;
	draw z3{right}..z6..{left}z4--z8 withcolor col;
	draw z4{right}..z7..{left}z5 withcolor col;

endchar(8);
end;
        