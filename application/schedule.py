import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

#@tl.job(interval=timedelta(hours=5))
def expurgarArquivos():
    print("5h job expurgarArquivos() time : {}".format(time.ctime()))