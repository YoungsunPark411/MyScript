import maya.cmds as mc
import pymel.core as pm, Wcmd as wc

#일 대 다
tmp=pm.ls(sl=1)    
src=tmp[0]
tg=tmp[1:]

for x in tg:
    wc.Mcon( src, x,r=1,t=1,mo=1)
    pb=wc.PairBlend(x,r=1,t=1)
    x.pbw.set(0.5)
    
    
    
    scaleAttrs=['s','sx','sy','sz']
    [ src.attr(satr).inputs(p=1)[0] >> x.attr(satr) for satr in scaleAttrs if len( src.attr(satr).inputs() ) ]
#일 대 일
slls = pm.ls(sl=1)
hSelSz= int(len(slls)/2)

sc=slls[:hSelSz]
tg=slls[hSelSz:]

for x in range(len(tg)):
    wc.Mcon( sc[x], tg[x],r=1,t=1)
    pb=wc.PairBlend(tg[x],r=1,t=1)
    tg[x].pbw.set(0.5)
    
    scaleAttrs=['s','sx','sy','sz']
    [ src.attr(satr).inputs(p=1)[0] >> x.attr(satr) for satr in scaleAttrs if len( src.attr(satr).inputs() ) ]