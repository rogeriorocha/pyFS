import hashlib 
import os
  
# Path 
path = "\\temp\\store"

FILE_HASH_EXT = ".hashfile"
  
class FileStorage:
    def __init__(self, id):
        self.id = id
        m = hashlib.md5()
        m.update(str(id).encode('utf-8'))
        md5 =m.hexdigest().upper()
        self.lvl_0 = md5[0:2]
        self.lvl_1 = md5[2:4]
        self.path = os.path.join(path, self.lvl_0, self.lvl_1)
        self.file = os.path.join(self.path, str(id))
        self.fileHash = self.file + FILE_HASH_EXT
    def exists(self):
       return os.path.exists(self.file)

class HashUtils:
   def getFileMD5(filename):
       return hashlib.md5(open(filename,'rb').read()).hexdigest().upper()

    

#st = Storage(1)
#print(st.id)
#print(st.lvl_0)
#print(st.lvl_1)
#print(st.)