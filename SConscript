import os
from building import *

objs = []

if GetDepend('PKG_USING_FEE'):
    objs += SConscript(os.path.join('src', 'SConscript'))
    objs += SConscript(os.path.join('port', 'SConscript'))

    if GetDepend('FEE_USING_SAMPLE'):
        objs += SConscript(os.path.join('samples', 'SConscript'))

Return('objs')
