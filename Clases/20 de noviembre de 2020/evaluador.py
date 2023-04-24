import re


# Programa que permite evaluar expresiones aritméticas que se le pasan por teclado y que involucren sumas, restas,
# productos y divisiones.


class Pila:
    """Clase Pila cuyos objetos permiten guardar elementos devolviéndolos en orden 'LIFO'.
    :ivar elementos: Lista que contiene los elementos de la pila."""

    def __init__(self):  # Constructor de clase que instancia una pila vacía.
        self.elementos = []

    def sacar(self):  # Devuelve el último elemento añadido a la pila sacándolo.
        if self.elementos:
            return self.elementos.pop()

    def mirar(self):  # Mira el último elemento añadido a la pila sin sacarlo.
        if self.elementos:
            return self.elementos[-1]

    def meter(self, elemento):  # Mete elemento en la pila.
        self.elementos.append(elemento)

    def vacia(self):  # Comprueba si la pila está vacía o no.
        if self.elementos:  # Si tiene elementos, devuelve False.
            return False
        else:  # Si no tiene elementos, devuelve True.
            return True

    def __len__(self):  # Calcula el número de elementos en la pila.
        return len(self.elementos)


expresion = input("Introduce una expresión aritmética: ")  # Introducimos una expresión aritmética por teclado.

# Otras expresiones que se pueden probar:
# expresion = "2*8*(8+1)+(-5)"
# expresion = "-56+((569-99.9)(-32))56-2"
# expresion = "-56-(2.5+1)"
# # expresion = ...

# Generamos la lista de los elementos de la expresión separando los números de los operadores.
generador = re.finditer(r'[+\-*/()]|\d+\.?\d*', expresion)  # No hace falta escapar "+" ni "*" en corchetes.
lista = [elem.group(0) for elem in generador]

# Debemos tener en cuenta que en la expresión puede haber sumandos o factores negativos aislados o no.
# La modificamos para tratar estos casos.
try:  # Como vamos a recorrer una lista eliminando elementos, queremos iterar hasta IndexError.
    for _ in range(len(lista) - 1):  # Recorremos la lista.
        if lista[_] == "-":
            try:  # Si el siguiente es un número, lo ponemos negativo.
                float("-" + lista[_ + 1])
                lista[_ + 1] = "-" + lista[_ + 1]
                try:  # El primer carácter de la expresión podría ser "-", capturamos el IndexError.
                    if lista[_ - 1] != "(":  # Si el anterior no es paréntesis, cambiamos por suma.
                        lista[_] = "+"
                    else:  # Si el anterior es paréntesis, eliminamos "-".
                        lista.pop(_)
                except IndexError:
                    pass
            except ValueError:
                pass
except IndexError:
    pass

if lista[0] == "+":  # Si el primer carácter era un "-", debemos eliminar el "+" que añadimos.
    lista.pop(0)

# Tenemos que tener en cuenta que podría haber productos expresados como yuxtaposición.
indices = []  # Guardará los índices de la lista donde hay que añadir un "*".
for _ in range(len(lista) - 1):  # Recorremos la lista.
    try:  # Como la expresión puede empezar por "(", queremos captuar IndexError en ese caso.
        if lista[_] == "(":
            if lista[_ - 1] == ")":  # Si "(" tiene antes ")", añadimos el índice.
                indices.append(_)
            else:
                try:  # Si el anterior es un número, también añadimos el índice.
                    float(lista[_ - 1])
                    indices.append(_)
                except ValueError:
                    pass
    except IndexError:
        pass

for _ in indices:  # Añadimos los "*" correspondientes.
    lista.insert(_, "*")

# Hacemos lo mismo en el caso en que la yuxtaposición sea por un número a derecha. Notar que
# ya no puede ser con un paréntesis porque lo hemos resuelto antes.
indices = []
for _ in range(len(lista) - 1):  # Recorremos la lista.
    if lista[_] == ")":  # Si el carácter es ")"...
        try:
            float(lista[_ + 1])  # y el siguiente es un número,
            indices.append(_ + 1)  # añadimos el índice.
        except ValueError:
            pass

for _ in indices:  # Añadimos los "*" correspondientes.
    lista.insert(_, "*")

lista.append("")  # Añadimos un 'string' vacío al final de la lista para poder terminar las iteraciones.
prioridad = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1, ")": 1, "": 0}  # Prioridades de los operadores.
operadores = Pila()  # Guardará los operadores según avancemos por la expresión.
operandos = Pila()  # Guardará los operandos según avancemos por la expresión.


def evaluador(item):  # Modifica la pila de operandos y la de operadores teniendo en cuenta el item que se le pasa.
    if item == "(":  # Si es un paréntesis de apertura, lo metemos en su pila y avanzamos.
        operadores.meter(item)
    else:
        try:  # Si es un número, lo metemos en su pila y avanzamos.
            operandos.meter(float(item))
        except ValueError:  # Si no es un paréntesis de apertura o un número.
            if operadores.vacia():  # Si la lista de operadores es vacía, lo metemos.
                operadores.meter(item)
            else:  # Si la lista de operadores no es vacía.
                if prioridad[item] <= prioridad[operadores.mirar()]:  # Si tiene menos prioridad que el anterior.
                    operacion = operadores.sacar()  # Sacamos el operador anterior y operamos.
                    if operacion == "*" or operacion == "/" or operacion == "+" or operacion == "-":
                        numero2 = operandos.sacar()  # Sacamos los números a operar.
                        numero1 = operandos.sacar()
                        if operacion == "*":  # Operamos según la operación que toque.
                            operandos.meter(numero1 * numero2)
                        elif operacion == "/":
                            operandos.meter(numero1 / numero2)
                        elif operacion == "+":
                            operandos.meter(numero1 + numero2)
                        else:  # (operacion == "-")
                            operandos.meter(numero1 - numero2)
                        if item == "":  # Si hemos llegado al final de la expresión.
                            while len(operandos) > 1:  # Mientras ocurra, quedará al menos una operación.
                                operacion = operadores.sacar()  # Operamos como antes.
                                numero2 = operandos.sacar()
                                numero1 = operandos.sacar()
                                if operacion == "*":
                                    operandos.meter(numero1 * numero2)
                                elif operacion == "/":
                                    operandos.meter(numero1 / numero2)
                                elif operacion == "+":
                                    operandos.meter(numero1 + numero2)
                                else:  # (operacion == "-")
                                    operandos.meter(numero1 - numero2)
                        elif item != ")":  # Si estamos en un cierre de paréntesis, eliminamos la apertura.
                            operadores.meter(item)
                        else:  # (item == ")")  # En otro caso, añadimos el operador a su pila.
                            operadores.sacar()
                    else:  # Entra cuando hay un error en la escritura, pero también cuando hay
                        # paréntesis redundantes o yuxtaposición, por ejemplo. Avisamos del posible fallo por erratas.
                        print("Si ha habido un fallo en la escritura, el resultado puede ser erróneo.")
                else:  # (item != ")")  # Si la prioridad es mayor, metemos el operador en su pila.
                    operadores.meter(item)


# El iterador siguiente avanza por la expresión evaluándola.
for k in lista:  # Para cada elemento de la lista, ejecutamos el evaluador.
    evaluador(k)
print("Resultado =", operandos.elementos[0])  # Imprimimos el resultado, el único elemento de la pila de operandos.
