import maya.cmds as cmds

selection = cmds.ls(orderedSelection=True, flatten=True)
print(selection)

vtx_selection = cmds.polyListComponentConversion(selection, toVertex=True)
print(cmds.filterExpand(vtx_selection, selectionMask=31, expand=True))]


for obj in selection:
    if 'vtx[' not in obj:
        selection.remove(obj)
print(selection)

cmds.filterExpand(selection, selectionMask=31, expand=True)

for obj in selection:
    print(cmds.ls(obj + ".vtx[*]", flatten=True))



#vtx_selection = cmds.polyListComponentConversion("pSphere1", toVertex=True)
#vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31)

cmds.select(vtx_selection)
scattered_instances = []

for vtx in vtx_selection:
    scatter_instance = cmds.instance("pCube1", name="pCube5")
    scattered_instances.extend(scatter_instance)
   #pos = cmds.xform([vtx], query=True, translation=True)
    pos = cmds.pointPosition([vtx])
    cmds.xform(scatter_instance, translation=pos)

cmds.group(scattered_instances, name="scattered")