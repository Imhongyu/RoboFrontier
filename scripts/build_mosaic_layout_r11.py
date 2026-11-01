"""Build nine R11 mosaic layout candidates and actual static MuJoCo images."""
import argparse
import json
from pathlib import Path

import mujoco
import numpy as np
from PIL import Image,ImageDraw,ImageFont

from robofrontier.suite import v2
from robofrontier.suite.mosaic_layout import build
from robofrontier.run_setup import write_json

OUT=v2.ROOT/'docs/generated/frontier-v2/mosaic-r11'


def main(replace_draft=False,revision=11):
    global OUT
    OUT=v2.ROOT/f'docs/generated/frontier-v2/mosaic-r{revision}'
    source_catalog='frontier-v2-r10.json' if revision==11 else 'frontier-mosaic-r11.json'
    catalog=json.loads((v2.ROOT/'configs/suites'/source_catalog).read_text())
    selected=[dict(c,scene_revision=revision,source_scene_revision=revision-1) for c in catalog['cases'] if c['family']=='mosaic']
    OUT.mkdir(parents=True,exist_ok=True);stocks={};summaries=[]
    for case in selected:
        case['directory']=str(v2.directory(case).relative_to(v2.ROOT))
        folder,m,d,positions=build(case,stocks.get(case['arms']),replace_draft);stocks[case['arms']]=positions
        old=mujoco.MjModel.from_xml_path(str(v2.directory(dict(case,scene_revision=revision-1))/'scene.xml'))
        for field in ['body_mass','body_inertia','geom_friction','jnt_range','actuator_gainprm','actuator_biasprm','actuator_forcerange']:
            if not np.array_equal(getattr(m,field),getattr(old,field)):raise ValueError('Unexpected physical parameter change: '+field)
        assert m.opt.timestep==old.opt.timestep
        m.vis.global_.offwidth=1920;m.vis.global_.offheight=1440
        target=OUT/case['id'];target.mkdir(exist_ok=True)
        with mujoco.Renderer(m,width=1920,height=1440,max_geom=max(5000,m.ngeom+1000)) as renderer:
            for view in ['top','global','global_rear']:
                renderer.update_scene(d,camera=view);im=Image.fromarray(renderer.render())
                im.save(target/(view+'.png'));im.save(folder/('preview-'+view+'.png'))
        env=json.loads((folder/'environment.json').read_text());summaries.append(dict(case=case['id'],directory=case['directory'],arms=case['arms'],level=case['level'],layout=env['mechanism']['layout_revision']))
        print('BUILT',case['id'],'relocated stock',env['mechanism']['layout_revision']['relocated_stock_count'],flush=True)
    write_json(v2.ROOT/f'configs/suites/frontier-mosaic-r{revision}.json',dict(schema_version=2,case_count=9,status='Layout candidates only; no Oracle or policy runs; default36-case catalog unchanged',cases=selected))
    write_json(OUT/'layout-summary.json',dict(physics_steps=0,source_revision_preserved=revision-1,physics_parameters_preserved=True,cases=summaries))
    font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',n)
    for view in ['top','global','global_rear']:
        sheet=Image.new('RGB',(3000,920),'#edf3f6');draw=ImageDraw.Draw(sheet)
        draw.text((30,18),f'Legacy Mosaic R{revision} · '+{'top':'Top layout','global':'Front oblique','global_rear':'Rear oblique'}[view],font=font(35),fill='#183245')
        for i,n in enumerate([4,6,8]):
            case=next(c for c in selected if c['arms']==n and c['level']==1)
            draw.text((i*1000+25,78),f'{n} arms · {case["rows"]}×{case["columns"]}',font=font(29),fill='#183245')
            with Image.open(OUT/case['id']/(view+'.png')) as im:im.thumbnail((980,770));sheet.paste(im,(i*1000+10,130))
        sheet.save(OUT/(view+'-overview.png'))
    cards=[]
    for c in selected:
        media=''.join(f'<a href="{c["id"]}/{v}.png"><span>{label}</span><img src="{c["id"]}/{v}.png"></a>' for v,label in [('top','Top'),('global','Front'),('global_rear','Rear')])
        cards.append(f'<article><h2>{c["arms"]} arms · L{c["level"]} · {c["rows"]}×{c["columns"]}</h2><div class="views">{media}</div></article>')
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Legacy Mosaic R11 layout</title><style>body{font:18px system-ui;background:#edf3f6;color:#183245;max-width:1800px;margin:30px auto;padding:0 24px}article{padding:20px;background:white;margin:24px 0;border-radius:12px}.views{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}img{width:100%}a{color:#17678c}span{display:block;padding:10px}</style><h1>Legacy Mosaic R11 · corner-facing layout</h1><p>R10 is retained. Four arms: both rows retreat 10cm, spread 10cm left/right and turn 30 degrees. Six arms: middle arms stay fixed; end arms spread 20cm and turn inward 45 degrees. Eight arms: end arms also spread 20cm and turn inward 45 degrees; middle spacing increases 10cm. Static construction/initial-contact checks only; no Oracle/GPT or all-goal reachability qualification.</p><p><a href="top-overview.png">Top overview</a> · <a href="global-overview.png">Front overview</a></p>'+''.join(cards))
    if revision==12:
        page=(OUT/'index.html').read_text().replace('R11','R12')
        first=page.index('<p>');last=page.index('</p>',first)
        page=page[:first]+'<p>Older versions are retained. At all three scales the four outer arms move 50mm toward the grid along their original headings. All headings and the middle arms in 6/8-arm layouts stay unchanged. Static construction/initial-contact checks only; no Oracle/GPT.</p>'+page[last+4:]
        (OUT/'index.html').write_text(page)
    print(OUT/'index.html',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replace-draft',action='store_true');p.add_argument('--revision',type=int,choices=[11,12],default=11);a=p.parse_args()
    main(a.replace_draft,a.revision)
