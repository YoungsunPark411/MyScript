# -*- coding: cp949 -*-
import pymel.core as pm
import sys
sys.path.append(r'E:\sealped')
from RIG import General as gn
#reload(gn)


def FKCtrlMake(JntList,shape_,cns):

    if 'Left' in str(JntList[0]):
        MainColor = 13
    elif 'Right' in str(JntList[0]):
        MainColor = 6
    else:
        MainColor = 17
    ctlList=[]
    for x in JntList:
        FKCtrl = gn.ControlMaker('%sFKCtrl' % x.replace('Jnt','').replace('FK',''), shape_, MainColor, exGrp=0, size= 3)
        gn.PosCopy(x, FKCtrl[0])
        ctlList.append(FKCtrl[0])

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

#FKCtrlMake(JntList,shape_,cns)
