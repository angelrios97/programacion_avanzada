def romanum(textorom):
    valores={'M':1000,'D':500,'C':100,'L':50,'X':10,'V':5,'I':1}
    num=0
    for letra in textorom:
      num+=valores[letra]
    return num

#prueba letras sueltas

#prueba alguna combinación

#prueba letras no existentes

#prueba texto vacío

#prueba sin argumentos