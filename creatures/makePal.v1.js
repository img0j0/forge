function makePal(S,c){
  const T=THEMES[c.theme],P=S.dark?T.dark:T.cute,b=S.body,dk=S.dark,p=[];
  p[2]=b;p[3]=mix(shade(b,dk?-.4:-.26),dk?'#2A1A4A':'#5B3E8F',.2);p[4]=shade(b,dk?.22:.34);
  p[1]=dk?mix(shade(b,-.85),'#05040A',.4):shade(b,-.64);
  p[5]=P.belly;p[12]=shade(P.belly,-.2);p[6]=P.accent;p[13]=shade(P.accent,-.28);
  p[7]='#FFFFFF';p[8]=dk?'#0A0810':'#2B2140';p[9]=P.glow||'#FFFFFF';p[10]=P.glow2||'#FFFFFF';
  p[11]=shade(b,dk?-.55:-.42);p[14]=dk?'#E6DEC6':'#FFFFFF';p[15]=dk?'#A89F86':'#D8D0F0';
  p[16]='#FF8FB0';p[17]='#FFD84A';p[18]='#C98A12';
  const out=[[0,0,0]];for(let i=1;i<19;i++)out[i]=hexRGB(p[i]||'#000000');
  CHARM_COL.forEach((h,i)=>out[19+i]=hexRGB(h));WARD_COL.forEach((h,i)=>out[24+i]=hexRGB(h));
  const pulse=out.slice();pulse[9]=hexRGB(mix(p[9],p[10],.45));
  return {pal:out,palP:pulse};
}