"""Render current cable-free tabletop initial states; no physics steps."""
from html import escape
import json
import mujoco
from PIL import Image, ImageDraw, ImageFont

from robofrontier.suite.v2 import ROOT,cases,directory

REVISION=max(c['scene_revision'] for c in cases() if c['family']=='relay')
OUT=ROOT/f'docs/generated/frontier-v2/relay-r{REVISION}'
FONT='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
DESCRIPTIONS={2:'L2 · 90° beam + closed-ring weight',3:'L3 · Spring hinge + rigid pendulum + weight'}


def sheet(selected,view,name,title):
    width,height=1600,1000;gap=24;margin=28;head=120;rowheight=1100
    image=Image.new('RGB',(3*width+2*gap+2*margin,head+2*rowheight+gap+margin),'#eef3f6')
    draw=ImageDraw.Draw(image)
    draw.text((margin,16),title,font=ImageFont.truetype(FONT,46),fill='#183345')
    draw.text((margin,77),'Actual MuJoCo static initial state · 600 g weight · No Oracle run',font=ImageFont.truetype(FONT,28),fill='#526979')
    for row,level in enumerate((2,3)):
        for col,arms in enumerate((8,12,16)):
            case=next(c for c in selected if c['arms']==arms and c['level']==level)
            x=margin+col*(width+gap);y=head+row*(rowheight+gap)
            draw.rounded_rectangle((x,y,x+width,y+rowheight),18,fill='white')
            draw.text((x+15,y+15),f'{DESCRIPTIONS[level]} · {arms} arms / {arms//4} beams',font=ImageFont.truetype(FONT,32),fill='#183345')
            with Image.open(OUT/case['id']/(view+'.png')) as source:image.paste(source,(x,y+80))
    image.save(OUT/(name+'.png'))
    image.thumbnail((2000,1300));image.save(OUT/(name+'-preview.jpg'),quality=94)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    selected=[c for c in cases() if c['family']=='relay' and c['level']>1]
    cards=[]
    for case in selected:
        folder=directory(case);target=OUT/case['id'];target.mkdir(exist_ok=True)
        m=mujoco.MjModel.from_xml_path(str(folder/'scene.xml'));d=mujoco.MjData(m)
        mujoco.mj_resetDataKeyframe(m,d,m.key('initial').id);mujoco.mj_forward(m,d)
        m.vis.global_.offwidth=1600;m.vis.global_.offheight=1000
        views=['top','global','global_rear','payload_01_close','payload_01_weight_close']
        labels=['Top','Front','Rear','Beam close-up','Closed-ring and weight close-up']
        task=json.loads((folder/'task.json').read_text());legend=[]
        if case['level']==3:
            for a in task['mechanism']['payload_assemblies']:
                mode=a.get('elastic_hinge',{}).get('mode','out_of_plane')
                name='In-plane hinge' if mode=='in_plane' else 'Out-of-plane hinge'
                views.append(a['id']+'_hinge_close');labels.append(a['id']+' · '+name)
                legend.append(a['id']+'：'+name)
        with mujoco.Renderer(m,width=1600,height=1000,max_geom=max(5000,m.ngeom+1000)) as renderer:
            for view in views:
                renderer.update_scene(d,camera=view);image=Image.fromarray(renderer.render())
                image.save(target/(view+'.png'));image.save(folder/('preview-'+view+'.png'))
        pictures=''.join(f'<a href="{case["id"]}/{v}.png"><strong>{label}</strong><img loading="lazy" src="{case["id"]}/{v}.png"></a>' for v,label in zip(views,labels))
        cards.append(f'<article><h2>{escape(DESCRIPTIONS[case["level"]])} · {case["arms"]} arms · {case["arms"]//4} beams</h2><p>{"；".join(legend)}</p><div class="views">{pictures}</div></article>')
        print(case['id'],flush=True)
    sheet(selected,'top','top-all','Cable-free Relay · Six revised top views')
    sheet(selected,'payload_01_weight_close','weights-all','Cable-free Relay · Closed-ring and weight details')
    sheet(selected,'payload_01_close','assemblies-all','Cable-free Relay · Transported beam details')
    comparison=Image.new('RGB',(3200,1130),'#eef3f6');draw=ImageDraw.Draw(comparison)
    for col,level in enumerate((2,3)):
        draw.text((col*1600+24,24),DESCRIPTIONS[level],font=ImageFont.truetype(FONT,40),fill='#183345')
        with Image.open(OUT/f'relay-a08-d{level}'/'payload_01_weight_close.png') as src:comparison.paste(src,(col*1600,110))
    comparison.save(OUT/'l2-l3-detail.png')
    hinges=Image.new('RGB',(3200,1130),'#eef3f6');draw=ImageDraw.Draw(hinges)
    for col,(ident,name) in enumerate((('payload_01','Beam 1: in-plane hinge'),('payload_02','Beam 2: out-of-plane hinge'))):
        draw.text((col*1600+24,24),name,font=ImageFont.truetype(FONT,42),fill='#183345')
        with Image.open(OUT/'relay-a08-d3'/(ident+'_hinge_close.png')) as src:hinges.paste(src,(col*1600,110))
    hinges.save(OUT/'hinge-directions.png')
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Cable-free Relay R8</title><style>body{font:18px system-ui;color:#183345;background:#eef3f6;max-width:1700px;margin:30px auto;padding:20px}a{color:#14618a}.views{display:grid;grid-template-columns:1fr 1fr;gap:20px}img{width:100%;display:block}article{background:white;padding:24px;margin:30px 0;border-radius:16px}strong{display:block;margin:12px 0}</style><h1>Cable-free Relay · R8</h1><p>L1 retained. L2: 90° beam, linked closed metal rings and 600 g weight. L3: 135° spring hinge, linked closed rings, approximately 120 mm rigid pendulum and 600 g weight. 8/12/16 arms carry 2/3/4 independent beams. Earlier Cable inputs are retained.</p><p>Actual tabletop initial-state MuJoCo renders; no robot transport or Oracle. The pictured spring represents a restoring hinge, not flexible Cable. The older Factory composite was not regenerated; revised scenes include offline-state replay manifests.</p><p><a href="top-all.png">High-resolution top views</a> · <a href="weights-all.png">High-resolution weight details</a> · <a href="checks.json">Passive checks and timing</a></p><a href="top-all.png"><img src="top-all-preview.jpg"></a>'+''.join(cards),encoding='utf-8')
    print(OUT/'index.html',flush=True)
    page=OUT/'index.html'
    page.write_text(page.read_text().replace('R8',f'R{REVISION}').replace('<p>L1 retained.','<p>L3 mixed hinges: 8 arms, one of each; 12 arms, one in-plane and two out-of-plane; 16 arms, two of each.<a href="hinge-directions.png">Compare the two hinge directions</a>。</p><p>L1 retained.'),encoding='utf-8')


if __name__=='__main__':main()
