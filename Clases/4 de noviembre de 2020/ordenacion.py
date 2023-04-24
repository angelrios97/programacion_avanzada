fichero = open('lista','r')
i = 1
prioridades = []
for linea in fichero.readlines():
    prioridades.append(int(linea.strip()))
    i += 1
    if i > 10:
        break
prioridades.sort(reverse=True)

for linea in fichero.readlines():
    linea = int(linea.strip())
    for i in range(len(prioridades)):
        if linea > prioridades[i]:
            prioridades.insert(i,linea)
            break
            
print(prioridades)