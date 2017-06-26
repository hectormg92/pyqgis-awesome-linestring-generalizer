# pyqgis-awesome-linestring-generalizer

<<<<<<< HEAD
# Índice
***

- [Introducción y objetivos](#introducción-y-objetivos)
    - [Algoritmos](#algoritmos)
    - [Desarrollo del formulario PyQt4 mediante Qt Designer](#desarrollo-del-formulario-pyqt4-mediante-qt-designer)
- [Desarrollo de la práctica](#desarrollo-de-la-práctica)
- [Prueba y Resultados](#pruebas-y-resultados)
- [Conclusiones](#conclusiones)

# Introducción y Objetivos
El proyecto final de la asignatura **`Desarrollo de aplicaciones SIG`** se ha centrado en las ideas listadas: 
* ``(13)`` **Aplicar el algoritmo de eliminación de [**`Douglas Peucker`**](https://es.wikipedia.org/wiki/Algoritmo_de_Ramer%E2%80%93Douglas%E2%80%93Peucker)**
* ``(14)`` **Aplicar el algoritmo de suavizamiento **`McMaster`** empleados en** generalización cartográfica.
Hemos decidido abordarlo desde **``QGIS (PyQGIS)``** principalmente por tratarse de software libre.

#### Algoritmos:
 - Algoritmo de eliminación de ***``Douglas-Peucker``***

![Animación Douglas Peucker](https://upload.wikimedia.org/wikipedia/commons/3/30/Douglas-Peucker_animated.gif)

El algoritmo de Douglas-Peucker se usa para reducir el número de puntos utilizados en la aproximación de una curva. El objetivo del algoritmo es, dada una curva compuesta por segmentos, encontrar una curva similar aproximada con menos puntos. El algoritmo define un parámetro basado en la máxima distancia entre la curva original y la simplificada.
El algoritmo seguido sería el siguiente:

```javascript
function DouglasPeucker(PointList[], epsilon)
    // Busca el punto con la distancia máxima
=======
# Ãndice
***

- [IntroducciÃ³n y objetivos](#introducciÃ³n-y-objetivos)
    - [Algoritmos](#algoritmos)
    - [Desarrollo del formulario PyQt4 mediante Qt Designer](#desarrollo-del-formulario-pyqt4-mediante-qt-designer)
- [Desarrollo de la prÃ¡ctica](#desarrollo-de-la-prÃ¡ctica)
- [Prueba y Resultados](#pruebas-y-resultados)
- [Conclusiones](#conclusiones)

# IntroducciÃ³n y Objetivos
El proyecto final de la asignatura **`Desarrollo de aplicaciones SIG`** se ha centrado en las ideas listadas: 
* ``(13)`` **Aplicar el algoritmo de eliminaciÃ³n de [**`Douglas Peucker`**](https://es.wikipedia.org/wiki/Algoritmo_de_Ramer%E2%80%93Douglas%E2%80%93Peucker)**
* ``(14)`` **Aplicar el algoritmo de suavizamiento **`McMaster`** empleados en** generalizaciÃ³n cartogrÃ¡fica.
Hemos decidido abordarlo desde **``QGIS (PyQGIS)``** principalmente por tratarse de software libre.

#### Algoritmos:
 - Algoritmo de eliminaciÃ³n de ***``Douglas-Peucker``***

![AnimaciÃ³n Douglas Peucker](https://upload.wikimedia.org/wikipedia/commons/3/30/Douglas-Peucker_animated.gif)

El algoritmo de Douglas-Peucker se usa para reducir el nÃºmero de puntos utilizados en la aproximaciÃ³n de una curva. El objetivo del algoritmo es, dada una curva compuesta por segmentos, encontrar una curva similar aproximada con menos puntos. El algoritmo define un parÃ¡metro basado en la mÃ¡xima distancia entre la curva original y la simplificada.
El algoritmo seguido serÃ­a el siguiente:

```javascript
function DouglasPeucker(PointList[], epsilon)
    // Busca el punto con la distancia mÃ¡xima
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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
 
<<<<<<< HEAD
        // Construcción de la lista resultado
=======
        // ConstrucciÃ³n de la lista resultado
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        ResultList[] = {recResults1[1...end-1] recResults2[1...end]}
    } else {
        ResultList[] = {PointList[1], PointList[end]}
    }
    // Devolver el resultado
    return ResultList[]
end
```

<<<<<<< HEAD
En resumen, el algoritmo construye una linea desde el primer hasta el último punto de la linea y busca el vertice con una mayor distancia (que forme un ángulo recto) al segmento y lo agrega si está a una distancia mayor a epsilon. Con los dos segmentos formados se repetiría el proceso hasta no haber puntos o que estos no superen el umbral epsilon. Es un proceso recursivo dónde la nueva curva es generada a partir de los puntos que han permanecido tras aplicar el algoritmo.

**Algoritmo de suavizado de McMaster**
También conocido como algoritmo de deslizamiento de McMaster. Este algoritmo dejará fijos el primer y último punto de la línea y calculará la nueva posición (posición media) de los demás puntos a partir de sus coordenadas y las de sus vecinos.
Tiene un parámetro de entrada que es el número de vertices con los que calculará la media de las coordenadas de cada uno, por lo que este deberá ser un número impar (mismo número de vecinos a cada lado del vértice y el propio vértice). Los vértices que no entren en el vecindario de suavizado se quedarán como estaban.
=======
En resumen, el algoritmo construye una linea desde el primer hasta el Ãºltimo punto de la linea y busca el vertice con una mayor distancia (que forme un Ã¡ngulo recto) al segmento y lo agrega si estÃ¡ a una distancia mayor a epsilon. Con los dos segmentos formados se repetirÃ­a el proceso hasta no haber puntos o que estos no superen el umbral epsilon. Es un proceso recursivo dÃ³nde la nueva curva es generada a partir de los puntos que han permanecido tras aplicar el algoritmo.

**Algoritmo de suavizado de McMaster**
TambiÃ©n conocido como algoritmo de deslizamiento de McMaster. Este algoritmo dejarÃ¡ fijos el primer y Ãºltimo punto de la lÃ­nea y calcularÃ¡ la nueva posiciÃ³n (posiciÃ³n media) de los demÃ¡s puntos a partir de sus coordenadas y las de sus vecinos.
Tiene un parÃ¡metro de entrada que es el nÃºmero de vertices con los que calcularÃ¡ la media de las coordenadas de cada uno, por lo que este deberÃ¡ ser un nÃºmero impar (mismo nÃºmero de vecinos a cada lado del vÃ©rtice y el propio vÃ©rtice). Los vÃ©rtices que no entren en el vecindario de suavizado se quedarÃ¡n como estaban.
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

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

<<<<<<< HEAD
Decir que los algoritmos planteados están escritos en pseudocódigo y no responden a ningún lenguaje de programación en sí.
Con este algoritmo lo que se conseguirá es un suavizado de las curvas por lo que éstas no serán tan acentuadas.

# Desarrollo del formulario PyQt4 mediante Qt Designer

# Desarrollo de la práctica
En primer lugar hemos utilizado ``uic.py`` para convertir el archivo ``.ui`` en un archivo ``.py`` que usaremos como archivo del proyecto.

Hemos añadido en la parte superior del archivo los imports necesarios para realizar nuestro proyecto:
=======
Decir que los algoritmos planteados estÃ¡n escritos en pseudocÃ³digo y no responden a ningÃºn lenguaje de programaciÃ³n en sÃ­.
Con este algoritmo lo que se conseguirÃ¡ es un suavizado de las curvas por lo que Ã©stas no serÃ¡n tan acentuadas.

# Desarrollo del formulario PyQt4 mediante Qt Designer

# Desarrollo de la prÃ¡ctica
En primer lugar hemos utilizado ``uic.py`` para convertir el archivo ``.ui`` en un archivo ``.py`` que usaremos como archivo del proyecto.

Hemos aÃ±adido en la parte superior del archivo los imports necesarios para realizar nuestro proyecto:
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

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

<<<<<<< HEAD
Después de los imports tomamos una referencia del **registro** de ``QGIS``:
=======
DespuÃ©s de los imports tomamos una referencia del **registro** de ``QGIS``:
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

```python
registry = QgsMapLayerRegistry.instance()
```

<<<<<<< HEAD
A continuación se muestra el código del formulario. Mostraremos solo las partes del código escritas por nosotros y evitaremos poner el código generado por uic.
=======
A continuaciÃ³n se muestra el cÃ³digo del formulario. Mostraremos solo las partes del cÃ³digo escritas por nosotros y evitaremos poner el cÃ³digo generado por uic.
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

```python
# Clase MainWindow
class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        QMainWindow.__init__(self)

        # Capa original
        self.original = None

<<<<<<< HEAD
        # Capa para mostrar la previsualización
=======
        # Capa para mostrar la previsualizaciÃ³n
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Botón previsualizar algoritmo Douglas Peucker
        self.btn_prev_dp.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.DOUGLAS_PEUCKER) )

        # Botón previsualizar algoritmo McMaster
        self.btn_prev_mcm.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.MC_MASTER) )

        # Botón cargar SHP
        self.btn_load_shp.clicked.connect(self.__openDialog)

        # Botón abrir diálogo para seleccionar carpeta de salida
=======
        # BotÃ³n previsualizar algoritmo Douglas Peucker
        self.btn_prev_dp.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.DOUGLAS_PEUCKER) )

        # BotÃ³n previsualizar algoritmo McMaster
        self.btn_prev_mcm.clicked.connect( partial(self.__showPreviewCanvas, self.Algorithms.MC_MASTER) )

        # BotÃ³n cargar SHP
        self.btn_load_shp.clicked.connect(self.__openDialog)

        # BotÃ³n abrir diÃ¡logo para seleccionar carpeta de salida
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.btn_sal.clicked.connect(self.__openDialog_folder)

        # Control de escala - Cuando se modifique la escala en el widget
        self.scaleControl.scaleChanged.connect(self.on_scale_changed)

        # Cuando cambia la escala en el canvas
        self.canvas.scaleChanged.connect(self.on_canvas_scale_changed)

        # Checkbox Algoritmo McMaster
        self.cb_dp.stateChanged.connect(self.activaGuardar)

        # Checkbox Algoritmo Douglas Peucker
        self.cb_mcm.stateChanged.connect(self.activaGuardar)

<<<<<<< HEAD
        # Botón Guardar
=======
        # BotÃ³n Guardar
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.btn_do.clicked.connect(self.guardaSHP)

    '''
    @method: guardaSHP
    @brief: Guarda los resultados en shapefile en el directorio de salida
            dependiendo de los checbox marcados
    '''
    def guardaSHP(self):

<<<<<<< HEAD
        # Si el checbox del algoritmo douglas peucker está marcado
=======
        # Si el checbox del algoritmo douglas peucker estÃ¡ marcado
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Si el checbox del algoritmo McMaster está marcado
=======
        # Si el checbox del algoritmo McMaster estÃ¡ marcado
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Mostramos un mensaje de información
        QMessageBox.information(None, u'Éxito', u'Guardado con éxito en : '+ str(self.folder))

    '''
    @method: activaGuardar
    @brief: Activa el botón de guardar dependiendo de los checbox marcados
=======
        # Mostramos un mensaje de informaciÃ³n
        QMessageBox.information(None, u'Ã‰xito', u'Guardado con Ã©xito en : '+ str(self.folder))

    '''
    @method: activaGuardar
    @brief: Activa el botÃ³n de guardar dependiendo de los checbox marcados
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            y si se ha especificado carpeta de salida
    '''
    def activaGuardar(self):

<<<<<<< HEAD
        # Si el checbox de el algoritmo Douglas Peucker está marcado
        if self.cb_dp.isChecked() or self.cb_mcm.isChecked():
            # Si se ha especificado carpeta de salida
            if self.folder:
                # Activamos el botón de guardar
                self.btn_do.setEnabled(True)

        # Si ningún checbox está marcado
        else:
            # Desactivamos el botón de guardar
=======
        # Si el checbox de el algoritmo Douglas Peucker estÃ¡ marcado
        if self.cb_dp.isChecked() or self.cb_mcm.isChecked():
            # Si se ha especificado carpeta de salida
            if self.folder:
                # Activamos el botÃ³n de guardar
                self.btn_do.setEnabled(True)

        # Si ningÃºn checbox estÃ¡ marcado
        else:
            # Desactivamos el botÃ³n de guardar
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            self.btn_do.setEnabled(False)


    '''
    @method: __showPreviewCanvas
<<<<<<< HEAD
    @brief: Muestra la previsualización de aplicar el algoritmo con el parámetro
=======
    @brief: Muestra la previsualizaciÃ³n de aplicar el algoritmo con el parÃ¡metro
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            seleccionado
    @param: algorithm - nombre del algoritmo a aplicar
    '''
    def __showPreviewCanvas(self, algorithm) :

        # Si el algoritmo seleccionado es Douglas-Peucker
        if algorithm == self.Algorithms.DOUGLAS_PEUCKER :
<<<<<<< HEAD
            # El parametro será el específicado en el spiner de Douglas-Peucker
            param = self.spn_dp.value()
        else :
            # El parametro será el específicado en el spiner de McMaster
            param = self.spn_mcm.value()

        # Aplicamos el algoritmo con el parámetro introducido sobre la capa
=======
            # El parametro serÃ¡ el especÃ­ficado en el spiner de Douglas-Peucker
            param = self.spn_dp.value()
        else :
            # El parametro serÃ¡ el especÃ­ficado en el spiner de McMaster
            param = self.spn_mcm.value()

        # Aplicamos el algoritmo con el parÃ¡metro introducido sobre la capa
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.simplify.applyAlgorithm(algorithm, param)

        # Se activa el checkbox de suavizado
        self.cb_suav.setEnabled(True)

        # El checkbox de suavizado se pone en checked (ya que la capa se encuentra visible)
        self.cb_suav.setCheckState(Qt.Checked)

        # Asignamos a la capa preview un objeto de la clase QgsMapCanvasLayer a partir de
        # la capa de salida almacenada en el objeto de la clase GeneraLine
        self.preview = QgsMapCanvasLayer(self.simplify.layer_salida)

<<<<<<< HEAD
        # Conectamos al checkbox la función para cambiar la visualización de la capa generalizada
        self.cb_suav.clicked.connect( partial(self.toggleCanvasVisibilityLayer, self.preview) )

        # Añadimos al canvas las dos capas (se visualizan)
=======
        # Conectamos al checkbox la funciÃ³n para cambiar la visualizaciÃ³n de la capa generalizada
        self.cb_suav.clicked.connect( partial(self.toggleCanvasVisibilityLayer, self.preview) )

        # AÃ±adimos al canvas las dos capas (se visualizan)
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.canvas.setLayerSet([ self.original, self.preview ])


    '''
    @method: __openDialog
<<<<<<< HEAD
    @brief: Muestra un diálogo para seleccionar el archivo SHP
=======
    @brief: Muestra un diÃ¡logo para seleccionar el archivo SHP
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
    '''
    def __openDialog(self):
        # Se crea un objeto del tipo QFileDialog
        dlg = QFileDialog()

        # Busca por archivos existentes en el sistema
        dlg.setFileMode(QFileDialog.ExistingFile)
<<<<<<< HEAD
        # Solo mostrar archivos con extensión shp
=======
        # Solo mostrar archivos con extensiÃ³n shp
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        dlg.setFilter("shapefile (*.shp)")

        # Cuando devuelva True ( Cuando se haya seleccionado la carpeta de salida )
        if dlg.exec_():
            # Obtenemos la ruta del archivo
            filepath = map(str, list(dlg.selectedFiles()))[0]
<<<<<<< HEAD
            # Llamamos a la función __addLayer con la ruta del archivo para añadirlo como capa
=======
            # Llamamos a la funciÃ³n __addLayer con la ruta del archivo para aÃ±adirlo como capa
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            self.__addLayer(filepath)


    '''
    @method: __openDialog_folder
<<<<<<< HEAD
    @brief: Muestra un diálogo para seleccionar la carpeta de salida
=======
    @brief: Muestra un diÃ¡logo para seleccionar la carpeta de salida
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
    '''
    def __openDialog_folder(self):
        # Crea un dialogo para seleccionar un directorio y devuelve la ruta
        self.folder = QFileDialog().getExistingDirectory()

        # Muestra en el label la ruta de la carpeta de salida
        self.label_selected_folder.setText(self.folder)

<<<<<<< HEAD
        # Llamamos a la función activaGuardar
=======
        # Llamamos a la funciÃ³n activaGuardar
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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
<<<<<<< HEAD
            # Devuelve un mensaje de aviso y no continúa
=======
            # Devuelve un mensaje de aviso y no continÃºa
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            QMessageBox.information(None,'Warning', 'No se trata de una capa LineString')
            return

        # Creamos un objeto de tipo QgsMapCanvasLayer
<<<<<<< HEAD
        # De esta forma podremos activar o desactivar la visualización a partir de la capa
=======
        # De esta forma podremos activar o desactivar la visualizaciÃ³n a partir de la capa
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        # y no utilizando la clase QgsLegend
        self.original = QgsMapCanvasLayer(layer)

        # Asignamos la capa al objeto de la clase GeneraLine ( capa de entrada )
        self.simplify.setLayer(layer)

<<<<<<< HEAD
        # Ponemos al canvas la extensión de la capa de entrada
        self.canvas.setExtent(layer.extent())

        # Añadimos al canvas la capa original
        self.canvas.setLayerSet([self.original])

        # Le aplicamos simbología
=======
        # Ponemos al canvas la extensiÃ³n de la capa de entrada
        self.canvas.setExtent(layer.extent())

        # AÃ±adimos al canvas la capa original
        self.canvas.setLayerSet([self.original])

        # Le aplicamos simbologÃ­a
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        symbols = layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QtGui.QColor.fromRgb(204, 51, 51))

        # Activamos botones y checkbox para que se pueda interactuar

<<<<<<< HEAD
        # Botón previsualizar la generalización de Douglas-Peucker
        self.btn_prev_dp.setEnabled(True)
        # Botón previsualizar la generalización de McMaster
        self.btn_prev_mcm.setEnabled(True)
        # Se activa el checkbox de visualización de la capa de entrada
=======
        # BotÃ³n previsualizar la generalizaciÃ³n de Douglas-Peucker
        self.btn_prev_dp.setEnabled(True)
        # BotÃ³n previsualizar la generalizaciÃ³n de McMaster
        self.btn_prev_mcm.setEnabled(True)
        # Se activa el checkbox de visualizaciÃ³n de la capa de entrada
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.cb_ori.setEnabled(True)
        # Se marca como checked
        self.cb_ori.setCheckState(Qt.Checked)
        # Se activa el checkbox del algoritmo Douglas-Peucker
        self.cb_dp.setEnabled(True)
        # Se activa el checkbox del algoritmo McMaster
        self.cb_mcm.setEnabled(True)
<<<<<<< HEAD
        # Se activa el botón de zoom extensión
=======
        # Se activa el botÃ³n de zoom extensiÃ³n
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Conectamos al checkbox de visualización de la capa de entrada a su función
        self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )

        # Conecta el botón de zoom con su función
=======
        # Conectamos al checkbox de visualizaciÃ³n de la capa de entrada a su funciÃ³n
        self.cb_ori.toggled.connect( partial(self.toggleCanvasVisibilityLayer, self.original) )

        # Conecta el botÃ³n de zoom con su funciÃ³n
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.btn_zoom.clicked.connect( partial( self.zoomExt, layer ) )


    '''
    @method: zoomExt
<<<<<<< HEAD
    @brief: Realiza un zoom extensión de la capa de entrada en el canvas
    @param: layer - capa de visualización
    '''
    def zoomExt(self,layer):
        # Asignamos la extensión del canvas a la extensión de la capa
=======
    @brief: Realiza un zoom extensiÃ³n de la capa de entrada en el canvas
    @param: layer - capa de visualizaciÃ³n
    '''
    def zoomExt(self,layer):
        # Asignamos la extensiÃ³n del canvas a la extensiÃ³n de la capa
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.canvas.setExtent(layer.extent())
        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: toggleCanvasVisibilityLayer
<<<<<<< HEAD
    @brief: Se visualiza o no la capa en función del estado de la capa
    @param: layer - capa de visualización
    '''
    def toggleCanvasVisibilityLayer(self, layer):
        # Boolean del estado de visualización la capa
        visibility = layer.isVisible()

        # Asignamos la visualización de la capa a lo contrario que había antes
        layer.setVisible(not visibility)

        # Hay que volver a añadir las capas para que se muestren
=======
    @brief: Se visualiza o no la capa en funciÃ³n del estado de la capa
    @param: layer - capa de visualizaciÃ³n
    '''
    def toggleCanvasVisibilityLayer(self, layer):
        # Boolean del estado de visualizaciÃ³n la capa
        visibility = layer.isVisible()

        # Asignamos la visualizaciÃ³n de la capa a lo contrario que habÃ­a antes
        layer.setVisible(not visibility)

        # Hay que volver a aÃ±adir las capas para que se muestren
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Modificamos la escala del canvas en función del QgsScaleWidget
=======
        # Modificamos la escala del canvas en funciÃ³n del QgsScaleWidget
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.canvas.zoomScale(1 / (self.scaleControl.scale() if not self.scaleControl.scale() == 0 else 1 ) )

        # Refrescamos el canvas
        self.canvas.refresh()

    '''
    @method: on_canvas_scale_changed
    @brief: Se ejecuta cuando cambia la escala del canvas.
            Modifica la escala del QgsScaleWidget.
    '''
    def on_canvas_scale_changed(self, scale):
<<<<<<< HEAD
        # Modifica la escala del QgsScaleWidget en función de la escala del canvas
=======
        # Modifica la escala del QgsScaleWidget en funciÃ³n de la escala del canvas
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.scaleControl.setScale(1 / scale)


    '''
    @method: __init_ui
    @brief: Inicializa los componentes del formulario. Obtenido de uic.
<<<<<<< HEAD
            Añadiéndole componente de QGIS: Canvas, QgsScaleWidget
=======
            AÃ±adiÃ©ndole componente de QGIS: Canvas, QgsScaleWidget
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
A continuación mostramos la clase **``GeneraLine``** que es la encargada de realizar los algoritmos.
=======
A continuaciÃ³n mostramos la clase **``GeneraLine``** que es la encargada de realizar los algoritmos.
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

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
<<<<<<< HEAD
@brief: Clase que servirá para ejecutar los algoritmos
        de suavizado y reducción de puntos sobre una capa de Líneas
=======
@brief: Clase que servirÃ¡ para ejecutar los algoritmos
        de suavizado y reducciÃ³n de puntos sobre una capa de LÃ­neas
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
@param: layer - Capa de entrada
'''
class GeneraLine:

<<<<<<< HEAD
    # Variable de clase estática que almacena la clase Algoritmos
=======
    # Variable de clase estÃ¡tica que almacena la clase Algoritmos
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
    Algorithms = Algorithms

    # Lista con los algoritmos posibles
    algorithms = [Algorithms.MC_MASTER, Algorithms.DOUGLAS_PEUCKER]

    # Constructor
    def __init__(self, layer = None):

        # Variable de clase self.layer_salida
<<<<<<< HEAD
        # Almacenará las features de salida
=======
        # AlmacenarÃ¡ las features de salida
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        self.layer_salida = None

        # Si se le pasa layer al constructor
        if layer :
            # Asignamos la capa como variable de clase
            self.setLayer(layer)

    '''
    @method: setLayer
    @brief: Asignamos como variable de clase la capa que se le pasa
            y creamos la capa de salida en memoria (layer_salida)
<<<<<<< HEAD
            con los parámetros de la capa de entrada (crs, nombre, ...)
=======
            con los parÃ¡metros de la capa de entrada (crs, nombre, ...)
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Cambiamos la simbología
=======
        # Cambiamos la simbologÃ­a
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        symbols = self.layer_salida.rendererV2().symbols()
        symbol = symbols[0]
        # Cambiamos el color de la capa de salida a un tono azulado
        symbol.setColor(QtGui.QColor.fromRgb(102, 102, 255))

<<<<<<< HEAD
        # Añadimos las capas al registro de QGIS
=======
        # AÃ±adimos las capas al registro de QGIS
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
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

<<<<<<< HEAD
        # Comenzamos la edición sobre la capa de salida
        with edit(self.layer_salida):
            # Metemos la lógica dentro de un bloque try-except
=======
        # Comenzamos la ediciÃ³n sobre la capa de salida
        with edit(self.layer_salida):
            # Metemos la lÃ³gica dentro de un bloque try-except
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            try :
                # Eliminamos las features que puedan haber
                # en la capa de salida (de proceso anteriores)
                listOfIds = [feat.id() for feat in self.layer_salida.getFeatures()]
                self.layer_salida.deleteFeatures( listOfIds )

                # Recorreremos todas las features de la capa de entrada
                for feature in self.layer.getFeatures():

<<<<<<< HEAD
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
=======
                    # Obtenemos una referencia de la geometrÃ­a
                    geom = feature.geometry()

                    # Creamos una feature temporal
                    # ServirÃ¡ para recorrer geometrÃ­as multiparte
                    temp_feature = QgsFeature()

                    # Comprobamos la geomtrÃ­a
                    if not geom : continue

                    # Se crea un nuevo feature (temporal)
                    # ServirÃ¡ para crear la feature de la capa de salida
                    f = QgsFeature()


                    # Si la geometrÃ­a es multiparte (MULTILINESTRING)
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
                    if geom.isMultipart():
                        # Recorremos cada LineString (geom) dentro del MultiLineString
                        for geom_ in geom.asGeometryCollection():

<<<<<<< HEAD
                            # Asignamos la geometría a la feature temporal
                            temp_feature.setGeometry(geom_)

                            # Extraemos los puntos de la geomtría
                            points = self.__extractPoints(temp_feature)

                            # Ejecutamos el algoritmo pertinente
                            # sobre los puntos extraidos de la geometría que estamos recorriendo
=======
                            # Asignamos la geometrÃ­a a la feature temporal
                            temp_feature.setGeometry(geom_)

                            # Extraemos los puntos de la geomtrÃ­a
                            points = self.__extractPoints(temp_feature)

                            # Ejecutamos el algoritmo pertinente
                            # sobre los puntos extraidos de la geometrÃ­a que estamos recorriendo
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
                            if name == self.Algorithms.MC_MASTER:
                                resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                            else :
                                resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]

<<<<<<< HEAD
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
=======
                            # Obtenemoss la geometrÃ­a (Polyline) resultante de aplicar el algoritmo
                            resultLine = QgsGeometry.fromPolyline(resultPoints)
                            # AÃ±adimos la geomtrÃ­a a la feature temporal
                            f.setGeometry(resultLine)

                            # AÃ±adimos la feature a la capa de salida
                            self.layer_salida.addFeature(f)

                    # Si la geometrÃ­a no es multiparte
                    else :

                        # Extraemos los puntos de la geomtrÃ­a
                        points = self.__extractPoints(feature)

                        # Se crea un nuevo feature (temporal)
                        # ServirÃ¡ para crear la feature de la capa de salida
                        f = QgsFeature()

                        # Ejecutamos el algoritmo pertinente
                        # sobre los puntos extraidos de la geometrÃ­a que estamos recorriendo
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
                        if name == self.Algorithms.MC_MASTER:
                            resultPoints = [ QgsPoint(*x) for x in self.__mcMaster(points, param) ] #if len(x) > 1 ]
                        else :
                            resultPoints = [ QgsPoint(*x) for x in self.__douglasPeucker(points, param) ] #if len(x) > 1 ]


<<<<<<< HEAD
                        # Obtenemoss la geometría (Polyline) resultante de aplicar el algoritmo
                        resultLine = QgsGeometry.fromPolyline(resultPoints)
                        # Añadimos la geomtría a la feature temporal
                        f.setGeometry(resultLine)

                        # Añadimos la feature a la capa de salida
                        self.layer_salida.addFeature(f)
            # Si se produce una excepción
=======
                        # Obtenemoss la geometrÃ­a (Polyline) resultante de aplicar el algoritmo
                        resultLine = QgsGeometry.fromPolyline(resultPoints)
                        # AÃ±adimos la geomtrÃ­a a la feature temporal
                        f.setGeometry(resultLine)

                        # AÃ±adimos la feature a la capa de salida
                        self.layer_salida.addFeature(f)
            # Si se produce una excepciÃ³n
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            except Exception as e:
                # mostramos un mensaje de error
                QMessageBox.information(None, 'ERROR!', str(e))

                print 'error', e

    '''
    @method: __shortestDistance
<<<<<<< HEAD
    @brief: Devuelve la ditancia más corta entre
            un punto y una recta
    @param: point - lista con los valores x,y del punto ej: [1000, 1000]
    @param: line: lista con los parámetros a,b,c que definen una línea ax + by + c = 0
    @return: double - distancia más corta
=======
    @brief: Devuelve la ditancia mÃ¡s corta entre
            un punto y una recta
    @param: point - lista con los valores x,y del punto ej: [1000, 1000]
    @param: line: lista con los parÃ¡metros a,b,c que definen una lÃ­nea ax + by + c = 0
    @return: double - distancia mÃ¡s corta
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
    '''
    def __shortestDistance(self,point, line):
        # Extraemos las coordenadas del punto
        xp, yp = point
<<<<<<< HEAD
        # Extraemos los parámetros de la línea
        a, b, c = line
        # Calculamos y deolvemos la ditancia mínima entre el punto y la recta
=======
        # Extraemos los parÃ¡metros de la lÃ­nea
        a, b, c = line
        # Calculamos y deolvemos la ditancia mÃ­nima entre el punto y la recta
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        return math.fabs(a*xp + b*yp + c)/math.sqrt(a**2 + b**2)

    '''
    @method: __extractPoints
    @brief: Extrae los puntos de una feature (simple)
    @param: feature - feature de entrada
<<<<<<< HEAD
    @return: [] - lista de puntos de la geomtría del feature pasado como parámetro
    '''
    def __extractPoints(self, feature):
        # Obtenemos una referencia de la geometría
        geom = feature.geometry()

        # Creamos una lista vacía
        points = []

        # Comprobamos que la geometría no sea None
        # En cuyo caso devolvemos una lista vacía
=======
    @return: [] - lista de puntos de la geomtrÃ­a del feature pasado como parÃ¡metro
    '''
    def __extractPoints(self, feature):
        # Obtenemos una referencia de la geometrÃ­a
        geom = feature.geometry()

        # Creamos una lista vacÃ­a
        points = []

        # Comprobamos que la geometrÃ­a no sea None
        # En cuyo caso devolvemos una lista vacÃ­a
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        if geom == None: return points

        # contador
        i = 0

<<<<<<< HEAD
        # Bucle while que recorre los  vértices de
        # la geometría
        while(geom.vertexAt(i) != QgsPoint(0,0)):
            # Obtenemos el vértice según el ídice i
            # y lo añadimos a la lista
=======
        # Bucle while que recorre los  vÃ©rtices de
        # la geometrÃ­a
        while(geom.vertexAt(i) != QgsPoint(0,0)):
            # Obtenemos el vÃ©rtice segÃºn el Ã­dice i
            # y lo aÃ±adimos a la lista
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            points.append(geom.vertexAt(i))
            # aumentamos el contador en 1
            i += 1

        # Devolvemos la lista
        return points

    '''
    @method: __mcMaster
<<<<<<< HEAD
    @brief: Aplica el algoritmo de generalización de McMaster
    @param: points - lista de puntos de la geomtría de la capa de entrada
    @param:  mu - número de vertices que entran en el cálculo de la media (impar > 1)
    @return: [] - lista de puntos con las coordenadas de la línea suavizada
    '''
    def __mcMaster(self, points, mu):
            # Si no hay puntos devuelve una lista vacía
            if not points : return []
            # Parámetro para el vecindario de cada vertice
=======
    @brief: Aplica el algoritmo de generalizaciÃ³n de McMaster
    @param: points - lista de puntos de la geomtrÃ­a de la capa de entrada
    @param:  mu - nÃºmero de vertices que entran en el cÃ¡lculo de la media (impar > 1)
    @return: [] - lista de puntos con las coordenadas de la lÃ­nea suavizada
    '''
    def __mcMaster(self, points, mu):
            # Si no hay puntos devuelve una lista vacÃ­a
            if not points : return []
            # ParÃ¡metro para el vecindario de cada vertice
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            half_mu = int(math.floor(mu/2))
            # Longitud de la lista de puntos
            end = len(points)

            # Lista con los puntos del suavizado
<<<<<<< HEAD
            # empezamos añadiendo los puntos primeros que quedan fuera del rango
=======
            # empezamos aÃ±adiendo los puntos primeros que quedan fuera del rango
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            # [0, half_mu)
            smooth_points = map( list, points[ : half_mu ] )
            #print smooth_points

<<<<<<< HEAD
            # Generamos un iterador para obtener los índices de los puntos de los
=======
            # Generamos un iterador para obtener los Ã­ndices de los puntos de los
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            # cuales podemos aplicar un vecindario de mu
            for i in range(half_mu, end - half_mu):

                # Obtenemos el punto situado en medio del vecindario
                xactual, yactual = points[i]

                # Obtenemos los puntos que forman parte del vecindario
                computed_points = points[i - half_mu : i + (mu + 1)/2]

                # Obtenemos las coordenadas de los puntos en listas (una para cada coord)
                xcoords = [p[0] for p in computed_points]
                ycoords = [p[1] for p in computed_points]

<<<<<<< HEAD
                # Obtenemos la media geométrica de los puntos que conforman el vecindario
                mediax, mediay = sum(xcoords)/len(xcoords), sum(ycoords)/len(ycoords)


                # Y realizamos la media geométrica con la media del vecindario y el punto
                # de estudio
                x, y = (mediax + xactual)/2, (mediay + yactual)/2
                # Finalmente lo añadimos a la lista de puntos del suavizado
                smooth_points.append([x, y])

            # finalizamos añadiendo los puntos primeros que quedan fuera del rango
=======
                # Obtenemos la media geomÃ©trica de los puntos que conforman el vecindario
                mediax, mediay = sum(xcoords)/len(xcoords), sum(ycoords)/len(ycoords)


                # Y realizamos la media geomÃ©trica con la media del vecindario y el punto
                # de estudio
                x, y = (mediax + xactual)/2, (mediay + yactual)/2
                # Finalmente lo aÃ±adimos a la lista de puntos del suavizado
                smooth_points.append([x, y])

            # finalizamos aÃ±adiendo los puntos primeros que quedan fuera del rango
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            # [end - half_mu, end)
            smooth_points += map( list, points[ -half_mu : ] )

            # Devuelve una lista con los puntos de la linea suavizada por el algoritmo
            # McMaster
            return smooth_points

    '''
    @method: __douglasPeucker
<<<<<<< HEAD
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
=======
    @brief: Aplica el algoritmo de generalizaciÃ³n de Douglas-Peucker
    @param: points - lista de puntos de la geomtrÃ­a de la capa de entrada
    @param:  epsilon - distancia mÃ­nima para incluir el vÃ©rtice
    @return: [] - lista de puntos con las coordenadas de la lÃ­nea generalizada
    '''
    def  __douglasPeucker(self,points, epsilon):
        # Distancia mÃ¡xima
        dmax = 0
        # Ãndice de la posiciÃ³n en la lista del punto de mÃ¡xima distancia
        index = 0

        # Ãndice final para el bucle
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        end = len(points) - 1

        # Punto inicial
        x0, y0 = points[0]
        # Punto final
        x1, y1 = points[-1]

<<<<<<< HEAD
        # Parámetros de la recta
=======
        # ParÃ¡metros de la recta
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        a = y1 - y0
        b = -(x1 - x0)
        c = a*(-x0) - b*y0


<<<<<<< HEAD
        # Si el primer y el último punto son el mismo
        if a == 0 and b == 0 : return []

        # Generamos un iterador para obtener los índices
=======
        # Si el primer y el Ãºltimo punto son el mismo
        if a == 0 and b == 0 : return []

        # Generamos un iterador para obtener los Ã­ndices
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        for i in range(1, end):

            # punto
            p = points[i]

<<<<<<< HEAD
            # distancia más corta entre el punto y la recta
=======
            # distancia mÃ¡s corta entre el punto y la recta
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            d = self.__shortestDistance(p, [a, b, c])

            # Si la distancia es mayor que lo que haya almacenado en dmax
            if d > dmax :
<<<<<<< HEAD
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
=======
                # Guardamos el Ã­ndice y la distancia en las variables
                index = i
                dmax = d

        # Si la ditancia mÃ¡xima es mayor o igual que epsilon
        if dmax >= epsilon :
            # Realizamos el algoritmo

            # res_ini almacenarÃ¡ los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porciÃ³n de la lista de puntos desde 0 hasta el Ã­ndice
            # del punto de "distancia mÃ¡xima sobre la recta" + 1
            res_ini = self.__douglasPeucker(points[: index + 1], epsilon)

            # res_fin almacenarÃ¡ los resultados de aplicar el algoritmo otra vez
            # (recursividad) sobre la porciÃ³n de la lista de puntos desde el Ã­ndice
            # del punto de "distancia mÃ¡xima sobre la recta" hasta len(points)
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
            res_fin = self.__douglasPeucker(points[index : ], epsilon)

            # Juntamos las dos listas resultantes y devolvemos el array juntado
            return res_ini[:-1] + res_fin

<<<<<<< HEAD
        # Si la distancia máxima es menor que epsilon
=======
        # Si la distancia mÃ¡xima es menor que epsilon
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
        else :
            # Devolvemos una lista con los puntos inicial y final
            return [ points[0], points[-1] ]


```

<<<<<<< HEAD
En primero lugar, lo que hicimos fue desarrollar los algoritmos en python como funciones y viendo si podriamos desarrollar otros procesos como funciones también. Por ejemplo el cálculo de la distancia mínima en el caso del algoritmo **Douglas-Peucker**, se ha desarrollado como una función externa.
    
Una vez desarrollados los algoritmos los metimos en una clase GeneraLine y hicimos checkeos como ver si la capa que se introduce es del tipo *`LineString(if layer.wkbType()==QGis.WKBLineString: ...)`*, comprovar si la capa es multiparte o recoger el EPSG de la capa. Para cada capa se recorrerán todos sus features y se aplicará el algoritmo seleccionado.

Creamos la función *`__extractPoints(feature)`* para extraer todos los puntos de cada feature y poder así aplicar los algoritmos sobre estos.
Con la función predefinida de PyQgis vertexAt(i), siendo i el índice del vértice, extraemos de la geometria de cada feature dichos puntos de la siguiente manera:
=======
En primero lugar, lo que hicimos fue desarrollar los algoritmos en python como funciones y viendo si podriamos desarrollar otros procesos como funciones tambiÃ©n. Por ejemplo el cÃ¡lculo de la distancia mÃ­nima en el caso del algoritmo **Douglas-Peucker**, se ha desarrollado como una funciÃ³n externa.
    
Una vez desarrollados los algoritmos los metimos en una clase GeneraLine y hicimos checkeos como ver si la capa que se introduce es del tipo *`LineString(if layer.wkbType()==QGis.WKBLineString: ...)`*, comprovar si la capa es multiparte o recoger el EPSG de la capa. Para cada capa se recorrerÃ¡n todos sus features y se aplicarÃ¡ el algoritmo seleccionado.

Creamos la funciÃ³n *`__extractPoints(feature)`* para extraer todos los puntos de cada feature y poder asÃ­ aplicar los algoritmos sobre estos.
Con la funciÃ³n predefinida de PyQgis vertexAt(i), siendo i el Ã­ndice del vÃ©rtice, extraemos de la geometria de cada feature dichos puntos de la siguiente manera:
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449

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
<<<<<<< HEAD
- Capa de Orografía (curvas)
Sabiendo que no tiene sentido generalizar de esta forma las curvas de nivel ya que pierden su significado geográfico y nos inventaríamos una forma del terreno distinta, hemos probado para ver como funcionan los algorítmos sobre un curvado tan complejo con distintos valores de parámetro.
    - Algoritmo Douglas-Peucker - distancia mínima 50
    - Algoritmo Douglas-Peucker - distancia mínima 5
    - Algoritmo Douglas-Peucker - distancia mínima 1
    Vemos que el algoritmo funciona mejor para este caso con una distancia mínima pequeña.
    - Algoritmo McMaster - vecindario 9
    - Algoritmo McMaster - vecindario 21
Como las curvas varían mucho en vecindarios pequeños se observa al aplicar vecindarios más grandes como el suavizado se aleja de la curva original drásicamente al realizar la media de todo el vecindario.

- Capa de Hidrografía
Para lineas menos cambiantes dependiende de nuestro próposito nos servirá uno mejor que otro. Para generalizar usaremos el algoritmo de Douglas-Peucker (eliminando puntos) y para suavizar usaremos el algorítmo de McMaster el cual atenuará los picos generados por la intersección en los vértices (curvará la linea).
=======
- Capa de OrografÃ­a (curvas)
Sabiendo que no tiene sentido generalizar de esta forma las curvas de nivel ya que pierden su significado geogrÃ¡fico y nos inventarÃ­amos una forma del terreno distinta, hemos probado para ver como funcionan los algorÃ­tmos sobre un curvado tan complejo con distintos valores de parÃ¡metro.
    - Algoritmo Douglas-Peucker - distancia mÃ­nima 50
    - Algoritmo Douglas-Peucker - distancia mÃ­nima 5
    - Algoritmo Douglas-Peucker - distancia mÃ­nima 1
    Vemos que el algoritmo funciona mejor para este caso con una distancia mÃ­nima pequeÃ±a.
    - Algoritmo McMaster - vecindario 9
    - Algoritmo McMaster - vecindario 21
Como las curvas varÃ­an mucho en vecindarios pequeÃ±os se observa al aplicar vecindarios mÃ¡s grandes como el suavizado se aleja de la curva original drÃ¡sicamente al realizar la media de todo el vecindario.

- Capa de HidrografÃ­a
Para lineas menos cambiantes dependiende de nuestro prÃ³posito nos servirÃ¡ uno mejor que otro. Para generalizar usaremos el algoritmo de Douglas-Peucker (eliminando puntos) y para suavizar usaremos el algorÃ­tmo de McMaster el cual atenuarÃ¡ los picos generados por la intersecciÃ³n en los vÃ©rtices (curvarÃ¡ la linea).
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
    - prueba1 _50
    - hidro_dp_20

    - hidro_mcm_9


# Conclusiones

Tras realizar varias pruebas con el software generado podemos poner en la mesa distintos puntos favorables y distintos puntos a mejorar:

- **Respecto al UI generado**

<<<<<<< HEAD
Se ha elaborado un UI bastante logrado que alberga muchas funcionalidades. Se podrían mejorar diversos aspectos de menor importancia que podrían ver luz en futuros releases.

Un aspecto importante que no se ha llegado a conseguir pero que se puede ver en el archivo [project_sig2.py](https://github.com/hectormg92/pyqgis-awesome-linestring-generalizer/blob/master/project_sig2.py) es ejecutar los procesos de la clase GeneraLine en otro hilo de ejecución para no interferir con el hilo de renderizado del UI y de esta manera no bloquearlo.

- **Respecto a los algoritmos**

El parámetro a introducir en el algoritmo de Douglas Peucker, para mejorar la experiencia del usuario, debería ser un número comprendido entre 0 y 1 (escalando con la distancia máxima entre los distintos vértices con la recta (que une el punto inicial y final).

Además esta misma idea también se podría aplicar al algoritmo McMster con el número de vértices máximo (ya que el mínimo es tres).

Se podría llevar a cabo una funcionalidad extra que concatenara distintas órdenes para ejecutar varios algoritmos de una vez con el resultado del proceso anterior (Parecido a como hace ArcMap con ModelBuilder).
Por ejemplo:

- Proceso 1 : Aplicar Douglas Peucker a la capa de entrada
- Proceso 2 : Aplicar McMaster a la capa resultante del proceso 1
=======
Se ha elaborado un UI bastante logrado que alberga muchas funcionalidades. Se podrÃ­an mejorar diversos aspectos de menor importancia que podrÃ­an ver luz en futuros releases.

Un aspecto importante que no se ha llegado a conseguir pero que se puede ver en el archivo [project_sig2.py](https://github.com/hectormg92/pyqgis-awesome-linestring-generalizer/blob/master/project_sig2.py) es ejecutar los procesos de la clase GeneraLine en otro hilo de ejecuciÃ³n para no interferir con el hilo de renderizado del UI y de esta manera no bloquearlo.

- **Respecto a los algoritmos**

El parÃ¡metro a introducir en el algoritmo de Douglas Peucker, para mejorar la experiencia del usuario, deberÃ­a ser un nÃºmero comprendido entre 0 y 1 (escalando con la distancia mÃ¡xima entre los distintos vÃ©rtices con la recta (que une el punto inicial y final).

AdemÃ¡s esta misma idea tambiÃ©n se podrÃ­a aplicar al algoritmo McMster con el nÃºmero de vÃ©rtices mÃ¡ximo (ya que el mÃ­nimo es tres).

Se podrÃ­a llevar a cabo una funcionalidad extra que concatenara distintas Ã³rdenes para ejecutar varios algoritmos de una vez con el resultado del proceso anterior (Parecido a como hace ArcMap con ModelBuilder).
Por ejemplo:

- Proceso 1 : Aplicar Douglas Peucker a la capa de entrada
- Proceso 2 : Aplicar McMaster a la capa resultante del proceso 1





    
    
    
    
    
    
    
>>>>>>> ae56f17afc1c98bcc4e77b9e0bdce7986984a449
