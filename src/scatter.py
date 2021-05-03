import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pm


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(350)
        self.setMinimumHeight(500)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatterfile = ScatterFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 32px")
        self.mount_lay = self._create_mount_ui()
        self.mountpercent_lay = self._create_mount_percent_ui()
        self.mounted_lay = self._create_mounted_ui()
        self.alignment_lay = self._create_alignment_ui()
        self.scale_lay = self._create_scale_ui()
        self.rotation_lay = self._create_rotation_ui()
        self.scale_lay = self._create_scale_ui()
        self.button_lay = self._create_bottom_buttons_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.mount_lay)
        self.main_lay.addLayout(self.mountpercent_lay)
        self.main_lay.addLayout(self.mounted_lay)
        self.main_lay.addLayout(self.alignment_lay)
        self.main_lay.addLayout(self.rotation_lay)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.mount_select_btn.clicked.connect(self._mount_select_highlighted)
        self.mounted_select_btn.clicked.connect(self.
                                                _mounted_select_highlighted)
        self.create_btn.clicked.connect(self._create_scatter)
        # self.remove_btn.clicked.connect(self._remove_instances_mounted)
        self.alignment_cbox.stateChanged.connect(self.scatterfile.checked_normal)

    @QtCore.Slot()
    def _mount_select_highlighted(self):
        self.scatterfile.select_highlighted()
        self.mount_selection_le.setText(','.join(self.scatterfile.selection))


    @QtCore.Slot()
    def _mounted_select_highlighted(self):
        self.scatterfile.select_highlighted()
        self.mounted_selection_le.setText(''.join(self.scatterfile.selection))


    # @QtCore.Slot()
    # def _align_normals(self):
    #     self.scatterfile.checked_normal()

    @QtCore.Slot()
    def _create_scatter(self):
        self._set_scatterfile_properties_from_ui()
        self.scatterfile.do_scatter_instance()

    @QtCore.Slot()
    def _remove_instances_mounted(self):
        self.scatterfile.delete_created_instances


    def _set_scatterfile_properties_from_ui(self):
        self.mount_text = self.mount_selection_le.text()
        self.scatterfile.mount = self.mount_text.split(',')
        self.scatterfile.vertex_percent = (self.percentage_amount_sbx.value())
        self.scatterfile.mounted = self.mounted_selection_le.text()
        self._set_rotation_properties_from_ui()
        self._set_scale_properties_from_ui()

    def _set_rotation_properties_from_ui(self):
        self.scatterfile.rotation_range_min[0] = self.min_xrotation_sbx.value()
        self.scatterfile.rotation_range_min[1] = self.min_yrotation_sbx.value()
        self.scatterfile.rotation_range_min[2] = self.min_zrotation_sbx.value()
        self.scatterfile.rotation_range_max[0] = self.max_xrotation_sbx.value()
        self.scatterfile.rotation_range_max[1] = self.max_yrotation_sbx.value()
        self.scatterfile.rotation_range_max[2] = self.max_zrotation_sbx.value()

    def _set_scale_properties_from_ui(self):
        self.scatterfile.scale_range_min[0] = self.min_xscale_sbx.value()
        self.scatterfile.scale_range_min[1] = self.min_yscale_sbx.value()
        self.scatterfile.scale_range_min[2] = self.min_zscale_sbx.value()
        self.scatterfile.scale_range_max[0] = self.max_xscale_sbx.value()
        self.scatterfile.scale_range_max[1] = self.max_yscale_sbx.value()
        self.scatterfile.scale_range_max[2] = self.max_zscale_sbx.value()

    def _create_bottom_buttons_ui(self):
        self.create_btn = QtWidgets.QPushButton("Create")
        # self.remove_btn = QtWidgets.QPushButton("Delete")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_btn)
        # layout.addWidget(self.remove_btn)
        return layout

    def _create_mount_ui(self):
        self.mount_title_lbl = QtWidgets.QLabel("Mount")
        self.mount_title_lbl.setStyleSheet("font: bold 16px")
        self.mount_selection_le = QtWidgets.QLineEdit("Select an object to mount on.")
        self.mount_selection_le.setMinimumWidth(100)
        self.mount_select_btn = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.mount_title_lbl, 0, 0)
        layout.addWidget(self.mount_selection_le, 0, 1)
        layout.addWidget(self.mount_select_btn, 0, 2)
        return layout

    def _create_mount_percent_ui(self):
        self.mount_percent_title_lbl = QtWidgets.QLabel("Vertex Range")
        self.mount_percent_title_lbl.setStyleSheet("font: bold")
        self.percentage_amount_sbx = QtWidgets.QDoubleSpinBox()
        self.percentage_amount_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.
                                                    PlusMinus)
        self.percentage_amount_sbx.setSingleStep(.01)
        self.percentage_amount_sbx.setFixedWidth(50)
        self.percentage_amount_sbx.setMaximum(1)
        self.percentage_amount_sbx.setValue(1)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.mount_percent_title_lbl, 0, 0)
        layout.addWidget(self.percentage_amount_sbx, 0, 1)
        layout.addWidget(QtWidgets.QLabel("%"), 0, 2)
        return layout

    def _create_mounted_ui(self):
        self.mounted_title_lbl = QtWidgets.QLabel("Mounted")
        self.mounted_title_lbl.setStyleSheet("font: bold 16px")
        self.mounted_selection_le = QtWidgets.QLineEdit("Select an object to be mounted.")
        self.mounted_selection_le.setMinimumWidth(100)
        self.mounted_select_btn = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.mounted_title_lbl, 0, 0)
        layout.addWidget(self.mounted_selection_le, 0, 1)
        layout.addWidget(self.mounted_select_btn, 0, 2)
        return layout

    def _create_alignment_ui(self):
        self.alignment_title_lbl = QtWidgets.QLabel("Align to Mount Normals")
        self.alignment_title_lbl.setStyleSheet("font: bold")
        self.alignment_cbox = QtWidgets.QCheckBox("Apply")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.alignment_title_lbl, 0, 0)
        layout.addWidget(self.alignment_cbox, 0, 1)
        return layout

    def _create_scale_sbx_ui(self):
        self.min_xscale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_xscale_sbx.setButtonSymbols(QtWidgets.QDoubleSpinBox.PlusMinus)
        self.min_xscale_sbx.setSingleStep(.01)
        self.min_xscale_sbx.setValue(1)
        self.min_xscale_sbx.setFixedWidth(50)

        self.max_xscale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_xscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_xscale_sbx.setSingleStep(.01)
        self.max_xscale_sbx.setValue(2)
        self.max_xscale_sbx.setFixedWidth(50)

        self.min_yscale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_yscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_yscale_sbx.setSingleStep(.01)
        self.min_yscale_sbx.setValue(1)
        self.min_yscale_sbx.setFixedWidth(50)

        self.max_yscale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_yscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_yscale_sbx.setSingleStep(.01)
        self.max_yscale_sbx.setValue(2)
        self.max_yscale_sbx.setFixedWidth(50)

        self.min_zscale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_zscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_zscale_sbx.setSingleStep(.01)
        self.min_zscale_sbx.setValue(1)
        self.min_zscale_sbx.setFixedWidth(50)

        self.max_zscale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_zscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_zscale_sbx.setSingleStep(.01)
        self.max_zscale_sbx.setValue(2)
        self.max_zscale_sbx.setFixedWidth(50)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.max_xscale_sbx, 1, 1)
        layout.addWidget(self.min_xscale_sbx, 2, 1)
        layout.addWidget(self.max_yscale_sbx, 1, 3)
        layout.addWidget(self.min_yscale_sbx, 2, 3)
        layout.addWidget(self.max_zscale_sbx, 1, 5)
        layout.addWidget(self.min_zscale_sbx, 2, 5)
        return layout

    def _create_scale_ui(self):
        layout = self._create_scale_sbx_ui()
        self.scale_title_lbl = QtWidgets.QLabel("Scale")
        self.scale_title_lbl.setStyleSheet("font: bold 16px")
        layout.addWidget(self.scale_title_lbl, 0, 0)
        layout.addWidget(QtWidgets.QLabel("Max X:"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Min X:"), 2, 0)
        layout.addWidget(QtWidgets.QLabel("Max Y:"), 1, 2)
        layout.addWidget(QtWidgets.QLabel("Min Y:"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("Max Z:"), 1, 4)
        layout.addWidget(QtWidgets.QLabel("Min Z:"), 2, 4)
        return layout


    def _create_rotation_sbx_ui(self):
        self.min_xrotation_sbx = QtWidgets.QSpinBox()
        self.min_xrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_xrotation_sbx.setMaximum(360)
        self.min_xrotation_sbx.setFixedWidth(50)

        self.max_xrotation_sbx = QtWidgets.QSpinBox()
        self.max_xrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_xrotation_sbx.setRange(1, 360)
        self.max_xrotation_sbx.setValue(360)
        self.max_xrotation_sbx.setFixedWidth(50)

        self.min_yrotation_sbx = QtWidgets.QSpinBox()
        self.min_yrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_yrotation_sbx.setMaximum(360)
        self.min_yrotation_sbx.setFixedWidth(50)

        self.max_yrotation_sbx = QtWidgets.QSpinBox()
        self.max_yrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_yrotation_sbx.setRange(1, 360)
        self.max_yrotation_sbx.setValue(360)
        self.max_yrotation_sbx.setFixedWidth(50)

        self.min_zrotation_sbx = QtWidgets.QSpinBox()
        self.min_zrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_zrotation_sbx.setMaximum(360)
        self.min_zrotation_sbx.setFixedWidth(50)

        self.max_zrotation_sbx = QtWidgets.QSpinBox()
        self.max_zrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_zrotation_sbx.setRange(1, 360)
        self.max_zrotation_sbx.setValue(360)
        self.max_zrotation_sbx.setFixedWidth(50)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.max_xrotation_sbx, 1, 1)
        layout.addWidget(self.min_xrotation_sbx, 2, 1)
        layout.addWidget(self.max_yrotation_sbx, 1, 3)
        layout.addWidget(self.min_yrotation_sbx, 2, 3)
        layout.addWidget(self.max_zrotation_sbx, 1, 5)
        layout.addWidget(self.min_zrotation_sbx, 2, 5)
        return layout

    def _create_rotation_ui(self):
        layout = self._create_rotation_sbx_ui()
        self.rotation_title_lbl = QtWidgets.QLabel("Rotation")
        self.rotation_title_lbl.setStyleSheet("font: bold 16px")
        layout.addWidget(self.rotation_title_lbl, 0, 0)
        layout.addWidget(QtWidgets.QLabel("Max X:"), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Min X:"), 2, 0)
        layout.addWidget(QtWidgets.QLabel("Max Y:"), 1, 2)
        layout.addWidget(QtWidgets.QLabel("Min Y:"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("Max Z:"), 1, 4)
        layout.addWidget(QtWidgets.QLabel("Min Z:"), 2, 4)
        return layout



class ScatterFile(object):
    """an abstract representation of a scatter file object"""
    def __init__(self):
        self.mount = ''
        self.mounted = ''
        self.scale_range_min = [1, 1, 1]
        self.scale_range_max = [2, 2, 2]
        self.rotation_range_min = [0, 0, 0]
        self.rotation_range_max = [360, 360, 360]

    def select_highlighted(self):
        self.selection = cmds.ls(orderedSelection=True, flatten=True,
                                 long=True)
    # def group_instances(self):
    #     instance_group = cmds.group(empty = True, name=transormName + 'instance+grp#')
    #     cmds.parent(self.mounted_selection_le)

    # def getInstances(self):
    #     instances = []
    #     iterDag = omui.MItDag(omui.MItDag.kBreadthFirst)
    #     while not iterDag.isDone():
    #         instanced = omui.MItDag.isInstanced(iterDag)
    #         if instanced:
    #             instances.append(iterDag.fullPathName())
    #         iterDag.next()
    #     return instances

    # def delete_created_instances(self):
    #     cmds.select(self.getInstances())
    #     cmds.delete(self.getInstances())
        # sel = cmds.ls(selection=True)
        # shapes = cmds.listRelatives(sel[0], shapes=True)
        # cmds.select(cmds.listRelatives(shapes[0], allParents=True))
        # cmds.delete()


    def do_scatter_instance(self):
        self.vertex_names = cmds.polyListComponentConversion(self.selection,
                                                             toVertex=True)
        self.vertex_names = cmds.filterExpand(self.mount,
                                              selectionMask=31, expand=True)
        self.vertex_names_percent = int(round(len(self.vertex_names) * self.vertex_percent))
        self.percent_selection = random.sample(self.vertex_names, k=self.vertex_names_percent)
        self.vtx = ''
        cmds.select(self.percent_selection)
        if cmds.objectType(self.mounted, isType="transform"):
            for self.vtx in self.percent_selection:
                self.scatter = cmds.instance(self.mounted,
                                             name="scatter_instance#")
                pos = cmds.pointPosition(self.vtx)
                cmds.move(pos[0], pos[1], pos[2], self.scatter)
                self.rand_rotation()
                self.rand_scale()
        else:
            print("Please ensure the first object you select is a transform.")

    def checked_normal(self, align):
            if align:
                cmds.normalConstraint(self.percent_selection, self.scatter)
                cmds.delete(constraints=True)
            else:
                print("")

    def rand_rotation(self):
        rand_x = random.randrange(self.rotation_range_min[0],
                                  self.rotation_range_max[0])
        rand_y = random.randrange(self.rotation_range_min[1],
                                  self.rotation_range_max[1])
        rand_z = random.randrange(self.rotation_range_min[2],
                                  self.rotation_range_max[2])
        cmds.rotate(rand_x, rand_y, rand_z, self.scatter)

    def rand_scale(self):
        rands_x = random.uniform(self.scale_range_min[0],
                                   self.scale_range_max[0])
        print(rands_x)
        rands_y = random.uniform(self.scale_range_min[1],
                                   self.scale_range_max[1])
        rands_z = random.uniform(self.scale_range_min[2],
                                   self.scale_range_max[2])
        cmds.scale(rands_x, rands_y, rands_z, self.scatter)
