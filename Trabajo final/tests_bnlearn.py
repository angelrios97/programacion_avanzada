#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Batería secundaria de pruebas para el desarrollo guiado por pruebas de redesbayesianas.

Las pruebas comprueban la igualdad de las inferencias respecto a los resultados que devuelve el paquete
de redes bayesianas bnlearn.

__author__: Ángel Ríos
__date__: 6 de septiembre de 2021
"""

import unittest
import matplotlib

matplotlib.use('TkAgg')
from bnlearn import bnlearn
from bnlearn import inference
import redesbayesianas as rb


class TestsRedesBayesianasBnlearn(unittest.TestCase):

    def test_red_alarma(self):
        """Prueba de la inferencia sobre red_alarma."""

        aristas = [('Robo', 'Alarma'), ('Terremoto', 'Alarma'), ('Alarma', 'Juanllama'), ('Alarma', 'Mariallama')]
        cpd_robo = bnlearn.TabularCPD(variable='Robo', variable_card=2, values=[[0.001], [0.999]])
        cpd_terremoto = bnlearn.TabularCPD(variable='Terremoto', variable_card=2, values=[[0.002], [0.998]])
        cpd_alarma = bnlearn.TabularCPD(variable='Alarma', variable_card=2,
                                        values=[[0.95, 0.94, 0.29, 0.001], [0.05, 0.06, 0.71, 0.999]],
                                        evidence=['Robo', 'Terremoto'], evidence_card=[2, 2])
        cpd_juanllama = bnlearn.TabularCPD(variable='Juanllama', variable_card=2,
                                           values=[[0.9, 0.05], [0.1, 0.95]],
                                           evidence=['Alarma'], evidence_card=[2])
        cpd_mariallama = bnlearn.TabularCPD(variable='Mariallama', variable_card=2,
                                            values=[[0.7, 0.01], [0.3, 0.99]],
                                            evidence=['Alarma'], evidence_card=[2])
        dag = bnlearn.make_DAG(aristas, [cpd_robo, cpd_terremoto, cpd_alarma, cpd_juanllama, cpd_mariallama],
                               verbose=0)
        inferencia = inference.fit(dag, variables=['Robo'],
                                   evidence={'Juanllama': 0, 'Mariallama': 0}, verbose=0).values
        red = rb.RedBayesiana()
        red.lee_estructura('red_alarma')
        salida = list(red.enumeracion('Robo', {'Juanllama': 'SI', 'Mariallama': 'SI'}).values())
        self.assertAlmostEqual(salida[0], inferencia[0], 4)  # 0.2841
        self.assertAlmostEqual(salida[1], inferencia[1], 4)  # 0.7158

    def test_red_infarto(self):
        """Prueba de la inferencia sobre red_infarto."""

        aristas = [('Deportista', 'Hipertensión'), ('AlimentaciónEquilibrada', 'Hipertensión'),
                   ('Hipertensión', 'Infarto'), ('Fumador', 'Infarto')]
        cpd_depor = bnlearn.TabularCPD('Deportista', 2, [[0.1], [0.9]])
        cpd_alim = bnlearn.TabularCPD('AlimentaciónEquilibrada', 2, [[0.4], [0.6]])
        cpd_fuma = bnlearn.TabularCPD('Fumador', 2, [[0.4], [0.6]])
        cpd_hiper = bnlearn.TabularCPD('Hipertensión', 2, [[0.01, 0.2, 0.25, 0.7], [0.99, 0.8, 0.75, 0.3]],
                                       ['Deportista', 'AlimentaciónEquilibrada'], [2, 2])
        cpd_infar = bnlearn.TabularCPD('Infarto', 2, [[0.8, 0.6, 0.7, 0.3], [0.2, 0.4, 0.3, 0.7]],
                                       ['Hipertensión', 'Fumador'], [2, 2])
        dag = bnlearn.make_DAG(aristas, [cpd_depor, cpd_alim, cpd_fuma, cpd_hiper, cpd_infar], verbose=0)
        inferencia = inference.fit(dag, ['Infarto'],
                                   {'Deportista': 0, 'AlimentaciónEquilibrada': 0}, verbose=0).values
        red = rb.RedBayesiana()
        red.lee_estructura('red_infarto')
        salida = list(red.enumeracion('Infarto', {'Deportista': 'SI', 'AlimentaciónEquilibrada': 'SI'}).values())
        self.assertAlmostEqual(salida[0], inferencia[0], 4)
        self.assertAlmostEqual(salida[1], inferencia[1], 4)

    def test_red_estudiante(self):
        """Prueba de la inferencia sobre red_estudiante."""

        aristas = [('D', 'G'), ('I', 'G'), ('I', 'G'), ('I', 'S'), ('G', 'L')]
        cpd_d = bnlearn.TabularCPD('D', 2, [[0.6], [0.4]])
        cpd_i = bnlearn.TabularCPD('I', 2, [[0.7], [0.3]])
        cpd_g = bnlearn.TabularCPD('G', 3,
                                   [[0.3, 0.05, 0.9, 0.5], [0.4, 0.25, 0.08, 0.3], [0.3, 0.7, 0.02, 0.2]],
                                   ['I', 'D'], [2, 2])
        cpd_s = bnlearn.TabularCPD('S', 2, [[0.95, 0.2], [0.05, 0.8]], ['I'], [2])
        cpd_l = bnlearn.TabularCPD('L', 2, [[0.1, 0.4, 0.99], [0.9, 0.6, 0.01]], ['G'], [3])
        dag = bnlearn.make_DAG(aristas, [cpd_d, cpd_i, cpd_g, cpd_s, cpd_l], verbose=0)
        inferencia = inference.fit(dag, ['L'], {'I': 0, 'D': 0}, verbose=0).values
        red = rb.RedBayesiana()
        red.lee_estructura('red_estudiante')
        salida = list(red.enumeracion('L', {'I': '0', 'D': '0'}).values())
        self.assertAlmostEqual(inferencia[0], salida[0], 4)  # 0.4870
        self.assertAlmostEqual(inferencia[1], salida[1], 4)  # 0.5130


unittest.main()
