import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


### TexReverse ###

# マテリアル選択→取得
def secmat():
    global mat
    objs = pm.ls(sl=True)
    SG = pm.listConnections(objs, s=False, d=True, t='shadingEngine')
    mat = pm.ls(pm.listConnections(SG, s=True, d=False), mat=True)
    StrMat = ''.join(mat[0])
    cmds.textField('tFld', edit=True, text=StrMat)

# Deffuse----------------
def createRev():
    NowRev = pm.shadingNode( 'reverse', asUtility=True, n='RevTex')
    NowTex = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='RevFile')
    pm.connectAttr(NowRev+'.outputX', mat[0]+'.colorR' , f=True)
    pm.connectAttr(NowRev+'.outputY', mat[0]+'.colorG' , f=True)
    pm.connectAttr(NowRev+'.outputZ', mat[0]+'.colorB' , f=True)
    pm.connectAttr(NowTex+'.outColorR', NowRev+'.inputX', f=True)
    pm.connectAttr(NowTex+'.outColorG', NowRev+'.inputY', f=True)
    pm.connectAttr(NowTex+'.outColorB', NowRev+'.inputZ', f=True)

# Specular----------------
def createSpec():
    NowSpec = pm.shadingNode( 'reverse', asUtility=True, n='RevSpec')
    NowTexC = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='Revfile')
    pm.connectAttr(NowTexC+'.outAlpha', NowSpec+'.inputX' , f=True)
    pm.connectAttr(NowSpec+'.outputX' , mat[0]+'.specularRoughness' , f=True)

# Bump Map----------------
def createBump():
    NowRevB = pm.shadingNode( 'reverse', asUtility=True, n='RevTex')
    NowBump = pm.shadingNode( 'bump2d', asUtility=True, n='RevBump')
    NowTexB = pm.shadingNode( 'file', asTexture=True, isColorManaged=True, n='RevFile')
    pm.connectAttr(NowTexB+'.outAlpha', NowRevB+'.inputX' , f=True)
    pm.connectAttr(NowRevB+'.outputX', NowBump+'.bumpValue' , f=True)
    pm.connectAttr(NowBump+'.outNormal',  mat[0]+'.normalCamera' , f=True)

####################################################################################

### KeyframeBox ###

def cpy():
    mel.eval("timeSliderCopyKey;")

def pst():
    mel.eval("timeSliderPasteKey false;")

def dlt():
    mel.eval("timeSliderClearKey;")

def cut():
    mel.eval("timeSliderCutKey;")

####################################################################################

### ManipBox ###

def wrd():
    cmds.manipMoveContext("Move", e=True, m=2)
    cmds.manipScaleContext("Scale", e=True, m=2)
    cmds.manipRotateContext("Rotate", e=True, m=1)

def lcl():
    cmds.manipMoveContext("Move", e=True, m=0)
    cmds.manipScaleContext("Scale", e=True, m=0)
    cmds.manipRotateContext("Rotate", e=True, m=0)

def cus():
    cmds.manipMoveContext("Move", e=True, m=6)
    cmds.manipScaleContext("Scale", e=True, m=6)
    cmds.manipRotateContext("Rotate", e=True, m=6)

####################################################################################



#Window ===============================


cmds.window(title='MocBox_Ver1.00', widthHeight=(300,310))
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)


child1 = cmds.columnLayout(adj=True)

cmds.button( label = 'Select Material', w=200, h=40, command='secmat()')
cmds.textField('tFld')

cmds.separator( h=10 )
cmds.text("Diffuse")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createRev()')

cmds.separator( h=10 )
cmds.text("Bump")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createBump()')

cmds.separator( h=10 )
cmds.text("Specular")
cmds.separator( h=10 )
cmds.button( label = 'Set', w=200, h=40, command='createSpec()')

cmds.setParent('..')


child2 = cmds.columnLayout(adj=True)
cmds.separator( h=3 )
cmds.text("KeyframeBox")
cmds.separator( h=3 )
cmds.button( label = 'Copy', w=100, h=40, command='cpy()')

cmds.button( label = 'Cut', w=100, h=40, command='cut()')

cmds.button( label = 'Paste', w=100, h=40, command='pst()')

cmds.button( label = 'Delete', w=100, h=40, command='dlt()')

cmds.setParent('..')


child3 = cmds.columnLayout(adj=True)
cmds.separator( h=3 )
cmds.text("MinipBox_V2")
cmds.separator( h=3 )
cmds.button( label = 'World', w=100, h=40, command='wrd()')

cmds.button( label = 'Object', w=100, h=40, command='lcl()')

cmds.button( label = 'Custom', w=100, h=40, command='cus()')

cmds.setParent('..')



cmds.tabLayout( tabs, edit=True, tabLabel=((child1,'TexRev'), (child2,'KeyBox'), (child3,'ManipBox')) )

cmds.showWindow()
