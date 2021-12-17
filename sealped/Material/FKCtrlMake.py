# -*- coding: cp949 -*-
import pymel.core as pm
import sys
sys.path.append(r'D:\MyScript\sealped')
from Material import General as gn
#reload(gn)

Scale = gn.scaleGet()
def FKCtrlMake(JntList,shape_,cns):

    if 'Left' in str(JntList[0]):
        MainColor = 13
    elif 'Right' in str(JntList[0]):
        MainColor = 6
    elif 'Neck' in str(JntList[0]):
        MainColor = 28
    elif 'Spine' in str(JntList[0]):
        MainColor = 15
    else:
        MainColor = 17
    ctlList=[]
    for x in JntList:
        FKCtrl = gn.ControlMaker('%sFKCtrl' % x.replace('Jnt','').replace('FK',''), shape_, MainColor, exGrp=0, size= Scale)
        gn.PosCopy(x, FKCtrl[0])
        ctlList.append(FKCtrl[0])
        gn.rotate_components(0, 0, 90, FKCtrl[0])

    for i in range(len(ctlList)):
        if i == 0: continue
        pm.parent(ctlList[i], ctlList[i - 1])
    #AllGrp=pm.createNode('transform',n='%sFKGrp'%JntList[0])
    #pm.parent(ctlList[0],AllGrp)
    if cns == 0:
        pass
    elif cns == 1:
        for i in range(len(ctlList)):
            gn.Mcon(ctlList[i],JntList[i],t=1, r=1, s=1, sh=1, mo=1, pvtCalc=1)
    for y in ctlList:
        gn.addNPO(y,'Grp')
    MotherFKCtrlGrp=pm.listRelatives(ctlList[0],p=1)[0]
    return MotherFKCtrlGrp

#FKCtrlMake(JntList,shape_,cns)
