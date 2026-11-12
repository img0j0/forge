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
  /* 0.54: the second generation (new finds) draws from a wider set with its own random stream, so the
     first generation above is untouched and every Forgeling found before 0.54 keeps its look. */
  if(c.gen===2){
    const q=mulberry32(c.seed^0x2c1b3c6d),qp=a=>a[Math.floor(q()*a.length)];s.g2=1;
    s.ex=Math.floor(q()*3)-1;s.ey=Math.floor(q()*3)-1;
    if(!dk){
      s.shape=qp(['round','tall','wide','chonk','pear','pear','drop','loaf','blob','noodle','mush','mush']);
      s.arms=s.shape==='loaf'||s.shape==='blob'?qp(['tuck','tuck','hug']):qp(['out','out','up','wave','hug','tuck']);
      if(s.shape==='mush')s.ears='none';
      else if(s.shape==='drop')s.ears=qp(['none','none','nubs','round']);
      else if(q()<.15)s.ears='none';
      s.eyes=q()<.45?s.eyes:qp(['happy','sparkle','bean','wink','sparkle','line']);
      s.mouth=q()<.4?s.mouth:qp(['fang','o','wavy','flat','fang','tongue']);
      if(s.shape==='blob'||s.shape==='loaf')s.tail=q()<.5?'none':s.tail;else if(q()<.2)s.tail='leaf';
      s.blush=q()<.75;s.nose=q()<.3;s.mask=q()<.14;s.fluff=s.shape!=='mush'&&s.ears!=='floppy'&&q()<.3;s.duo=q()<.35;
      s.mark=q()<.6?s.mark:qp(['patch','socks','belly0']);
    }else{
      s.shape=qp(['hulk','wraith','beast','shard','imp','imp','slink','tower']);
      s.arms=qp(['claws','claws','raised','none']);
      s.eyes=q()<.5?s.eyes:qp(['many','void','glare','slit']);
      s.mouth=q()<.5?s.mouth:qp(['stitch','tusks','fangs']);
      s.mark=q()<.6?s.mark:'veins';
      if(s.shape==='slink')s.third=false;
    }
  }
  return s;
}
