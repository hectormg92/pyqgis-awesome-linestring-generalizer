# pyqgis-awesome-linestring-generalizer

El proyecto final de la asignatura Desarrollo de aplicaciones SIG se ha centrado en las ideas listadas: 13- Aplicar el algoritmo de eliminación de Douglas Peucker y 14- Aplicar el algoritmo de suavizamiento McMaster empleados en generalización cartográfica.
Hemos decidido abordarlo desde QGIS (PyQGIS) principalmente por tratarse de software libre.
----------

# Algoritmos:
 - Algoritmo de eliminación de Douglas-Peucker
 
El algoritmo de Douglas-Peucker se usa para reducir el número de puntos utilizados en la aproximación de una curva. El objetivo del algoritmo es, dada una curva compuesta por segmentos, encontrar una curva similar aproximada con menos puntos. El algoritmo define un parámetro basado en la máxima distancia entre la curva original y la simplificada.
El algoritmo seguido sería el siguiente:

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

En resumen, el algoritmo construye una linea desde el primer hasta el último punto de la linea y busca el vertice con una mayor distancia (que forme un ángulo recto) al segmento y lo agrega si está a una distancia mayor a epsilon. Con los dos segmentos formados se repetiría el proceso hasta no haber puntos o que estos no superen el umbral epsilon. Es un proceso recursivo dónde la nueva curva es generada a partir de los puntos que han permanecido tras aplicar el algoritmo.

- Algoritmo de suavizamiento de McMaster
También conocido como algoritmo de deslizamiento de McMaster. Este algoritmo dejará fijos el primer y último punto de la línea y calculará la nueva posición (posición media) de los demás puntos a partir de sus coordenadas y las de sus vecinos.
Tiene un parámetro de entrada que es el número de vertices con los que calculará la media de las coordenadas de cada uno, por lo que este deberá ser un número impar (mismo número de vecinos a cada lado del vértice y el propio vértice).

El algoritmo seguido es el siguiente:

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
    
    Decir que los algoritmos planteados están en pseudocódigo y no responden a ningún lenguaje de programación en sí. Para entender y ver mejor lo efectuado revisar el código python.
    

    
    
    
    
    
    
    
    
    
    
    
