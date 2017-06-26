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

# Es necesario ejecutar el script desde el entorno de QGis

registry = QgsMapLayerRegistry.instance()
#legend = iface.legendInterface()


'''
@class: Algorithms
@brief: namespace para los algoritmos
'''
class Algorithms:
    MC_MASTER = 'MC_MASTER'
    DOUGLAS_PEUCKER = 'DOUGLAS_PEUCKER'

'''
@class: GeneraLine
@brief: Clase que servirá para ejecutar los algoritmos
        de suavizado y reducción de puntos sobre una capa de Líneas
@param: layer - Capa de entrada
'''
class GeneraLine:

    # Variable de clase estática que almacena la clase Algoritmos
    Algorithms = Algorithms

    # Lista con los algoritmos posibles
    algorithms = [Algorithms.MC_MASTER, Algorithms.DOUGLAS_PEUCKER]

    # Constructor
    def __init__(self, layer = None):

        # Variable de clase self.layer_salida
        # Almacenará las features de salida
        self.layer_salida = None

        # Si se le pasa layer al constructor
        if layer :
            # Asignamos la capa como variable de clase
            self.setLayer(layer)

    '''
    @method: setLayer
    @brief: Asignamos como variable de clase la capa que se le pasa
            y creamos la capa de salida en memoria (layer_salida)
            con los parámetros de la capa de entrada (crs, nombre, ...)
    '''
    def setLayer(self, layer):
        # Asignamos la capa
        self.layer = layer

        # Obtenemos el EPSG
        self.__crs = layer.crs().authid()

        # Creamos la capa layer_salida - se guarda en memoria
        self.layer_salida = QgsVectorLayer( 'LineString?crs={}'.format(self.__crs)
                                        , 'generalizacion_{}'.format(self.layer.name())
                                        , 'memory' )

        # Cambiamos la simbología
        symbols = self.layer_salida.rendererV2().symbols()
        symbol = symbols[0]
        # Cambiamos el color de la capa de salida a un tono azulado
        symbol.setColor(QtGui.QColor.fromRgb(102, 102, 255))

        # Añadimos las capas al registro de QGIS
        registry.addMapLayer(self.layer)
        registry.addMapLayer(self.layer_salida)


    '''
    @method: applyAlgorithm
    @brief: Aplica el algoritmo sobre la capa de entrada y guarda el resultado
            en la capa de salida

    @param: name - nombre del algoritmo a aplicar (namespace Algorithms)
    '''
    def applyAlgorithm(self, name, param):

        # Comprobamos el nombre del algoritmo
        if name not in self.algorithms : return None

        # Comenzamos la edición sobre la capa de salida
        with edit(self.layer_salida):
            # Metemos la lógica dentro de un bloque try-except
            try :
                # Eliminamos las features que puedan haber
                # en la capa de salida (de proceso anteriores)
                listOfIds = [feat.id() for feat in self.layer_salida.getFeatures()]
                self.layer_salida.deleteFeatures( listOfIds )

                # Recorreremos todas las features de la capa de entrada
                for feature in self.layer.getFeatures():

                    # Obtenemos una referencia de la geometría
                    geom = feature.geometry()

                    # Creamos una feature temporal
                    # Servirá para recorrer geometrías multiparte
                    temp_feature = QgsFeature()

                    # Comprobamos la geomtría
                    if not geom : continue

                    # Se crea un nuevo feature (temporal)
                    # Servirá para crear la feature de la capa de salida
                    f = QgsFeature()


                    # Si la geometría es multiparte (MULTILINESTRING)
                    if geom.isMultipart():
                        # Recorremos cada LineString (geom) dentro del MultiLineString
                        for geom_ in geom.asGeometryCollection():

                            # Asignamos la geometría a la feature temporal
                            temp_feature.setGeometry(geom_)

                            # Extraemos los puntos de la geomtría
                            points = self.__extractPoints(temp_feature)

                            # Ejecutamos el algoritmo pertinente
                            # sobre los puntos extraidos de la geometría que estamos recorriendo
                            if name == self.Algorithms.MC_MASTER:
                                resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                            else :
                                resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]

                            # Obtenemoss la geometría (Polyline) resultante de aplicar el algoritmo
                            resultLine = QgsGeometry.fromPolyline(resultPoints)
                            # Añadimos la geomtría a la feature temporal
                            f.setGeometry(resultLine)

                            # Añadimos la feature a la capa de salida
                            self.layer_salida.addFeature(f)

                    # Si la geometría no es multiparte
                    else :

                        # Extraemos los puntos de la geomtría
                        points = self.__extractPoints(feature)

                        # Se crea un nuevo feature (temporal)
                        # Servirá para crear la feature de la capa de salida
                        f = QgsFeature()

                        # Ejecutamos el algoritmo pertinente
                        # sobre los puntos extraidos de la geometría que estamos recorriendo
                        if name == self.Algorithms.MC_MASTER:
                            resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                        else :
                            resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]


                        # Obtenemoss la geometría (Polyline) resultante de aplicar el algoritmo
                        resultLine = QgsGeometry.fromPolyline(resultPoints)
                        # Añadimos la geomtría a la feature temporal
                        f.setGeometry(resultLine)

                        # Añadimos la feature a la capa de salida
                        self.layer_salida.addFeature(f)
            # Si se produce una excepción
            except Exception as e:
                # mostramos un mensaje de error
                QMessageBox.information(None, 'ERROR!', str(e))

                print 'error', e

    '''
    @method: __shortestDistance
    @brief: Devuelve la ditancia más corta entre
            un punto y una recta
    @param: point - lista con los valores x,y del punto ej: [1000, 1000]
    @param: line: lista con los parámetros a,b,c que definen una línea ax + by + c = 0
    @return: double - distancia más corta
    '''
    def __shortestDistance(self,point, line):
        # Extraemos las coordenadas del punto
        xp, yp = point
        # Extraemos los parámetros de la línea
        a, b, c = line
        # Calculamos y deolvemos la ditancia mínima entre el punto y la recta
        return math.fabs(a*xp + b*yp + c)/math.sqrt(a**2 + b**2)

    '''
    @method: __extractPoints
    @brief: Extrae los puntos de una feature (simple)
    @param: feature - feature de entrada
    @return: [] - lista de puntos de la geomtría del feature pasado como parámetro
    '''
    def __extractPoints(self, feature):
        # Obtenemos una referencia de la geometría
        geom = feature.geometry()

        # Creamos una lista vacía
        points = []

        # Comprobamos que la geometría no sea None
        # En cuyo caso devolvemos una lista vacía
        if geom == None: return points

        # contador
        i = 0

        # Bucle while que recorre los  vértices de
        # la geometría
        while(geom.vertexAt(i) != QgsPoint(0,0)):
            # Obtenemos el vértice según el ídice i
            # y lo añadimos a la lista
            points.append(geom.vertexAt(i))
            # aumentamos el contador en 1
            i += 1

        # Devolvemos la lista
        return points

    '''
    @method: __mcMaster
    @brief: Aplica el algoritmo de generalización de McMaster
    @param: points - lista de puntos de la geomtría de la capa de entrada
    @param:  mu - número de vertices que entran en el cálculo de la media (impar > 1)
    @return: [] - lista de puntos con las coordenadas de la línea suavizada
    '''
    def __mcMaster(self, points, mu):
            # Si no hay puntos devuelve una lista vacía
            if not points : return []
            # Parámetro para el vecindario de cada vertice
            half_mu = int(math.floor(mu/2))
            # Longitud de la lista de puntos
            end = len(points)

            # Lista con los puntos del suavizado
            # empezamos añadiendo los puntos primeros que quedan fuera del rango
            # [0, half_mu)
            smooth_points = map( list, points[ : half_mu ] )
            #print smooth_points

            # Generamos un iterador para obtener los índices de los puntos de los
            # cuales podemos aplicar un vecindario de mu
            for i in range(half_mu, end - half_mu):

                # Obtenemos el punto situado en medio del vecindario
                xactual, yactual = points[i]

                # Obtenemos los puntos que forman parte del vecindario
                computed_points = points[i - half_mu : i + (mu + 1)/2]

                # Obtenemos las coordenadas de los puntos en listas (una para cada coord)
                xcoords = [p[0] for p in computed_points]
                ycoords = [p[1] for p in computed_points]

                # Obtenemos la media geométrica de los puntos que conforman el vecindario
                mediax, mediay = sum(xcoords)/len(xcoords), sum(ycoords)/len(ycoords)


                # Y realizamos la media geométrica con la media del vecindario y el punto
                # de estudio
                x, y = (mediax + xactual)/2, (mediay + yactual)/2
                # Finalmente lo añadimos a la lista de puntos del suavizado
                smooth_points.append([x, y])

            # finalizamos añadiendo los puntos primeros que quedan fuera del rango
            # [end - half_mu, end)
            smooth_points += map( list, points[ -half_mu : ] )

            # Devuelve una lista con los puntos de la linea suavizada por el algoritmo
            # McMaster
            return smooth_points

    '''
    @method: __douglasPeucker
    @brief: Aplica el algoritmo de generalización de Douglas-Peucker
    @param: points - lista de puntos de la geomtría de la capa de entrada
    @param:  epsilon - distancia mínima para incluir el vértice
    @return: [] - lista de puntos con las coordenadas de la línea generalizada
    '''
    def  __douglasPeucker(self,points, epsilon):
        # Distancia máxima
        dmax = 0
        # Índice de la posición en la lista del punto de máxima distancia
        index = 0

        # Índice final para el bucle
        end = len(points) - 1

        # Punto inicial
        x0, y0 = points[0]
        # Punto final
        x1, y1 = points[-1]

        # Parámetros de la recta
        a = y1 - y0
        b = -(x1 - x0)
        c = a*(-x0) - b*y0


        # Si el primer y el último punto son el mismo
        if a == 0 and b == 0 : return []

        # Generamos un iterador para obtener los índices
        for i in range(1, end):

            # punto
            p = points[i]

            # distancia más corta entre el punto y la recta
            d = self.__shortestDistance(p, [a, b, c])

            # Si la distancia es mayor que lo que haya almacenado en dmax
            if d > dmax :
                # Guardamos el índice y la distancia en las variables
                index = i
                dmax = d

        # Si la ditancia máxima es mayor o igual que epsilon
        if dmax >= epsilon :
            # Realizamos el algoritmo

            # res_ini almacenará los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porción de la lista de puntos desde 0 hasta el índice
            # del punto de "distancia máxima sobre la recta" + 1
            res_ini = self.__douglasPeucker(points[: index + 1], epsilon)

            # res_fin almacenará los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porción de la lista de puntos desde el índice
            # del punto de "distancia máxima sobre la recta" hasta len(points)
            res_fin = self.__douglasPeucker(points[index : ], epsilon)

            # Juntamos las dos listas resultantes y devolvemos el array juntado
            return res_ini[:-1] + res_fin

        # Si la distancia máxima es menor que epsilon
        else :
            # Devolvemos una lista con los puntos inicial y final
            return [ points[0], points[-1] ]



'''
##############
# FORMULARIO #
##############
'''
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


# Clase MainWindow
class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        QMainWindow.__init__(self)

        # Capa original
        self.original = None

        # Capa para mostrar la previsualización
        self.preview = None

        # Carpeta de salida de datos
        self.folder= None

        # Objeto de la clase GeneraLine (para aplicar algoritmos sobre la capa)
        self.simplify = GeneraLine()

        # namespace Algorithms (Contiene los nombres de los algorritmos)
        self.Algorithms = GeneraLine.Algorithms

        # Inicializamos el formulario
        self.__init_ui()

        # Conectamos los eventos con los funciones

        # Botón previsualizar algoritmo Douglas Peucker
        self.btn_prev_dp.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.DOUGLAS_PEUCKER) )

        # Botón previsualizar algoritmo McMaster
        self.btn_prev_mcm.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.MC_MASTER) )

        # Botón cargar SHP
        self.btn_load_shp.clicked.connect(self.__openDialog)

        # Botón abrir diálogo para seleccionar carpeta de salida
        self.btn_sal.clicked.connect(self.__openDialog_folder)

        # Control de escala - Cuando se modifique la escala en el widget
        self.scaleControl.scaleChanged.connect(self.on_scale_changed)

        # Cuando cambia la escala en el canvas
        self.canvas.scaleChanged.connect(self.on_canvas_scale_changed)

        # Checkbox Algoritmo McMaster
        self.cb_dp.stateChanged.connect(self.activaGuardar)

        # Checkbox Algoritmo Douglas Peucker
        self.cb_mcm.stateChanged.connect(self.activaGuardar)

        # Botón Guardar
        self.btn_do.clicked.connect(self.guardaSHP)

    '''
    @method: guardaSHP
    @brief: Guarda los resultados en shapefile en el directorio de salida
            dependiendo de los checbox marcados
    '''
    def guardaSHP(self):

        # Si el checbox del algoritmo douglas peucker está marcado
        if self.cb_dp.isChecked():

            # Aplicamos el algoritmo
            self.simplify.applyAlgorithm(self.Algorithms.DOUGLAS_PEUCKER, self.spn_dp.value())

            # Obtenemos el string con la ruta de salida del shapefile
            filepath = os.path.join( self.folder
                                    , '{}_{}_{}_{}'.format(
                                            'DOUGLAS_PEUCKER'
                                            , self.spn_dp.value()
                                            , self.simplify.layer.name()
                                            , '.shp') )

            # Guardamos la capa
            QgsVectorFileWriter.writeAsVectorFormat(self.simplify.layer_salida, filepath, 'utf-8', None, "ESRI Shapefile")

        # Si el checbox del algoritmo McMaster está marcado
        if self.cb_mcm.isChecked():

            # Aplicamos el algoritmo
            self.simplify.applyAlgorithm(self.Algorithms.MC_MASTER, self.spn_mcm.value())

            # Obtenemos el string con la ruta de salida del shapefile
            filepath = os.path.join( self.folder
                                    , '{}_{}_{}_{}'.format(
                                            'MC_MASTER'
                                            , self.spn_mcm.value()
                                            , self.simplify.layer.name()
                                            , '.shp') )

            # Guardamos la capa
            QgsVectorFileWriter.writeAsVectorFormat(self.simplify.layer_salida, filepath, 'utf-8', None, "ESRI Shapefile")

        # Mostramos un mensaje de información
        QMessageBox.information(None, u'Éxito', u'Guardado con éxito en : '+ str(self.folder))

    '''
    @method: activaGuardar
    @brief: Activa el botón de guardar dependiendo de los checbox marcados
            y si se ha especificado carpeta de salida
    '''
    def activaGuardar(self):

        # Si el checbox de el algoritmo Douglas Peucker está marcado
        if self.cb_dp.isChecked() or self.cb_mcm.isChecked():
            # Si se ha especificado carpeta de salida
            if self.folder:
                # Activamos el botón de guardar
                self.btn_do.setEnabled(True)

        # Si ningún checbox está marcado
        else:
            # Desactivamos el botón de guardar
            self.btn_do.setEnabled(False)


    '''
    @method: __showPreviewCanvas
    @brief: Muestra la previsualización de aplicar el algoritmo con el parámetro
            seleccionado
    @param: algorithm - nombre del algoritmo a aplicar
    '''
    def __showPreviewCanvas(self, algorithm) :

        # Si el algoritmo seleccionado es Douglas-Peucker
        if algorithm == self.Algorithms.DOUGLAS_PEUCKER :
            # El parametro será el específicado en el spiner de Douglas-Peucker
            param = self.spn_dp.value()
        else :
            # El parametro será el específicado en el spiner de McMaster
            param = self.spn_mcm.value()

        # Aplicamos el algoritmo con el parámetro introducido sobre la capa
        self.simplify.applyAlgorithm(algorithm, param)

        # Se activa el checkbox de suavizado
        self.cb_suav.setEnabled(True)

        # El checkbox de suavizado se pone en checked (ya que la capa se encuentra visible)
        self.cb_suav.setCheckState(Qt.Checked)

        # Asignamos a la capa preview un objeto de la clase QgsMapCanvasLayer a partir de
        # la capa de salida almacenada en el objeto de la clase GeneraLine
        self.preview = QgsMapCanvasLayer(self.simplify.layer_salida)

        # Conectamos al checkbox la función para cambiar la visualización de la capa generalizada
        self.cb_suav.clicked.connect( partial(self.toggleCanvasVisibilityLayer, self.preview) )

        # Añadimos al canvas las dos capas (se visualizan)
        self.canvas.setLayerSet([ self.original, self.preview ])


    '''
    @method: __openDialog
    @brief: Muestra un diálogo para seleccionar el archivo SHP
    '''
    def __openDialog(self):
        # Se crea un objeto del tipo QFileDialog
        dlg = QFileDialog()

        # Busca por archivos existentes en el sistema
        dlg.setFileMode(QFileDialog.ExistingFile)
        # Solo mostrar archivos con extensión shp
        dlg.setFilter("shapefile (*.shp)")

        # Cuando devuelva True ( Cuando se haya seleccionado la carpeta de salida )
        if dlg.exec_():
            # Obtenemos la ruta del archivo
            filepath = map(str, list(dlg.selectedFiles()))[0]
            # Llamamos a la función __addLayer con la ruta del archivo para añadirlo como capa
            self.__addLayer(filepath)


    '''
    @method: __openDialog_folder
    @brief: Muestra un diálogo para seleccionar la carpeta de salida
    '''
    def __openDialog_folder(self):
        # Crea un dialogo para seleccionar un directorio y devuelve la ruta
        self.folder = QFileDialog().getExistingDirectory()

        # Muestra en el label la ruta de la carpeta de salida
        self.label_selected_folder.setText(self.folder)

        # Llamamos a la función activaGuardar
        self.activaGuardar()

    '''
    @method: __addLayer
    @brief: Crea las capas de entrada y salida a partir del path
    @param: path - ruta de la capa de entrada
    '''
    def __addLayer(self, path):

        # Objeto de la clase QgsVectorLayer ( capa de entrada )
        layer = QgsVectorLayer(path, os.path.basename(path), "ogr")

        # Si la capa no es de tipo lineString
        if not layer.geometryType()==1:
            # Devuelve un mensaje de aviso y no continúa
            QMessageBox.information(None,'Warning', 'No se trata de una capa LineString')
            return

        # Creamos un objeto de tipo QgsMapCanvasLayer
        # De esta forma podremos activar o desactivar la visualización a partir de la capa
        # y no utilizando la clase QgsLegend
        self.original = QgsMapCanvasLayer(layer)

        # Asignamos la capa al objeto de la clase GeneraLine ( capa de entrada )
        self.simplify.setLayer(layer)

        # Ponemos al canvas la extensión de la capa de entrada
        self.canvas.setExtent(layer.extent())

        # Añadimos al canvas la capa original
        self.canvas.setLayerSet([self.original])

        # Le aplicamos simbología
        symbols = layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QtGui.QColor.fromRgb(204, 51, 51))

        # Activamos botones y checkbox para que se pueda interactuar

        # Botón previsualizar la generalización de Douglas-Peucker
        self.btn_prev_dp.setEnabled(True)
        # Botón previsualizar la generalización de McMaster
        self.btn_prev_mcm.setEnabled(True)
        # Se activa el checkbox de visualización de la capa de entrada
        self.cb_ori.setEnabled(True)
        # Se marca como checked
        self.cb_ori.setCheckState(Qt.Checked)
        # Se activa el checkbox del algoritmo Douglas-Peucker
        self.cb_dp.setEnabled(True)
        # Se activa el checkbox del algoritmo McMaster
        self.cb_mcm.setEnabled(True)
        # Se activa el botón de zoom extensión
        self.btn_zoom.setEnabled(True)
        # Se activa el spiner de Douglas-Peucker
        self.spn_dp.setEnabled(True)
        # Se activa el spiner de McMaster
        self.spn_mcm.setEnabled(True)
        # Se activa el control de escala
        self.scaleControl.setEnabled(True)
        # Mostramos en el label el nombre de la capa seleccionada
        self.label_shp_path.setText(layer.name())

        # Ponemos como sistema de referencia del canvas el de la capa de entrada
        self.canvas.mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(layer.crs().authid()))

        # Conectamos al checkbox de visualización de la capa de entrada a su función
        self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )

        # Conecta el botón de zoom con su función
        self.btn_zoom.clicked.connect( partial( self.zoomExt, layer ) )


    '''
    @method: zoomExt
    @brief: Realiza un zoom extensión de la capa de entrada en el canvas
    @param: layer - capa de visualización
    '''
    def zoomExt(self,layer):
        # Asignamos la extensión del canvas a la extensión de la capa
        self.canvas.setExtent(layer.extent())
        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: toggleCanvasVisibilityLayer
    @brief: Se visualiza o no la capa en función del estado de la capa
    @param: layer - capa de visualización
    '''
    def toggleCanvasVisibilityLayer(self, layer):
        # Boolean del estado de visualización la capa
        visibility = layer.isVisible()

        # Asignamos la visualización de la capa a lo contrario que había antes
        layer.setVisible(not visibility)

        # Hay que volver a añadir las capas para que se muestren
        layerSet = [ l for l in [self.original, self.preview] if l]
        self.canvas.setLayerSet(layerSet)

        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: on_scale_changed
    @brief: Se ejecuta cuando cambia la escala del QgsScaleWidget.
            Modifica la escala del canvas.
    '''
    def on_scale_changed(self):

        #iface.mapCanvas().zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )

        # Modificamos la escala del canvas en función del QgsScaleWidget
        self.canvas.zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )

        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: on_canvas_scale_changed
    @brief: Se ejecuta cuando cambia la escala del canvas.
            Modifica la escala del QgsScaleWidget.
    '''
    def on_canvas_scale_changed(self, scale):
        # Modifica la escala del QgsScaleWidget en función de la escala del canvas
        self.scaleControl.setScale(1 / scale)


    '''
    @method: __init_ui
    @brief: Inicializa los componentes del formulario. Obtenido de uic.
            Añadiéndole componente de QGIS: Canvas, QgsScaleWidget
    '''
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
