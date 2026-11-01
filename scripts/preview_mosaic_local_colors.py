"""Exact colour/layout diagrams and zero-step MuJoCo previews for Mosaic R14."""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from robofrontier.suite.mosaic_policy_package import ROOT, read, write, checksum


def font(size):
    return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',size)


def diagram(case, plan, old=False):
    folder=ROOT/case['directory'];env=read(folder/'environment.json')
    colours={a['object_id']:a['previous_colour'] if old else a['colour'] for a in plan['assignments']}
    image=Image.new('RGB',(1500,1500),'#F1F5F7');d=ImageDraw.Draw(image)
    ink='#19384C';muted='#526A78'
    d.text((42,27),f"{case['arms']} arms · L{case['level']} · {'Original colors R13' if old else 'Revised colors R14'}",font=font(39),fill=ink)
    d.text((42,88),'Supply colors only; positions, arms and target retained',font=font(25),fill=muted)
    d.text((42,132),'North up; center cells show the target, not placed blocks',font=font(24),fill=muted)
    hx,hy=env['tables'][0]['half_size_m'][:2]
    scale=min(1370/(2*hx),1010/(2*hy));cx,cy=750,730
    def point(x,y):return cx+x*scale,cy-y*scale
    def square(position,side,fill,outline,width=1):
        x,y=position[:2];a=point(x-side/2,y+side/2);b=point(x+side/2,y-side/2)
        d.rectangle((*a,*b),fill=fill,outline=outline,width=width)
    d.rectangle((*point(-hx,hy),*point(hx,-hy)),fill='#E7DCC7',outline='#BFB398',width=2)
    for g in env['goals']:
        square(g['position_m'],env['grid']['pitch_m']*.94,env['grid']['palette'][g['requires']['color']],'#FFFFFF')
    for o in env['objects']:
        square(o['initial_position_m'],env['grid']['cube_side_m'],env['grid']['palette'][colours[o['id']]],'#273D48',2)
    for station in env['stations']:
        x,y=station['base_position_m'][:2];px,py=point(x,y)
        tip=point(x+.13*math.cos(station['yaw_rad']),y+.13*math.sin(station['yaw_rad']))
        d.line((px,py,*tip),fill='#205E89',width=5)
        d.ellipse((px-17,py-17,px+17,py+17),fill='#205E89',outline='white',width=2)
        d.text((px,py),station['id'],anchor='mm',font=font(23),fill='white')
    y=1280
    for index,row in enumerate(plan['per_robot']):
        col=index%4;line=index//4
        text=f"{row['robot']}: {row['certified_local_pairs']}/{row['nearby_stock']} ({row['certified_local_fraction']:.0%})"
        d.text((45+col*365,y+line*42),text,font=font(27),fill=ink)
    if old:
        d.rectangle((30,1260,1470,1380),fill='#F1F5F7')
        d.text((45,1283),'Original nearby supplies often shared one color, requiring cross-zone pickup.',font=font(26),fill=ink)
    else:
        d.text((42,1390),'Ratio = distinct supply/target pairs reachable by one arm / nearest supplies.',font=font(22),fill=muted)
        d.text((42,1427),'Sampled geometry only; no revised Oracle/GPT run or parallel-path qualification.',font=font(22),fill=muted)
    return image


def previews(cases,plans,output):
    import mujoco
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    cards=[];manifest=[]
    all_nine=Image.new('RGB',(3000,3000),'#F1F5F7')
    before_after=Image.new('RGB',(3600,2400),'#F1F5F7')
    for case in cases:
        dest=output/case['id'];dest.mkdir()
        plan=plans[case['arms']];layout=diagram(case,plan)
        layout.save(dest/'colour-layout.png')
        col=[4,6,8].index(case['arms']);row=case['level']-1
        all_nine.paste(layout.resize((1000,1000),Image.Resampling.LANCZOS),(col*1000,row*1000))
        if case['level']==1:
            before_after.paste(diagram(case,plan,True).resize((1200,1200),Image.Resampling.LANCZOS),(col*1200,0))
            before_after.paste(layout.resize((1200,1200),Image.Resampling.LANCZOS),(col*1200,1200))
        model=mujoco.MjModel.from_xml_path(str(ROOT/case['directory']/'scene.xml'));data=mujoco.MjData(model)
        mujoco.mj_resetDataKeyframe(model,data,model.key('initial').id);mujoco.mj_forward(model,data)
        model.vis.global_.offwidth=1600;model.vis.global_.offheight=1200
        with mujoco.Renderer(model,width=1600,height=1200,max_geom=max(5000,model.ngeom+1000)) as renderer:
            for camera in ('top','global'):
                renderer.update_scene(data,camera=camera)
                Image.fromarray(renderer.render()).save(dest/(camera+'.png'))
        print('PREVIEW',case['id'],flush=True)
        assets={name:checksum(dest/name) for name in ('colour-layout.png','top.png','global.png')}
        manifest.append(dict(case_id=case['id'],scene_sha256=checksum(ROOT/case['directory']/'scene.xml'),files=assets,physics_steps=0))
        links=''.join(f'<a href="{case["id"]}/{file}"><span>{title}</span><img src="{case["id"]}/{file}"></a>' for file,title in [('colour-layout.png','Exact colors; center is target reference'),('top.png','Actual initial top view'),('global.png','Actual initial oblique view')])
        cards.append(f'<article><h2>{case["arms"]} arms · L{case["level"]} · {case["rows"]}×{case["columns"]}</h2><div>{links}</div></article>')
    all_nine.save(output/'all-nine-colour-layouts.jpg',quality=95)
    before_after.save(output/'before-after-colours.jpg',quality=95)
    write(output/'preview-manifest.json',dict(scene_revision=14,physics_steps=0,cases=manifest))
    (output/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Mosaic R14 block colors</title><style>body{font:18px system-ui;color:#19384c;background:#f1f5f7;max-width:1800px;margin:30px auto;padding:0 20px}article{background:white;padding:22px;margin:20px 0}article div{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}img{width:100%}span{display:block;margin:10px 0}p{line-height:1.7}a{color:#205e89}</style><h1>Mosaic R14: revised supply colors for nine tasks</h1><p>Only initial block colors changed. Color totals, target, block positions/sizes, table, arms and physics stayed unchanged. Supply colors match across levels of the same scale. Center cells illustrate the target; top/oblique images show the actual initial state.</p><p>About seven tenths of the nearby supplies for each arm have same-arm geometric pickup/placement evidence for distinct target cells; the rest allow cross-zone coordination. The design allocation is not a fixed GPT route; GPT may find fewer handoffs. No revised Oracle or GPT trial was run.</p><p><a href="all-nine-colour-layouts.jpg">All nine layouts</a> · <a href="before-after-colours.jpg">Original/revised at three scales</a></p>'+''.join(cards),encoding='utf-8')
