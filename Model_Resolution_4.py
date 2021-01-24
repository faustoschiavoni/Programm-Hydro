from pyomo.opt import SolverFactory
from pyomo.core import *
from pyomo.environ import *
from Constraints_3 import *
import time


def Model_Resolution(model, Optimization_Goal, datapath="Inputs/Data.dat"):

    if Optimization_Goal == 'NPV':
            model.ObjectiveFunction = Objective(rule=Net_Present_Value, sense=maximize)

            model.V_forNPV = Constraint(rule=V_forNPV)
            #model.Separo_NPV = Constraint(rule=Separo_NPV)

    if Optimization_Goal == 'IRR':
            model.ObjectiveFunction = Objective(rule=IRR, sense=maximize)

            model.V_forIRR1 = Constraint(rule=V_forIRR1)
            model.V_forIRR2 = Constraint(rule=V_forIRR2)
            model.V_forIRR3 = Constraint(rule=V_forIRR3)
            model.V_forIRR4 = Constraint(rule=V_forIRR4)

    model.V_Portata_A = Constraint(model.giorni, model.nmax, rule=V_Portata_A)
    model.V_Portata_B = Constraint(model.giorni, model.nmax, rule=V_Portata_B)
    model.V_Qavailable = Constraint(model.giorni, rule=V_Qavailable)
    model.V_Hnet_A = Constraint(model.giorni, model.nmax, rule=V_Hnet_A)
    model.V_Hnet_B = Constraint(model.giorni, model.nmax, rule=V_Hnet_B)
    model.V_Potenza_A = Constraint(model.giorni, rule=V_Potenza_A)
    model.V_Potenza_B = Constraint(model.giorni, rule=V_Potenza_B)
    model.V_EnergiaAnnua = Constraint(rule=V_EnergiaAnnua)
    model.V_Costo_Turbine_Variabile = Constraint(rule=V_Costo_Turbine_Variabile)

    model.V_foo1 = Constraint(rule=V_foo1)
    model.V_foo2 = Constraint(rule=V_foo2)
    model.V_foo3 = Constraint(rule=V_foo3)
    model.V_foo4 = Constraint(rule=V_foo4)
    model.V_foo5 = Constraint(rule=V_foo5)
    model.V_foo6 = Constraint(rule=V_foo6)
    model.V_foo7 = Constraint(rule=V_foo7)

    model.Separo_INV_COST = Constraint(rule=Separo_INV_COST)

    #Nuovi vincoli per portata parziale
    model.V_Portata_P = Constraint(model.giorni, model.nmax, rule=V_Portata_P)
    model.V_Hnet_P = Constraint(model.giorni, model.nmax, rule=V_Hnet_P)
    model.V_p = Constraint(model.giorni, model.nmax, rule=V_p)
    model.V_Eta_P = Constraint(model.giorni, model.nmax, rule=V_Eta_P)
    model.V_Potenza_P = Constraint(model.giorni, rule=V_Potenza_P)

    model.V_Separo_Portata = Constraint(model.giorni, model.nmax, rule=V_Separo_Portata)
    model.V_Separo_Hnet_P = Constraint(model.giorni, model.nmax, rule=V_Separo_Hnet_P)

    model.V_Separo_Portata_0 = Constraint(model.giorni, model.nmax, rule=V_Separo_Portata_0) 

    model.V_Somma_Portate = Constraint(model.giorni, rule=V_Somma_Portate)

    #Carico i valori veri da recuperare dal Data.dat
    instance = model.create_instance(datapath)
    print('\nInstance created')
    opt = SolverFactory('gurobi')

    opt.set_options('Method=-1 MIPGap=0.1 Basis=0 ImproveTime=30 Mipfocus=1 BarHomogeneous=1 NonConvex=2 Crossover=0 BarConvTol=1e-3 OptimalityTol=1e-3 FeasibilityTol=1e-3 IterationLimit=1e17')


    print('Calling solver...')
    print('\n\nOrario partenza risoluzione sistema: ', time.strftime("%H:%M:%S"), '\n\n')

    results = opt.solve(instance, tee=True, keepfiles=True)
    print('Instance solved')

    instance.solutions.load_from(results)
    return instance
