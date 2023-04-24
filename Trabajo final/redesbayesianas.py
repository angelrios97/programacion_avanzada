#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Permite construir construir redes bayesianas y aplicar el algoritmo de enumeración para inferencia exacta.

    __author__: Ángel Ríos
    __date__: 6 de septiembre de 2021
"""

import doctest
from collections import defaultdict
from itertools import filterfalse, product, repeat
from functools import reduce, partial
from copy import copy
import graphviz as gv
import numpy as np


class GrafoDirigido:
    """Grafo dirigido dado a partir de su lista de aristas o diccionario de adyacencias.

        Clase con métodos propios de los grafos dirigidos como añadir o eliminar aristas orientadas, consultar los
        padres directos de un vértice, dualizar el grafo invirtiendo el sentido de las aristas o devolver los vértices
        según un orden topológico entre otros.

        :param aristas: Lista de pares ordenados de vértices ordenados según el sentido de la arista.
        :param adyacencias: Diccionario de adyacencias que tiene por claves vértices origen y por valores
        listas de vértices de llegada.
        :param vertices: Conjunto de los nombres de los vértices.
        :type aristas: list Lista de tuplas de strings.
        :type adyacencias: :collections.defaultdict: defaultdict(list) Diccionario por defecto en list.
        :type vertices: set Conjunto de strings.
    """

    def __init__(self, aristas=None, adyacencias=None):
        """Constructor de la clase GrafoDirigido que por defecto instancia un GrafoDirigido vacío.

            :param aristas: Lista de pares ordenados de vértices ordenados según el sentido de la arista.
            :param adyacencias: Diccionario de adyacencias que tiene por claves vértices origen y por valores
            listas de vértices de llegada.
            :type aristas: list
            :type adyacencias: :collections.defaultdict: defaultdict(list) Diccionario por defecto en list.
        """
        # Si no se pasa un arugmento, asigna el valor vacío.
        if aristas is None:
            aristas = []
        if adyacencias is None:
            adyacencias = defaultdict(list)
        if type(aristas) is defaultdict or type(aristas) is dict:  # Si pasamos solo un diccionario,
            adyacencias = aristas  # es el diccionario de adyacencias.
            aristas = []
        # Si pasamos solo uno de los arugmentos, actualiza el otro.
        if aristas and not adyacencias:
            self.aristas = aristas
            self.actualiza_adyacencias()
        elif adyacencias and not aristas:
            self.adyacencias = adyacencias
            self.actualiza_aristas()
        elif aristas and adyacencias:
            if not self.dict_adyacencias(aristas) == adyacencias and not self.list_aristas(
                    adyacencias) == aristas:  # Si aristas y adyacencias tienen información contradictoria.
                raise ValueError("La lista de aristas no es congruente con el diccionario de adyacencias")
        else:  # Asigna los atirbutos vacíos
            self.aristas = aristas
            self.adyacencias = adyacencias
        if self.aristas:  # Calcula y actualiza los vértices automáticamente.
            self.actualiza_vertices()
        else:  # Si es el grafo dirigido vacío.
            self.vertices = set()

    @staticmethod
    def dict_adyacencias(aristas):
        """Devuelve el diccionario de adyacencias a partir de una lista de pares ordenados de vértices.

            :param aristas: Lista de pares ordenados de vértices.
            :type aristas: list Lista de tuplas de strings.
            :return dic: Diccionario de adyacencias dado por aristas.
            :rtype dic: :collections.defaultdict: defaultdict(list)
        """
        dic = defaultdict(list)
        for _ in aristas:
            dic[_[0]].append(_[1])
        return dic

    @staticmethod
    def list_aristas(adyacencias):
        """Devuelve una lista de pares ordenados de vértices a partir de un diccionario de adyacencias.

            :param adyacencias: Diccionario de adyacencias.
            :type adyacencias: collections.defaultdict defaultdict(list) Diccionario por defecto en list.
            :return salida: Lista de pares ordenados de aristas dada por adyacencias.
            :rtype salida: list Lista de tuplas de strings.
        """
        aristas = []
        for key, value in adyacencias.items():
            aristas.append(list(product([key], value)))
        salida = []
        for _ in aristas:
            salida.extend(_)
        return salida

    def actualiza_aristas(self):
        """Asigna el atributo aristas a partir del atributo adyacencias."""
        self.aristas = self.list_aristas(self.adyacencias)

    def actualiza_adyacencias(self):
        """Asigna el atributo adyacencias a partir del atributo aristas."""
        self.adyacencias = self.dict_adyacencias(self.aristas)

    def actualiza_vertices(self):
        """Asigna el atributo vertices a partir del atributo aristas."""
        # Si el atributo de aristas es vacío, asigna los valores nulos.
        if not self.aristas:
            self.vertices = set()
        # En caso contrario, concatena todas las aristas, unifica y asigna como conjunto.
        else:
            self.vertices = (set(reduce(tuple.__add__, self.aristas)))

    def invertir_digrafo(self):
        """Dualiza el grafo dirigido invirtiendo el sentido de todas las aristas."""
        aristas = []
        for key, value in self.adyacencias.items():  # Recorre las adyacencias.
            # Añade [(padre1, hijo11), ..., (padre1, hijo1m)], ..., [(padren, hijon1), ..., (padren, hijonm)]
            aristas.append(list(product([key], value)))
        salida = []
        for _ in aristas:  # Extiende en salida todas las listas de tuplas.
            salida.extend(_)
        salida = [(_[1], _[0]) for _ in salida]  # Invierte el sentido de las aristas.
        self.adyacencias = self.dict_adyacencias(salida)
        self.actualiza_aristas()

    def padres(self, vertice):
        """Devuelve los vértices predecesores directos o padres de un vértice dado."

            :param vertice: Vértice del que se calculan los padres.
            :type vertice: str
            :return: Lista de vértices padre en el grafo dirigido.
            :rtype: list
        """
        filtro = filter(lambda x: vertice in x[1], self.adyacencias.items())
        return [_[0] for _ in filtro]

    def inserta_aristas(self, aristas):
        """Inserta un conjunto de aristas en el grafo dirigido.

            :param aristas: Lista de pares ordenados de vértices a insertar.
            :type aristas: list
        """
        self.aristas.extend(aristas)
        self.aristas = list(set(self.aristas))
        self.actualiza_adyacencias()
        self.actualiza_vertices()

    def quita_aristas(self, aristas):
        """Elimina un conjunto de aristas del grafo dirigido.

            :param aristas: Lista de pares ordenados de vértices a eliminar.
            :type aristas: list
        """
        self.aristas = list(filterfalse(lambda x: x in aristas, self.aristas))
        self.actualiza_adyacencias()
        self.actualiza_vertices()

    def orden_topologico(self):
        """Devuelve los vértices del grafo dirigido en orden topológico.

            Implementación del algoritmo de Kahn para calcular un orden
            topológico de los vértices de un grafo dirigido. Además,
            decide si el grafo dirigido es acíclico.

            :return: Lista de los vértices del grafo dirigido en un orden
            topológico si el grafo es acíclico.
            :rtype: list
            :raise ValueException: Si el grafo contiene ciclos.
        """
        grafo = copy(self)  # Aplica el algoritmo a una copia del grafo.
        orden = []  # Guarda el orden topológico.
        fuentes = [_ for _ in grafo.vertices if len(grafo.padres(_)) == 0]  # Vértices sin padres.
        while fuentes:  # Mientras haya vértices sin padres:
            # Extrae uno de los vértices y añádelo al orden topológico.
            vertice = fuentes[0]
            fuentes = fuentes[1:]
            orden.append(vertice)
            # Para todas las aristas desde el vértice,
            for adyacente in grafo.adyacencias[vertice]:
                grafo.quita_aristas([(vertice, adyacente)])  # elimina la arista del grafo.
                if not grafo.padres(adyacente):  # Si el adyacente no tiene padres,
                    fuentes.append(adyacente)  # añádelo a fuentes para procesarlo.
        if not grafo.aristas:  # Si no hay aristas, no hay ciclos y termina.
            return orden
        else:  # El grafo dirigido tiene al menos un ciclo, lanza error.
            raise ValueError('El grafo dirigido no es acíclico.')

    def grafo_pdf(self, filename='grafo'):
        """Muestra visualmente el grafo por pantalla y lo guarda en un archivo.

            :param filename: Nombre del fichero en que se guardará la imagen.
            :type filename: str
        """
        digrafo = gv.Digraph(filename=filename)
        for _ in self.aristas:
            digrafo.edge(*_)  # Añade cada arista.
        digrafo.view()  # Guarda la imagen y muéstrala o no por pantalla.


class RedBayesiana(GrafoDirigido):
    """Clase que hereda de GrafoDirigido para la construcción redes bayesianas e inferencia.

        Permite definir una red bayesiana a partir de un grafo dirigido acíclico tratando los vértices
        como variables y asignando a sus valores probabilidades. Contiene métodos como la lectura de una
        red a partir de un fichero de texto y la inferencia exacta mediante el método de enumeración.

        :param aristas: Lista de pares ordenados de vértices ordenados según el sentido de la arista.
        :param adyacencias: Diccionario de adyacencias que tiene por claves vértices origen y por valores
        listas de vértices de llegada.
        :param vertices: Lista de los nombres de los vértices.
        :param valores: Diccionario que tiene por claves los vértices y por valores, los posibles valores
        de la variable correspondiente.
        :param probabilidades: Lista de las probabilidades de cada posible valor de la variable dados los padres.
        :param factor: Diccionario de probabilidades de cada variable de la forma {vértice: {valor: probabilidad}}.
        :type aristas: list Lista de tuplas de strings.
        :type adyacencias: :collections.defaultdict: defaultdict(list) Diccionario por defecto en list.
        :type vertices: list Lista de strings.
        :type valores: list Lista de tuplas de string.
        :type probabiliaddes: list Lista de float.
        :type factor: :collections.defaultdict: defaultdict(dict) Diccionario por defecto en dict.
    """

    def __init__(self, aristas=None, adyacencias=None, valores=None, probabilidades=None):
        """Constructor de RedBayesiana que por defecto instancia una red bayesiana vacía extendiendo
        GrafoDirigido.__init__.

            :param aristas: Lista de pares ordenados de vértices ordenados según el sentido de la arista.
            :param adyacencias: Diccionario de adyacencias que tiene por claves vértices origen y por valores
            listas de vértices de llegada.
            :param valores: Diccionario que tiene por claves los vértices y por valores, los posibles valores
            de la variable correspondiente.
            :param probabilidades: Lista de las probabilidades de cada posible valor de la variable dados los padres.
            :type aristas: list
            :type adyacencias: defaultdict
            :type valores: defaultdict
            :type probabilidades: defaultdict
        """
        GrafoDirigido.__init__(self, aristas, adyacencias)  # Llama al constructor de la clase GrafoDirigido.
        # Si no se le pasa alguno de los argumentos, asigna los valores vacíos.
        if valores is None:
            valores = defaultdict(list)
        if probabilidades is None:
            probabilidades = {}
        # Asigna los valores vacíos a los atributos.
        self.valores = valores
        self.probabilidades = probabilidades
        self.actualiza_factor()

    def lee_estructura(self, nomfichero):
        """Lee y asigna la estructura completa de una red bayesiana a partir de un fichero de texto.

            :param nomfichero: String con el nombre del fichero alojado en el misma carpeta.
            :type nomfichero: str
        """
        fichero = open(nomfichero)
        lineas = list(map(str.split, fichero.readlines()))  # Lista con todas las líneas del fichero.
        fichero.close()
        lineas = list(filterfalse(lambda x: x == [], lineas))  # Elimina las líneas vacías
        valores = defaultdict(list)
        padres = defaultdict(list)
        probabilidades = defaultdict(list)
        for _ in range(len(lineas)):  # Recorre los índices de las líneas.
            if lineas[_][0] == 'variable':  # Si la línea _-ésima comienza por 'variable',
                valores.update({lineas[_][1]: lineas[_][2:]})  # actualiza el diccionario de valores.
                if len(lineas[_ + 1]) >= 2:  # Si la línea de padres contiene,
                    padres.update({lineas[_][1]: lineas[_ + 1][1:]})  # actualiza el diccionario de padres y
                probabilidades.update(
                    {lineas[_][1]: list(map(float, lineas[_ + 2]))})  # actualiza el diccionario de probabilidades.
        self.valores = valores
        self.probabilidades = probabilidades
        # Asigna como adyacencias la dada por el diccionario de padres, actualiza aristas y vértices.
        self.adyacencias = padres
        self.actualiza_aristas()
        self.actualiza_vertices()
        # La red bayesiana introducida es la que resulta de invertir el grafo dirigido.
        self.invertir_digrafo()
        self.actualiza_factor()
        # Comprueba que la suma de las probabilidades dadas las condiciones es 1.
        self.comprueba_probabilidades()

    def comprueba_probabilidades(self):
        """Comprueba para cada variable que la suma de las probabilidades de sus valores fijada cada combinación de
         probabilidades de los padres es 1.
        """
        for variable in self.vertices:  # Recorre las variables.
            prob = np.array(self.probabilidades[variable])  # Vector de probabilidades condicionadas.
            npartes = len(self.valores[variable])  # Número de partes en que dividimos el vector.
            particion = np.split(prob, npartes)  # Particion de prob
            sumas = np.array(reduce(np.ndarray.__add__, particion))
            if any(map(lambda x: x != 1, sumas)):  # Si alguna probabilidad no es 1, lanza error.
                raise ValueError("Error en la entrada: La suma de las probabilidades fijada una condición no es 1.")

    def actualiza_factor(self):
        """Asigna el atributo factor a partir del atributo probabilidades como {variable : {valor: probabilidad}}."""
        perm_valor = defaultdict(list)
        for _ in self.vertices:  # Recorre las variables.
            aux = [_]  # Variable.
            aux.extend(self.padres(_))  # Padres de la variable.
            # Actualiza el diccionario de valores de la forma {variable: valores} donde valor es el producto cartesiano
            # de todos los posibles valores de la variable y de sus padres en la red bayesiana.
            perm_valor.update({_: tuple(product(*[self.valores[i] for i in aux]))})
        prob = defaultdict(dict)
        # Actualiza el diccionario de probabilidades de la forma {variable: {valor: probabilidad}} recorriendo el
        # diccionario anterior de valores y añadiendo las probabilidades para cada combinación de valores.
        prob.update({k: {v[i]: self.probabilidades[k][i] for i in range(len(v))} for k, v in perm_valor.items()})
        self.factor = prob

    def mult_probabilidad_condicional(self, variable_valor, evidencias):
        """Devuelve un múltiplo de la probabilidad para un valor de una variable dadas unas evidencias apriori.

            :param variable_valor: Diccionario con el nombre de la variable y el valor.
            :param evidencias: Diccionario con los nombres de las variables de evidencias y su valor a priori.
            :type variable_valor: dict
            :type evidencias: dict
            :return: Un múltiplo de la probabilidad de que la variable tome el valor dadas las evidencias a priori.
            :rtype: float
        """
        # Consideramos la variable, su valor y sus padres en la red bayesiana.
        variable = list(variable_valor.keys())[0]
        valor = variable_valor[variable]
        padres = self.padres(variable)
        if not set(evidencias).issubset(padres):  # Si las evidencias no asignan valores a los padres, lanza error.
            raise ValueError('Las evidencias no asignan valores a los padres.')
        prob = self.factor[variable]

        def filtro(cond):  # Filtro que decide los valores de los padres en las evidencias.
            if cond[0] != valor:  # Descarta las condiciones que no involucren al valor de la variable.
                return False
            for _ in evidencias.keys():  # Descarta las condiciones que no coincidan con las dadas por las evidencias.
                if cond[padres.index(_) + 1] != evidencias[_]:  # El valor para el padre no coincide con el observado.
                    return False
            return True

        indices = filter(filtro, prob.keys())  # Filtra las condiciones por el filtro
        subprob = {_: prob[_] for _ in indices}  # Subdiccionario con las probabilidades a multiplicar.
        return reduce(float.__mul__, subprob.values())  # El resultado es la multiplicación de los valores.

    def mult_probabilidades_condicionales(self, variable, evidencias):
        """Aplica mult_probabilidad_condicional a cada uno de los posibles valores de una variable.

            :param variable: Nombre de la variable sobre la que se calculan los múltiplos de las probabilidades.
            :param evidencias: Diccionario con los nombres de las variables de evidencias y su valor a priori.
            :type variable: str
            :type evidencias: dict
            :rtype: list
        """
        # Función parcial que aplica la función anterior a un diccionario {variable: valor} con evidencias fijas.
        spc_aux = partial(self.mult_probabilidad_condicional, evidencias=evidencias)
        # Lista de todos los diccionarios {variable: valor} posibles en la red bayesiana con variable fija.
        variable_valores = [{variable: val} for val in self.valores[variable]]
        return list(map(spc_aux, variable_valores))  # Devuelve el resultado de aplicar la función anterior a cada uno.

    def enumeracion_aux(self, preguntas, evidencias):
        """Función auxiliar para el algoritmo de enumeración para inferencia exacta en redes bayesianas.

            Función recursiva auxiliar para el algoritmo de enumeración en redes bayesainas que servirá
            para calcular un múltiplo de la probabilidad de que se den las evidencias apriorísticas.

            :param preguntas: Lista de variables pregunta para la inferencia.
            :param evidencias: Diccionario con los nombres de las variables de evidencias y su valor a priori.
            :type preguntas: list
            :type evidencias: dict
            :rtype: float
        """
        if len(preguntas) == 0:  # Condición de parada de la recursión.
            return 1
        # Toma la primera de las variables que queden y el conjunto de evidencias sobre sus padres.
        y = preguntas[0]
        padres_e = {key: value for (key, value) in evidencias.items() if key in self.padres(y)}
        # Calcula el múltiplo de la probabilidad de manera recursiva.
        if y in evidencias:
            # y está asignado, calcula el producto directamente.
            return self.mult_probabilidad_condicional({y: evidencias[y]}, padres_e) * self.enumeracion_aux(
                preguntas[1:],
                evidencias)
        else:
            # y no está asignado, calcula las sumas con todos los posibles valores de y.
            factor1 = self.mult_probabilidades_condicionales(y, padres_e)
            factor2 = [self.enumeracion_aux(preguntas[1:], dict(evidencias, **{y: val})) for val in self.valores[y]]
            return sum(np.array(factor1) * np.array(factor2))  # El resultado es la suma de los productos.

    def enumeracion(self, variable, evidencias):
        """Implementación recursiva del algoritmo de enumeración para inferencia exacta en redes bayesianas.

            Se le pasa una variable pregunta y un diccionario de evidencias a priori de los valores de un conjunto de
            variables de la red bayesiana y devuelve la distribución de probabilidad a posterori de la variable
            calculada mediante el algoritmo de enumeración para inferencia exacta en redes bayesianas.

            :param variable: Variable pregunta de la que se calcula la distribución de probabilidad a posteriori.
            :param evidencias: Variables y valores conocidos como evidencia a priori.
            :type variable: str
            :type evidencias: dict
            :return: Distribución de probabilidad de la variable pregunta dadas las evidencias.
            :rtype: dict

            Ejemplo:

            >>> red = RedBayesiana()
            >>> red.lee_estructura('red_alarma')
            >>> red.enumeracion('Robo', {'Juanllama': 'SI', 'Mariallama': 'SI'})
            {'SI': 0.2841718353643929, 'NO': 0.7158281646356071}
        """
        # Si los nombres de las variables o los valores no son los de la red, lanza error.
        if not {variable}.union(set(evidencias.keys())).issubset(self.vertices):
            raise ValueError('Error en los nombres de las variables.')
        if any(map(lambda x: evidencias[x] not in self.valores[x], evidencias)):
            raise ValueError('Error en los valores de las variables en las evidencias.')
        # Función parcial que aplica la función auxiliar a todas las variables en orden topológico.
        ea_aux = partial(self.enumeracion_aux, self.orden_topologico())
        # Añade a las evidencias el par {variable: valor} y aplica la función anterior a cada uno.
        lista = [dict(evidencias, **{variable: val}) for val in self.valores[variable]]
        salida = np.array(list(map(ea_aux, lista)))
        # Normaliza los resultados para obtener una distribución de probabilidad.
        salida = salida / np.sum(salida)
        return {val: _ for val, _ in zip(self.valores[variable], salida)}  # Salida como diccionario.

    def enumeracion_total(self, evidencias):
        """Aplica el algoritmo de enumeración para todas las varibles de la red dadas las evidencias.

            Se le pasa un diccionario de evidencias de los valores de un conjunto de variables a priori y
            devuelve la distribución de probabilidad a posteriori de cada una de las variables de la red
            calculadas aplicando el algoritmo de enumeración para inferencia exacta en redes bayesianas.

            :param evidencias: Variables y valores conocidos como evidencia a priori.
            :type evidencias: dict
            :rtype: dict
        """
        # Función parcial que aplica el algoritmo de enumeración a una variable con evidencias fijas.
        enum = partial(self.enumeracion, evidencias=evidencias)
        distribucion = map(enum, self.vertices)  # Calcula todas las distribuciones de probabilidad.
        return {key: value for key, value in zip(self.vertices, distribucion)}  # Salida como diccionario.
