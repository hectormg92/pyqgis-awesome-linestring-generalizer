# pyqgis-awesome-linestring-generalizer

# �ndice
***

- [Introducci�n y objetivos](#introducci�n-y-objetivos)
    - [Algoritmos](#algoritmos)
    - [Desarrollo del formulario PyQt4 mediante Qt Designer](#desarrollo-del-formulario-pyqt4-mediante-qt-designer)
- [Desarrollo de la pr�ctica](#desarrollo-de-la-pr�ctica)
- [Prueba y Resultados](#pruebas-y-resultados)
- [Conclusiones](#conclusiones)

# Introducci�n y Objetivos
El proyecto final de la asignatura **`Desarrollo de aplicaciones SIG`** se ha centrado en las ideas listadas: 
* ``(13)`` **Aplicar el algoritmo de eliminaci�n de [**`Douglas Peucker`**](https://es.wikipedia.org/wiki/Algoritmo_de_Ramer%E2%80%93Douglas%E2%80%93Peucker)**
* ``(14)`` **Aplicar el algoritmo de suavizamiento **`McMaster`** empleados en** generalizaci�n cartogr�fica.
Hemos decidido abordarlo desde **``QGIS (PyQGIS)``** principalmente por tratarse de software libre.

#### Algoritmos:
 - Algoritmo de eliminaci�n de ***``Douglas-Peucker``***

![Animaci�n Douglas Peucker](https://upload.wikimedia.org/wikipedia/commons/3/30/Douglas-Peucker_animated.gif)

El algoritmo de Douglas-Peucker se usa para reducir el n�mero de puntos utilizados en la aproximaci�n de una curva. El objetivo del algoritmo es, dada una curva compuesta por segmentos, encontrar una curva similar aproximada con menos puntos. El algoritmo define un par�metro basado en la m�xima distancia entre la curva original y la simplificada.
El algoritmo seguido ser�a el siguiente:

```javascript
function DouglasPeucker(PointList[], epsilon)
    // Busca el punto con la distancia m�xima
    dmax = 0
    index = 0
    end = length(PointList)
    for i = 1 to ( end - 1) {
        d = shortestDistanceToSegment(PointList[i], Line(PointList[1], PointList[end])) 
        if ( d > dmax ) {
            index = i
            dmax = d
        }
    }
    // Si la distancia es mayor que epsilon, simplificar recursivamente
    if ( dmax > epsilon ) {
        // Llamada recursiva
        recResults1[] = DouglasPeucker(PointList[1...index], epsilon)
        recResults2[] = DouglasPeucker(PointList[index...end], epsilon)
 
        // Construcci�n de la lista resultado
        ResultList[] = {recResults1[1...end-1] recResults2[1...end]}
    } else {
        ResultList[] = {PointList[1], PointList[end]}
    }
    // Devolver el resultado
    return ResultList[]
end
```

En resumen, el algoritmo construye una linea desde el primer hasta el �ltimo punto de la linea y busca el vertice con una mayor distancia (que forme un �ngulo recto) al segmento y lo agrega si est� a una distancia mayor a epsilon. Con los dos segmentos formados se repetir�a el proceso hasta no haber puntos o que estos no superen el umbral epsilon. Es un proceso recursivo d�nde la nueva curva es generada a partir de los puntos que han permanecido tras aplicar el algoritmo.

**Algoritmo de suavizado de McMaster**
Tambi�n conocido como algoritmo de deslizamiento de McMaster. Este algoritmo dejar� fijos el primer y �ltimo punto de la l�nea y calcular� la nueva posici�n (posici�n media) de los dem�s puntos a partir de sus coordenadas y las de sus vecinos.
Tiene un par�metro de entrada que es el n�mero de vertices con los que calcular� la media de las coordenadas de cada uno, por lo que este deber� ser un n�mero impar (mismo n�mero de vecinos a cada lado del v�rtice y el propio v�rtice). Los v�rtices que no entren en el vecindario de suavizado se quedar�n como estaban.

El algoritmo seguido es el siguiente:

```javascript
function McMaster(PointList[], nu)
    half_nu = int(nu/2) # nu = 3 -> half_nu = 1
    end = length(PointList)
    x0, y0 = PointList[0]
    x1, y1 = PointList[-1]
    smooth_points = []
    smooth_points.append([x0,y0])
    
    for i = half_nu to (end - half_nu){
        Xactual, Yactual = PointList[i]
        for j = -half_nu to half_nu{
            x, y +=  PointList[i + j]
        }
        mediax, mediay = x/nu, y/nu
        smooth_points.append(mediax, mediay)
    }
    return smooth_points[]
```

Decir que los algoritmos planteados est�n escritos en pseudoc�digo y no responden a ning�n lenguaje de programaci�n en s�.
Con este algoritmo lo que se conseguir� es un suavizado de las curvas por lo que �stas no ser�n tan acentuadas.

# Desarrollo del formulario PyQt4 mediante Qt Designer

# Desarrollo de la pr�ctica
En primer lugar hemos utilizado ``uic.py`` para convertir el archivo ``.ui`` en un archivo ``.py`` que usaremos como archivo del proyecto.

Hemos a�adido en la parte superior del archivo los imports necesarios para realizar nuestro proyecto:

```python
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
```

Despu�s de los imports tomamos una referencia del **registro** de ``QGIS``:

```python
registry = QgsMapLayerRegistry.instance()
```

A continuaci�n se muestra el c�digo del formulario. Mostraremos solo las partes del c�digo escritas por nosotros y evitaremos poner el c�digo generado por uic.

```python
# Clase MainWindow
class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        QMainWindow.__init__(self)

        # Capa original
        self.original = None

        # Capa para mostrar la previsualizaci�n
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

        # Bot�n previsualizar algoritmo Douglas Peucker
        self.btn_prev_dp.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.DOUGLAS_PEUCKER) )

        # Bot�n previsualizar algoritmo McMaster
        self.btn_prev_mcm.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.MC_MASTER) )

        # Bot�n cargar SHP
        self.btn_load_shp.clicked.connect(self.__openDialog)

        # Bot�n abrir di�logo para seleccionar carpeta de salida
        self.btn_sal.clicked.connect(self.__openDialog_folder)

        # Control de escala - Cuando se modifique la escala en el widget
        self.scaleControl.scaleChanged.connect(self.on_scale_changed)

        # Cuando cambia la escala en el canvas
        self.canvas.scaleChanged.connect(self.on_canvas_scale_changed)

        # Checkbox Algoritmo McMaster
        self.cb_dp.stateChanged.connect(self.activaGuardar)

        # Checkbox Algoritmo Douglas Peucker
        self.cb_mcm.stateChanged.connect(self.activaGuardar)

        # Bot�n Guardar
        self.btn_do.clicked.connect(self.guardaSHP)

    '''
    @method: guardaSHP
    @brief: Guarda los resultados en shapefile en el directorio de salida
            dependiendo de los checbox marcados
    '''
    def guardaSHP(self):

        # Si el checbox del algoritmo douglas peucker est� marcado
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

        # Si el checbox del algoritmo McMaster est� marcado
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

        # Mostramos un mensaje de informaci�n
        QMessageBox.information(None, u'�xito', u'Guardado con �xito en : '+ str(self.folder))

    '''
    @method: activaGuardar
    @brief: Activa el bot�n de guardar dependiendo de los checbox marcados
            y si se ha especificado carpeta de salida
    '''
    def activaGuardar(self):

        # Si el checbox de el algoritmo Douglas Peucker est� marcado
        if self.cb_dp.isChecked() or self.cb_mcm.isChecked():
            # Si se ha especificado carpeta de salida
            if self.folder:
                # Activamos el bot�n de guardar
                self.btn_do.setEnabled(True)

        # Si ning�n checbox est� marcado
        else:
            # Desactivamos el bot�n de guardar
            self.btn_do.setEnabled(False)


    '''
    @method: __showPreviewCanvas
    @brief: Muestra la previsualizaci�n de aplicar el algoritmo con el par�metro
            seleccionado
    @param: algorithm - nombre del algoritmo a aplicar
    '''
    def __showPreviewCanvas(self, algorithm) :

        # Si el algoritmo seleccionado es Douglas-Peucker
        if algorithm == self.Algorithms.DOUGLAS_PEUCKER :
            # El parametro ser� el espec�ficado en el spiner de Douglas-Peucker
            param = self.spn_dp.value()
        else :
            # El parametro ser� el espec�ficado en el spiner de McMaster
            param = self.spn_mcm.value()

        # Aplicamos el algoritmo con el par�metro introducido sobre la capa
        self.simplify.applyAlgorithm(algorithm, param)

        # Se activa el checkbox de suavizado
        self.cb_suav.setEnabled(True)

        # El checkbox de suavizado se pone en checked (ya que la capa se encuentra visible)
        self.cb_suav.setCheckState(Qt.Checked)

        # Asignamos a la capa preview un objeto de la clase QgsMapCanvasLayer a partir de
        # la capa de salida almacenada en el objeto de la clase GeneraLine
        self.preview = QgsMapCanvasLayer(self.simplify.layer_salida)

        # Conectamos al checkbox la funci�n para cambiar la visualizaci�n de la capa generalizada
        self.cb_suav.clicked.connect( partial(self.toggleCanvasVisibilityLayer, self.preview) )

        # A�adimos al canvas las dos capas (se visualizan)
        self.canvas.setLayerSet([ self.original, self.preview ])


    '''
    @method: __openDialog
    @brief: Muestra un di�logo para seleccionar el archivo SHP
    '''
    def __openDialog(self):
        # Se crea un objeto del tipo QFileDialog
        dlg = QFileDialog()

        # Busca por archivos existentes en el sistema
        dlg.setFileMode(QFileDialog.ExistingFile)
        # Solo mostrar archivos con extensi�n shp
        dlg.setFilter("shapefile (*.shp)")

        # Cuando devuelva True ( Cuando se haya seleccionado la carpeta de salida )
        if dlg.exec_():
            # Obtenemos la ruta del archivo
            filepath = map(str, list(dlg.selectedFiles()))[0]
            # Llamamos a la funci�n __addLayer con la ruta del archivo para a�adirlo como capa
            self.__addLayer(filepath)


    '''
    @method: __openDialog_folder
    @brief: Muestra un di�logo para seleccionar la carpeta de salida
    '''
    def __openDialog_folder(self):
        # Crea un dialogo para seleccionar un directorio y devuelve la ruta
        self.folder = QFileDialog().getExistingDirectory()

        # Muestra en el label la ruta de la carpeta de salida
        self.label_selected_folder.setText(self.folder)

        # Llamamos a la funci�n activaGuardar
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
            # Devuelve un mensaje de aviso y no contin�a
            QMessageBox.information(None,'Warning', 'No se trata de una capa LineString')
            return

        # Creamos un objeto de tipo QgsMapCanvasLayer
        # De esta forma podremos activar o desactivar la visualizaci�n a partir de la capa
        # y no utilizando la clase QgsLegend
        self.original = QgsMapCanvasLayer(layer)

        # Asignamos la capa al objeto de la clase GeneraLine ( capa de entrada )
        self.simplify.setLayer(layer)

        # Ponemos al canvas la extensi�n de la capa de entrada
        self.canvas.setExtent(layer.extent())

        # A�adimos al canvas la capa original
        self.canvas.setLayerSet([self.original])

        # Le aplicamos simbolog�a
        symbols = layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QtGui.QColor.fromRgb(204, 51, 51))

        # Activamos botones y checkbox para que se pueda interactuar

        # Bot�n previsualizar la generalizaci�n de Douglas-Peucker
        self.btn_prev_dp.setEnabled(True)
        # Bot�n previsualizar la generalizaci�n de McMaster
        self.btn_prev_mcm.setEnabled(True)
        # Se activa el checkbox de visualizaci�n de la capa de entrada
        self.cb_ori.setEnabled(True)
        # Se marca como checked
        self.cb_ori.setCheckState(Qt.Checked)
        # Se activa el checkbox del algoritmo Douglas-Peucker
        self.cb_dp.setEnabled(True)
        # Se activa el checkbox del algoritmo McMaster
        self.cb_mcm.setEnabled(True)
        # Se activa el bot�n de zoom extensi�n
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

        # Conectamos al checkbox de visualizaci�n de la capa de entrada a su funci�n
        self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )

        # Conecta el bot�n de zoom con su funci�n
        self.btn_zoom.clicked.connect( partial( self.zoomExt, layer ) )


    '''
    @method: zoomExt
    @brief: Realiza un zoom extensi�n de la capa de entrada en el canvas
    @param: layer - capa de visualizaci�n
    '''
    def zoomExt(self,layer):
        # Asignamos la extensi�n del canvas a la extensi�n de la capa
        self.canvas.setExtent(layer.extent())
        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: toggleCanvasVisibilityLayer
    @brief: Se visualiza o no la capa en funci�n del estado de la capa
    @param: layer - capa de visualizaci�n
    '''
    def toggleCanvasVisibilityLayer(self, layer):
        # Boolean del estado de visualizaci�n la capa
        visibility = layer.isVisible()

        # Asignamos la visualizaci�n de la capa a lo contrario que hab�a antes
        layer.setVisible(not visibility)

        # Hay que volver a a�adir las capas para que se muestren
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

        # Modificamos la escala del canvas en funci�n del QgsScaleWidget
        self.canvas.zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )

        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: on_canvas_scale_changed
    @brief: Se ejecuta cuando cambia la escala del canvas.
            Modifica la escala del QgsScaleWidget.
    '''
    def on_canvas_scale_changed(self, scale):
        # Modifica la escala del QgsScaleWidget en funci�n de la escala del canvas
        self.scaleControl.setScale(1 / scale)


    '''
    @method: __init_ui
    @brief: Inicializa los componentes del formulario. Obtenido de uic.
            A�adi�ndole componente de QGIS: Canvas, QgsScaleWidget
    '''
    def __init_ui(self):
        # solo hemos tenido que crear el canvas y el QgsScaleWidget
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
```

A continuaci�n mostramos la clase **``GeneraLine``** que es la encargada de realizar los algoritmos.

```python

'''
@class: Algorithms
@brief: namespace para los algoritmos
'''
class Algorithms:
    MC_MASTER = 'MC_MASTER'
    DOUGLAS_PEUCKER = 'DOUGLAS_PEUCKER'

'''
@class: GeneraLine
@brief: Clase que servir� para ejecutar los algoritmos
        de suavizado y reducci�n de puntos sobre una capa de L�neas
@param: layer - Capa de entrada
'''
class GeneraLine:

    # Variable de clase est�tica que almacena la clase Algoritmos
    Algorithms = Algorithms

    # Lista con los algoritmos posibles
    algorithms = [Algorithms.MC_MASTER, Algorithms.DOUGLAS_PEUCKER]

    # Constructor
    def __init__(self, layer = None):

        # Variable de clase self.layer_salida
        # Almacenar� las features de salida
        self.layer_salida = None

        # Si se le pasa layer al constructor
        if layer :
            # Asignamos la capa como variable de clase
            self.setLayer(layer)

    '''
    @method: setLayer
    @brief: Asignamos como variable de clase la capa que se le pasa
            y creamos la capa de salida en memoria (layer_salida)
            con los par�metros de la capa de entrada (crs, nombre, ...)
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

        # Cambiamos la simbolog�a
        symbols = self.layer_salida.rendererV2().symbols()
        symbol = symbols[0]
        # Cambiamos el color de la capa de salida a un tono azulado
        symbol.setColor(QtGui.QColor.fromRgb(102, 102, 255))

        # A�adimos las capas al registro de QGIS
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

        # Comenzamos la edici�n sobre la capa de salida
        with edit(self.layer_salida):
            # Metemos la l�gica dentro de un bloque try-except
            try :
                # Eliminamos las features que puedan haber
                # en la capa de salida (de proceso anteriores)
                listOfIds = [feat.id() for feat in self.layer_salida.getFeatures()]
                self.layer_salida.deleteFeatures( listOfIds )

                # Recorreremos todas las features de la capa de entrada
                for feature in self.layer.getFeatures():

                    # Obtenemos una referencia de la geometr�a
                    geom = feature.geometry()

                    # Creamos una feature temporal
                    # Servir� para recorrer geometr�as multiparte
                    temp_feature = QgsFeature()

                    # Comprobamos la geomtr�a
                    if not geom : continue

                    # Se crea un nuevo feature (temporal)
                    # Servir� para crear la feature de la capa de salida
                    f = QgsFeature()


                    # Si la geometr�a es multiparte (MULTILINESTRING)
                    if geom.isMultipart():
                        # Recorremos cada LineString (geom) dentro del MultiLineString
                        for geom_ in geom.asGeometryCollection():

                            # Asignamos la geometr�a a la feature temporal
                            temp_feature.setGeometry(geom_)

                            # Extraemos los puntos de la geomtr�a
                            points = self.__extractPoints(temp_feature)

                            # Ejecutamos el algoritmo pertinente
                            # sobre los puntos extraidos de la geometr�a que estamos recorriendo
                            if name == self.Algorithms.MC_MASTER:
                                resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                            else :
                                resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]

                            # Obtenemoss la geometr�a (Polyline) resultante de aplicar el algoritmo
                            resultLine = QgsGeometry.fromPolyline(resultPoints)
                            # A�adimos la geomtr�a a la feature temporal
                            f.setGeometry(resultLine)

                            # A�adimos la feature a la capa de salida
                            self.layer_salida.addFeature(f)

                    # Si la geometr�a no es multiparte
                    else :

                        # Extraemos los puntos de la geomtr�a
                        points = self.__extractPoints(feature)

                        # Se crea un nuevo feature (temporal)
                        # Servir� para crear la feature de la capa de salida
                        f = QgsFeature()

                        # Ejecutamos el algoritmo pertinente
                        # sobre los puntos extraidos de la geometr�a que estamos recorriendo
                        if name == self.Algorithms.MC_MASTER:
                            resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                        else :
                            resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]


                        # Obtenemoss la geometr�a (Polyline) resultante de aplicar el algoritmo
                        resultLine = QgsGeometry.fromPolyline(resultPoints)
                        # A�adimos la geomtr�a a la feature temporal
                        f.setGeometry(resultLine)

                        # A�adimos la feature a la capa de salida
                        self.layer_salida.addFeature(f)
            # Si se produce una excepci�n
            except Exception as e:
                # mostramos un mensaje de error
                QMessageBox.information(None, 'ERROR!', str(e))

                print 'error', e

    '''
    @method: __shortestDistance
    @brief: Devuelve la ditancia m�s corta entre
            un punto y una recta
    @param: point - lista con los valores x,y del punto ej: [1000, 1000]
    @param: line: lista con los par�metros a,b,c que definen una l�nea ax + by + c = 0
    @return: double - distancia m�s corta
    '''
    def __shortestDistance(self,point, line):
        # Extraemos las coordenadas del punto
        xp, yp = point
        # Extraemos los par�metros de la l�nea
        a, b, c = line
        # Calculamos y deolvemos la ditancia m�nima entre el punto y la recta
        return math.fabs(a*xp + b*yp + c)/math.sqrt(a**2 + b**2)

    '''
    @method: __extractPoints
    @brief: Extrae los puntos de una feature (simple)
    @param: feature - feature de entrada
    @return: [] - lista de puntos de la geomtr�a del feature pasado como par�metro
    '''
    def __extractPoints(self, feature):
        # Obtenemos una referencia de la geometr�a
        geom = feature.geometry()

        # Creamos una lista vac�a
        points = []

        # Comprobamos que la geometr�a no sea None
        # En cuyo caso devolvemos una lista vac�a
        if geom == None: return points

        # contador
        i = 0

        # Bucle while que recorre los  v�rtices de
        # la geometr�a
        while(geom.vertexAt(i) != QgsPoint(0,0)):
            # Obtenemos el v�rtice seg�n el �dice i
            # y lo a�adimos a la lista
            points.append(geom.vertexAt(i))
            # aumentamos el contador en 1
            i += 1

        # Devolvemos la lista
        return points

    '''
    @method: __mcMaster
    @brief: Aplica el algoritmo de generalizaci�n de McMaster
    @param: points - lista de puntos de la geomtr�a de la capa de entrada
    @param:  mu - n�mero de vertices que entran en el c�lculo de la media (impar > 1)
    @return: [] - lista de puntos con las coordenadas de la l�nea suavizada
    '''
    def __mcMaster(self, points, mu):
            # Si no hay puntos devuelve una lista vac�a
            if not points : return []
            # Par�metro para el vecindario de cada vertice
            half_mu = int(math.floor(mu/2))
            # Longitud de la lista de puntos
            end = len(points)

            # Lista con los puntos del suavizado
            # empezamos a�adiendo los puntos primeros que quedan fuera del rango
            # [0, half_mu)
            smooth_points = map( list, points[ : half_mu ] )
            #print smooth_points

            # Generamos un iterador para obtener los �ndices de los puntos de los
            # cuales podemos aplicar un vecindario de mu
            for i in range(half_mu, end - half_mu):

                # Obtenemos el punto situado en medio del vecindario
                xactual, yactual = points[i]

                # Obtenemos los puntos que forman parte del vecindario
                computed_points = points[i - half_mu : i + (mu + 1)/2]

                # Obtenemos las coordenadas de los puntos en listas (una para cada coord)
                xcoords = [p[0] for p in computed_points]
                ycoords = [p[1] for p in computed_points]

                # Obtenemos la media geom�trica de los puntos que conforman el vecindario
                mediax, mediay = sum(xcoords)/len(xcoords), sum(ycoords)/len(ycoords)


                # Y realizamos la media geom�trica con la media del vecindario y el punto
                # de estudio
                x, y = (mediax + xactual)/2, (mediay + yactual)/2
                # Finalmente lo a�adimos a la lista de puntos del suavizado
                smooth_points.append([x, y])

            # finalizamos a�adiendo los puntos primeros que quedan fuera del rango
            # [end - half_mu, end)
            smooth_points += map( list, points[ -half_mu : ] )

            # Devuelve una lista con los puntos de la linea suavizada por el algoritmo
            # McMaster
            return smooth_points

    '''
    @method: __douglasPeucker
    @brief: Aplica el algoritmo de generalizaci�n de Douglas-Peucker
    @param: points - lista de puntos de la geomtr�a de la capa de entrada
    @param:  epsilon - distancia m�nima para incluir el v�rtice
    @return: [] - lista de puntos con las coordenadas de la l�nea generalizada
    '''
    def  __douglasPeucker(self,points, epsilon):
        # Distancia m�xima
        dmax = 0
        # �ndice de la posici�n en la lista del punto de m�xima distancia
        index = 0

        # �ndice final para el bucle
        end = len(points) - 1

        # Punto inicial
        x0, y0 = points[0]
        # Punto final
        x1, y1 = points[-1]

        # Par�metros de la recta
        a = y1 - y0
        b = -(x1 - x0)
        c = a*(-x0) - b*y0


        # Si el primer y el �ltimo punto son el mismo
        if a == 0 and b == 0 : return []

        # Generamos un iterador para obtener los �ndices
        for i in range(1, end):

            # punto
            p = points[i]

            # distancia m�s corta entre el punto y la recta
            d = self.__shortestDistance(p, [a, b, c])

            # Si la distancia es mayor que lo que haya almacenado en dmax
            if d > dmax :
                # Guardamos el �ndice y la distancia en las variables
                index = i
                dmax = d

        # Si la ditancia m�xima es mayor o igual que epsilon
        if dmax >= epsilon :
            # Realizamos el algoritmo

            # res_ini almacenar� los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porci�n de la lista de puntos desde 0 hasta el �ndice
            # del punto de "distancia m�xima sobre la recta" + 1
            res_ini = self.__douglasPeucker(points[: index + 1], epsilon)

            # res_fin almacenar� los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porci�n de la lista de puntos desde el �ndice
            # del punto de "distancia m�xima sobre la recta" hasta len(points)
            res_fin = self.__douglasPeucker(points[index : ], epsilon)

            # Juntamos las dos listas resultantes y devolvemos el array juntado
            return res_ini[:-1] + res_fin

        # Si la distancia m�xima es menor que epsilon
        else :
            # Devolvemos una lista con los puntos inicial y final
            return [ points[0], points[-1] ]


```

En primero lugar, lo que hicimos fue desarrollar los algoritmos en python como funciones y viendo si podriamos desarrollar otros procesos como funciones tambi�n. Por ejemplo el c�lculo de la distancia m�nima en el caso del algoritmo **Douglas-Peucker**, se ha desarrollado como una funci�n externa.
    
Una vez desarrollados los algoritmos los metimos en una clase GeneraLine y hicimos checkeos como ver si la capa que se introduce es del tipo *`LineString(if layer.wkbType()==QGis.WKBLineString: ...)`*, comprovar si la capa es multiparte o recoger el EPSG de la capa. Para cada capa se recorrer�n todos sus features y se aplicar� el algoritmo seleccionado.

Creamos la funci�n *`__extractPoints(feature)`* para extraer todos los puntos de cada feature y poder as� aplicar los algoritmos sobre estos.
Con la funci�n predefinida de PyQgis vertexAt(i), siendo i el �ndice del v�rtice, extraemos de la geometria de cada feature dichos puntos de la siguiente manera:

```python
def __extractPoints(self, feature):
        geom = feature.geometry()
        points = []
        if geom == None: return points
        i = 0
        while(geom.vertexAt(i) != QgsPoint(0,0)):
            points.append(geom.vertexAt(i))
            i += 1
        return points
```


# Pruebas y Resultados
Al terminar y depurar el programa hicimos varias pruebas para ver que tal funciona.
- Capa de Orograf�a (curvas)
Sabiendo que no tiene sentido generalizar de esta forma las curvas de nivel ya que pierden su significado geogr�fico y nos inventar�amos una forma del terreno distinta, hemos probado para ver como funcionan los algor�tmos sobre un curvado tan complejo con distintos valores de par�metro.
    - Algoritmo Douglas-Peucker - distancia m�nima 50
    - Algoritmo Douglas-Peucker - distancia m�nima 5
    - Algoritmo Douglas-Peucker - distancia m�nima 1
    Vemos que el algoritmo funciona mejor para este caso con una distancia m�nima peque�a.
    - Algoritmo McMaster - vecindario 9
    - Algoritmo McMaster - vecindario 21
Como las curvas var�an mucho en vecindarios peque�os se observa al aplicar vecindarios m�s grandes como el suavizado se aleja de la curva original dr�sicamente al realizar la media de todo el vecindario.

- Capa de Hidrograf�a
Para lineas menos cambiantes dependiende de nuestro pr�posito nos servir� uno mejor que otro. Para generalizar usaremos el algoritmo de Douglas-Peucker (eliminando puntos) y para suavizar usaremos el algor�tmo de McMaster el cual atenuar� los picos generados por la intersecci�n en los v�rtices (curvar� la linea).
    - prueba1 _50
    - hidro_dp_20

    - hidro_mcm_9


# Conclusiones

Tras realizar varias pruebas con el software generado podemos poner en la mesa distintos puntos favorables y distintos puntos a mejorar:

- **Respecto al UI generado**

Se ha elaborado un UI bastante logrado que alberga muchas funcionalidades. Se podr�an mejorar diversos aspectos de menor importancia que podr�an ver luz en futuros releases.

Un aspecto importante que no se ha llegado a conseguir pero que se puede ver en el archivo [project_sig2.py](https://github.com/hectormg92/pyqgis-awesome-linestring-generalizer/blob/master/project_sig2.py) es ejecutar los procesos de la clase GeneraLine en otro hilo de ejecuci�n para no interferir con el hilo de renderizado del UI y de esta manera no bloquearlo.

- **Respecto a los algoritmos**

El par�metro a introducir en el algoritmo de Douglas Peucker, para mejorar la experiencia del usuario, deber�a ser un n�mero comprendido entre 0 y 1 (escalando con la distancia m�xima entre los distintos v�rtices con la recta (que une el punto inicial y final).

Adem�s esta misma idea tambi�n se podr�a aplicar al algoritmo McMster con el n�mero de v�rtices m�ximo (ya que el m�nimo es tres).

Se podr�a llevar a cabo una funcionalidad extra que concatenara distintas �rdenes para ejecutar varios algoritmos de una vez con el resultado del proceso anterior (Parecido a como hace ArcMap con ModelBuilder).
Por ejemplo:

- Proceso 1 : Aplicar Douglas Peucker a la capa de entrada
- Proceso 2 : Aplicar McMaster a la capa resultante del proceso 1