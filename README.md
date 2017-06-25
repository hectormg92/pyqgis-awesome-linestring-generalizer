# pyqgis-awesome-linestring-generalizer

El proyecto final de la asignatura **`Desarrollo de aplicaciones SIG`** se ha centrado en las ideas listadas: 
* ``(13)`` **Aplicar el algoritmo de eliminación de [**`Douglas Peucker`**](https://es.wikipedia.org/wiki/Algoritmo_de_Ramer%E2%80%93Douglas%E2%80%93Peucker)**
* ``(14)`` **Aplicar el algoritmo de suavizamiento **`McMaster`** empleados en** generalización cartográfica.
Hemos decidido abordarlo desde **``QGIS (PyQGIS)``** principalmente por tratarse de software libre.

# Algoritmos:
 - Algoritmo de eliminación de ***``Douglas-Peucker``***

![Animación Douglas Peucker](https://upload.wikimedia.org/wikipedia/commons/3/30/Douglas-Peucker_animated.gif)

El algoritmo de Douglas-Peucker se usa para reducir el número de puntos utilizados en la aproximación de una curva. El objetivo del algoritmo es, dada una curva compuesta por segmentos, encontrar una curva similar aproximada con menos puntos. El algoritmo define un parámetro basado en la máxima distancia entre la curva original y la simplificada.
El algoritmo seguido sería el siguiente:

```javascript
function DouglasPeucker(PointList[], epsilon)
    // Busca el punto con la distancia máxima
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
 
        // Construcción de la lista resultado
        ResultList[] = {recResults1[1...end-1] recResults2[1...end]}
    } else {
        ResultList[] = {PointList[1], PointList[end]}
    }
    // Devolver el resultado
    return ResultList[]
end
```
En resumen, el algoritmo construye una linea desde el primer hasta el último punto de la linea y busca el vertice con una mayor distancia (que forme un ángulo recto) al segmento y lo agrega si está a una distancia mayor a epsilon. Con los dos segmentos formados se repetiría el proceso hasta no haber puntos o que estos no superen el umbral epsilon. Es un proceso recursivo dónde la nueva curva es generada a partir de los puntos que han permanecido tras aplicar el algoritmo.

- Algoritmo de ***``suavizamiento de McMaster``***
También conocido como algoritmo de deslizamiento de McMaster. Este algoritmo dejará fijos el primer y último punto de la línea y calculará la nueva posición (posición media) de los demás puntos a partir de sus coordenadas y las de sus vecinos.
Tiene un parámetro de entrada que es el número de vertices con los que calculará la media de las coordenadas de cada uno, por lo que este deberá ser un número impar (mismo número de vecinos a cada lado del vértice y el propio vértice).

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
    Decir que los algoritmos planteados están en pseudocódigo y no responden a ningún lenguaje de programación en sí. Para entender y ver mejor lo efectuado revisar el código python.
    
Con este algoritmo lo que se conseguirá es un suavizado de las curvas por lo que éstas no serán tan acentuadas.

# Proceso
En primero lugar, lo que hicimos fue desarrollar los algoritmos en python como funciones y viendo si podriamos desarrollar otros procesos como funciones también. Por ejemplo el cálculo de la distancia mínima en el caso del algoritmo **Douglas-Peucker**, se ha desarrollado como una función externa.
    
Una vez desarrollados los algoritmos los metimos en una clase GeneraLine y hicimos checkeos como ver si la capa que se introduce es del tipo *`LineString(if layer.wkbType()==QGis.WKBLineString: ...)`*, comprovar si la capa es multiparte o recoger el EPSG de la capa. Para cada capa se recorrerán todos sus features y se aplicará el algoritmo seleccionado.

Creamos la función *`__extractPoints(feature)`* para extraer todos los puntos de cada feature y poder así aplicar los algoritmos sobre estos.
Con la función predefinida de PyQgis vertexAt(i), siendo i el índice del vértice, extraemos de la geometria de cada feature dichos puntos de la siguiente manera:

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

En la misma clase generaLine definimos la función para aplicar el algoritmo (según), applyAlgorithm. En la cual empezaremos la edición de una capa de salida, creada en cuanto se cargue la capa de entrada, dónde se recorrerán los features de la capa de entrada, se mirará si es multipart o no, para recorrer todas las partes si es necesario, se efectuará la extracción de los puntos mediante la función antes mencionada y se aplicará el algoritmo deseado por el usuario. De esta manera obtendremos los puntos de la generalización realizada, los cuales los transformaremos a linea como linedp = QgsGeometry.fromPolyline(points), se añadirá al feature y posteriormente a la capa de salida. Finalmente se terminará la edición. Esta función devuelve la capa de salida, layer_salida.


Para la creación de la herramienta se ha utilizado QtDesigner con PyQt4. Se ha creado un diálogo gráfico con pestañas, botones, checkbox, ventana de visualización y alguna cosa más. Para su buen funcionamiento lo hemos tenido que pasar a código python y "acoplar" al programa principal, de modo que todo el programa se encuentra en un único script ejecutable desde QGis. Algunos aspectos del diálogo se han tenido que modificar desde el propio código.
Además hemos tenido en cuenta al usuario y se ha facilitado, activando y desactivando botones (y funciones) conforme se requiere del programa.
Por lo que si no se introduce ninguna capa, no tendremos botones activos que no sea el de cargar el SHP. Al introducir la capa (de lineas) podremos aplicar y visualizar con los parámetros que queramos los algoritmos de Douglas-Peucker o McMaster. Podremos visualizar la capa original y la suavizada y activar o desactivar esta visualización. Y podremos aplicar estos algoritmos tantas veces como queramos para visualizarlos antes de guardar y así decidir cual algoritmo (o los dos) y que valor de parámetro queremos. Una vez decididos a guardar nuestros resultados, deberemos específicar una carpeta de salida en la pestaña "Carpeta de salida" y que algoritmos queremos aplicar para guardar en los checkbox debajo de la ventana de visualización; una vez hecho esto, se activará el botón de guardar y ya podremos guardar la generalización de la capa shape que hayamos introducido.


    
    
    
    
    
    
    
    
