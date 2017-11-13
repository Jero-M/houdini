'''
Author: Jeronimo Maggi
Houdini Version: 16.5.268

Copy the parameter values from one node to another, based on
the parameter name.
'''

from PySide2 import QtWidgets, QtGui, QtCore


class CopyValues(QtWidgets.QDialog):
    
    def __init__(self, *args, **kwargs):
        super(CopyValues, self).__init__(*args, **kwargs)
        self.setMinimumSize(500,90)
        self.setWindowTitle("Copy Values")
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window) 
        self.setStyleSheet(hou.qt.styleSheet())

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.copy_from_label = QtWidgets.QLabel("Copy From", self)
        self.gridLayout.addWidget(self.copy_from_label, 0, 0, 1, 1)
        self.copy_from_text = QtWidgets.QLineEdit(self)
        self.copy_from_text.setAcceptDrops(True)
        self.gridLayout.addWidget(self.copy_from_text, 0, 1, 1, 1)
        self.from_button = hou.qt.createNodeChooserButton()
        self.gridLayout.addWidget(self.from_button, 0, 2, 1, 1)
        self.copy_to_label = QtWidgets.QLabel("Copy To", self)
        self.gridLayout.addWidget(self.copy_to_label, 1, 0, 1, 1)
        self.copy_to_text = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.copy_to_text, 1, 1, 1, 1)
        self.to_button = hou.qt.createNodeChooserButton()
        self.gridLayout.addWidget(self.to_button, 1, 2, 1, 1)
        self.copy_button = QtWidgets.QPushButton("Copy Values", self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_button.sizePolicy().hasHeightForWidth())
        self.copy_button.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.copy_button, 2, 1, 1, 1)

        self.from_button.nodeSelected.connect(self.update_from_text)
        self.to_button.nodeSelected.connect(self.update_to_text)
        self.connect(self.copy_button, QtCore.SIGNAL('clicked()'), self.copy)

    def update_from_text(self, node):
        self.copy_from_text.clear()
        self.copy_from_text.insert(node.path())

    def update_to_text(self, node):
        self.copy_to_text.clear()
        self.copy_to_text.insert(node.path())

    def copy(self):
        copy_from_node = hou.node(self.copy_from_text.text())
        copy_to_node = hou.node(self.copy_to_text.text())
        
        for parm in copy_from_node.parms():
            if type(parm.eval()) == type(hou.Ramp()):
                ramp_name = parm.name()
                shader_ramp = copy_to_node.parm(ramp_name)
                shader_ramp.set(parm.eval())
            elif not parm.isMultiParmInstance() and parm.isSpare():
                parm_name = parm.name()
                try:
                    shader_parm = copy_to_node.parm(parm_name)
                    shader_parm.set(parm.eval())
                except:
                    continue
                    

copy_values = CopyValues()
copy_values.show()