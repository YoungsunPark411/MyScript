import pymel.core as pm

sel=pm.ls(sl=1)


driver=sel[0]+'.outputX'
driven=sel[1]+'.input[0]'


pm.setDrivenKeyframe(driven, cd=driver, dv=0.0, v=0.0)
pm.setDrivenKeyframe(driven, cd=driver, dv=3, v=0.1)

#
import pymel.core as pm

sel=pm.ls(sl=1)


driver=sel[0]+'.translateZ'
driven=sel[1]+'.rotateY'


pm.setDrivenKeyframe(driven, cd=driver, dv=0.0, v=0.0)
pm.setDrivenKeyframe(driven, cd=driver, dv=-3, v=20)