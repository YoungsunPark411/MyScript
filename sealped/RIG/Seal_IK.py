# -*- coding: cp949 -*-
import pymel.core as pm
import sys
path = r'E:\sealped'
if not path in sys.path:
    sys.path.insert(0, path)
from RIG import General as gn
from RIG import Seal_IKStretchSet as st
#reload(gn)
#reload(st)
# 첫번째와 마지막 조인트 잡고 실행해주세요

# 크기 정하기
Scale = gn.scaleGet()

def IKCtrlMake(biJnt):
    Jnt_=biJnt
    CtrlList=[]
    for x in Jnt_:
        # 색 정하기
        if 'Left' in x:
            MainColor = 13
            SubColor = 31
        elif 'Right' in x:
            MainColor = 6
            SubColor = 29
        else:
            MainColor = 21
            SubColor = 17
        name_=x.replace('Jnt','').replace('BI','')
        

        if x == Jnt_[0]:
            IKCtrl = gn.ControlMaker(name_+'IKCtrl', 'circle', MainColor, exGrp=0, size=Scale)
            CtrlList.append(IKCtrl[0])
        elif x == Jnt_[-1]:
            IKCtrl = gn.ControlMaker(name_+'IKCtrl', 'circle', MainColor, exGrp=0, size=Scale)
            pm.select(IKCtrl[0])
            if 'Arm' in x:
                pm.addAttr(ln="Follow", at='enum', en='Clavicle:Root:Fly:World', k=1)
            else:
                pm.addAttr(ln="Follow", at='enum', en='RootSub:Root:Fly:World', k=1)
            CtrlList.append(IKCtrl[0])
        else:
            IKCtrl = gn.ControlMaker(name_+'IKCtrl', 'circle', SubColor, exGrp=0, size=Scale)
            pm.select(IKCtrl[0])
            pm.addAttr(ln="Pbw", at='double', min=0, max=1, dv=0, k=1)
            CtrlList.append(IKCtrl[0])
        gn.PosCopy(x,IKCtrl[0])
    return CtrlList

def BIIKJntMake(crv_,_count):
    biJnt=gn.spine_joint_make(crv_, crv_.replace('IKCrv',''), _count, 1, 'BI', ojVal='xzy', sawoVal='xdown')
    
    ctrl = IKCtrlMake(biJnt)
    
    biJntList=[]
    for x,y in zip(ctrl,biJnt):
        gn.PosCopy(x,y)
        pm.parent(y,x)
        new=pm.rename(y,x.replace('IKCtrl','BIJnt'))
        biJntList.append(new)
        gn.rotate_components(0, 0, 90, x)
    return [biJntList,ctrl]

def PBConnect(srcA,srcB,tg):
    srcA_ = gn.Mcon(srcA, tg, r=1, t=1, sh=1)
    find_ = tg.listConnections(d=0, s=1, p=1)[0].split('.')[0]
    dm = pm.PyNode(find_)
    gn.Mcon(srcB, tg, r=1, t=1)
    pb = gn.PairBlend(tg, r=1, t=1, sh=1)
    tg.pbw.set(0.5)

    dm.outputTranslateX >> pb.itx1
    dm.outputTranslateY >> pb.ity1
    dm.outputTranslateZ >> pb.itz1
    dm.outputRotateX >> pb.irx1
    dm.outputRotateY >> pb.iry1
    dm.outputRotateZ >> pb.irz1

    return pb

def PBRig(ctrl):
    wVale = 1.0 / (len(ctrl) - 1)
    PBGrpList=[]
    i = 0
    for x in ctrl[1:-1]:
        PBGrp_=gn.addNPO(x,'PBGrp')[0]
        PBGrpList.append(PBGrp_)
    if len(ctrl) == 5:       
        ValuList=[[0,-1,1],[0,2,0],[2,-1,-1]]
        for x in ValuList:
            vl=x
            pb=PBConnect(ctrl[vl[0]],ctrl[vl[1]],PBGrpList[vl[2]])
            ctrl_=PBGrpList[vl[2]].listRelatives(c=1)[0]
            ctrl_.Pbw.set(0.5)
            ctrl_.Pbw>>PBGrpList[vl[2]].pbw       
    else:
        for y in PBGrpList: 
            pb=PBConnect(ctrl[0],ctrl[-1],y)
            i = i + wVale        
            ctrl_=y.listRelatives(c=1)[0]
            ctrl_.Pbw.set(i)
            ctrl_.Pbw>>y.pbw

def connectStretchSquash(ctrl,name_,Jnt_):

    stMDL = pm.PyNode(name_.replace('1', '') + 'IKStretchMDL')
    sqMDL = pm.PyNode(name_.replace('1', '') + 'IKSquashMDL')
    for x,y in zip(Jnt_[1:],ctrl[1:]):
        sAttr_ = x.attr('sy')
        F_md=sAttr_.listConnections(d=0, s=1, t='multiplyDivide')[0]
        F_md.oy//x.sy
        F_md.oz//x.sz
        '''
        mm=pm.createNode('multMatrix',n=x.replace('Jnt','')+'MM')
        dm=pm.createNode('decomposeMatrix',n=x.replace('Jnt','')+'DM')
        y.worldMatrix>>mm.matrixIn[2]

        '''
        gn.Mcon(y,x,s=1,mo=1)
            
        sAttr_2 = x.attr('s')
        F_dm = sAttr_2.listConnections(d=0, s=1, t='decomposeMatrix')[0]
        
        F_dm.os//x.s
        F_dm.outputShear//x.shear
        

        #F_mm=x.listConnections(d=1, s=0, t='multMatrix')[0]
        #x.parentInverseMatrix//F_mm.matrixIn[3]


        F_dm.os>>F_md.input1
        F_md.oy>>x.sy
        F_md.oz>>x.sz
        


    pm.addAttr(ctrl[-1],ln="Stretch", at='double',  min=0, max=10, dv=0, k=1)
    pm.addAttr(ctrl[-1], ln="Squash", at='double',  min=0, max=10, dv=0, k=1)

    ctrl[-1].Stretch>>stMDL.input1
    ctrl[-1].Squash >> sqMDL.input1









def Spline(sel,BIjoint_count):
    crv_Jnt=st.IKStretch(sel)
    crv_=crv_Jnt[0]
    Jnt_=crv_Jnt[1]
    name_ = sel[0].split('IKJnt')[0]
    if BIjoint_count==None:
        count_=len(Jnt_)
    elif BIjoint_count>=1:
        count_=BIjoint_count
    JntnCtrl=BIIKJntMake( crv_, count_)
    BIIKJnt_ = JntnCtrl[0]
    pm.skinCluster(crv_, BIIKJnt_, sm=1, tsb=1, n='%sSkinCluster' % name_)
    grp_=pm.createNode('transform',n=sel[0].replace('Jnt','')+'CtrlGrp')
    ctrl=JntnCtrl[1]
    pm.parent(ctrl,grp_)
    for x in ctrl:
        gn.addNPO(x,'Grp')
    SPIKHandle = pm.ikHandle(sj=Jnt_[0], ee=Jnt_[-1], n=name_+'Handle', sol='ikSplineSolver', ccv=0, c=crv_)
    handle = SPIKHandle[0]
    handle.dTwistControlEnable.set(1)
    handle.dWorldUpType.set(4)
    ctrl[0].worldMatrix[0]>>handle.dWorldUpMatrix
    ctrl[-1].worldMatrix[0] >> handle.dWorldUpMatrixEnd
    if BIjoint_count==None:
        PBRig(ctrl)
    else:
        pass
    SysGrp_=pm.PyNode(Jnt_[0].replace('Jnt','SysGrp').replace('1',''))
    pm.parent(crv_,handle,SysGrp_)
    connectStretchSquash(ctrl, name_,Jnt_)
    

'''
sel = pm.ls(sl=1,r=1,fl=1)
tt=Spline(sel,BIjoint_count=None)
'''