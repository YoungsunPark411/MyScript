# -*- coding: cp949 -*-
import maya.cmds as mc
import pymel.core as pm, Ycmd as yc


slls = pm.ls(sl=1)
for x in slls:
    JntGrp=yc.addNPO(x,'SetGrp')
    yc.rotate_components(0, 0, 90, nodes=x)
#검색하기--------------------------------------------------------------------------------------------

yc.selectNodesTypeBelow('locator')   
yc.selectNodesTypeBelow('mesh')       
yc.selectNodesTypeBelow('nurbsCurve')   
yc.selectNodesTypeBelow('joint')
yc.selectNodesTypeBelow('parentConstraint')
pm.delete()

#검색해서 선택    
yc.SearcchThings('*RV*','reverse')
yc.SearcchThings('bindPose*','dagPose')
yc.SearcchThings('tweak*','tweak')
yc.SearcchThings('Biped_Guide*','multiplyDivide')
yc.SearcchThings('','RedshiftAOV')

yc.SearcchThings('*M','multMatrix')


#ctrl 잡고 joint 잡고-------------------------------------------------------------------------------------

slls = pm.ls(sl=1)
hSelSz= int(len(slls)/2)

sc=slls[:hSelSz]
tg=slls[hSelSz:]

for i in range(hSelSz):
    #sc[i].result.position>>tg[i].translate
    pm.delete(pm.pointConstraint(sc[i],tg[i]))
    #yc.PosCopy(sc[i],tg[i])
    #pm.connectAttr(sc[i]+'.allCoordinates',tg[i]+'.translate')
    #pm.delete(pm.parentConstraint(sc[i],tg[i]))

    #pm.parentConstraint(sc[i],tg[i])
    #pm.parent(sc[i],tg[i])
    #sc[i].s >> tg[i].inverseScale
    #matchParent( sc[i],tg[i])
    #OneParentCNS( sc[i],tg[i])
    
    yc.Mcon(sc[i],tg[i],t=1, r=1, s=1, sh=1, mo=1, pvtCalc=1)
    #pm.aimConstraint( sc[i],tg[i])
    
    




#---------------------------------------------------------------        
#ctrl 잡고 joint 잡고2
import pymel.core as pm
slls = pm.ls(sl=1)


sc=slls[0]
tg=slls[1:]


for i in range(len(tg)):
    #mc.scaleConstraint(sc,tg[i])
    #sc.FacialDetailCtrlVis >> tg[i].getShape().visibility
    #sc.FacialCtrlVis >> tg[i].getShape().visibility
    
    
    #print sc

    #sc[i].s >> tg[i].inverseScale
    #matchParent( sc[i],tg[i])
    #OneParentCNS( sc[i],tg[i])
    #yc.Mcon(sc,tg[i],t=1, r=1, s=1, pvtCalc=1)
   
    #mc.select(sc,tg[i])
    #mc.copySkinWeights(noMirror=True, sa='closestPoint' ,ia='label')
    

    '''
    yc.Mcon(sc,tg[i],t=1, r=1, s=1, pvtCalc=1)
    pb=yc.PairBlend(tg[i],r=1,t=1)
    tg[i].pbw.set(0.5)
    scaleAttrs=['s','sx','sy','sz']
    [ sc.attr(satr).inputs(p=1)[0] >> tg[i].attr(satr) for satr in scaleAttrs if len( sc.attr(satr).inputs() ) ]
    '''
    
     
    
    #sc.FacialDetailCtrlVis >> tg[i].getShape().visibility
    sc.FacialCtrlVis >> tg[i].getShape().visibility
    sc.FacialCtrlVis >> tg[i].replace('Left','Right').getShape().visibility
    
#-----------------------------------------------------------------------

    



#---------------------------------------------------------------        
#리스트 커맨드 반복



#컨트롤에 그룹 두개에 조인트 붙여넣기
'''
sel=pm.selected()
Grp1=addNPO(sel,'Zero')
Grp2=addNPO(sel,'Sub')
'''


slls = pm.ls(sl=1)
for i in slls:
    
    sel=pm.select(i)
    
    addNPO(sel,'Set')
    #addNPO(sel,'EyeBrowPBGrp')
    #addNPO(sel,'EyeLidPBGrp')
 
    #PairBlend(slls[i],tr=1,rt=1)
    
    
    #Grp1=addNPO(slls[i],'BrowPBGrp')
    #Grp2=addNPO(slls[i],'EyelidPBGrp')
    '''
    jnt=pm.createNode('joint',n='%s'%slls[i].replace('Ctrl','Jnt'))
    pm.delete(pm.parentConstraint( slls[i],jnt))
    pm.parent(jnt,slls[i])
    pm.select(jnt)
    pm.makeIdentity (apply=1,t =0,r= 1 ,s =0 ,n =0 ,pn= 1)
    '''
    
slls = pm.ls(sl=1)
for i in xrange(len(slls)):
    '''
    #Grp1=addNPO(slls[i],'Zero')
    Grp2=addNPO(slls[i],'Sub')
    jnt=pm.createNode('joint',n='%s'%slls[i].replace('Ctrl','Jnt'))
    pm.delete(pm.parentConstraint( slls[i],jnt))
    pm.parent(jnt,slls[i])
    pm.select(jnt)
    pm.makeIdentity (apply=1,t =0,r= 1 ,s =0 ,n =0 ,pn= 1)
    '''
    
    jnt=pm.createNode('joint',n='%s'%slls[i].replace('Ctrl','Jnt'))
    pm.select(jnt)
    pm.makeIdentity (apply=1,t =0,r= 1 ,s =0 ,n =0 ,pn= 1)
    
    pm.delete(pm.parentConstraint( slls[i],jnt))
    Grp2=addNPO(jnt,'Grp')
    yc.Mcon(slls[i],Grp2[0],t=1, r=1, s=1, pvtCalc=1)


    




  










#선택한 컨트롤 안에 조인트 붙여넣기 or Mcon하기
slls = pm.ls(sl=1)
for i in slls:
    jnt=pm.createNode('joint',n='%s'%i.replace('Ctrl','Jnt'))
    
    pm.delete(pm.parentConstraint( i,jnt))
    
    pm.select('%s'%jnt)
    
    pm.makeIdentity (apply=1,t =0,r= 1 ,s =0 ,n =0 ,pn= 1)
    #pm.parent(jnt,slls[i])
    #sel=pm.select(jnt)
    
    #grp=addNPO(i,'Grp')
    JntGrp=yc.addNPO(jnt,'Grp')
    
    yc.Mcon(i,JntGrp[0],t=1, r=1, s=1, pvtCalc=1)
    
   
    



for i in range(10,41):
    #pm.parent(sc[i],tg[i])
    #sc[i].s >> tg[i].inverseScale
    #matchParent( sc[i],tg[i])
    #OneParentCNS( sc[i],tg[i])
    yc.Mcon('Frenchfriess%Ctrl'%i,'Frenchfries_0s%_geoGrp'%,t=1, r=1, s=1, pvtCalc=1)
  
    
#같은 이름 컨트롤, 조인트 Mcon 하기 
ctrl=pm.ls(sl=1)
for x in ctrl:
    if x.replace('Ctrl','JntGrp'):
        select=pm.select(x,x.replace('Ctrl','JntGrp'))
        print(select)
        sel=pm.ls(sl=1)
   
        yc.Mcon(sel[0],sel[1],t=1, r=1, s=1,sh=1, mo=1, pvtCalc=1)
  
#클러스터에 컨트롤 달기
clu=pm.ls(sl=1)
for x in clu:
    ctrl=pm.circle(n='%sCtrl'%x)
    pm.delete(ctrl[0],ch=1)
    pm.delete(pm.parentConstraint(x,ctrl[0]))
    tg=pm.listConnections(x.worldMatrix[0])[0]
    crv=pm.listConnections(tg.outputGeometry[0])[0]
    cl=pm.cluster(crv+'.cv[0]')
    dx=pm.duplicate(x)
    pm.setAttr(dx[0]+'.translateY',2)
    
    pm.aimConstraint(cl[1],ctrl[0],wut=1,wuo=dx[0])
    pm.delete(dx[0],cl[0])

    select=pm.select(ctrl[0],x)
    sel=pm.ls(sl=1)
    yc.Mcon(sel[0],sel[1],t=1, r=1, s=1,sh=1, mo=1, pvtCalc=1)
    

#커브에 조인트 만들기 
# -*- coding: cp949 -*-
import pymel.core as pm
import sys
sys.path.append(r'E:Sealped')
from RIG import General as gn
reload(gn)

sel=pm.ls(sl=1)
gn.JntMake(sel[0],3, '')      

#displacement 켜기
tt=pm.ls('*',type='mesh')  
#Mesh_=pm.ls(sl=1)   
for x in tt:
    x.rsEnableDisplacement.set(1)
    
# 그룹 만들기
sel=pm.ls(sl=1)
yc.addNPO(sel,'SetGrp')

#조인트에 사각 컨트롤 달기 
Jnt=pm.ls(sl=1)
shape_='square'
Color=20
for x in Jnt:
    ctrl=yc.ControlMaker('%sCtrl' % x.replace('Jnt',''), shape_, Color, exGrp=0, size= 1)
    yc.PosCopy(x, ctrl[0])
    yc.Mcon(ctrl[0],x,t=1, r=1, s=1,sh=1, mo=1, pvtCalc=1)