settings.outformat="pdf";
size(20cm);

real findtheta(real phi, real epsilon=realEpsilon) {
// Determines for given phi the unique solution -pi/2<=theta<=pi/2 off
// 2*theta+sin(2*theta)=pi*sin(phi)
// in the non-trivial cases by Newton iteration;
// theoretically the initial guess pi*sin(phi)/4  always works.
    real nwtn(real x, real y) {return x-(2x+sin(2x)-y)/(2+2*cos(2x));};
	real y=pi*sin(phi);
	if(y==0) return 0.0;
	if(abs(y)==1) return pi/2;
	real startv=y/4;
	real endv=nwtn(startv,y);
	if(epsilon<500*realEpsilon) epsilon=500*realEpsilon;
	while(abs(endv-startv)>epsilon) {startv=endv; endv=nwtn(startv,y);};
	return endv;
	};
pair mollweide(real lambda, real phi, real lambda0=0){
// calculates the Mollweide projection centered at lambda0 for the poin with coordinates (phi,lambda)
	static real c1=2*sqrt(2)/pi;
	static real c2=sqrt(2);
	real theta=findtheta(phi);
	return (c1*(lambda-lambda0)*cos(theta), c2*sin(theta));
};

pair lambert(real lambda, real phi, real lambda0=0){
  return (lambda, phi);
};
	
guide gfrompairs(pair[] data) {
	guide gtmp;
	for(int i=0;i<data.length;++i) { 
		pair tmp=lambert(radians(data[i].y),radians(data[i].x));
		gtmp=gtmp--tmp;
	};
	return gtmp;
};

guide borderline(string coodstr, bool plain=true) {
	string[] cood=split(coodstr,";");
	guide bdl;
	pair tmp;
	for(int i=0;i<cood.length-1;++i) {
		string[] strpr=split(cood[i],",");
		if (plain) {
			tmp=(radians((real) strpr[0]),radians((real) strpr[1]));
		} else
		{
 			// tmp=mollweide(radians((real) strpr[0]),radians((real) strpr[1]));
			tmp=lambert(radians((real) strpr[0]),radians((real) strpr[1]));
		}
		bdl=bdl--tmp;
	}
	return bdl--cycle;
}

string datafile="mapdata1_rgb.csv";
file in=input(datafile).line(); 
string[] splt;
int brdrcnt;
int cnt=0;
guide bdl;
real hue;
real sq=sqrt(3);
real r, g, b;
while(true) {
	if(eof(in)) break;
	splt=split(in,'\t');
	brdrcnt=(int) splt[6];
	// hue=cnt*sq;
	// hue=hue-floor(hue);// in[0,1[
	// // For irrational alpha the numbers n*alpha-floor(n*alpha) are equidistributed mod 1
	// hue=150*hue-45;
	r = (real) splt[3];
	g = (real) splt[4];
	b = (real) splt[5];
	write(r, g, b);
	string[] _tmp=split(splt[7+0],";");
	string[] _tmp2=split(_tmp[0],",");
	//if ((real)_tmp2[0] > -26 && (real)_tmp2[0] < 28 && (real)_tmp2[1] > 36 && (real)_tmp2[1] < 71)
	{
		for(int i=0;i<brdrcnt;++i){
				write(7+i);
				bdl=borderline(splt[7+i],plain=false);
				fill(bdl,rgb(r,g,b));
				draw(bdl,black+0.2bp);
		};
	}
	splt.delete();
	// write(cnt);
	++cnt;
};	

close(in);


void draw_legend(real x, real y, real dx, real dy, real green, string text) {
    fill((x,y)--(x+dx,y)--(x+dx,y+dy)--(x,y+dy)--cycle, rgb(1,green,0));
    draw((x,y)--(x+dx,y)--(x+dx,y+dy)--(x,y+dy)--cycle, rgb(0,0,0));
    label(text, (x+0.05, y-0.025), E, black+fontsize(6));
}

draw_legend(-2.5, -1.000+0.5, 0.05, -0.05, 0/6, "0-9\,\%");
draw_legend(-2.5, -1.075+0.5, 0.05, -0.05, 1/6, "10-19\,\%");
draw_legend(-2.5, -1.150+0.5, 0.05, -0.05, 2/6, "20-29\,\%");
draw_legend(-2.5, -1.225+0.5, 0.05, -0.05, 3/6, "30-39\,\%");
draw_legend(-2.5, -1.300+0.5, 0.05, -0.05, 4/6, "40-49\,\%");
draw_legend(-2.5, -1.375+0.5, 0.05, -0.05, 5/6, "50-59\,\%");
draw_legend(-2.5, -1.450+0.5, 0.05, -0.05, 6/6, "60-69\,\%");

pair[] constlong(real lambda, int np=100) {
	pair[] tmp;
	for(int i=0;i<=np;++i) tmp.push((-90+i*180/np,lambda));
	return tmp;
};
pair[] constlat(real phi, int np=100) {
	pair[] tmp;
	for(int i=0;i<=2*np;++i) tmp.push((phi,-180+i*180/np));
	return tmp;
};
// for(int j=1;j<=5;++j) draw(gfrompairs(constlong(-180+j/6*360)),white);
// draw(gfrompairs(constlong(-180)),1.5bp+white);
// draw(gfrompairs(constlong(180)),1.5bp+white);
// for(int j=0;j<=12;++j) draw(gfrompairs(constlat(-90+j/6*180)),white);	

guide boundary=gfrompairs(constlong(-180))--reverse(gfrompairs(constlong(180)))--cycle;
picture pic;
add(pic,currentpicture);
erase();
fill(boundary,paleblue);
add(pic);
shipout(bbox(1mm,gray(0.7),Fill(gray(0.7))), view=true);

