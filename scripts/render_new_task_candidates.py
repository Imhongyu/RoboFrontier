"""Render concrete candidate task cards for a multi-arm tabletop benchmark."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/new-task-ideas-20261023/task-candidates.png'
W,H=1800,1650
BG='#F3F0E9'; CARD='#FFFCF6'; INK='#26343D'; MUTED='#65727A'; LINE='#CFC8BC'
BLUE='#3784BF'; RED='#D94E45'; GREEN='#37886F'; GOLD='#E5A53A'; PURPLE='#7962A1'
fp='/System/Library/Fonts/STHeiti Medium.ttc'
def f(n): return ImageFont.truetype(fp,n)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
def text(x,y,s,n=23,c=INK,a='la'): d.text((x,y),s,font=f(n),fill=c,anchor=a)
def card(x,y,w,h,num,title,tag,color,goal,actions,reason,arms,complexity):
    d.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=CARD,outline=LINE,width=2)
    d.rounded_rectangle((x+22,y+22,x+74,y+74),radius=14,fill=color)
    text(x+48,y+48,str(num),25,'white','mm')
    text(x+94,y+24,title,30,INK)
    text(x+w-24,y+38,tag,19,color,'ra')
    d.line((x+24,y+88,x+w-24,y+88),fill='#E4DED4',width=2)
    text(x+28,y+109,'Task',19,MUTED)
    # Wrap the quoted, concrete goal over two lines.
    goal_lines=goal.split('|')
    for i,line in enumerate(goal_lines): text(x+28,y+142+i*34,'“'+line+'”' if i==0 else ' '+line,22,INK)
    yy=y+142+len(goal_lines)*34+15
    text(x+28,yy,'Act.',18,MUTED); text(x+93,yy,actions,20,INK)
    text(x+28,yy+43,'Planning',18,MUTED); text(x+125,yy+43,reason,20,INK)
    text(x+28,yy+85,'Multi-arm',18,MUTED); text(x+125,yy+85,arms,20,INK)
    d.rounded_rectangle((x+w-180,y+h-43,x+w-24,y+h-12),radius=12,fill='#F0ECE5')
    text(x+w-102,y+h-27,'Sim cost: '+complexity,16,MUTED,'mm')

text(60,38,'Long-horizon task concepts beyond the existing four',47)
text(65,102,'Grasp, move, rotate and push; state dependencies create long-horizon planning. Concepts only.',24,MUTED)

cw,ch=810,415
card(55,155,cw,ch,1,'Load-bearing bridge','Structural stability',BLUE,
     'Span the gap with 6 supports and 2 deck panels.|A ball must roll across the bridge.',
     'Grasp · Place · Push',
     'Supports before deck; wrong order can block or collapse it.',
     'Build supports in parallel, then place and test the deck.','Med')
card(925,155,cw,ch,2,'Gear train','Causal configuration',PURPLE,
     'Select gears to connect input and output shafts.|One input turn must produce two opposite output turns.',
     'Grasp · Place · Rotate',
     'Tooth counts and intermediate gears set ratio/direction.',
     'Place gears in parallel; one arm turns the input to test.','Med-high')
card(55,600,cw,ch,3,'Balance weights','Quantity and physics',GREEN,
     'Use weights to hold the pointer in green for 2 seconds.|Then retrieve the key.',
     'Grasp · Place · Move',
     'Adjust weight and lever arm; observe before changing.',
     'Load both sides; other arms prepare or clear weights.','Med')
card(925,600,cw,ch,4,'Constrained packing','Space and order',GOLD,
     'Pack 8 different shapes and close the lid.|Every block must fit completely inside.',
     'Grasp · Rotate · Place · Push',
     'Order and orientation set free space and later access.',
     'Prepare in parallel; sequence placements at the opening.','Med')
card(55,1045,1680,415,5,'Domino chain','Propagation and concurrency',RED,
     'Arrange dominoes from the start to the bell.|Push the first; the chain must fall and ring the bell.',
     'Grasp · Rotate · Place · Push',
     'Spacing/orientation errors propagate; plan the route and check segment joins.',
     'Place separate segments concurrently, verify joins, then trigger the chain.','Med-high')

text(66,1500,'Bridge: support. Gears: causality. Balance: physical feedback. Packing: space. Dominoes: error propagation.',21,MUTED)
im.save(OUT);print(OUT)
