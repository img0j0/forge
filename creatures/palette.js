/* 0.55: the palette adds mid tones (29 body, 30 accent, 31 belly) and part outlines (32 accent, 33 horn, 34 gold);
   shadows lean cool and highlights warm. */
function makePal(S,c){
  const T=THEMES[c.theme],P=S.dark?T.dark:T.cute,b=S.body,dk=S.dark,p=[];
  p[2]=b;p[3]=mix(shade(b,dk?-.4:-.26),dk?'#2A1A4A':'#5B3E8F',.2);p[4]=mix(shade(b,dk?.22:.34),'#FFF1C8',dk?.06:.14);
  p[1]=dk?mix(shade(b,-.85),'#05040A',.4):shade(b,-.64);
  p[5]=P.belly;p[12]=mix(shade(P.belly,-.2),'#7A6AA8',.12);p[6]=P.accent;p[13]=mix(shade(P.accent,-.28),'#4A3A7A',.14);
  p[7]='#FFFFFF';p[8]=dk?'#0A0810':'#2B2140';p[9]=P.glow||'#FFFFFF';p[10]=P.glow2||'#FFFFFF';
  p[11]=mix(shade(b,dk?-.55:-.42),dk?'#1A1030':'#3A2A6A',.15);p[14]=dk?'#E6DEC6':'#FFFFFF';p[15]=dk?'#A89F86':'#D8D0F0';
  p[16]='#FF8FB0';p[17]='#FFD84A';p[18]='#C98A12';
  const out=[[0,0,0]];for(let i=1;i<19;i++)out[i]=hexRGB(p[i]||'#000000');
  CHARM_COL.forEach((h,i)=>out[19+i]=hexRGB(h));WARD_COL.forEach((h,i)=>out[24+i]=hexRGB(h));
  out[29]=hexRGB(mix(p[2],p[3],.5));out[30]=hexRGB(mix(p[6],p[13],.5));out[31]=hexRGB(mix(p[5],p[12],.5));
  out[32]=hexRGB(mix(shade(p[6],-.62),p[1],.35));out[33]=hexRGB(shade(p[15],dk?-.6:-.45));out[34]=hexRGB('#7A4A0C');out[39]=hexRGB(mix(p[2],p[4],.5));out[40]=hexRGB(mix(p[6],p[7],.3));out[41]=hexRGB(mix(p[5],p[7],.35));out[35]=out[11];out[36]=out[13];out[37]=out[15];out[38]=out[18];
  const pulse=out.slice();pulse[9]=hexRGB(mix(p[9],p[10],.45));
  return {pal:out,palP:pulse};
}
