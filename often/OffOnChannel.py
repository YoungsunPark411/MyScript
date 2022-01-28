import pymel.core as pm, pymel.core.datatypes as dt,pymel.core.general as gn,maya.cmds as mc
sel=mc.ls(sl=1)
for i in range(len(sel)):
    mc.addAttr (sel,ln = "FacialCtrlVis",at= 'bool',dv= 0,k=1)
    mc.addAttr (sel,ln = "ScaleZ",at= 'double',dv= 0,k=1)
    
    
    
    mc.addAttr (sel,ln = "DnTwistFix",at= 'double',dv= 0,k=1)
    #mc.addAttr (sel,ln = "Follow",at= 'enum',dv= 0,k=1,en= "off:on:")
    mc.addAttr (sel,ln = "FragmentAVis",at= 'double',dv= 0,k=1,min=0,max=1)
    mc.addAttr (sel,ln = "FragmentBVis",at= 'double',dv= 0,k=1,min=0,max=1)
    mc.addAttr (sel,ln = "DnTwistFix",at= 'double',dv= 0,k=1)
    
mc.connectAttr('RootCtrl.SimDummyVis','DynGrp.visibility')


sel=mc.ls(sl=1)
for i in range(len(sel)):
    mc.addAttr (sel,ln = "Follow",at= 'enum',dv= 0,k=1,en= "World:Move:Fly")
    
Cream:Blue:Mind:Red:Deep_Green:Gold:White
Olive:Sky:Lemmon:Orange:Cream:Purple
Cream:Blue:Mind:Red:Deep_Green:Gold:White
Red:Blue:DarkBlue:White:Sliver:Black
Lunar_Sky:DeepBlue:Crimson_Red:Alpine_White:Black_Sappire:Tectonic_Silver
#------------------------눈 채널 만들고, 연결

def addEyeAttribute():
    sideList=['Left','Right']
    for side in sideList:
        mc.select('%sEyeCtrl'%side)        
        mc.addAttr(ln="CorneaScale", at='double', dv=0, k=1)
        mc.addAttr(ln="CorneaSize", at='double', min=-10, max=30,dv=0, k=1)
        mc.addAttr(ln="IrisDepth", at='double', dv=0, k=1)
        mc.addAttr(ln="PupilSize", at='double', min=-10, max=10,dv=0, k=1)
        
        mc.connectAttr('%sEyeCtrl'%side+'.CorneaScale','EyeBD_%s.CorneaScale'%side[0])
        mc.connectAttr('%sEyeCtrl'%side+'.CorneaSize','EyeBD_%s.CorneaSize'%side[0])
        mc.connectAttr('%sEyeCtrl'%side+'.IrisDepth','EyeBD_%s.IrisDepth'%side[0])
        mc.connectAttr('%sEyeCtrl'%side+'.PupilSize','EyeBD_%s.PupilSize'%side[0])
        
        
        
addEyeAttribute()




i='WorldCtrl'
mc.select(i)
mc.addAttr (i,ln = "PolyLevel",at= 'long',dv= 0,k=1,min= 0, max= 2)
mc.setAttr(i+'.PolyLevel',k=0,cb=1)
mc.setDrivenKeyframe('PolyLevel0.visibility', cd='WorldCtrl.PolyLevel', dv=0, v=1 )
mc.setDrivenKeyframe('PolyLevel0.visibility', cd='WorldCtrl.PolyLevel', dv=1, v=0 )
mc.setDrivenKeyframe('PolyLevel0.visibility', cd='WorldCtrl.PolyLevel', dv=2, v=0 )

mc.setDrivenKeyframe('PolyLevel1.visibility', cd='WorldCtrl.PolyLevel', dv=0, v=0 )
mc.setDrivenKeyframe('PolyLevel1.visibility', cd='WorldCtrl.PolyLevel', dv=1, v=1 )
mc.setDrivenKeyframe('PolyLevel1.visibility', cd='WorldCtrl.PolyLevel', dv=2, v=1 )

mc.setDrivenKeyframe('PolyLevel2.visibility', cd='WorldCtrl.PolyLevel', dv=0, v=0 )
mc.setDrivenKeyframe('PolyLevel2.visibility', cd='WorldCtrl.PolyLevel', dv=1, v=0 )
mc.setDrivenKeyframe('PolyLevel2.visibility', cd='WorldCtrl.PolyLevel', dv=2, v=1 )

mc.addAttr (i,ln = "CharacterVis",at= 'long',dv= 0,k=1,min= 0, max= 1)
mc.setAttr(i+'.CharacterVis',k=0,cb=1)

    

#visinlity 채널 
i=mc.ls(sl=1)
mc.addAttr (i,ln = "ModelChange",at= 'long',dv= 0,k=1,min= 0, max= 1)    
    

    