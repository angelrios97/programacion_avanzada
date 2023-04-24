#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batería principal de pruebas unitarias y funcionales para el desarrollo guiado por pruebas de
redesbayesianas.

Las pruebas comprueban el funcionamiento de los métodos para construir y manipular tanto grafos
dirigidos como las redes bayesianas y la lectura de la estructura a partir de un fichero. Además,
comprueban la inferencia exacta respecto a ejemplos de bibliografía de los que se conoce los
resultados.

__author__: Ángel Ríos
__date__: 6 de septiembre de 2021
"""
import unittest
from collections import defaultdict
import redesbayesianas as rb


class TestsRedesBayesianas(unittest.TestCase):

    # Tests sobre GrafoDirigido
    def test_constructor_gd(self):
        """Pruebas del constructor de la clase GrafoDirigido."""
        # Atributos vacíos
        grafo = rb.GrafoDirigido()
        attr_vacios = {'aristas': [], 'adyacencias': defaultdict(list, {}), 'vertices': set()}
        self.assertDictEqual(grafo.__dict__, attr_vacios)
        aristas = [('A', 'C'), ('B', 'C')]
        adyacencias = {'A': ['C'], 'B': ['C']}
        vertices = {'A', 'B', 'C'}
        # Adyacencias vacío, aristas no
        grafo = rb.GrafoDirigido(aristas)
        attr_uno_vacio = {'aristas': aristas, 'adyacencias': adyacencias,
                          'vertices': vertices}
        self.assertDictEqual(grafo.__dict__, attr_uno_vacio)
        # Aristas vacío, adyacencias no
        grafo = rb.GrafoDirigido(adyacencias=adyacencias)
        self.assertDictEqual(grafo.__dict__, attr_uno_vacio)
        # Artistas y adyacencias contradictorias, debe lanzar error.
        with self.assertRaises(ValueError):
            rb.GrafoDirigido([('A', 'C'), ('B', 'C')], {'A': ['B'], 'B': ['C']})

    def test_dict_adyacencias(self):
        """Pruebas del método estático dict_adyacencias de la clase GrafoDirigido."""
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C'), ('D', 'C'), ('A', 'D')])
        adyacencias = {'A': ['C', 'D'], 'B': ['C'], 'D': ['C']}
        self.assertDictEqual(grafo.dict_adyacencias(grafo.aristas), adyacencias)

    def test_list_aristas(self):
        """Pruebas del método estático list_aristas de la clase GrafoDirigido."""
        grafo = rb.GrafoDirigido(adyacencias={'A': ['C', 'D'], 'B': ['C'], 'D': ['C']})
        aristas = [('A', 'C'), ('B', 'C'), ('D', 'C'), ('A', 'D')]
        self.assertSetEqual(set(grafo.list_aristas(grafo.adyacencias)), set(aristas))

    def test_actualiza_vertices(self):
        """Pruebas del método actualiza_vertices de la clase GrafoDirigido."""
        # Sin vertices
        grafo = rb.GrafoDirigido()
        grafo.actualiza_vertices()
        self.assertSetEqual(grafo.vertices, set())
        # Con vértices
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C')])
        grafo.actualiza_vertices()
        self.assertSetEqual(grafo.vertices, {'A', 'B', 'C'})

    def test_actualiza_adyacencias(self):
        """Pruebas del método actualiza_adyacencias de la clase GrafoDirigido."""
        # Sin aristas
        grafo = rb.GrafoDirigido()
        grafo.actualiza_adyacencias()
        self.assertDictEqual(grafo.adyacencias, {})
        # Con aristas
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C')])
        grafo.actualiza_adyacencias()
        self.assertDictEqual(grafo.adyacencias, {'A': ['C'], 'B': ['C']})

    def test_actualiza_aristas(self):
        """Pruebas del método actualiza_aristas de la clase GrafoDirigido."""
        # Sin aristas
        grafo = rb.GrafoDirigido()
        grafo.actualiza_aristas()
        self.assertListEqual(grafo.aristas, [])
        # Con aristas
        grafo = rb.GrafoDirigido(adyacencias={'A': ['C'], 'B': ['C']})
        grafo.actualiza_adyacencias()
        self.assertListEqual(grafo.aristas, [('A', 'C'), ('B', 'C')])

    def test_invertir_digrafo(self):
        """Pruebas del método invertir_digrafo de la clase GrafoDirigido."""
        # Grafo vacío
        grafo = rb.GrafoDirigido()
        grafo.invertir_digrafo()
        grafo1 = rb.GrafoDirigido()
        self.assertDictEqual(grafo.__dict__, grafo1.__dict__)
        # Grafo no vacío
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C')])
        grafo.invertir_digrafo()
        grafo1 = rb.GrafoDirigido([('C', 'A'), ('C', 'B')])
        self.assertDictEqual(grafo.__dict__, grafo1.__dict__)

    def test_padres(self):
        """Pruebas del método padres de la clase GrafoDirigido."""
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C'), ('D', 'C'), ('A', 'D')])
        self.assertListEqual(grafo.padres('A'), [])  # Sin padres
        self.assertListEqual(grafo.padres('D'), ['A'])  # Padre único
        self.assertListEqual(grafo.padres('C'), ['A', 'B', 'D'])  # Múltiples padres

    def test_inserta_aristas(self):
        """Pruebas del método inserta_aristas de la clase GrafoDirigido."""
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C')])
        grafo.inserta_aristas([('D', 'C'), ('A', 'D')])
        aristas = [('A', 'D'), ('B', 'C'), ('A', 'C'), ('D', 'C')]
        adyacencias = {'A': {'D', 'C'}, 'B': {'C'}, 'D': {'C'}}
        self.assertSetEqual(set(grafo.aristas), set(aristas))
        self.assertDictEqual({key: set(value) for key, value in grafo.adyacencias.items()}, adyacencias)

    def test_quita_aristas(self):
        """Pruebas del método quita_aristas de la clase GrafoDirigido."""
        grafo = rb.GrafoDirigido([('A', 'D'), ('B', 'C'), ('A', 'C'), ('D', 'C')])
        grafo.quita_aristas([('D', 'C'), ('A', 'D')])
        aristas = [('B', 'C'), ('A', 'C')]
        self.assertSetEqual(set(grafo.aristas), set(aristas))
        self.assertDictEqual(grafo.adyacencias, {'B': ['C'], 'A': ['C']})

    def test_orden_topologico(self):
        """Pruebas del método orden_topologico de la clase GrafoDirigido."""
        # Grafo acíclico
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C'), ('D', 'C'), ('A', 'D')])
        orden = grafo.orden_topologico()
        # El ordenamiento topológico no es único.
        verdad = orden == ['A', 'B', 'D', 'C'] or orden == ['B', 'A', 'D', 'C']
        self.assertTrue(verdad)
        # Grafo cíclico, debe lanzar error.
        grafo = rb.GrafoDirigido([('A', 'C'), ('B', 'C'), ('C', 'D'), ('D', 'A')])
        with self.assertRaises(ValueError):
            grafo.orden_topologico()

    # Tests sobre RedBayesiana
    def test_constructor_rb(self):
        """Pruebas del constructor de de la clase RedBayesiana."""
        # Red bayesiana vacía
        red = rb.RedBayesiana()
        attr_vacios = {'aristas': [], 'adyacencias': {}, 'vertices': set(),
                       'valores': {}, 'probabilidades': {}, 'factor': {}}
        self.assertDictEqual(red.__dict__, attr_vacios)
        # Red Bayesiana no vacía
        aristas = [('Lluvia', 'Rociador'), ('Rociador', 'HierbaHúmeda'), ('Lluvia', 'HierbaHúmeda')]
        valores = defaultdict(list, {'Lluvia': ('SI', 'NO'), 'Rociador': ['SI', 'NO'], 'HierbaHúmeda': ['SI', 'NO']})
        probabilidades = defaultdict(list, {'Lluvia': [0.2, 0.8], 'Rociador': [0.01, 0.4, 0.99, 0.6],
                                            'HierbaHúmeda': [0.99, 0.9, 0.8, 0, 0.01, 0.1, 0.2, 1]})
        red = rb.RedBayesiana(aristas, valores=valores, probabilidades=probabilidades)
        factor = {'Rociador': {('SI', 'SI'): 0.01, ('SI', 'NO'): 0.4, ('NO', 'SI'): 0.99, ('NO', 'NO'): 0.6},
                  'Lluvia': {('SI',): 0.2, ('NO',): 0.8},
                  'HierbaHúmeda': {('SI', 'SI', 'SI'): 0.99, ('SI', 'SI', 'NO'): 0.9, ('SI', 'NO', 'SI'): 0.8,
                                   ('SI', 'NO', 'NO'): 0, ('NO', 'SI', 'SI'): 0.01, ('NO', 'SI', 'NO'): 0.1,
                                   ('NO', 'NO', 'SI'): 0.2, ('NO', 'NO', 'NO'): 1}}
        self.assertDictEqual(red.factor, factor)  # Esencialmente test sobre rb.actualiza_factor()

    def test_lee_estructura(self):
        """Pruebas del método lee_estructura junto a comprueba_probabilidades de la clase RedBayesiana."""
        # Entrada correcta
        aristas = [('Robo', 'Alarma'), ('Terremoto', 'Alarma'), ('Alarma', 'Juanllama'), ('Alarma', 'Mariallama')]
        adyacencias = {'Robo': ['Alarma'], 'Terremoto': ['Alarma'], 'Alarma': ['Juanllama', 'Mariallama']}
        vertices = {'Robo', 'Terremoto', 'Alarma', 'Juanllama', 'Mariallama'}
        valores = {variable: ['SI', 'NO'] for variable in vertices}
        probabilidades = {'Robo': [0.001, 0.999],
                          'Terremoto': [0.002, 0.998],
                          'Alarma': [0.95, 0.94, 0.29, 0.001, 0.05, 0.06, 0.71, 0.999],
                          'Juanllama': [0.9, 0.05, 0.1, 0.95],
                          'Mariallama': [0.7, 0.01, 0.3, 0.99]}
        factor = {'Robo': {('SI',): 0.001, ('NO',): 0.999},
                  'Terremoto': {('SI',): 0.002, ('NO',): 0.998},
                  'Alarma': {('SI', 'SI', 'SI'): 0.95, ('SI', 'SI', 'NO'): 0.94,
                             ('SI', 'NO', 'SI'): 0.29, ('SI', 'NO', 'NO'): 0.001,
                             ('NO', 'SI', 'SI'): 0.05, ('NO', 'SI', 'NO'): 0.06,
                             ('NO', 'NO', 'SI'): 0.71, ('NO', 'NO', 'NO'): 0.999},
                  'Mariallama': {('SI', 'SI'): 0.7, ('SI', 'NO'): 0.01, ('NO', 'SI'): 0.3, ('NO', 'NO'): 0.99},
                  'Juanllama': {('SI', 'SI'): 0.9, ('SI', 'NO'): 0.05, ('NO', 'SI'): 0.1, ('NO', 'NO'): 0.95}}
        atributos = {'aristas': aristas, 'adyacencias': adyacencias, 'vertices': vertices,
                     'valores': valores, 'probabilidades': probabilidades, 'factor': factor}
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        self.assertDictEqual(red.__dict__, atributos)
        # Entrada incorrecta
        with self.assertRaises(ValueError):
            red.lee_estructura('red_alarma_error')

    def test_mult_probabilidad_condicional(self):
        """Pruebas del método mult_probabilidad_condicional de la clase RedBayesiana."""
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        evidencias1 = {'Robo': 'SI'}
        evidencias2 = {'Robo': 'SI', 'Terremoto': 'NO'}
        salida1 = red.mult_probabilidad_condicional({'Alarma': 'SI'}, evidencias1)
        salida2 = red.mult_probabilidad_condicional({'Alarma': 'SI'}, evidencias2)
        self.assertEqual(salida2, 0.94)
        self.assertEqual(salida1, 0.8929999999999999)
        # Las evidencias no asignan valores a los padres, debe lanzar error.
        with self.assertRaises(ValueError):
            red.mult_probabilidad_condicional({'Juanllama': 'NO'}, evidencias1)

    def test_mult_probabilidades_condicionales(self):
        """Pruebas del método mult_probabilidades_condicionales de la clase RedBayesiana."""
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        evidencias1 = {'Robo': 'SI'}
        evidencias2 = {'Robo': 'SI', 'Terremoto': 'NO'}
        salida1 = red.mult_probabilidades_condicionales('Alarma', evidencias1)
        salida2 = red.mult_probabilidades_condicionales('Alarma', evidencias2)
        self.assertListEqual(salida1, [0.8929999999999999, 0.003])
        self.assertListEqual(salida2, [0.94, 0.06])
        # Las evidencias no asignan valores a los padres, debe lanzar error.
        with self.assertRaises(ValueError):
            red.mult_probabilidades_condicionales('Juanllama', evidencias1)

    def test_enumeracion_aux(self):
        """Pruebas del método test_enumeracion_aux de la clase RedBayesiana."""
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        evidencias = {'Juanllama': 'SI', 'Mariallama': 'SI'}
        salida = red.enumeracion_aux(['Robo'], evidencias)
        self.assertEqual(salida, 1.0)

    def test_enumeracion(self):
        """Pruebas del método enumeracion de la clase RedBayesiana."""
        # Puede variar ligeramente el resultado por errores numéricos. Prueba la igualdad a 4 decimales.
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')  # Red principal de pruebas
        salida = red.enumeracion('Robo', {'Juanllama': 'SI', 'Mariallama': 'SI'})
        salida_test = {'SI': 0.28417, 'NO': 0.71582}
        self.assertAlmostEqual(salida['SI'], salida_test['SI'], 4)
        self.assertAlmostEqual(salida['NO'], salida_test['NO'], 4)

        red.lee_estructura('red_infarto')  # Red alternativa
        salida = red.enumeracion('Fumador', {'Infarto': 'SI', 'Deportista': 'NO'})
        salida_test = {'SI': 0.52367, 'NO': 0.47632}
        self.assertAlmostEqual(salida['SI'], salida_test['SI'], 4)
        self.assertAlmostEqual(salida['NO'], salida_test['NO'], 4)

        red.lee_estructura('red_estudiante')  # Red con variables no binarias
        salida = red.enumeracion('L', {'D': '0', 'I': '0'})
        salida_test = {'0': 0.487, '1': 0.513}
        self.assertAlmostEqual(salida['0'], salida_test['0'], 4)
        self.assertAlmostEqual(salida['1'], salida_test['1'], 4)

        # La entrada del algoritmo es incorrecta, debe lanzar error.
        red.lee_estructura('red_alarma')
        with self.assertRaises(ValueError):  # Nombre de variable incorrecta.
            red.enumeracion('Ropo', {'Juanllama': 'SI'})
        with self.assertRaises(ValueError):  # Nombres de variables en evidencias incorrectos.
            red.enumeracion('Terremoto', {'ALARMA': 'SI', 'Maria': 'NO'})
        with self.assertRaises(ValueError):  # Valor de variable incorrecto.
            red.enumeracion('Robo', {'Juanllama': 'si', 'Alarma': 'SI'})

    def test_enumeracion_total(self):
        """Pruebas del método enumeracion_total de la clase RedBayesiana."""
        # Puede variar ligeramente el resultado por errores numéricos. Prueba la igualdad a 4 decimales.
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        evidencias = {'Juanllama': 'SI', 'Mariallama': 'SI'}
        salida_test = {'Mariallama': {'SI': 0.03997, 'NO': 0.96002},
                       'Juanllama': {'SI': 0.17757, 'NO': 0.82242},
                       'Robo': {'SI': 0.28417, 'NO': 0.71582},
                       'Alarma': {'SI': 0.76069, 'NO': 0.23930},
                       'Terremoto': {'SI': 0.17606, 'NO': 0.82393}}
        salida = red.enumeracion_total(evidencias)
        for variable in red.vertices:
            for valor in red.valores[variable]:
                self.assertAlmostEqual(salida[variable][valor], salida_test[variable][valor], 4)


unittest.main()
