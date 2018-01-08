
from data import Version

class lastCD:
    """docstring for ."""
    def __init__(self,shema):
        #super(, self).__init__()
        self.shema = shema
        self.version_uat= version[-1][self.shema]               #curUat.execute("select (CD) from %s.audit_patches",[self.shema])
        self.version_prod= version[0][self.shema]               #curProd.execute("select (CD) from %s.audit_patches",[self.shema])
        self.info= self.shema+' UAT='+self.version_uat+' PROD='+self.version_prod
# import from data file -> #print(version[0]['CAR_OWNER'])
version=Version()
base=[
lastCD('CAR_OWNER'),
lastCD('CRDS_OWNER'),
lastCD('STG_OWNER')
]

#CAR_OWNER=lastCD('CAR_OWNER')
#CRDS_OWNER=lastCD('CRDS_OWNER')
#CAR_OWNER=lastCD('STG_OWNER')


'''
k=0
for i in base:
    #print(i.info)
    #base[i].shema=base[i].shema+1
    base[k].shema=base[k].shema+'1123'
    print(base[k].shema)
    k=k+1
#print(base[1].shema)
for i in base:
    print(i.shema)
'''
#base[1].shema=str(5)
#print (base[1].shema)
