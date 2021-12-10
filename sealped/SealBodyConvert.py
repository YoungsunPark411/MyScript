# -*- coding: cp949 -*-
import pymel.core as pm
import sys
try:
    from imp import *
except:
    pass
sys.path.append(r'E:\sealped')
from RIG import General as gn
#from RIG import ArmLegShare as al
reload(gn)
#reload(al)

def get_transform(Jnt):
    _name = Jnt.name()
    trans = pm.xform(_name, q=1, ws=1, rp=1 )
  
    return trans
    

def MakeCrv(Jnt):
    point=[]
    for x in Jnt:
        trans=get_transform(x)
        point.append(trans)

    AllCurve=pm.curve( p=point, k=(list(range(len(point)))),d=1)
    return AllCurve


def SealBodyRig(Jnt=sel):
    # 이름 뽑기
    AllCurve = MakeCrv(Jnt)
    side = gn.NameExtraction(AllCurve)[0]
    ob = gn.NameExtraction(AllCurve)[1]
    subob = gn.NameExtraction(AllCurve)[2]
    
  
    # 그룹만들기
    GrpList = gn.GrpMake()
    RigGrp = GrpList[0]
    CtrlGrp = GrpList[1]
    RigSysGrp = GrpList[2]
    EtcGrp = GrpList[3]
    
    def JntAxesChange(Axes,SAO,JntList):
        for x in JntList:
            pm.select(x)
            pm.joint(e=1  ,oj =Axes ,secondaryAxisOrient= SAO,ch =1 ,zso=1)
        pm.setAttr ("%s.jointOrientX"%JntList[-1], 0)
        pm.setAttr ("%s.jointOrientY"%JntList[-1], 0)
        pm.setAttr ("%s.jointOrientZ"%JntList[-1], 0)

    # 조인트만들기


    def ShortJntMake(AllCurve, Type='Drv'):
        Jnt = gn.JntMake(AllCurve, len(sel), Type)
        Nlist = gn.jntList(Jnt[0], len(sel))

        gn.PosCopy(Nlist[0], RigSysGrp)
        pm.parent(Nlist[0], RigSysGrp)
        return Nlist
        
    orgJnt = sel

    DrvJnt = ShortJntMake(AllCurve, 'Drv')

    IKJnt = ShortJntMake(AllCurve, 'IK')
    FKJnt = ShortJntMake(AllCurve, 'FK')
    JntAxesChange('xzy','ydown',DrvJnt)
    JntAxesChange('xzy','ydown',IKJnt)
    JntAxesChange('xzy','ydown',FKJnt)
    
    # 색 정하기
    if 'Left' in side:
        MainColor = 13
        SubColor = 31
        fingerMainColor = 20
    elif 'Right' in side:
        MainColor = 6
        SubColor = 29
        fingerMainColor = 18
    else:
        MainColor = 13
        SubColor = 31
        fingerMainColor = 20
        

    # 크기 정하기
    Scale = gn.scaleGet()

    # IK 리깅 만들기
    def IKCtrlMake():
        IKCtrl = gn.ControlMaker('side_ob_IKCtrl', 'circle', MainColor, exGrp=0, size=Scale)
       
        pm.select(IKCtrl[0])
        pm.addAttr(ln="Twist", at='double', dv=0, k=1)
        pm.addAttr(ln="Stretch", at='double', min=0, max=10, dv=0, k=1)
        pm.addAttr(ln="Squash", at='double', min=0, max=10, dv=0, k=1)

        pm.addAttr(ln="ConstCtrlVis", at='double', min=0, max=1, dv=0, k=1)
        pm.setAttr(IKCtrl[0] + '.ConstCtrlVis', keyable=0, channelBox=1)
        IKConstCtrl = gn.ControlMaker('side_ob_IKConstCtrl', 'hexagon', MainColor, exGrp=0, size=Scale * 1.2)
        IKSubCtrl = gn.ControlMaker('side_ob_IKSubCtrl', 'circle', SubColor, exGrp=0, size=Scale * 0.8)
        gn.rotate_components(0, 0, 90, nodes=IKCtrl[0])
        gn.rotate_components(0, 0, 90, nodes=IKConstCtrl[0])
        gn.rotate_components(0, 0, 90, nodes=IKSubCtrl[0])
        

    def IKCtrlMatch():
        IKCtrl = pm.PyNode('side_ob_IKCtrl')
        IKConstCtrl = pm.PyNode('side_ob_IKConstCtrl')
        IKSubCtrl= pm.PyNode('side_ob_IKSubCtrl')
        pm.parent(IKCtrl, IKConstCtrl)
        pm.parent(IKSubCtrl, IKCtrl)
        gn.PosCopy(orgJnt[-1], IKConstCtrl)
        gn.addNPO(IKConstCtrl, 'Grp')
        gn.addNPO(IKCtrl, 'Grp')
        gn.addNPO(IKSubCtrl, 'Grp')
        RX = IKConstCtrl.rotateX.get()
        IKConstCtrl.rotateX.set(RX - 180)


    def IKRig():
        ctrl = IKCtrlMake()
        ctrlmatch = IKCtrlMatch()
        ikh, _effector, _curve = pm.ikHandle(sj=IKJnt[0], ee=IKJnt[-1], n='side_ob_IKHandle', sol='ikSplineSolver', ccv=1)
        pm.parent(ikh, RigSysGrp)
        pm.rename(_curve,'side_ob_IKCurve')
        IKPos = pm.createNode('transform', n='side_ob_IKPos')
        pm.parent(IKPos, 'side_ob_IKCtrl')
        list = pm.ls('side_ob_IKSubCtrl', ikh)
        gn.Mcon(list[0], list[1], t=1, mo=0, pvtCalc=1)


        
    # FK 리깅 만들기
    def FKCtrlMake():
        list=[]
        for x in FKJnt:
            FKCtrl = gn.ControlMaker(x.replace('Jnt','Ctrl'), 'diamond', MainColor, exGrp=0, size=Scale * 1.2)
            list.append(FKCtrl[0])
        return list


    def FKCtrlMatch():
        FKCtrlList = FKCtrlMake()
        for x,y in zip(FKJnt,FKCtrlList):
            tt=pm.PyNode(y)
            ta=pm.PyNode(x)
            gn.rotate_components(0, 0, 90, nodes=tt)
            gn.PosCopy(ta,tt)
            gn.Mcon(tt,ta,t=1, r=1, sh=1, mo=1, pvtCalc=1)
        for i in xrange(len(FKJnt)):
            if i==0: continue
            pm.parent( FKCtrlList[i], FKCtrlList[i-1] )
        for i in FKCtrlList:
            tt=pm.PyNode(i)
            gn.addNPO(tt, 'Grp')

    def FKRig():
        #ctrl = FKCtrlMake()
        ctrlmatch = FKCtrlMatch()
    
    xyzList=['x','y','z']
    trsList = ['t', 'r', 's']
    
    #Drv 리깅 만들기
    def IKFKCtrlMake():
        IKFKCtrl = gn.ControlMaker('side_ob_IKFKCtrl', 'switch', MainColor, exGrp=1, size=Scale)
        for i,j in zip(xyzList,trsList):
            pm.setAttr(IKFKCtrl[0]+'.'+j+i, lock=1, k=0, channelBox=0)
        pm.select(IKFKCtrl[0])
        pm.addAttr(ln="IKFK", at='double', min=0, max=1, dv=0, k=1)
        pm.addAttr(ln="Arc", at='double', min=0, max=10, dv=0, k=1)
        pm.addAttr(ln="UpTwistFix", at='double', dv=0, k=1)
        pm.addAttr(ln="DnTwistFix", at='double', dv=0, k=1)
        pm.addAttr(ln="AutoHideIKFK", at='enum', en='Off:On', k=1)
        pm.addAttr(ln="ArcCtrlVis", at='enum', en='Off:On', k=1)
        pm.setAttr(IKFKCtrl[0]+'.AutoHideIKFK', keyable=0, channelBox=1)
        pm.setAttr(IKFKCtrl[0]+'.ArcCtrlVis', keyable=0, channelBox=1)
        tt=pm.PyNode(orgJnt[-1])
        gg=pm.PyNode(IKFKCtrl[1])
        gn.PosCopy(tt,gg)
        gn.Mcon(tt,gg,t=1, r=0, s=0, sh=1, mo=1, pvtCalc=1)
        gn.rotate_components(-90, 0, 0, nodes=IKFKCtrl[0])
        gn.translate_components(0, -2 * Scale, 0, nodes=IKFKCtrl[0])
   

    def DrvJntBlend(IK, FK, Drv, ikfkCtrl):
        tBC = pm.createNode('blendColors', n='%sTrsBC' % Drv)
        pm.connectAttr(IK + '.translate', tBC + '.color2')
        pm.connectAttr(FK + '.translate', tBC + '.color1')
        pm.connectAttr(tBC + '.output', Drv + '.translate')
        pm.connectAttr(ikfkCtrl + '.IKFK', tBC + '.blender')

        pb = pm.createNode('pairBlend', n='%sRotPB' % Drv)
        pm.setAttr(pb + '.rotInterpolation', 1)
        list(map(lambda a: pm.connectAttr(IK + '.rotate%s' % a, pb + '.inRotate%s1' % a), ['X', 'Y', 'Z']))
        list(map(lambda a: pm.connectAttr(FK + '.rotate%s' % a, pb + '.inRotate%s2' % a), ['X', 'Y', 'Z']))
        list(map(lambda a: pm.connectAttr(pb + '.outRotate%s' % a, Drv + '.rotate%s' % a), ['X', 'Y', 'Z']))
        pm.connectAttr(ikfkCtrl + '.IKFK', pb + '.weight')

    def IKFKVisSet():
        IKFKRVS=pm.createNode('reverse',n='side_ob_IKFKRVS')
        IKFKCDT = pm.createNode('condition', n='side_ob_IKFKCDT')
        IKFKCtrl=pm.PyNode('side_ob_IKFKCtrl')
        #IKCtrlGrp = pm.PyNode('side_ob_IKConstCtrlGrp')
        #IKFK1CtrlGrp = pm.PyNode('side_subob1_FKCtrlGrp')
        #PolevectorShape=pm.PyNode('side_ob_PoleVectorCtrlShape')
        IKFKCtrl.IKFK>>IKFKRVS.input.inputX
        IKFKRVS.output.outputX>>IKFKCDT.colorIfTrue.colorIfTrueR
        IKFKCtrl.IKFK >> IKFKCDT.colorIfTrue.colorIfTrueG
        IKFKCtrl.AutoHideIKFK >> IKFKCDT.firstTerm
        IKFKCDT.secondTerm.set(1)
        #IKFKCDT.outColor.outColorR>>IKCtrlGrp.visibility
        #IKFKCDT.outColor.outColorR >> PolevectorShape.visibility
        #IKFKCDT.outColor.outColorG >> IKFK1CtrlGrp.visibility
        IKFKCtrl.AutoHideIKFK.set(1)

    def DrvRig():
        IKFKCtrl=IKFKCtrlMake()
  
        for x in range(len(DrvJnt)):
            DrvJntBlend(IKJnt[x],FKJnt[x],DrvJnt[x], 'side_ob_IKFKCtrl')
        IKFKVisSet()
    



    #Bind 리깅
    def BindRig():
        for (i,j) in zip(DrvJnt,orgJnt):
            gn.Mcon(i,j,t=1, r=1, sh=1, mo=1, pvtCalc=1)

    #RootCtrl 만들기
    def RootCtrlMake():

        if 'Arm' in ob:
            result=pm.createNode('transform',n='side_ob_RootGrp')
            gn.PosCopy(orgJnt[0], result)
            pm.parent(result, CtrlGrp)
            
        else:
            RootCtrl = gn.ControlMaker('side_ob_RootCtrl', 'crosspin', MainColor, exGrp=0, size=Scale)
            RootCtrl[0].sx.set(lock=1, k=0, channelBox=0)
            RootCtrl[0].sy.set(lock=1, k=0, channelBox=0)
            RootCtrl[0].sz.set(lock=1, k=0, channelBox=0)
            gn.PosCopy(orgJnt[0], RootCtrl[0])
            pm.parent(RootCtrl[0], CtrlGrp)
            gn.addNPO(RootCtrl[0], 'Grp')
            result=RootCtrl[0]
        return result

    #스트레치 리깅
    #스트레치저장값만들기 (원래전체길이,원래Up길이,원래Dn길이)

    def Divide(numerator, denominator): 
        nm=str(numerator)
        if 'All' in nm:
            name='All'        
        elif 'Up' in nm:
            name='Up'
        elif 'Dn' in nm:
            name='Dn'
        elif 'PV' in nm:
            name='PV'
    
        RatioMD = pm.createNode('multiplyDivide', n='side_ob_%sRatioMD'%name)
        RatioMD.operation.set(2)
        numerator.distance >> RatioMD.input1X
        attr_='%sLength'%name
        denominator.attr(attr_) >> RatioMD.input2X
        
        return RatioMD

    def Stretch(AllCurve):
        nm = len(orgJnt)

        div = 0
        PointList = []
        for i in range(nm):

            rate = float(1) / float(nm-1)
            div = rate*i
            PointList.append(div)
        print(PointList)
        count=nm

        PCList = []
        for i in range(0, count):
            tBC = pm.createNode('pointOnCurveInfo', n='%s%sPC' % (AllCurve, i + 1))
            tBC.turnOnPercentage.set(1)
            PCList.append(tBC)
            sh_=AllCurve.getShape()
            pm.connectAttr(sh_ + '.worldSpace[0]', tBC + '.ic')
           
            pm.setAttr(tBC + '.parameter', PointList[i])

        DB_List = []
        for i in range(0, count - 1):
            makeDB = pm.createNode('distanceBetween', n='%s%sDB' % (AllCurve, i + 1))
            DB_List.append(makeDB)
            pm.connectAttr(PCList[i] + '.result.position', DB_List[i] + '.point1')
            pm.connectAttr(PCList[i + 1] + '.result.position', DB_List[i] + '.point2')

        STRaitoMD_List = []
        for i in range(0, count - 1):
            makeSTRaitoMD = pm.createNode('multiplyDivide', n='%s%sSTRaitoMD' % (AllCurve, i + 1))
            STRaitoMD_List.append(makeSTRaitoMD)
            pm.connectAttr(DB_List[i] + '.distance', STRaitoMD_List[i] + '.input1X')
            #pm.connectAttr('ScaleChkGrp.scaleY', STRaitoMD_List[i] + '.input2X')

            pm.setAttr(STRaitoMD_List[i] + '.operation', 2)

        STdivMD_List = []
        for i in range(0, count - 1):
            makeSTdivMD = pm.createNode('multiplyDivide', n='%s%sSTdivMD' % (AllCurve, i + 1))
            STdivMD_List.append(makeSTdivMD)
            pm.connectAttr(STRaitoMD_List[i] + '.outputX', STdivMD_List[i] + '.input1X')

            originLength = pm.getAttr(DB_List[i] + '.distance')
            pm.setAttr(STdivMD_List[i] + '.input2.input2X', originLength)

            pm.setAttr(STdivMD_List[i] + '.operation', 2)

        STmulMD_List = []
        for i in range(0, count - 1):
            makeSTmulMD = pm.createNode('multiplyDivide', n='%s%sSTmulMD' % (AllCurve, i + 1))
            STmulMD_List.append(makeSTmulMD)
            pm.connectAttr(STdivMD_List[i] + '.outputX', STmulMD_List[i] + '.input1X')

            originLength = pm.getAttr(DB_List[i] + '.distance')
            pm.setAttr(STmulMD_List[i] + '.input2.input2X', originLength)

            pm.setAttr(STmulMD_List[i] + '.operation', 1)

        STBA_List = []
        for i in range(0, count - 1):
            STML = pm.createNode('multDoubleLinear', n='%s%sSTML' % (AllCurve, i + 1))
            pm.connectAttr('side_ob_IKCtrl' + '.Stretch', STML + '.input1')
            pm.setAttr(STML + '.input2', 0.1)
            makeSTBA = pm.createNode('blendTwoAttr', n='%s%sSTBA' % (AllCurve, i + 1))
            STBA_List.append(makeSTBA)
            pm.connectAttr(STML + '.output', STBA_List[i] + '.attributesBlender')
            pm.connectAttr(STmulMD_List[i] + '.output.outputX', STBA_List[i] + '.input[1]')

            pm.setAttr(STBA_List[i] + '.input[0]', originLength)

        for i in range(0, count - 1):
            pm.connectAttr(STBA_List[i] + '.output', IKJnt[i] + '.translateX')
        '''
        #
        SQRaitoMD_List = []
        for i in range(0, count - 1):
            makeSQRaitoMD = pm.createNode('multiplyDivide', n='%s%sSQRaitoMD' % (AllCurve, i + 1))
            SQRaitoMD_List.append(makeSQRaitoMD)
            pm.connectAttr(DB_List[i] + '.distance', SQRaitoMD_List[i] + '.input1X')

            pm.setAttr(SQRaitoMD_List[i] + '.operation', 2)
            TransX = pm.getAttr('%s.translateX' % IKJnt[i])
            pm.setAttr(SQRaitoMD_List[i] + '.input2.input2X', TransX)

        SQBA_List = []
        for i in range(0, count - 1):
            SQML = pm.createNode('multDoubleLinear', n='%s%sSQML' % (AllCurve, i + 1))
            pm.connectAttr('side_ob_IKCtrl' + '.Squash', SQML + '.input1')
            pm.setAttr(SQML + '.input2', 0.1)
            makeSQBA = pm.createNode('blendTwoAttr', n='%s%sSQBA' % (AllCurve, i + 1))
            SQBA_List.append(makeSQBA)
            pm.connectAttr(SQML + '.output', SQBA_List[i] + '.attributesBlender')
            pm.connectAttr(SQRaitoMD_List[i] + '.output.outputX', SQBA_List[i] + '.input[1]')
            pm.setAttr(SQBA_List[i] + '.input[0]', 1)

        SQPowerMD_List = []
        for i in range(0, count - 1):
            makeSQPowerMD = pm.createNode('multiplyDivide', n='%s%sSQPowerMD' % (AllCurve, i + 1))
            SQPowerMD_List.append(makeSQPowerMD)
            pm.connectAttr(SQBA_List[i] + '.output', SQPowerMD_List[i] + '.input1X')
            pm.setAttr(SQPowerMD_List[i] + '.operation', 3)
            pm.setAttr(SQPowerMD_List[i] + '.input2X', 0.5)

        SQDivMD_List = []
        for i in range(0, count - 1):
            makeSQDivMD = pm.createNode('multiplyDivide', n='%s%sSQDivMD' % (AllCurve, i + 1))
            SQDivMD_List.append(makeSQDivMD)
            pm.connectAttr(SQPowerMD_List[i] + '.outputX', SQDivMD_List[i] + '.input2X')
            pm.setAttr(SQDivMD_List[i] + '.operation', 2)
            pm.setAttr(SQDivMD_List[i] + '.input1X', 1)

        ScaleZAL_List = []
        ScaleYAL_List = []
        for i in range(0, count - 1):
            makeScaleZAL = pm.createNode('addDoubleLinear', n='%s%sScaleZAL' % (AllCurve, i + 1))
            ScaleZAL_List.append(makeScaleZAL)
            makeScaleZAL = pm.createNode('addDoubleLinear', n='%s%sScaleYAL' % (AllCurve, i + 1))
            ScaleYAL_List.append(makeScaleZAL)
            pm.connectAttr(SQDivMD_List[i] + '.output.outputX', ScaleZAL_List[i] + '.input1')
            pm.connectAttr(SQDivMD_List[i] + '.output.outputX', ScaleYAL_List[i] + '.input1')
        
        for i in range(0, count - 1):
            pm.connectAttr(ScaleYAL_List[i] + '.output', IKJnt[i] + '.SquashYValue')
            pm.connectAttr(ScaleZAL_List[i] + '.output', IKJnt[i] + '.SquashZValue')
      
        SplineRIgjnt_List = ['PelvisRigJnt', 'Spine1RigJnt', 'Spine2RigJnt', 'Spine3RigJnt', 'ChestRigJnt']

        for i in range(0, count - 1):
            pm.connectAttr(IKJnt[i] + '.SquashYValue', SplineRIgjnt_List[i] + '.scale.scaleY')
            pm.connectAttr(IKJnt[i] + '.SquashZValue', SplineRIgjnt_List[i] + '.scale.scaleZ')

        SplineRIgjnt_List = ['PelvisRigJnt', 'Spine1RigJnt', 'Spine2RigJnt', 'Spine3RigJnt', 'ChestRigJnt']
        Bindjnt_List = ['RootJnt', 'Spine1Jnt', 'Spine2Jnt', 'Spine3Jnt', 'ChestJnt']

        for i in range(0, count - 1):
            pm.connectAttr(SplineRIgjnt_List[i] + '.scaleY', Bindjnt_List[i] + '.scaleY')
            pm.connectAttr(SplineRIgjnt_List[i] + '.scaleZ', Bindjnt_List[i] + '.scaleZ')
        '''

    def StretchPractice():
        
        #UpDB=pm.PyNode('side_ob_ArcUpDB')
        #DnDB=pm.PyNode('side_ob_ArcDnDB')
        IKCtrl=pm.PyNode('side_ob_IKCtrl')
        Stretch(AllCurve)

    def TwistUpEnd():
        #TwistUpPos1 만들기
        TwistUpPos1=pm.createNode('transform',n='side_ob_%sTwistUpPos'%subob[0])
        IKFKCtrl=pm.PyNode('side_ob_IKFKCtrl')
        if side == 'Left':
            TwistUpPosMDL=pm.createNode('multDoubleLinear',n='side_ob_TwistUpPosMDL')
            TwistUpPosMDL.input2.set(-1)
            IKFKCtrl.UpTwistFix>>TwistUpPosMDL.input1
        else:
            IKFKCtrl.UpTwistFix>>TwistUpPos1.rotateX
        TwistUpPos1Grp=gn.addNPO(TwistUpPos1, 'Grp')[0]
        TwistUpAimPos = pm.createNode('transform', n='side_ob_%sTwistUpAimPos' % subob[0])
        TwistUpVecPos = pm.createNode('transform', n='side_ob_%sTwistUpVecPos' % subob[0])
        gn.PosCopy(DrvJnt[1],TwistAimPos1,t=1,r=1,mo=0)
        gn.PosCopy(TwistUpPos1Grp, TwistAimPos1, t=1, r=1,mo=0)
        TwistUpFixGrp = pm.createNode('transform', n='side_ob_%sTwistUpFixGrp' % subob[0])
        pm.parent(TwistUpVecPos,TwistUpAimPos,sTwistUpPos1FixGrp)

        # TwistUpPos1 연결
        pm.pointConstraint(DrvJnt[0],TwistUpAimPos,mo=1)
        TwistVP=pm.createNode('vectorProduct',n='side_ob_TwistVP')
        TwistUpAimPos.translate>>TwistVP.input1
        pm.setDrivenKeyframe(TwistUpVecPos + '.rotateZ', cd=TwistVP + '.outputX', dv=-1, v=-90)
        pm.setDrivenKeyframe(TwistUpVecPos + '.rotateZ', cd=TwistVP + '.outputX', dv=0, v=0)
        pm.setDrivenKeyframe(TwistUpVecPos + '.rotateZ', cd=TwistVP + '.outputX', dv=1, v=90)
        pm.aimConstraint(TwistUpAimPos,TwistUpPos1Grp,wut=2,worldUpObject= TwistUpVecPos)
        pm.parent(TwistUpFixGrp,RigSysGrp)

        # TwistUpPos2 만들기
        if side == 'Left':
            TwistUpPos1=pm.createNode('transform',n='side_ob_%sTwistUpPos'%subob[0])
        else:
            IKFKCtrl.UpTwistFix>>TwistUpPos1.rotateX




    def Organize():
        RootCtrl=RootCtrlMake()
        CtrlList=['side_ob_IKConstCtrl','side_subob1_FKCtrl','side_ob_UpArcCtrl','side_ob_MidArcCtrl','side_ob_DnArcCtrl','side_ob_IKFKCtrl','side_ob_PoleVectorCtrl']
        for x in CtrlList:
            if pm.objExists(x):
                grp=pm.PyNode(x+'Grp')
                pm.parent(grp,RootCtrl)
            else:
                pass
        SysList=[DrvJnt[0].replace('DrvJnt','ArcPos'),DrvJnt[1].replace('DrvJnt','ArcPos'),DrvJnt[2].replace('DrvJnt','ArcPos'),'side_ob_UpArcHandle','side_ob_DnArcHandle','side_ob_UpArcCurve','side_ob_DnArcCurve']
        for x in SysList:
            if pm.objExists(x):
                sys=pm.PyNode(x)
                pm.parent(sys,EtcGrp)
            else:
                pass

        gn.Mcon(RootCtrl,IKJnt[0],t=1, r=1, sh=1, mo=1, pvtCalc=1)
        pm.parent(AllCrv,UpCurve,DnCurve,EtcGrp)

        
    def NameChange():
        SideSel=pm.ls('*side_*')
        ObSel=pm.ls('*ob_*')
        subob1Sel=pm.ls('*subob1_*')
        subob2Sel=pm.ls('*subob2_*')
        subob3Sel=pm.ls('*subob3_*')
        for x in SideSel:
            pm.rename(x,x.replace('side_',side))          
        for y in ObSel:
            pm.rename(y,y.replace('ob_',ob))
        for i,j,k in zip(subob1Sel,subob2Sel,subob3Sel):
            pm.rename(i,i.replace('subob1_',subob[0]))
            pm.rename(j,j.replace('subob2_',subob[1]))
            pm.rename(k,k.replace('subob3_',subob[2]))
        # 블랜드쉐입 타겟 네이밍 수정
        BS = pm.ls('%s%sArcBS' % (side, ob), type='blendShape')[0]
        pm.aliasAttr('%s%sArcCrvGrp' % (side, ob), BS.w[0])
        # 컨스트레인 노드 어트리뷰트 네이밍 수정
        CNSList = ['pointConstraint', 'parentConstraint', 'orientConstraint','aimConstraint']
        for x in CNSList:
            cns = pm.ls(type=x)
            for i in cns:
                find = i.attr('target[0].targetWeight')
                Str_find = str(find)
                F_attr = find.listConnections(d=0, s=1, p=1)[0]
                Str_attr = str(F_attr).split('.')[-1]
                if 'ob_' in Str_attr:
                    pm.renameAttr(F_attr, Str_attr.replace('side_', side).replace('ob_', ob))
                else:
                    pass

    IKRig()
  
    FKRig()

    DrvRig()
    #ArcRig()
    BindRig()
    StretchPractice()
    #Organize()
    #NameChange()
    
   

    ###### 스쿼시 만들기, 트위스트 넣기 , 다리 안된다.... , 조인트 오리엔트 방향 맞추기!
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
sel=pm.ls(sl=1)

    

LeftArmRig=SealBodyRig(Jnt=sel)
#RightArmRig=ArmLegRig(AllCurve='RightArm_GuideCurve')
'''

sel=pm.ls(sl=1)
tt=gn.jntList(sel[0],len(sel))
print(tt)

'''



'''

LeftLegRig=ArmLegRig(AllCurve='LeftLeg_GuideCurve')
RightLegRig=ArmLegRig(AllCurve='RightLeg_GuideCurve')

'''
