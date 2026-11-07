# 用 PIL 畫 16-bit 風格房間底圖（靜態部分），輸出 img/room.png
from PIL import Image, ImageDraw
import random, re
random.seed(7)
T=32; W=16
MAP=re.findall(r'"([#.rWBDbdSCPGM]+)"', open('angu-house/index.html',encoding='utf-8').read().split('const MAP=[')[1].split('];')[0])
H=len(MAP)
im=Image.new('RGBA',(W*T,H*T),(0,0,0,255)); d=ImageDraw.Draw(im)
ov=Image.new('RGBA',(W*T,H*T),(0,0,0,0)); od=ImageDraw.Draw(ov)
def R(x,y,w,h,c): d.rectangle([x,y,x+w-1,y+h-1],fill=c)
def P(x,y,c): d.point((x,y),fill=c)
# 調色盤
WALL=(72,16,26); WALL2=(90,24,36); WALL3=(52,10,18); GREEN=(36,110,72); GREEN2=(58,150,98); GREEN3=(22,70,46); LEATHER=(32,78,56); PAPER=(236,226,200); GOLD=(201,162,39); GOLD2=(138,109,28); GOLD3=(240,210,122)
WOOD=(58,38,30); WOOD2=(74,50,38); WOOD3=(44,28,22); WOOD4=(90,62,46)
FL=(52,36,34); FL2=(62,44,40); FL3=(40,27,26); FL4=(70,50,45)
WINE=(107,15,26); WINE2=(130,28,40); WINE3=(74,10,18); CREAM=(232,224,208); CREAM2=(200,190,170)
INK=(14,10,12)

def floor(x,y):
    for i in range(2):
        yy=y+i*16
        R(x,yy,T,16,FL if (i+(y//T))%2==0 else FL2)
        d.line([x,yy,x+T-1,yy],fill=FL3); d.line([x,yy+1,x+T-1,yy+1],fill=FL4)
        off=((x//T)*11+(y//T+i)*17)%T
        d.line([x+off,yy+2,x+off,yy+15],fill=FL3)
        for k in range(4): P(x+(off+6+k*7)%T,yy+4+k*3,FL3)
def wall(x,y,top=False):
    R(x,y,T,T,WALL)
    # 錦緞花紋
    for (ox,oy) in [(8,6),(24,22)]:
        cx,cy=x+ox,y+oy
        for k in range(-4,5):
            P(cx+k,cy,WALL2); P(cx,cy+k,WALL2)
        for k in range(-2,3):
            P(cx+k,cy+k,WALL2); P(cx+k,cy-k,WALL2)
        P(cx,cy,GOLD2)
    if top: R(x,y,T,3,WALL3)
def dado(x,y):  # 牆底的踢腳板＋橫飾條
    R(x,y+T-8,T,8,WOOD3); R(x,y+T-8,T,1,GOLD2); R(x,y+T-7,T,1,WOOD4); R(x,y+T-2,T,2,INK)
def wall_bottom_edge(x,y):  # 下牆：木牆沿（看得到牆的厚度）
    R(x,y,T,T,INK)
    R(x,y,T,16,WOOD2); R(x,y,T,1,GOLD2); R(x,y+1,T,1,WOOD4)
    for k in range(3,16,4): d.line([x,y+k,x+T-1,y+k],fill=WOOD3)
    R(x,y+13,T,3,WOOD3); R(x,y+16,T,2,INK)
    # 木板接縫
    off=((x//T)*9)%T; d.line([x+off,y+2,x+off,y+12],fill=WOOD3)
def side_wall(x,y,left):
    R(x,y,T,T,INK)
    if left: R(x+T-12,y,12,T,WOOD2); R(x+T-12,y,1,T,GOLD2); R(x+T-11,y,1,T,WOOD4); R(x+T-3,y,3,T,WOOD3)
    else: R(x,y,12,T,WOOD2); R(x+11,y,1,T,GOLD2); R(x+10,y,1,T,WOOD4); R(x,y,3,T,WOOD3)
def rug(x,y,ex,ey):  # ex,ey: 是否在地毯邊緣（上下左右）
    R(x,y,T,T,WINE)
    # 細紋
    for i in range(0,T,4):
        for j in range(0,T,4):
            if (i+j)%8==0: P(x+i+1,y+j+1,WINE3)
    u,dn,l,r=ex
    if u: R(x,y,T,4,GOLD2); R(x,y+1,T,2,GOLD); R(x,y+4,T,1,WINE3)
    if dn: R(x,y+T-4,T,4,GOLD2); R(x,y+T-3,T,2,GOLD); R(x,y+T-5,T,1,WINE3)
    if l: R(x,y,4,T,GOLD2); R(x+1,y,2,T,GOLD)
    if r: R(x+T-4,y,4,T,GOLD2); R(x+T-3,y,2,T,GOLD)
    if not any(ex):  # 中央菱形
        for k in range(-5,6): P(x+16+k,y+16+abs(k)-5,GOLD2); P(x+16+k,y+16-abs(k)+5,GOLD2)
def shadow_below(x,y,h=4):  # 家具下方的接地陰影
    for i in range(h):
        od.line([x+1,y+T-1-i,x+T-2,y+T-1-i],fill=(0,0,0,int(90-i*20)))
def window(x,y,left):
    wall(x,y)
    fx=x+4 if left else x; fw=T-4
    # 亮窗格（外面有光）
    R(fx,y+4,fw,T-8,(246,236,206))
    R(fx,y+4,fw,2,(255,250,230))
    for k in range(3): R(fx+2+k*9,y+6,1,T-12,(228,214,180))
    # 拱頂
    if left: d.pieslice([fx,y-2,fx+fw*2-1,y+14],180,270,fill=(246,236,206))
    else: d.pieslice([fx-fw,y-2,fx+fw-1,y+14],270,360,fill=(246,236,206))
    # 窗櫺
    d.line([fx,y+4,fx+fw-1,y+4],fill=WOOD3); d.line([fx,y+15,fx+fw-1,y+15],fill=WOOD3)
    d.line([fx,y+4,fx,y+T-5],fill=WOOD3); d.line([fx+fw-1,y+4,fx+fw-1,y+T-5],fill=WOOD3)
    R(fx,y+T-5,fw,2,WOOD2); R(fx,y+T-3,fw,1,GOLD2)   # 窗台
    # 綠窗簾（拉到兩側，金色綁帶）
    cx=x if left else x+T-8
    R(cx,y,8,T-4,GREEN3); R(cx+1,y,3,T-4,GREEN); R(cx+5,y,1,T-4,GREEN2)
    R(cx,y+18,8,3,GOLD2); R(cx+1,y+19,6,1,GOLD)
    R(cx,y,8,2,GOLD2)   # 窗簾桿
    # 壁燈
    sx=x-6 if left else x+T+2
    if 0<=sx<W*T:
        R(sx,y+12,3,6,GOLD2); R(sx-1,y+9,5,3,GOLD); R(sx,y+6,3,3,(255,240,180)); P(sx+1,y+5,(255,200,120))
def bookshelf(x,y,top,bottom):
    R(x,y,T,T,WOOD3); R(x,y,2,T,WOOD2); R(x+T-2,y,2,T,WOOD2)
    if top: R(x,y,T,3,WOOD2); R(x,y,T,1,WOOD4)
    cols=[WINE,GOLD,(43,58,90),(74,107,58),CREAM,(90,40,100),WINE2,(60,60,70)]
    for row in (0,1):
        sy=y+4+row*14
        R(x+2,sy+10,T-4,2,WOOD2)   # 層板
        R(x+2,sy+12,T-4,1,INK)
        bx=x+3; i=(x//T+row*3)%8
        while bx<x+T-3:
            w=random.choice([3,4,4,5]); h=random.choice([8,9,10])
            c=cols[i%8]; i+=1
            R(bx,sy+10-h,w,h,c); R(bx,sy+10-h,1,h,tuple(max(0,v-40) for v in c)); P(bx+w//2,sy+10-h+2,GOLD3)
            bx+=w+ (1 if random.random()<.3 else 0)
    if bottom: R(x,y+T-3,T,3,WOOD3); shadow_below(x,y,2)
def desk(x,y,top,right=False):
    if top and right:  # 右半桌面：一疊卡稿、小蠟燭、羽毛筆
        R(x,y,T,T,WOOD2); R(x,y,T,2,WOOD4); R(x,y+2,T,1,GOLD2)
        R(x+2,y+5,T-4,T-7,LEATHER); R(x+2,y+5,T-4,1,(44,100,72)); R(x+T-3,y+6,1,T-9,(44,100,72))
        for k in range(3): R(x+5+k,y+18-k*2,12,10,PAPER); R(x+5+k,y+18-k*2,12,1,(200,190,165))
        R(x+8,y+16,6,1,(150,140,120)); R(x+8,y+18,8,1,(150,140,120))
        R(x+22,y+14,3,10,CREAM); R(x+21,y+24,5,2,GOLD2); P(x+23,y+13,GOLD3)
        d.line([x+19,y+10,x+26,y+4],fill=CREAM); d.line([x+20,y+10,x+27,y+5],fill=CREAM2); P(x+19,y+11,INK)
    elif top:  # 桌面：深木框＋綠皮墊、攤開的卡稿、墨水瓶、羽毛筆、一根小蠟燭
        R(x,y,T,T,WOOD2); R(x,y,T,2,WOOD4); R(x,y+2,T,1,GOLD2)
        R(x+2,y+5,T-4,T-7,LEATHER); R(x+2,y+5,T-4,1,(44,100,72)); R(x+3,y+6,1,T-9,(44,100,72))
        R(x+4,y+9,12,14,PAPER); R(x+5,y+10,10,1,(200,190,165))
        for k in range(4): R(x+6,y+12+k*2,8-(k%2)*3,1,(150,140,120))
        R(x+18,y+12,7,7,(20,20,28)); R(x+19,y+11,5,2,GOLD2); P(x+20,y+14,(60,60,80))
        d.line([x+24,y+8,x+28,y+2],fill=CREAM); d.line([x+25,y+8,x+29,y+3],fill=CREAM2); P(x+24,y+9,INK)
        R(x+26,y+20,3,8,CREAM); R(x+25,y+28,5,2,GOLD2); P(x+27,y+19,GOLD3)
    else:   # 桌前：抽屜
        R(x,y,T,T,WOOD2); R(x,y,T,1,GOLD2)
        for k in range(2):
            R(x+3,y+3+k*12,T-6,10,WOOD3); R(x+3,y+3+k*12,T-6,1,WOOD4); R(x+13,y+7+k*12,6,2,GOLD)
        R(x,y+T-4,T,4,WOOD3); R(x+2,y+T-4,4,4,INK); R(x+T-6,y+T-4,4,4,INK); shadow_below(x,y,3)
def bed(x,y,head):
    if head:
        R(x,y,T,T,WINE3)
        R(x,y,T,8,WOOD2); R(x,y,T,2,WOOD4); R(x+1,y+2,T-2,1,GOLD2); # 床頭板
        R(x+2,y+8,T-4,T-8,WINE); R(x+2,y+8,T-4,2,WINE2)
        R(x+6,y+11,20,9,CREAM); R(x+6,y+11,20,2,(245,240,228)); R(x+6,y+19,20,1,CREAM2) # 枕頭
        R(x+2,y+22,T-4,10,WINE2); R(x+2,y+22,T-4,1,GOLD2)
    else:
        R(x,y,T,T,WINE2); R(x+2,y,T-4,T-8,WINE2)
        for i in range(4): R(x+2,y+2+i*6,T-4,1,WINE3)  # 被子皺摺
        for i in range(3): R(x+4+i*9,y+9,6,1,WINE)
        R(x,y+T-8,T,8,WOOD2); R(x,y+T-8,T,1,GOLD2); R(x,y+T-2,T,2,WOOD3); shadow_below(x,y,2)
    R(x,y,1,T,WOOD3); R(x+T-1,y,1,T,WOOD3)
def trophy(x,y):
    wall(x,y)
    R(x+1,y+22,T-2,3,WOOD2); R(x+1,y+22,T-2,1,WOOD4); R(x+1,y+25,T-2,1,INK)
    # 兩座獎盃
    for ox in (4,18):
        R(x+ox+2,y+8,6,7,GOLD); R(x+ox+3,y+8,2,5,GOLD3); R(x+ox,y+9,2,4,GOLD2); R(x+ox+8,y+9,2,4,GOLD2)
        R(x+ox+4,y+15,2,3,GOLD2); R(x+ox+2,y+18,6,2,WOOD3); R(x+ox+2,y+20,6,2,GOLD2)
    R(x+14,y+16,4,5,CREAM); R(x+15,y+17,2,1,WINE)  # 小卡
def frame(x,y):
    wall(x,y)
    R(x+5,y+3,22,22,GOLD2); R(x+6,y+4,20,20,GOLD); R(x+7,y+5,18,18,(24,18,26))
    for k in range(0,20,2): P(x+6+k,y+4,GOLD3); P(x+6+k,y+23,GOLD3)
    # 自畫像：白髮、鹿角、黑裙
    R(x+12,y+9,8,6,(244,244,244)); R(x+11,y+7,2,3,GOLD); R(x+19,y+7,2,3,GOLD)
    R(x+13,y+15,6,3,(241,220,200)); P(x+14,y+15,(42,79,214)); P(x+17,y+15,(42,79,214))
    R(x+11,y+18,10,5,INK); R(x+11,y+18,10,1,GOLD2)
def portrait(x,y):  # 2x2 大肖像，x,y 為左上格
    S=64
    R(x+4,y+4,S-8,S-10,GOLD2); R(x+6,y+6,S-12,S-14,GOLD); R(x+9,y+9,S-18,S-20,(28,18,30))
    for k in range(6,S-6,3): P(x+k,y+6,GOLD3); P(x+k,y+S-9,GOLD3); P(x+6,y+k,GOLD3); P(x+S-7,y+k,GOLD3)
    for (cx,cy) in [(x+6,y+6),(x+S-7,y+6),(x+6,y+S-9),(x+S-7,y+S-9)]: R(cx-1,cy-1,3,3,GOLD3)
    # 背景暗紅簾
    R(x+9,y+9,S-18,S-20,(52,14,24)); 
    for k in range(0,S-18,6): d.line([x+9+k,y+9,x+9+k,y+S-12],fill=(62,18,30))
    # 人物：白短髮、鹿角、黑羽耳翼、藍眼、黑金裙
    hx,hy=x+22,y+16
    R(hx,hy+2,20,14,(244,244,244)); R(hx-1,hy+6,2,8,(244,244,244)); R(hx+20,hy+6,2,8,(244,244,244))
    R(hx-2,hy+12,3,2,(230,230,230)); R(hx+20,hy+12,3,2,(230,230,230))
    for (ax,dx) in [(hx+2,-1),(hx+16,1)]:
        R(ax,hy-6,2,8,GOLD2); R(ax+dx*2,hy-8,2,4,GOLD2); R(ax-dx*1,hy-3,2,2,GOLD2); P(ax,hy-7,GOLD3)
    R(hx-4,hy+7,3,5,INK); R(hx+21,hy+7,3,5,INK); P(hx-4,hy+6,(40,40,50)); P(hx+23,hy+6,(40,40,50))
    R(hx+3,hy+12,14,9,(241,220,200)); R(hx+5,hy+14,3,3,(38,70,200)); R(hx+12,hy+14,3,3,(38,70,200)); P(hx+5,hy+14,(120,160,255)); P(hx+12,hy+14,(120,160,255))
    R(hx+8,hy+19,4,1,(60,90,200))
    R(hx+2,hy+21,16,4,INK); R(hx+2,hy+21,16,1,GOLD2)        # 領
    R(hx-2,hy+25,24,14,INK); R(hx-2,hy+25,24,1,GOLD2); R(hx+8,hy+27,4,3,GOLD); R(hx+6,hy+30,8,1,GOLD2)
    R(hx-4,hy+33,28,8,INK); R(hx-4,hy+40,28,1,GOLD)
    R(hx+6,hy+26,1,12,GOLD2); R(hx+13,hy+26,1,12,GOLD2)
    # 簽名
    R(x+S-20,y+S-14,9,1,GOLD2); R(x+S-18,y+S-16,5,1,GOLD2)
def candle(x,y):
    floor(x,y)
    R(x+11,y+26,10,3,GOLD2); R(x+12,y+25,8,1,GOLD); R(x+14,y+14,4,12,GOLD2); R(x+15,y+14,1,12,GOLD3)
    R(x+13,y+12,6,3,GOLD); R(x+14,y+5,4,8,CREAM); R(x+14,y+5,1,8,CREAM2)
def mat(x,y):
    floor(x,y)
    R(x+2,y+6,T-4,20,WINE3); R(x+3,y+7,T-6,18,WINE); R(x+5,y+9,T-10,14,WINE2)
    for i in range(0,T-4,3): P(x+2+i,y+6,GOLD2); P(x+2+i,y+25,GOLD2)
def gramo_floor(x,y): floor(x,y)  # 唱機本體由 JS 畫（會動）

# ---- 畫格子 ----
for yy,row in enumerate(MAP):
    for xx,t in enumerate(row):
        x,y=xx*T,yy*T
        if t=='#':
            if yy==0: wall(x,y,top=True)
            elif yy==1: wall(x,y); dado(x,y)
            elif yy==H-1: wall_bottom_edge(x,y)
            elif xx==0: side_wall(x,y,True)
            else: side_wall(x,y,False)
        elif t=='.': floor(x,y)
        elif t=='r':
            u=MAP[yy-1][xx]!='r'; dn=MAP[yy+1][xx]!='r'; l=row[xx-1]!='r'; r_=row[xx+1]!='r'
            rug(x,y,(u,dn,l,r_),None)
        elif t=='W': window(x,y,left=row[xx-1]!='W')
        elif t=='B': bookshelf(x,y,top=MAP[yy-1][xx]!='B',bottom=MAP[yy+1][xx]!='B')
        elif t=='D': desk(x,y,top=MAP[yy-1][xx]!='D',right=row[xx-1]=='D')
        elif t=='b': bed(x,y,True)
        elif t=='d': bed(x,y,False)
        elif t=='S': trophy(x,y)
        elif t=='C': candle(x,y)
        elif t=='P': wall(x,y,top=(yy==0))
        elif t=='G': mat(x,y)
        elif t=='M': gramo_floor(x,y)
# 第 1 列牆面的物件格也要踢腳板
for xx,t in enumerate(MAP[1]):
    if t in 'WSP': dado(xx*T,1*T)
# 大肖像（找 2x2 的左上角）
for yy,row in enumerate(MAP):
    for xx,t in enumerate(row):
        if t=='P' and (yy==0 or MAP[yy-1][xx]!='P') and (xx==0 or row[xx-1]!='P'): portrait(xx*T,yy*T)
# 地板與牆交界的陰影
for xx in range(W):
    if MAP[2][xx] in '.r': 
        for i in range(5): od.line([xx*T,2*T+i,xx*T+T-1,2*T+i],fill=(0,0,0,110-i*20))
im=Image.alpha_composite(im,ov); im.save('angu-house/img/room.png'); print('saved', im.size)
