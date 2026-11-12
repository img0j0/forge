function genSpec(c){
  const r=mulberry32(c.seed),rr=mulberry32(c.seed^0x7f4a7c15),pick=a=>a[Math.floor(r()*a.length)];
  const T=THEMES[c.theme],dk=c.dark,P=dk?T.dark:T.cute;
  const s={dark:dk,seed:c.seed,body:pick(P.bodies),flip:r()<.5};
  if(!dk){
    s.shape=pick(['round','tall','wide','chonk']);
    s.ears=r()<.7?pick(BIAS[c.v].ears):pick(['pointy','round','bunny','nubs','antenna','tuft','floppy']);
    s.eyes=r()<.75?pick(BIAS[c.v].eyes):pick(['big','round','dot','sleepy']);
    s.mouth=pick(['smile','cat','open','smile','tiny']);
    s.tail=pick(['curl','fluffy','stub']);
    s.mark=pick(['spots','stripes','none','spots','none']);
  }else{
    s.shape=pick(['hulk','wraith','beast','shard']);
    s.horns=r()<.6?['up','ram','crown'][c.v%3]:pick(['up','ram','crown','none']);
    s.eyes=r()<.6?['glare','slit','hollow','cyclops'][c.v%4]:pick(['glare','slit','hollow','cyclops']);
    s.mouth=pick(['fangs','grin','maw','snarl']);
    s.tail=pick(['spade','scorpion','whip']);
    s.mark=pick(['cracks','runes','ribs','none']);
    s.spines=r()<.5;
  }
  const R=c.rarity;
  s.wings=dk?(rr()<[.2,.35,.55,.85,.7][R]):((R===3&&rr()<.7)||(R===4&&rr()<.55));
  s.third=dk&&R>=2&&rr()<.5;
  s.crown=R===4;s.keep=c.keep||'';
  return s;
}