# -*- coding: cp949 -*-
#양쪽 CV 수가 맞아야한다.
import pymel.core as pm
def MirrorCurve(source, target):
    sourceCV=pm.ls('%s.cv[*]'%source, fl=1)
    targetCV=pm.ls('%s.cv[*]'%target, fl=1)
    sourcePosX=[]
    sourcePosY=[]
    sourcePosZ=[]
    #trans=source.getTranslation(space="world")
    #pm.setAttr('%s.translateX'%target,((trans[0])*-1))
    #pm.setAttr('%s.translateY'%target,trans[1])
    #pm.setAttr('%s.translateZ'%target,trans[2])
    for ii in range(len(sourceCV)):
        sourcePos=pm.pointPosition( sourceCV[ii], w=1 )        
        sourcePosX.append(sourcePos[0])        
        sourcePosY.append(sourcePos[1])
        sourcePosZ.append(sourcePos[2])
    for i, cv in enumerate(targetCV):       
        pm.move(((sourcePosX[i])*-1),sourcePosY[i],sourcePosZ[i], cv)
   
sel=pm.ls(sl=1)
halfS=int(len(sel)/2)
sc=sel[0:halfS]
tg=sel[halfS:]

if sel:
    for n in range(len(sc)):
        MirrorCurve(sc[n], tg[n])