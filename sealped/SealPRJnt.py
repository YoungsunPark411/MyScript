# -*- coding: cp949 -*-
import pymel.core as pm
import sys
sys.path.append(r'E:\sealped')


from RIG import General as gn
reload(gn)


def PosCopy_Parent(par,cha):
    gn.PosCopy(par, cha)
    pm.parent(cha, par)


def PRJntMake(sel_):

    x=sel_[0]
    nn=x.replace('Jnt','')
    CenterJnt=pm.createNode('joint',n='%sPRJnt'%nn)
    PosCopy_Parent(x,CenterJnt)

    UpJnt=pm.createNode('joint',n='%sPRAJnt'%nn)
    PosCopy_Parent(CenterJnt,UpJnt)
    UpJnt.translateY.set(5)

    DnJnt = pm.createNode('joint', n='%sPRBJnt' % nn)
    PosCopy_Parent(CenterJnt, DnJnt)
    DnJnt.translateY.set(-5)

    LeftJnt = pm.createNode('joint', n='%sPRCJnt' % nn)
    PosCopy_Parent(CenterJnt, LeftJnt)
    LeftJnt.translateZ.set(5)

    RightJnt = pm.createNode('joint', n='%sPRDJnt' % nn)
    PosCopy_Parent(CenterJnt, RightJnt)
    RightJnt.translateZ.set(-5)

    PRJntList=[UpJnt,DnJnt,LeftJnt,RightJnt]
    for i in PRJntList:
        gn.addNPO(objs=i, GrpName='Grp')
        gn.addNPO(objs=i, GrpName='SetDriven')


def PoseReaderRig(sel_):  
    x=sel_[0]
    nn=x.replace('Jnt','')
    LocalPoseReaderLoc=pm.spaceLocator(n='%sLocalPoseReaderLoc'%nn)
    gn.PosCopy(x,LocalPoseReaderLoc)
    return LocalPoseReaderLoc

def localScaleModi(AxisLoc,size):
    list(map(lambda A:pm.setAttr(AxisLoc+'.localScale%s'%A,size), ['X','Y','Z']))

def Loc_to_LocalPoseReaderLoc(Loc,LocalPoseReaderLoc):
    DM=pm.createNode('decomposeMatrix',n=Loc+'DM')
    Loc.worldMatrix>>DM.inputMatrix
    AB=pm.createNode('angleBetween',n=Loc+'AB')
    DM.outputTranslate>>AB.vector2
    RV = pm.createNode('remapValue', n=Loc + 'RV')
    RV.inputMax.set(90)
    RV.outputMin.set(1)
    RV.outputMax.set(0)
    AB.angle>>RV.inputValue
    pm.addAttr(LocalPoseReaderLoc,ln='%sVec'%Loc.split('Axis')[0], at='double', dv=0, k=1)
    pm.connectAttr(RV+'.outValue',LocalPoseReaderLoc+'.%sVec'%Loc.split('Axis')[0])
    return AB

def findNodesTypeBelow(nodeType):
    pm.select(hi=1)
    sel=pm.ls(sl=1,type=nodeType)
    return sel

def AimVis_Dup(AimLoc):
    Grp1=gn.addNPO(objs=AimLoc, GrpName='OffGrp')
    Grp2=gn.addNPO(objs=AimLoc, GrpName='SpcGrp')
    dup_=pm.duplicate(Grp1[0])
    pm.select(dup_)
    List=findNodesTypeBelow('transform')
    n_list=[]
    for x in List:
        nn=pm.rename(x,x.replace('Aim','AimVisual').replace('1',''))
        n_list.append(nn)
    n_list[1].translateX.set(1)
    pm.select(Grp1)
    o_list=findNodesTypeBelow('transform')
    n_list[0].rotate>>o_list[0].rotate
    n_list[1].translate>>o_list[1].translate
    n_list[2].translate>>o_list[2].translate

    return n_list


def PoseReaderSet(sel_):
    x=sel_[0]
    nn=x.replace('Jnt','')
    WGrp_=pm.createNode('transform',n='%sWorldPoseReaderGrp'%nn)

    AimLoc = pm.spaceLocator(n='%sAimLoc' % nn)
    AimDM = pm.createNode('decomposeMatrix', n='%sAimDM' % nn)
    AimLoc.worldMatrix >> AimDM.inputMatrix
    
    av=AimVis_Dup(AimLoc)
    pm.parentConstraint(sel_,av[0])

    LocalPoseReaderLoc=PoseReaderRig(sel_)

    list=['X','Y','Z','RvsX','RvsY','RvsZ']
    for i in list:
        AxisLoc=pm.spaceLocator(n='%s%sAxisLoc'%(nn,i))
        localScaleModi(AxisLoc,0.1)

        pm.parent(AxisLoc,WGrp_)
        ax=i.replace('Rvs','')

        if 'Rvs' in i:
            mv=-1
        else:
            mv=1
        pm.setAttr(AxisLoc+'.translate%s'%(ax),mv)
        gn.addNPO(objs=AxisLoc, GrpName='Grp')

        AB_=Loc_to_LocalPoseReaderLoc(AxisLoc, LocalPoseReaderLoc)
        AimDM.outputTranslate>>AB_.vector1
        
    #organize
    PoseReaderGrp=pm.createNode('transform',n='%sPoseReaderGrp'%nn)
    AimGrp=AimLoc.getParent().getParent()
    pm.parent(AimGrp,LocalPoseReaderLoc)
    pm.parent(WGrp_,LocalPoseReaderLoc,PoseReaderGrp)
    gn.addNPO(objs=AxisLoc, GrpName='Grp')
    LocalPoseReaderLoc.rotate>>WGrp_.rotate
    
        
    








sel_=pm.ls(sl=1)
PRJntMake(sel_)
PoseReaderSet(sel_)

### 조인트에 서브 컨트롤 추가, 조인트랑 수치랑 셋드리븐 하기 



