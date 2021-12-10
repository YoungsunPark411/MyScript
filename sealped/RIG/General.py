# -*- coding: cp949 -*-
'''
Ycmds
note:
date: 21.09.07
'''
import pymel.core as pm, pymel.core.datatypes as dt, maya.cmds as mc
#General-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def eqDistanceCurveDivide(curvename,segmentcurveLength):
	curveLength=pm.arclen(curvename)

	uVale=1.0/(segmentcurveLength-1)
	i=0
	posList=[]
	for x in range(segmentcurveLength):
		pointA=pm.pointOnCurve(curvename,top=True, pr=i, p=True )
		posList.append(pointA)
		i=i+uVale
	return posList


def spine_joint_make(curve_Name,spineName,joint_count,joint_start_n,type,ojVal='xzy',sawoVal='xdown'):
	jointParentName=[]
	jointPosition=eqDistanceCurveDivide(curve_Name,joint_count)

	jointList=[]
	mc.select(cl=1)
	mc.select(cl=1)
	for x in jointPosition:
		createName='%s%s%sJnt'%(spineName,str(joint_start_n).zfill(1),type)
		jointList.append(createName)
		mc.joint(p=x,n=createName)
		joint_start_n+=1
	if jointList:
		mc.select(jointList[0]);
		mc.makeIdentity (apply=1,t =0,r= 1 ,s =0 ,n =0 ,pn= 1);
		mc.joint(e=1  ,oj ='xzy' ,secondaryAxisOrient= 'zdown',ch =1 ,zso=1);
		mc.setAttr ("%s.jointOrientX"%jointList[-1], 0);
		mc.setAttr ("%s.jointOrientY"%jointList[-1], 0);
		mc.setAttr ("%s.jointOrientZ"%jointList[-1], 0);
		mc.select(jointList)



	return jointList

def NameExtraction(curve1):
	cn = curve1
	side = []
	ob = []
	if 'Left' in cn:
		side = 'Left'
	elif 'Right' in cn:
		side = 'Right'
	elif 'Up' in cn:
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

def GrpMake():
	RigGrp = pm.createNode('transform', n='side_ob_RigGrp')
	CtrlGrp = pm.createNode('transform', n='side_ob_CtrlGrp')
	RigSysGrp = pm.createNode('transform', n='side_ob_RigSysGrp')
	EtcGrp = pm.createNode('transform', n='side_ob_EtcGrp')
	GrpList = [RigGrp, CtrlGrp, RigSysGrp, EtcGrp]
	pm.parent(CtrlGrp, RigSysGrp, EtcGrp, RigGrp)
	return GrpList

def JntMake(AllCurve,segNumber, Type):
	#pm.rebuildCurve(AllCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=segNumber, d=3, tol=0.01)
	JntList=spine_joint_make(curve_Name=AllCurve, spineName='%s'%(AllCurve.split('_')[0]), joint_count=segNumber, joint_start_n=0,type= Type)
	return JntList

def NameChange():
	sideList=pm.ls('side_*')
	for x in sideList:
		pm.rename(x,x.replace('side_',side))
	obList=pm.ls('*ob_*')
	for x in sideList:
		pm.rename(x,x.replace('ob_',ob))

def scaleGet():
	if not pm.objExists('Global'):
		Scale=8
	else:
		Scale = pm.getAttr('Global.scaleX')
	return Scale

# Wcms-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Curve Shape Change
def CurveCenterPiv(crv):
	vtxNum = crv.cp.get(mi=1)
	vtxSz = len(vtxNum)
	mn = [0.0, 0.0, 0.0]
	mx = [0.0, 0.0, 0.0]
	vtxXfm = []
	for i in range(vtxSz):
		vtxXfm.append(pm.xform('%s.cv[%d]' % (crv, vtxNum[i]), q=1, ws=1, t=1))
		bfr = []
		[bfr.append(vtxXfm[i][ii]) for ii in range(3)]
		if i == 0:
			mn[0] = bfr[0]
			mn[1] = bfr[1]
			mn[2] = bfr[2]
			mx[0] = bfr[0]
			mx[1] = bfr[1]
			mx[2] = bfr[2]
		if mn[0] > bfr[0]: mn[0] = bfr[0]
		if mn[1] > bfr[1]: mn[1] = bfr[1]
		if mn[2] > bfr[2]: mn[2] = bfr[2]
		if mx[0] < bfr[0]: mx[0] = bfr[0]
		if mx[1] < bfr[1]: mx[1] = bfr[1]
		if mx[2] < bfr[2]: mx[2] = bfr[2]
	cntVec = []
	i1 = 0
	[cntVec.append((mx[i1] + mn[i1]) / 2) for i1 in range(3)]
	return cntVec


def ChangeCurveTransform(crv, type, transVec, pvt=0):
	pm.select(crv)
	ct=pm.ls(sl=1)

	if 'EyeCtrl' in ct:
		span = len(crv.getCVs())
	else:
		span = crv.spans.get()

	deg = crv.d.get()
	endCv = span - 1 if deg == 3 else span
	cntPiv = CurveCenterPiv(crv) if pvt == 0 else crv.getTranslation(space='world')
	pm.move(crv.cv[0:endCv], transVec, r=1) if type == 'translate' else (pm.rotate(crv.cv[0:endCv], transVec, r=1, os=1, p=cntPiv) if type == 'rotate' else (pm.scale(crv.cv[0:endCv], transVec, r=1, p=cntPiv) if type == 'scale' else None))


# Control Maker
def ChangeCurveColor(crv, colorNum=0):
	crvSh = crv.listRelatives(s=1)[0]
	crvSh.overrideEnabled.set(1)
	crvSh.overrideColor.set(colorNum)
	crv.v.set(l=1)
	crvSh.rename('%sShape' % crv)


def ControlMaker(name, form, colorNum, exGrp=False, size=1.0):
	rst = [None, None]

	if form == 'circle':
		rst[0] = pm.circle(n=name, c=[0, 0, 0], nr=[0, 1, 0], sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]


	elif form == 'cross':
		rst[0] = pm.curve(d=1, n=name, p=[(-0.332874, 0, -0.332874), (-0.332874, 0, -0.998623), (0.332874, 0, -0.998623), (0.332874, 0, -0.332874),
										  (0.998623, 0, -0.332874), (0.998623, 0, 0.332874), (0.332874, 0, 0.332874), (0.332874, 0, 0.998623),
										  (-0.332874, 0, 0.998623), (-0.332874, 0, 0.332874), (-0.998623, 0, 0.332874), (-0.998623, 0, -0.332874), (-0.332874, 0, -0.332874)],
						  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

	elif form == 'square':
		rst[0] = pm.curve(d=1, n=name, p=[(-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)], k=[0, 1, 2, 3, 4])
	elif form == 'reverscheck':
		rst[0] = pm.curve(d=1, n=name, p=[(-0.999454, 0, 0.637922), (-0.490766, 0, 0.637922), (0, 0, -0.133233), (0.490766, 0, 0.637922),
										  (0.999454, 0, 0.637922), (0, 0, -0.86126), (-0.999454, 0, 0.637922)],
						  k=[0, 1, 2, 3, 4, 5, 6])
	elif form == 'diamond':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0, -1.414214), (-1.414214, 0, 0), (0, 0, 1.414214), (1.414214, 0, 0), (0, 0, -1.414214)], k=[0, 1, 2, 3, 4])
	elif form == 'check':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0, 0), (-1.255324, 0, -1.255324), (-0.627662, 0, -1.882986), (0, 0, -1.255324), (0.627662, 0, -1.882986), (1.255324, 0, -1.255324), (0, 0, 0)],
						  k=[0, 1, 2, 3, 4, 5, 6])
	elif form == 'switch':
		rst[0] = pm.curve(d=1, n=name, p=[(-0.270729, 0, -0.217609), (-0.270729, 0, -0.454896), (-0.988736, 0, 0.217609), (0.270729, 0, 0.217609), (0.270729, 0, 0.454896), (0.988736, 0, -0.217609), (-0.270729, 0, -0.217609)], k=[0, 1, 2, 3, 4, 5, 6])
	elif form == 'pyramid':
		rst[0] = pm.curve(d=1, n=name, p=[(-0.497381, 0, 0), (0, 0, 0.49738), (0.497381, 0, 0), (0, 0, -0.49738), (-0.497381, 0, 0), (0, 0.642429, 0), (0, 0, 0.49738), (0.497381, 0, 0), (0, 0.642429, 0), (0, 0, -0.49738)], k=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
	elif form == 'pin':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0.0270211, 0), (-0.0158826, 0.0218603, 0), (-0.0256986, 0.00834981, 0), (-0.0256986, -0.00835026, 0), (-0.0158826, -0.0218607, 0), (0, -0.0270211, 0), (0.0158826, -0.0218607, 0),
										  (0.0256986, -0.00835026, 0), (0.0256986, 0.00834981, 0), (0.0158826, 0.0218603, 0), (0, 0.0270211, 0), (0, 0.607018, 0), (-0.118932, 0.645661, 0), (-0.192436, 0.74683, 0), (-0.192436, 0.871884, 0),
										  (-0.118932, 0.973053, 0), (0, 1.011698, 0), (0.118932, 0.973053, 0), (0.192436, 0.871884, 0), (0.192436, 0.74683, 0), (0.118932, 0.645661, 0), (0, 0.607018, 0)],
						  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
	elif form == 'crosspin':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0.0500343, 0), (-0.0500343, 0, 0), (0, -0.0500343, 0), (0.0500343, 0, 0), (0, 0.0500343, 0), (0, 1.257438, 0), (-0.120872, 1.257438, 0),
										  (-0.120872, 1.499182, 0), (-0.362616, 1.499182, 0), (-0.362616, 1.740926, 0), (-0.120872, 1.740926, 0), (-0.120872, 1.98267, 0), (0.120872, 1.98267, 0),
										  (0.120872, 1.740926, 0), (0.362616, 1.740926, 0), (0.362616, 1.499182, 0), (0.120872, 1.499182, 0), (0.120872, 1.257438, 0), (0, 1.257438, 0)],
						  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
	elif form == 'cube':
		rst[0] = pm.curve(d=1, n=name, p=[(-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
										  (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5),
										  (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5)],
						  k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
	elif form == 'triangle':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0.497911, 0), (-0.674025, -0.497911, 0), (0.674025, -0.497911, 0), (0, 0.497911, 0)],
						  k=[0, 1, 2, 3])
	elif form == 'diamondpin':
		rst[0] = pm.curve(d=1, n=name, p=[(0, 0.0835952, 0), (-0.0835952, 0, 0), (0, -0.0835952, 0), (0.0835952, 0, 0),
										  (0, 0.0835952, 0), (0, 1.008552, 0), (-0.326239, 1.334791, 0), (0, 1.66103, 0),
										  (0.326239, 1.334791, 0), (0, 1.008552, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
	elif form == 'hexagon':
		rst[0] = pm.curve(d=1, n=name, p=[(0.414019, 0.0, -1), (-0.414019, 0, -1), (-1, 0, -0.414019), (-1, 0, 0.414019),
										  (-0.414019, 0, 1), (0.414019, 0, 1), (1, 0, 0.414019), (1, 0, -0.414019),
										  (0.414019, 0, -1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8])
	elif form == 'lip':
		rst[0] = pm.circle(n=name, c=[0, 0, 0], nr=[0, 0, 1], sw=360, r=1, d=3, ut=0, tol=0.01, s=12, ch=0)[0]
		cvLs = [[0.18785, 0.38091, 0.0], [0.0, 0.12507, 0.0], [-0.18785, 0.38091, 0.0], [-0.90213, 0.07120, 0.0],
				[-1.04222, -0.00209, 0.0], [-0.90213, -0.09035, 0.0], [-0.52110, -0.28769, 0.0], [0.0, -0.38091, 0.0],
				[0.52110, -0.28769, 0.0], [0.90213, -0.09035, 0.0], [1.04222, -0.00209, 0.0], [0.90213, 0.07120, 0.0]]
		list(map(lambda i: rst[0].cp[i].set(cvLs[i][0], cvLs[i][1], cvLs[i][2]), range(12)))
	elif form == 'Eye':
		rst[0] = pm.curve(d=3, n=name, p=[([-6.57046234737, -2.68684513344, -2.45785996638e-15]),
										  ([-7.13261542002, -1.55289293303e-15, -2.0205055052e-15]),
										  ([-6.57046234737, 2.68684513344, -1.26466103408e-15]),
										  ([-5.04301250688, 4.0313768254, -5.33423701453e-16]),
										  ([-2.72163958787, 3.23831878984, -5.19265312134e-17]),
										  ([-5.84260756747e-05, 2.42230306612, 5.37842776564e-16]),
										  ([2.72178063184, 3.23848663844, 1.49010618821e-15]),
										  ([5.04278651622, 4.03132065496, 2.32363816017e-15]),
										  ([6.57089451076, 2.6868860558, 2.45799147489e-15]),
										  ([7.13159295183, 5.51934689293e-16, 2.02021586354e-15]),
										  ([6.57089451076, -2.6868860558, 1.26477436941e-15]),
										  ([5.04278651622, -4.03132065496, 5.33372155853e-16]),
										  ([2.72178063184, -3.23848663844, 5.19292158421e-17]),
										  ([-5.8426075672e-05, -2.42230306612, -5.37875878084e-16]),
										  ([-2.72163958787, -3.23831878984, -1.49002896383e-15]),
										  ([-5.04301250688, -4.0313768254, -2.32371465045e-15]),
										  ([-6.57046234737, -2.68684513344, -2.45785996638e-15]),
										  ([-7.13261542002, -1.55289293303e-15, -2.0205055052e-15]),
										  ([-6.57046234737, 2.68684513344, -1.26466103408e-15])],
						  k=[-0.125, -0.0625, 0.0, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625, 0.6874999999999999, 0.75, 0.8125, 0.875, 0.9375, 1.0, 1.0625, 1.125])
	elif form == 'Finger':
		rst[0] = pm.circle(n=name, c=[0, 0, 0], nr=[0, 0, 1], sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]
		cvLs = [([2.08110460065, 0.0, -2.08110460065]),
				([-1.7763568394e-15, 0.0, -9.66382982837]),
				([-2.08110460065, 0.0, -2.08110460065]),
				([-9.66382982837, 0.0, -7.1054273576e-15]),
				([-2.08110460065, 0.0, 2.08110460065]),
				([-1.7763568394e-15, 0.0, 9.66382982837]),
				([2.08110460065, 0.0, 2.08110460065]),
				([9.66382982837, 0.0, -5.3290705182e-15]),
				([2.08110460065, 0.0, -2.08110460065]),
				([-1.7763568394e-15, 0.0, -9.66382982837]),
				([-2.08110460065, 0.0, -2.08110460065])]
		list(map(lambda i: rst[0].cp[i].set(cvLs[i][0], cvLs[i][1], cvLs[i][2]), range(8)))
	elif form == 'Foot':
		rst[0] = pm.circle(n=name, c=[0, 0, 0], nr=[0, 0, 1], sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]
		cvLs = [([6.46143430945, -3.51626510985, -5.30795876314]),
				([-4.92168523566e-15, -0.677263312252, -7.98519284539]),
				([-6.46143430945, -3.51626510985, -5.30795876314]),
				([-6.46145648162, -5.28434019544, 4.64329670962]),
				([-6.46143430945, -3.6000032127, 15.1140753866]),
				([-4.51429995311e-15, -0.669079682525, 18.8503117448]),
				([6.46143430945, -3.6000032127, 15.1140753866]),
				([6.46145648162, -5.28434019544, 4.64329670962]),
				([6.46143430945, -3.51626510985, -5.30795876314]),
				([-4.92168523566e-15, -0.677263312252, -7.98519284539]),
				([-6.46143430945, -3.51626510985, -5.30795876314])]
		list(map(lambda i: rst[0].cp[i].set(cvLs[i][0], cvLs[i][1], cvLs[i][2]), range(8)))
	elif form == 'Jaw':
		rst[0] = pm.circle(n=name, c=[0, 0, 0], nr=[0, 0, 1], sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)[0]
		cvLs = [([-2.62482745568, -1.69682008917, -3.76769746328e-16]),
				([4.26679597871e-15, -2.7840592202, -6.18185329637e-16]),
				([2.62482745568, -1.69682008917, -3.76769746328e-16]),
				([3.71206658671, 2.78402209953, 6.18177087194e-16]),
				([2.62482745568, 2.78404834781, 6.18182915481e-16]),
				([7.27952347739e-15, 2.7840592202, 6.18185329637e-16]),
				([-2.62482745568, 2.78404834781, 6.18182915481e-16]),
				([-3.71206658671, 2.78402209953, 6.18177087194e-16]),
				([-2.62482745568, -1.69682008917, -3.76769746328e-16]),
				([4.26679597871e-15, -2.7840592202, -6.18185329637e-16]),
				([2.62482745568, -1.69682008917, -3.76769746328e-16])]
		list(map(lambda i: rst[0].cp[i].set(cvLs[i][0], cvLs[i][1], cvLs[i][2]), range(8)))



	ChangeCurveColor(rst[0],colorNum)
	if pm.floatField( 'ControlSizeFloatField', ex=1 ):
		ctrlSize=pm.floatField( 'ControlSizeFloatField', q=1, v=1 )
	else: ctrlSize=1
	size=size*ctrlSize
	ChangeCurveTransform( rst[0], 'scale', dt.Vector(size,size,size), 1 )
	if exGrp:
		exNm='%sGrp'% name
		if pm.objExists(exNm):
			rst[1]=pm.createNode( 'transform', n='%sOffGrp'% name)
		else: rst[1]=pm.createNode( 'transform', n=exNm )
		pm.parent(rst[0],rst[1])

	return rst



# Pair Blend
def PairBlend(Target, **op):
	if op.get('t') or op.get('r'):
		if not Target.hasAttr('pbw'):
			Target.addAttr('pbw', min=0, max=1, k=1)
		PB = pm.createNode('pairBlend', n='%sPB' % Target)
		PB.ri.set(1)
		if Target.t.inputs(p=1):
			Target.t.inputs(p=1)[0] >> PB.it2
			Target.t.inputs(p=1)[0] // Target.t
		if Target.tx.inputs(p=1):
			Target.tx.inputs(p=1)[0] >> PB.itx2
		if Target.ty.inputs(p=1):
			Target.ty.inputs(p=1)[0] >> PB.ity2
		if Target.tz.inputs(p=1):
			Target.tz.inputs(p=1)[0] >> PB.itz2
		if Target.r.inputs(p=1):
			Target.r.inputs(p=1)[0] >> PB.ir2
			Target.r.inputs(p=1)[0] // Target.r
		if Target.rx.inputs(p=1):
			Target.rx.inputs(p=1)[0] >> PB.irx2
		if Target.ry.inputs(p=1):
			Target.ry.inputs(p=1)[0] >> PB.iry2
		if Target.rz.inputs(p=1):
			Target.rz.inputs(p=1)[0] >> PB.irz2
		Target.pbw >> PB.w
		if op.get('t'):
			PB.itx1.set(Target.tx.get())
			PB.ity1.set(Target.ty.get())
			PB.itz1.set(Target.tz.get())
			PB.otx >> Target.tx
			PB.oty >> Target.ty
			PB.otz >> Target.tz
		if op.get('r'):
			PB.irx1.set(Target.rx.get())
			PB.iry1.set(Target.ry.get())
			PB.irz1.set(Target.rz.get())
			PB.orx >> Target.rx
			PB.ory >> Target.ry
			PB.orz >> Target.rz
	else:
		pm.warning('we need flag t or r')
	return PB


# ---Mcon---
def Mcon(src, tg, **op):
	if op.get('pos'): pm.matchTransform(tg, src, pos=1, rot=1, scl=0)
	mm = pm.createNode('multMatrix', n='%sMM' % tg)
	dm = pm.createNode('decomposeMatrix', n='%sDM' % tg)
	rtn = [None, None]
	if op.get('pvtCalc'):
		tgRotatePivot = tg.getRotatePivot(space='transform')
		tg.setScalePivot(tgRotatePivot, space='transform')
		tgScalePivotMtx = dt.Matrix()
		tgScalePivotMtx[3] = tg.getScalePivot(space='transform')
		mm.i[0].set(tgScalePivotMtx)
		mm.i[1].set(tg.getMatrix(worldSpace=1))
		mm.i[1].set(tg.getMatrix(worldSpace=1))
		mm.i[2].set(src.getMatrix(worldSpace=1).inverse())
		src.wm >> mm.i[3]
		tg.pim >> mm.i[4]
		tgTMRPM = dt.Matrix()
		tgTMRPM[3] = tg.transMinusRotatePivot.get()
		mm.i[5].set(tgTMRPM)
	else:
		mm.i[0].set(tg.getMatrix(worldSpace=1))
		mm.i[1].set(src.getMatrix(worldSpace=1).inverse())
		src.wm >> mm.i[2]
		tg.pim >> mm.i[3]
	mm.o >> dm.imat
	if op.get('t'):
		dm.ot >> tg.t
	if op.get('r'):
		if tg.nodeType() == 'joint':
			eq = pm.createNode('eulerToQuat', n='%sEQ' % tg)
			qi = pm.createNode('quatInvert', n='%sQI' % tg)
			qp = pm.createNode('quatProd', n='%sQP' % tg)
			qe = pm.createNode('quatToEuler', n='%sQE' % tg)
			tg.jo >> eq.irt
			eq.oq >> qi.iq
			dm.oq >> qp.iq1
			qi.oq >> qp.iq2
			qp.oq >> qe.iq
			qe.ort >> tg.r
		else:
			dm.attr('or') >> tg.r
	if op.get('s'):
		dm.os >> tg.s
		dm.osh >> tg.sh


# Ycms-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addNPO(objs=None, GrpName=None, *args):
	npoList = []

	if not objs:
		objs = pm.selected()

	if not isinstance(objs, list):
		objs = [objs]

	for obj in objs:
		oParent = obj.getParent()
		oTra = pm.createNode("transform",
							 n=obj.name().replace("Grp", "") + GrpName,
							 p=oParent,
							 ss=True)

		oTra.setTransformation(obj.getMatrix())
		pm.parent(obj, oTra)
		npoList.append(oTra)

	return npoList


def rotate_components(rx, ry, rz, nodes=None):
	if nodes is None:
		nodes = pm.ls(sl=True) or []
	else:
		nodes = pm.ls(nodes)

	for node in nodes:
		# print node
		pivot = pm.xform(node, q=True, rp=True, ws=True)
		pm.rotate(
			"{0}.cv[*]".format(node), rx, ry, rz, r=True, p=pivot, os=True, fo=True
		)


def translate_components(tx, ty, tz, nodes=None):
	if nodes is None:
		nodes = pm.ls(sl=True) or []
	else:
		nodes = pm.ls(nodes)
	for node in nodes:
		# print node
		pivot = pm.xform(node, q=True, rp=True, ws=True)
		pm.move("{0}.cv[*]".format(node), tx, ty, tz, relative=True, objectSpace=True, worldSpaceDistance=True)

def PosCopy(src, tg):
	tmpCons = pm.parentConstraint(src, tg)
	pm.delete(tmpCons)

def jntList(objs,joint_count):
	if not objs:
		objs = pm.selected()
	if not isinstance(objs, list):
		objs = [objs]
	if joint_count:
		for obj in objs:
			pm.select(obj)
			selectNodesTypeBelow('joint')
			List = pm.ls(sl=1)
			Spinejnt_List = List[:(joint_count)]
			pm.select(Spinejnt_List)
			result = pm.ls(sl=1)
	if not joint_count:
		for obj in objs:
			pm.select(obj)
			selectNodesTypeBelow('joint')
			result = pm.ls(sl=1)
	return result

def selectNodesTypeBelow(nodeType):
	nodesToSelect = []
	nodes = findNodesTypeBelow(nodeType)
	for n in nodes:
		nodesToSelect.append(n)
	mc.select(nodesToSelect, r=1)
	return True

def findNodesTypeBelow(nodeType):
	mc.select(hi=1)
	sel = mc.ls(sl=1, type=nodeType)
	return sel

def CrvFromJnt(JntList):
	pointList = []
	for x in JntList:
		tg = pm.xform(x, q=1, t=1, ws=1)
		pointList.append(tg)
	kList = []
	for i in range(len(pointList)):
		kList.append(i)
	Curve = pm.curve(p=pointList, k=kList, d=1)
	return Curve

def MakeBindPreMtxCluster(ev=None):
	slls=pm.ls(sl=1,l=1)
	clustHdlLs=[]
	mesh=[]
	for sl in slls:
		sh=pm.listRelatives(sl,s=1,f=1)[0]
		cfmNode=pm.nodeType(sh)
		if cfmNode=='mesh': mesh.append(sl)
		elif cfmNode=='clusterHandle': clustHdlLs.append(sl)
	if len(clustHdlLs)==0 and len(mesh)==0:
		pm.error('메쉬나 클러스터를 선택하여야 스크립트가 실행됩니다.')
	if len(mesh):
		meshSlClst=pm.cluster(mesh)
		clustHdlLs.append(meshSlClst[1])
	for ch in clustHdlLs:
		sh=pm.listRelatives(ch,s=1)[0]
		clst=pm.listConnections('%s.worldMatrix[0]'% ch)[0]
		pm.setAttr('%s.rotatePivot'% ch, 0, 0, 0)
		pm.setAttr('%s.scalePivot'% ch, 0, 0, 0)
		pm.setAttr('%s.origin'% sh, 0, 0, 0)
		clstGrp=pm.createNode('transform',n='%sGrp'% ch)
		clstIvsMtx=pm.createNode('transform',n='%sZeroMtx'% ch,p=clstGrp)
		pm.parent(ch,clstGrp)
		pm.connectAttr('%s.worldInverseMatrix'% clstIvsMtx,'%s.bindPreMatrix'% clst)
	return clstGrp

def JntAxesChange(Axes,SAO,JntList):
    for x in JntList:
        pm.select(x)
        pm.joint(e=1  ,oj =Axes ,secondaryAxisOrient= SAO,ch =1 ,zso=1)
    pm.setAttr ("%s.jointOrientX"%JntList[-1], 0)
    pm.setAttr ("%s.jointOrientY"%JntList[-1], 0)
    pm.setAttr ("%s.jointOrientZ"%JntList[-1], 0)

