"""f = open('alumnos.txt', 'r')
nombres = f.read()
print(nombres)
f.seek(9)
nombres2 = f.read()
print(nombres2)
f.close() """

"""f = open('alumnos.txt', 'r')
#nombres = f.readline()
#print(nombres)
#f.close()"""

"""f = open('alumnos.txt', 'r')
nombres = f.readlines()

for item in nombres:
    print(item, end = '')
f.close()"""

f = open('alumnos.txt', 'a')
f.write('\n' + '!!!Hola mundo!!!')
f.close()
