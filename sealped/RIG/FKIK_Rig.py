# -*- coding: cp949 -*-
import pymel.core as pm
import sys
path = r'E:\sealped'
if not path in sys.path:
    sys.path.insert(0, path)
from RIG import General as gn

from RIG import IKFKBlend as kb
from SealBasicJnt import JntAxesChange
from RIG import Seal_IK as si
from FKCtrlMake import FKCtrlMake

reload(gn)
#print (sys.path)
#sys.path.remove(sys.path[0])
def type_JntMake(orgJnt,type):
    guideCrv=gn.CrvFromJnt(orgJnt)
    
    type_Jnt = gn.JntMake(guideCrv, len(orgJnt), type)
    pm.delete(guideCrv)
    n_type_Jnt=[]
    for x,y in zip(orgJnt,type_Jnt):

        nj=pm.rename(y,x.replace('Jnt',type+'Jnt'))
        n_type_Jnt.append(nj)

    JntAxesChange('xzy', 'ydown', n_type_Jnt)
    return n_type_Jnt

def IKFK_JntRig_Make(orgJnt):
    IKJnt=type_JntMake(orgJnt,'IK')
    FKJnt=type_JntMake(orgJnt,'FK')
    DrvJnt = type_JntMake(orgJnt, 'Drv')
    #IKRig
    print('ok')
    si.Spline(IKJnt, BIjoint_count=None)
    #FKRig

    if  'Neck' in orgJnt[-1]:
        shape_='square'
        obj='Neck'
    elif 'Spine' in orgJnt[-1]:
        shape_='square'
        obj='Spine'
    elif 'Arm' in orgJnt[-1]:
        shape_='pin'
        obj='Arm'
    elif 'Finger' in orgJnt[-1]:
        shape_='circle'
    else:
        shape_='pin'
    FKCtrlMake(FKJnt,shape_,cns=1)
    print(obj)
    switch=pm.PyNode(obj+'IKFKCtrl')
    Jnt_sel = [IKJnt,FKJnt,DrvJnt,switch]
    kb.IKFKBlend(Jnt_sel)





orgJnt=pm.ls(sl=1)
IKFK_JntRig_Make(orgJnt)



