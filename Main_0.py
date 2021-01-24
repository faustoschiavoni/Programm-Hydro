import time
from pyomo.core import *
from pyomo.environ import AbstractModel
from Model_Creation_2 import Model_Creation
from Model_Resolution_4 import Model_Resolution
from Results_5 import Risultati

start = time.time()
print('\n\nPartenza: ', time.strftime("%H:%M:%S"), '\n\n')
model = AbstractModel()

Optimization_Goal = "NPV" #"NPV", "IRR" (non funge perché molto non-lineare)

Model_Creation(model, Optimization_Goal)

instance = Model_Resolution(model, Optimization_Goal)

end = time.time()
elapsed = end - start
print('\n\nModel run complete (overall time: ', round(elapsed, 0), 's,', round(elapsed/60, 1), ' m)\n')


startR = time.time()

Risultati(instance, Optimization_Goal)

endR = time.time()
elapsedR = endR - startR
print('\n\nResults run complete (overall time: ', round(elapsedR, 2), 's)\n')
