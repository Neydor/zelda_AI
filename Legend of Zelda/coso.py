lista = []
listaLis = []
listaPrimos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
for i in range(100000):
    lista.append(i)
for y in lista:
    numero = y
    numero = str(numero)
    dig = len(numero)
    list_num = []
    for n in range(5):
        # if n != '0':
        if dig <= 4:
            list_num.insert(0, 0)
            numero = "0"+numero
            dig = dig + 1
        else:
            nume = int(numero[n])
            list_num.append(nume)
    listaLis.append(list_num)
listaFull = listaLis

for q in range(len(listaFull)):
    number = set(listaFull[q])
    listaFull[q] = number

listaA = []
for h in range(len(listaFull)):
    if len(listaFull[h]) == 5:
        listaA.append(listaFull[h])
lista = listaA
cont = 0
for j in range(len(lista)):
    unidad = list(lista[j])[4]
    decena = list(lista[j])[3]
    centena = list(lista[j])[2]
    if unidad and decena and centena in listaPrimos and (unidad + decena + centena) % 2 == 0:
        cont = cont + 1
print(cont)
