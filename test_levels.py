import os
import hashlib 

md5 = "1234567890"

# params
qtdLevels = 0
qtdCaracLevel = 2

# vars
qLvlProc = 0
icaracInicial = 0

print(len(md5))

print(qtdLevels * qtdCaracLevel)
if qtdLevels > 0 and (qtdLevels * qtdCaracLevel) > len(md5):
    raise Exception("String deve ter no minimo {} caracteres".format(qtdLevels * qtdCaracLevel))

lst = []
while qLvlProc < qtdLevels:
    item = md5[icaracInicial:icaracInicial + qtdCaracLevel]
    icaracInicial = icaracInicial + qtdCaracLevel
    lst.append(item)
    qLvlProc=qLvlProc+1


print(os.sep.join(lst))

print(os.path.join("/temp", os.sep.join(lst)))