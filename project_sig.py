# -*- coding: utf-8 -*-
import math
import sys
import os
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
import qgis
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QFileDialog, QMainWindow, QMessageBox
from functools import partial


registry = QgsMapLayerRegistry.instance()
#legend = iface.legendInterface()


class GeneraLine:
    class Algorithms:
        MC_MASTER = 'MC_MASTER'
        DOUGLAS_PEUCKER = 'DOUGLAS_PEUCKER'

    Algorithms = Algorithms

    algorithms = [Algorithms.MC_MASTER, Algorithms.DOUGLAS_PEUCKER]

    def __init__(self, layer = None):

        self.layer_salida = None

        if layer :
            self.setLayer(layer)

    def setLayer(self, layer):
        self.layer = layer

        #EPSG
        self.__crs = layer.crs().authid()

        # Elementos de la capa
        #self.__features = layer.getFeatures()

        self.layer_salida = QgsVectorLayer( 'LineString?crs={}'.format(self.__crs)
                                        , 'generalizacion_{}'.format(self.layer.name())
                                        , 'memory' )

        symbols = self.layer_salida.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QtGui.QColor.fromRgb(102, 102, 255))

        registry.addMapLayer(self.layer)

        registry.addMapLayer(self.layer_salida)


    def applyAlgorithm(self, name, param):

        if name not in self.algorithms :
            return None

        with edit(self.layer_salida):
            try :
                listOfIds = [feat.id() for feat in self.layer_salida.getFeatures()]
                self.layer_salida.deleteFeatures( listOfIds )
                #self.layer_salida.startEditing()

                #Para recorrer todos los elementos de la capa
                for feature in self.layer.getFeatures():
                    # Guarda la geometria en geom
                    geom = feature.geometry()
                    temp_feature = QgsFeature()

                    if not geom : continue
                    if geom.isMultipart():
                        #print 'multipart'

                        for geom_ in geom.asGeometryCollection():
                            temp_feature.setGeometry(geom_)
                            points = self.__extractPoints(temp_feature)
                            # Se crea un nuevo feature
                            f = QgsFeature()

                            if name == self.Algorithms.MC_MASTER:
                                dp = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                            else :
                                dp = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]

                            linedp = QgsGeometry.fromPolyline(dp)
                            f.setGeometry(linedp)

                            self.layer_salida.addFeature(f)

                    else :
                        points = self.__extractPoints(feature)

                        # Se crea un nuevo feature
                        f = QgsFeature()

                        if name == self.Algorithms.MC_MASTER:
                            dp = [ QgsPoint(*x) for x in self.__mcMaster(points, param) if len(x) > 1 ]
                        else :
                            dp = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) if len(x) > 1 ]


                        linedp = QgsGeometry.fromPolyline(dp)
                        f.setGeometry(linedp)

                        self.layer_salida.addFeature(f)

            except Exception as e:

                print 'error', e

    def __shortestDistance(self,point, line):
        xp, yp = point
        a, b, c = line
        return math.fabs(a*xp + b*yp + c)/math.sqrt(a**2 + b**2)

    def __extractPoints(self, feature):
        geom = feature.geometry()

        points = []

        if geom == None: return points

        i = 0

        while(geom.vertexAt(i) != QgsPoint(0,0)):
            points.append(geom.vertexAt(i))
            i += 1

        return points

    def __mcMaster(self, points, mu):
            if not points : return []

            half_mu = int(math.floor(mu/2))

            end = len(points)

            x0, y0 = points[0]
            x1, y1 = points[-1]

            smooth_points = []
            smooth_points.append([x0,y0])

            for i in range(half_mu, end - half_mu):

                xactual, yactual = points[i]

                computed_points = points[i - half_mu : i + (mu + 1)/2]

                xcoords = [p[0] for p in computed_points]
                ycoords = [p[1] for p in computed_points]

                mediax, mediay = sum(xcoords)/len(xcoords), sum(ycoords)/len(ycoords)

                x, y = (mediax + xactual)/2, (mediay + yactual)/2
                smooth_points.append([x, y])

            smooth_points.append([x1,y1])

            return smooth_points

    def  __douglasPeucker(self,points, epsilon):
        dmax = 0
        index = 0

        end = len(points) - 1
        x0, y0 = points[0]
        x1, y1 = points[-1]


        a = y1 - y0
        b = -(x1 - x0)
        c = a*(-x0) - b*y0


        # Si el primer y el Último punto son el mismo
        if a == 0 and b == 0 : return []

        for i in range(1, end):
            p = points[i]

            d = self.__shortestDistance(p, [a, b, c])

            if d > dmax :
                index = i
                dmax = d

        if dmax >= epsilon :
            res_ini = self.__douglasPeucker(points[: index + 1], epsilon)
            res_fin = self.__douglasPeucker(points[index : ], epsilon)

            return res_ini[:-1] + res_fin

        else :
            return [ points[0], points[-1] ]



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.original = None

        self.preview = None

        self.folder= None

        self.__init_ui()

        self.simplify = GeneraLine()

        self.Algorithms = GeneraLine.Algorithms



        self.btn_prev_dp.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.DOUGLAS_PEUCKER) )

        self.btn_prev_mcm.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.MC_MASTER) )

        self.btn_load_shp.clicked.connect(self.__openDialog)

        self.btn_sal.clicked.connect(self.__openDialog_folder)


        self.scaleControl.scaleChanged.connect(self.on_scale_changed)


        self.canvas.scaleChanged.connect(self.on_canvas_scale_changed)


        self.cb_dp.stateChanged.connect(self.activaGuardar)
        self.cb_mcm.stateChanged.connect(self.activaGuardar)


        self.btn_do.clicked.connect(self.guardaSHP)


    def guardaSHP(self):

        if self.cb_dp.isChecked():

            self.simplify.applyAlgorithm(self.Algorithms.DOUGLAS_PEUCKER, self.spn_dp.value())

            filepath = os.path.join( self.folder
                                    , '{}_{}_{}_{}'.format(
                                            'DOUGLAS_PEUCKER'
                                            , self.spn_dp.value()
                                            , self.simplify.layer.name()
                                            , '.shp') )
            QgsVectorFileWriter.writeAsVectorFormat(self.simplify.layer_salida, filepath, 'utf-8', None, "ESRI Shapefile")

        if self.cb_mcm.isChecked():

            self.simplify.applyAlgorithm(self.Algorithms.MC_MASTER, self.spn_mcm.value())

            filepath = os.path.join( self.folder
                                    , '{}_{}_{}_{}'.format(
                                            'MC_MASTER'
                                            , self.spn_mcm.value()
                                            , self.simplify.layer.name()
                                            , '.shp') )
            QgsVectorFileWriter.writeAsVectorFormat(self.simplify.layer_salida, filepath, 'utf-8', None, "ESRI Shapefile")


    def activaGuardar(self):
        if self.cb_dp.isChecked() or self.cb_mcm.isChecked():
            if self.folder:
                self.btn_do.setEnabled(True)
        else:
            self.btn_do.setEnabled(False)


    def __showPreviewCanvas(self, algorithm) :
        print algorithm
        if algorithm == self.Algorithms.DOUGLAS_PEUCKER :
            param = self.spn_dp.value()
        else :
            param = self.spn_mcm.value()

        print param

        self.simplify.applyAlgorithm(algorithm, param)

        self.cb_suav.setEnabled(True)
        self.cb_suav.setCheckState(Qt.Checked)

        self.addLayerToPreviewCanvas(self.simplify.layer, self.simplify.layer_salida)



    def addLayerToPreviewCanvas(self, original, preview):
        #self.original = QgsMapCanvasLayer(original)
        self.preview = QgsMapCanvasLayer(preview)
        self.cb_suav.clicked.connect( partial(self.toggleCanvasVisibilityLayer, self.preview) )
        #self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )
        self.canvas.setLayerSet([ self.original, self.preview ])

    def __openDialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        # Solo mostrar archivos con extensiÃÂ³n shp
        dlg.setFilter("shapefile (*.shp)")

        if dlg.exec_():
            # Obtenemos la ruta del archivo
            filepath = map(str, list(dlg.selectedFiles()))[0]
            self.__addLayer(filepath)

    def __openDialog_folder(self):
        self.folder = QFileDialog().getExistingDirectory()

        self.label_selected_folder.setText(self.folder)

        self.activaGuardar()

    def __addLayer(self, path):

        layer = QgsVectorLayer(path, os.path.basename(path), "ogr")

        if not layer.geometryType()==1:
            QMessageBox.information(None,'Warning', 'No se trata de una capa LineString')
            return


        self.original = QgsMapCanvasLayer(layer)

        self.simplify.setLayer(layer)

        self.canvas.setExtent(layer.extent())

        self.canvas.setLayerSet([self.original])

        symbols = layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QtGui.QColor.fromRgb(204, 51, 51))

        self.btn_prev_dp.setEnabled(True)
        self.btn_prev_mcm.setEnabled(True)
        #self.cb_suav.setEnabled(True)
        self.cb_ori.setEnabled(True)
        self.cb_ori.setCheckState(Qt.Checked)
        self.cb_dp.setEnabled(True)
        self.cb_mcm.setEnabled(True)
        #self.cb_suav.setEnabled(False)
        self.btn_zoom.setEnabled(True)
        self.spn_dp.setEnabled(True)
        self.spn_mcm.setEnabled(True)
        self.scaleControl.setEnabled(True)


        self.canvas.mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(layer.crs().authid()))

        self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )


        self.label_shp_path.setText(layer.name())

        self.btn_zoom.clicked.connect( partial( self.zoomExt, layer ) )

    def zoomExt(self,layer):
        print 'zoomExt'
        #self.canvas.setExtent(rendererV2.fullExtent())
        self.canvas.setExtent(layer.extent())
        self.canvas.refresh()

    def toggleCanvasVisibilityLayer(self, layer):
        #visibility = legend.isLayerVisible(layer)
        #legend.setLayerVisible(layer,not visibility)
        visibility = layer.isVisible()

        layer.setVisible(not visibility)
        layerSet = [ l for l in [self.original, self.preview] if l]
        self.canvas.setLayerSet(layerSet)
        self.canvas.refresh()

    def on_scale_changed(self):
        #print("Scale changed")
        iface.mapCanvas().zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )
        self.canvas.zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )
        self.canvas.refresh()

    def on_canvas_scale_changed(self, scale):
        #print scale
        self.scaleControl.setScale(1 / scale)


    def __init_ui(self):
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setObjectName(_fromUtf8("tabs"))
        self.tab_dp = QtGui.QWidget()
        self.tab_dp.setAcceptDrops(False)
        self.tab_dp.setObjectName(_fromUtf8("tab_dp"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_dp)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.tab_dp)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.spn_dp = QtGui.QDoubleSpinBox(self.tab_dp)
        self.spn_dp.setEnabled(False)
        self.spn_dp.setMaximum(9999999.0)
        self.spn_dp.setObjectName(_fromUtf8("spn_dp"))
        self.horizontalLayout_5.addWidget(self.spn_dp)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)


        self.btn_prev_dp = QtGui.QPushButton(self.tab_dp)
        self.btn_prev_dp.setEnabled(False)
        self.btn_prev_dp.setObjectName(_fromUtf8("btn_prev_dp"))
        self.horizontalLayout_2.addWidget(self.btn_prev_dp)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.tabs.addTab(self.tab_dp, _fromUtf8(""))
        self.tab_mcm = QtGui.QWidget()
        self.tab_mcm.setObjectName(_fromUtf8("tab_mcm"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_mcm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_8 = QtGui.QLabel(self.tab_mcm)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_6.addWidget(self.label_8)
        self.spn_mcm = QtGui.QSpinBox(self.tab_mcm)
        self.spn_mcm.setEnabled(False)
        self.spn_mcm.setMinimum(3)
        self.spn_mcm.setMaximum(999)
        self.spn_mcm.setSingleStep(2)
        self.spn_mcm.setProperty("value", 3)
        self.spn_mcm.setObjectName(_fromUtf8("spn_mcm"))
        self.horizontalLayout_6.addWidget(self.spn_mcm)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)


        self.btn_prev_mcm = QtGui.QPushButton(self.tab_mcm)
        self.btn_prev_mcm.setEnabled(False)
        self.btn_prev_mcm.setObjectName(_fromUtf8("btn_prev_mcm"))
        self.horizontalLayout_10.addWidget(self.btn_prev_mcm)


        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.tabs.addTab(self.tab_mcm, _fromUtf8(""))
        self.tab_sal = QtGui.QWidget()
        self.tab_sal.setObjectName(_fromUtf8("tab_sal"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_sal)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_sal = QtGui.QToolButton(self.tab_sal)
        self.btn_sal.setAcceptDrops(False)
        self.btn_sal.setObjectName(_fromUtf8("btn_sal"))
        self.horizontalLayout.addWidget(self.btn_sal)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.scrollArea_2 = QtGui.QScrollArea(self.tab_sal)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 380, 70))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))

        self.label_selected_folder = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.label_selected_folder.setObjectName(_fromUtf8("label_selected_folder"))
        self.horizontalLayout_11.addWidget(self.label_selected_folder)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        self.tabs.addTab(self.tab_sal, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabs)

        self.map_controls_container = QtGui.QHBoxLayout()
        self.map_controls_container.setContentsMargins(-1, 0, -1, -1)
        self.map_controls_container.setObjectName(_fromUtf8("map_controls_container"))

        self.cb_suav = QtGui.QCheckBox(self.centralwidget)
        self.cb_suav.setObjectName(_fromUtf8("Suavizado"))
        self.map_controls_container.addWidget(self.cb_suav)

        self.cb_ori = QtGui.QCheckBox(self.centralwidget)
        self.cb_ori.setObjectName(_fromUtf8("Original"))
        self.map_controls_container.addWidget(self.cb_ori)


        self.btn_zoom = QtGui.QPushButton(self.centralwidget)
        self.btn_zoom.setObjectName(_fromUtf8("Zoom extensión"))
        self.map_controls_container.addWidget(self.btn_zoom)


        self.canvas_container = QtGui.QHBoxLayout()
        self.canvas_container.setObjectName(_fromUtf8("canvas_container"))


        self.canvas = QgsMapCanvas()
        self.canvas_container.addWidget( self.canvas )



        self.scaleControl = QgsScaleWidget()
        self.scaleControl.setMapCanvas(self.canvas)
        self.scaleControl.setScaleFromCanvas()
        self.scaleControl.setEnabled(False)
        self.map_controls_container.addWidget( self.scaleControl )

        self.verticalLayout_3.addLayout(self.map_controls_container)

        self.verticalLayout_3.addLayout(self.canvas_container)


        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_3.addWidget(self.line_2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))


        self.cb_dp = QtGui.QCheckBox(self.centralwidget)
        self.cb_dp.setEnabled(False)
        self.cb_dp.setObjectName(_fromUtf8("cb_dp"))
        self.horizontalLayout_8.addWidget(self.cb_dp)

        self.cb_mcm = QtGui.QCheckBox(self.centralwidget)
        self.cb_mcm.setEnabled(False)
        self.cb_mcm.setObjectName(_fromUtf8("cb_mcm"))
        self.horizontalLayout_8.addWidget(self.cb_mcm)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_3.addWidget(self.line)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_3.addWidget(self.label_7)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 404, 69))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_shp_path = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_shp_path.setObjectName(_fromUtf8("label_shp_path"))
        self.verticalLayout_4.addWidget(self.label_shp_path)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))

        self.btn_load_shp = QtGui.QPushButton(self.centralwidget)
        self.btn_load_shp.setObjectName(_fromUtf8("btn_load_shp"))
        self.horizontalLayout_12.addWidget(self.btn_load_shp)

        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.btn_do = QtGui.QPushButton(self.centralwidget)
        self.btn_do.setEnabled(False)
        self.btn_do.setObjectName(_fromUtf8("btn_do"))
        self.horizontalLayout_12.addWidget(self.btn_do)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 424, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        self.label_2.setText(_translate("MainWindow", "Epsilon", None))
        self.btn_prev_dp.setText(_translate("MainWindow", "Previsualizar", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_dp), _translate("MainWindow", "Generalización Douglas-Peucker", None))
        self.label_8.setText(_translate("MainWindow", "μ", None))
        self.btn_prev_mcm.setText(_translate("MainWindow", "Previsualizar", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_mcm), _translate("MainWindow", "Suavizado McMaster", None))
        self.btn_sal.setText(_translate("MainWindow", "Seleccione la carpeta de salida...", None))
        self.label_selected_folder.setText(_translate("MainWindow", "Ninguna carpeta seleccionada", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_sal), _translate("MainWindow", "Carpeta de salida", None))


        self.cb_suav.setText(_translate("MainWindow", "Suavizado", None))
        self.cb_suav.setEnabled(False)
        self.cb_ori.setText(_translate("MainWindow", "Original", None))
        self.cb_ori.setEnabled(False)

        self.btn_zoom.setText(_translate("MainWindow", "Zoom Extensión", None))
        self.btn_zoom.setEnabled(False)

        self.cb_dp.setText(_translate("MainWindow", "Douglas-Peucker", None))
        self.cb_mcm.setText(_translate("MainWindow", "McMaster", None))
        self.label_7.setText(_translate("MainWindow", "Shapefile de entrada (shp)", None))
        self.label_shp_path.setText(_translate("MainWindow", "Ningún archivo SHP seleccionado", None))
        self.btn_load_shp.setText(_translate("MainWindow", "SHP", None))
        self.btn_do.setText(_translate("MainWindow", "Guardar", None))



window = MainWindow()
window.show()
