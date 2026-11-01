from lib import *
# 0.48.2: the cover (Hunter, on his phone). The Forgeling on the label is drawn at a real size, scaled to the screen;
# its ears and sides stay clear of the sprite's frame; the label, Begin and the small line all sit inside the stitching
# without touching each other, at every phone size (the cover shows before there is a save, so in handwriting).
GEO="""async()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return {t:b.top,b:b.bottom,l:b.left,r:b.right,h:b.height}};
 const im=document.querySelector('.jlabel img');await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);
 const d=x.getImageData(0,0,c.width,c.height).data,W=c.width,H=c.height;let edge=0;for(let i=0;i<W;i++){if(d[(i)*4+3]||d[(W+i)*4+3]||d[(i*W)*4+3]||d[(i*W+W-1)*4+3])edge++;}
 let ink=0;for(let i=3;i<d.length;i+=4)if(d[i])ink++;
 const wm=document.querySelector('.wordmark'),rg=document.createRange();rg.selectNodeContents(wm);const wr=rg.getBoundingClientRect();return {wtext:{l:wr.left,r:wr.right},img:r('.jlabel img'),label:r('.jlabel'),tag:r('.jlabel .tagline'),word:r('.wordmark'),go:r('#titleGo'),small:r('.tsmall'),stitch:r('.jstitch'),band:r('.jband'),edge,ink}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for hand in (True,):
        for W,H in [(320,568),(375,667),(390,844),(430,932),(768,1024)]:
            ctx,pg=newpage(b,W,H)
            pg.goto(P); pg.wait_for_selector("#titleGo"); pg.wait_for_timeout(500)
            if pg.locator(".jlabel img").count()==0: rec("Cover",f"{W}x{H}: the cover label is shown",False); ctx.close(); continue
            g=pg.evaluate(GEO); tag=("hand" if hand else "plain")+f" {W}x{H}"
            rec("Cover",f"{tag}: the Forgeling is drawn at a real size (at least 80 points)",g["img"]["h"]>=80,round(g["img"]["h"]))
            rec("Cover",f"{tag}: its ears and sides stay clear of the sprite's frame",g["edge"]==0 and g["ink"]>80,(g["edge"],g["ink"]))
            rec("Cover",f"{tag}: the label sits below the title and above Begin",g["label"]["t"]>=g["word"]["b"]-2 and g["label"]["b"]<=g["go"]["t"]-8,(round(g["word"]["b"]),round(g["label"]["t"]),round(g["label"]["b"]),round(g["go"]["t"])))
            rec("Cover",f"{tag}: the title and the label stay clear of the dark band",g["wtext"]["r"]<=g["band"]["l"]-2 and g["label"]["r"]<=g["band"]["l"]-2,(round(g["wtext"]["r"]),round(g["label"]["r"]),round(g["band"]["l"])))
            rec("Cover",f"{tag}: the tagline stays inside its label",g["tag"]["b"]<=g["label"]["b"]+1,(round(g["tag"]["b"]),round(g["label"]["b"])))
            rec("Cover",f"{tag}: the small line sits inside the stitching",g["small"]["b"]<=g["stitch"]["b"]-4,(round(g["small"]["b"]),round(g["stitch"]["b"])))
            rec("All",f"{tag}: no page errors",not pg._errs,pg._errs[:2]); ctx.close()
    b.close()
save_results("qa_482"); print(sum(r["ok"] for r in RES),"/",len(RES))
