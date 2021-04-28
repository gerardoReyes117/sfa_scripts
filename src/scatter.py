import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


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
        # self.instance_lay = self._create_instance_ui()
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
        # self.main_lay.addLayout(self.instance_lay)
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
        self.remove_btn.clicked.connect(self._remove_instances_mounted)
        self.alignment_cbox.stateChanged.connect(self._align_normals)

    @QtCore.Slot()
    def _mount_select_highlighted(self):
        self.scatterfile.select_highlighted()
        self.mount_selection_le.setText(','.join(self.scatterfile.selection))

    @QtCore.Slot()
    def _mounted_select_highlighted(self):
        self.scatterfile.select_highlighted()
        self.mounted_selection_le.setText(','.join(self.scatterfile.selection))


    @QtCore.Slot()
    def _align_normals(self):
        return

    @QtCore.Slot()
    def _create_scatter(self):
        self._set_scatterfile_properties_from_ui()
        self.scatterfile.scatter_instance()

    @QtCore.Slot()
    def _remove_instances_mounted(self):
        return

    def _set_scatterfile_properties_from_ui(self):
        self.scatterfile.mount = self.mount_selection_le.text()
        self.scatterfile.mounted = self.mounted_selection_le.text()

    def _create_bottom_buttons_ui(self):
        self.create_btn = QtWidgets.QPushButton("Create")
        self.remove_btn = QtWidgets.QPushButton("Delete")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.create_btn)
        layout.addWidget(self.remove_btn)
        return layout

    def _create_mount_ui(self):
        self.mount_title_lbl = QtWidgets.QLabel("Mount")
        self.mount_title_lbl.setStyleSheet("font: bold 16px")
        self.mount_selection_le = QtWidgets.QLineEdit()
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
        self.percentage_amount_sbx = QtWidgets.QSpinBox()
        self.percentage_amount_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.
                                                    PlusMinus)
        self.percentage_amount_sbx.setFixedWidth(50)
        self.percentage_amount_sbx.setMaximum(100)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.mount_percent_title_lbl, 0, 0)
        layout.addWidget(self.percentage_amount_sbx, 0, 1)
        layout.addWidget(QtWidgets.QLabel("%"), 0, 2)
        return layout

    def _create_mounted_ui(self):
        self.mounted_title_lbl = QtWidgets.QLabel("Mounted")
        self.mounted_title_lbl.setStyleSheet("font: bold 16px")
        self.mounted_selection_le = QtWidgets.QLineEdit()
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

    # def _create_instance_ui(self):
    #     self.instances_title_lbl = QtWidgets.QLabel("Instances")
    #     self.instances_title_lbl.setStyleSheet("font: bold")
    #     self.instance_amount_sbx = QtWidgets.QSpinBox()
    #     self.instance_amount_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.
    #                                               PlusMinus)
    #     self.instance_amount_sbx.setFixedWidth(50)
    #     layout = QtWidgets.QGridLayout()
    #     layout.addWidget(self.instances_title_lbl, 0, 0)
    #     layout.addWidget(self.instance_amount_sbx, 0, 1)
    #     return layout

    def _create_scale_sbx_ui(self):
        self.min_xscale_sbx = QtWidgets.QSpinBox()
        self.min_xscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_xscale_sbx.setFixedWidth(50)
        self.max_xscale_sbx = QtWidgets.QSpinBox()
        self.max_xscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_xscale_sbx.setFixedWidth(50)
        self.min_yscale_sbx = QtWidgets.QSpinBox()
        self.min_yscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_yscale_sbx.setFixedWidth(50)
        self.max_yscale_sbx = QtWidgets.QSpinBox()
        self.max_yscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_yscale_sbx.setFixedWidth(50)
        self.min_zscale_sbx = QtWidgets.QSpinBox()
        self.min_zscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_zscale_sbx.setFixedWidth(50)
        self.max_zscale_sbx = QtWidgets.QSpinBox()
        self.max_zscale_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
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
        self.min_xrotation_sbx.setFixedWidth(50)
        self.max_xrotation_sbx = QtWidgets.QSpinBox()
        self.max_xrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_xrotation_sbx.setFixedWidth(50)
        self.min_yrotation_sbx = QtWidgets.QSpinBox()
        self.min_yrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_yrotation_sbx.setFixedWidth(50)
        self.max_yrotation_sbx = QtWidgets.QSpinBox()
        self.max_yrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_yrotation_sbx.setFixedWidth(50)
        self.min_zrotation_sbx = QtWidgets.QSpinBox()
        self.min_zrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_zrotation_sbx.setFixedWidth(50)
        self.max_zrotation_sbx = QtWidgets.QSpinBox()
        self.max_zrotation_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
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
    def __init__(self, mount=None, mounted=None, instances=0,
                 scale_range=((1, 1), (1, 1), (1, 1)),
                 rotation_range=((0, 0), (0, 0), (0, 0))):
        self.mount = 'Select object to mount on'
        self.mounted = 'Select object to mount'
        self.instances = 0
        self.scale_range = scale_range
        self.rotation_range = rotation_range

    def select_highlighted(self):
        self.selection = cmds.ls(orderedSelection=True, flatten=True,
                                 long=True)

    def scatter_instance(self):
        self.scatter = cmds.instance(self.mounted)


#selection = cmds.ls(orderedSelection=True, flatten=True)
# print(selection)
# vtx_selection = cmds.polyListComponentConversion(selection, toVertex=True)
# print(cmds.filterExpand(vtx_selection, selectionMask=31, expand=True))]
# cmds.select(vtx_selection)
# for obj in selection:
#     if 'vtx[' not in obj:
#         selection.remove(obj)
# print(selection)
# cmds.filterExpand(selection, selectionMask=31, expand=True)
# for obj in selection:
#     print(cmds.ls(obj + ".vtx[*]", flatten=True))
# vtx_selection = cmds.polyListComponentConversion("pSphere1", toVertex=True)
# vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31)
# -cmds.select(vtx_selection)
# scattered_instances = []
# for vtx in vtx_selection:
#     scatter_instance = cmds.instance("pCube1", name="pCube5")
#     scattered_instances.extend(scatter_instance)
#    #pos = cmds.xform([vtx], query=True, translation=True)
#     pos = cmds.pointPosition([vtx])
#     cmds.xform(scatter_instance, translation=pos)
#
# cmds.group(scattered_instances, name="scattered")
# cmds.select(vtx_selection)