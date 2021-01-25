from pyomo.environ import Param, RangeSet, NonNegativeReals, NonNegativeIntegers, Var, Set, PositiveIntegers, Reals, Binary
from pyomo.core import *
from Initialize_1 import Initialize_Duration_Curve, Initialize_Hgross, Initialize_Efficiency, Initialize_Qp_max_min, Initialize_Act, gp


def Model_Creation(model, Optimization_Goal):
    #Param. per Sets
    model.Giorni = Param(within=NonNegativeReals)
    model.Numero_TipiTurbine = Param(within=NonNegativeReals)
    model.Nmax = Param(within=NonNegativeIntegers)
    #Sets
    model.giorni = RangeSet(model.Giorni)
    model.t = RangeSet(model.Numero_TipiTurbine)
    model.nmax = RangeSet(model.Nmax)

    #Parametri singoli
    model.DMV = Param(within=NonNegativeReals)
    model.Eta_aux = Param(within=NonNegativeReals)
    model.Revenues_Specific = Param(within=NonNegativeReals)
    model.Perc_OeM = Param(within=NonNegativeReals)
    model.Inv_Cost = Param(within=NonNegativeReals)
    model.Ammortization = Param(within=NonNegativeReals)
    model.Taxes = Param(within=NonNegativeReals)
    model.Discount_Rate = Param(within=NonNegativeReals)
    model.Lifetime = Param(within=NonNegativeIntegers)
    model.Coeff = Param(within=NonNegativeReals)
    model.T_parz = Param(within=NonNegativeIntegers)

    #Param. multi-ingresso indicizzati sul numero di turbine diversi prevsisto (2: A e B)
    model.Portata_Nom = Param(model.t, within=NonNegativeReals)
    model.Portata_Min = Param(model.t, within=NonNegativeReals)
    model.Portata_Max = Param(model.t, within=NonNegativeReals)
    model.Etas = Param(model.t, within=NonNegativeReals)
    model.Cost_turb = Param(model.t, within=NonNegativeReals)

    #Param. inizializzati da me da excel (da dare come input)
    model.Duration_Curve = Param(model.giorni, within=NonNegativeReals, initialize=Initialize_Duration_Curve)  # già tolto il DMV
    model.Hgross = Param(model.giorni, within=NonNegativeReals, initialize=Initialize_Hgross)

    #Var. Binarie
    #Binary_Turbines ti dice se il giorno i la turbina n sta venendo usata (accesa/spenta quel giorno quella turbina)
    model.Binary_Turbines_A = Var(model.giorni, model.nmax, within=Binary)
    model.Binary_Turbines_B = Var(model.giorni, model.nmax, within=Binary)
    #Binary ti dice se la turbina in generale è stata usata (funziona o non funziona-->la pago o non la pago per NPV)
    model.Binary_A = Var(model.nmax, within=Binary)
    model.Binary_B = Var(model.nmax, within=Binary)

    # Var. modello
    model.Portata_A = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Portata_B = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Hnet_A = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Hnet_B = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Potenza_giorn_A = Var(model.giorni, within=NonNegativeReals)
    model.Potenza_giorn_B = Var(model.giorni, within=NonNegativeReals)
    model.EnergiaAnnua = Var(within=NonNegativeReals)
    model.Costo_Turbine_Variabile = Var(within=NonNegativeReals)

    #Var. per visualizzare NPV e dati in uscita
    model.cf = Var(within=Reals)
    model.INV_COST = Var(within=NonNegativeReals)

    #Portata Parziale

    #Parametri per Portata Parziale
    model.PolyCoefs = Param(range(1, grado_poly + 2), initialize=Initialize_Efficiency)

    #Var per Portata Parziale

    Pmin, Pmax = Initialize_Qp_max_min()
    model.Q_Parziale = Var(model.giorni, bounds=(Pmin, Pmax))

    model.Portata_Parziale = Var(model.giorni, model.nmax, bounds=(-1, Pmax))
    model.Binary_Parz = Var(model.giorni, within=Binary)
    model.Hnet_P = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Eta_P = Var(model.giorni, model.nmax, within=NonNegativeReals)
    model.Qp = Var(model.giorni, model.nmax, bounds=(-1, Pmax)) 
    model.Potenza_giorn_P = Var(model.giorni, within=NonNegativeReals)

    model.Separo_P = Var(model.giorni, model.nmax, bounds=(0, 1))
    model.Portata_Quadratica = Var(model.giorni, model.nmax, within=NonNegativeReals)

    model.Separo_Portata_0 = Var(model.giorni, model.nmax, bounds=(0, 1))

    model.Somma_portate = Var(model.giorni, within=NonNegativeReals)

    #Scorporo l'npv per implementare pbt e irr
    model.Revenues = Var(within=NonNegativeReals)
    model.Costs_forTax = Var(within=NonNegativeReals)
    model.Costs_forCF = Var(within=NonNegativeReals)
    model.Taxes_first = Var()
    model.Taxes_second = Var()
    model.CF_first = Var()
    model.CF_second = Var()

    Act_1, Act_2 = Initialize_Act()

    model.Act_1 = Param(initialize=Act_1)
    model.Act_2 = Param(initialize=Act_2)

    if Optimization_Goal == "IRR": #ottimizzazione troppo non-lineare (esponenti > 10)
        model.irr_rate = Var()
        model.cf_irr = Var()
        model.att1 = Var()
        model.att2 = Var()
