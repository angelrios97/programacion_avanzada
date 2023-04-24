import unittest
import numerosromanos

class UnitTests(unittest.TestCase):
    def test_romanum(self):
        valores = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
        for l in valores.keys(): #Probamos con todas las letras
            self.assertEquals(romanum(l),valores[l])
        self.assertEquals(romanum('LX'),60) #Probamos con algunas combinaciones
        self.assertEquals(romanum('DCXI'),611)
        self.assertEquals(romanum('MMXX'),2020)
        self.assertRaises(romanum('J'),KeyError) #Probamos con algunas letras no existentes
        self.assertRaises(romanum('P'),KeyError)
        self.assertRaises(romanum('A'),KeyError)
        self.assertEquals(romanum(''),0) #Probamos con input string vacío
        self.assertRaises(romanum(),TypeError) #Probamos con input vacío

