# -*- coding: cp949 -*-
import pymel.core as pm

def NameExtraction(sel):
	cn = curve1
	side = []
	ob = []
	if 'LeftArm' in cn:
		side = 'Left'
	elif 'RightArm' in cn:
		side = 'Right'
	elif 'Neck' in cn:
		side = 'Up'
	elif 'Dn' in cn:
		side = 'Dn'
	else:
		side = ''
	obList=['Arm','UpArm','DnArm','Leg','UpLeg','DnLeg','Clavicle','Neck','Spine','Thumb','Index','Middle','Ring','Pinky','Eye','Tongue']
	for i in range(len(obList)):
		if obList[i] in cn:
			ob = obList[i]
		else:
			pass

	if 'Arm' in ob:
		subOb = ['Shoulder', 'Elbow', 'Wrist']
	elif 'Leg' in ob:
		subOb = ['Thigh', 'Knee', 'Ankle']
	else:
		subOb =''

	list=[side,ob,subOb]
	return list

def CnsMake(cns,pa,ch):
	if cns == 'scale':
		cns_=pm.parentConstraint(pa,ch)
	elif cns == 'orient':
		cns_ = pm.orientConstraint(pa, ch)
	elif cns == 'point':
		cns_ = pm.pointConstraint(pa, ch)
	elif cns == 'parent':
		cns_ = pm.scaleConstraint(pa, ch)
	else:
		pass
	return cns_

# 드라이브 들 선택 후 드리븐 선택
def FollowMake(sel,cnsType):
	driven=sel[-1]
	driver=sel[:-1]

	set_names = []
	for x in driver:
		dirGrp=x.split('Ctrl')[0]+'Grp'
		if pm.objExists(dirGrp):
			dir_Grp=pm.createNode('transform',n=dirGrp)
			pm.delete(pm.parentConstraint(x,dir_Grp))
			pm.parent(dir_Grp,x)
		else:
			dir_Grp=dirGrp
		space = pm.createNode('transform', n=driver.split('Ctrl')[0]+x.split('Ctrl')[0]+'Space')
		pm.delete(pm.parentConstraint(x, space))
		pm.parent(space,dir_Grp)

	CNS_=CnsMake(cnsType, driver, driven)



		for i, set_name in enumerate(set_names):
			set_members = [set_name] or []
			for member in set_members:
				for j in range(len(set_names)):
					pm.setDrivenKeyframe(member, cd="{}.Follow".format(driver), dv=j, v=i == j)

###
sel=pm.ls(sl=1)
cns=pm.parentConstraint(sel[:-1],sel[-1])
attrlist=[]
for i in range(len(sel[:-1])):
    find = cns.attr('target[%s].targetWeight'%i)
    Str_find = str(find)
    F_attr = find.listConnections(d=0, s=1, p=1)[0]
    Str_attr = str(F_attr)
    attrlist.append(Str_attr)
