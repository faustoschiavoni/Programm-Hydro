import numpy.polynomial.polynomial as poly
#Objective Functions


def V_Portata_A(model, i, n):
    return model.Portata_A[i, n] == model.Binary_A[n] * model.Binary_Turbines_A[i, n] * model.Portata_Nom[1]


def V_Portata_B(model, i, n):
    return model.Portata_B[i, n] == model.Binary_B[n] * model.Binary_Turbines_B[i, n] * model.Portata_Nom[2]


'''Portata_P'''


def V_Separo_Portata_0(model, i, n):
    return model.Separo_Portata_0[i, n] == model.Binary_A[n] * model.Binary_Parz[i]


def V_Separo_Portata(model, i, n):
    return model.Separo_P[i, n] == (1 - model.Binary_Turbines_A[i, n]) * model.Separo_Portata_0[i, n]


def V_Portata_P(model, i, n):
    return model.Portata_Parziale[i, n] == model.Separo_P[i, n] * model.Q_Parziale[i] #parzializzo con la A # model.Portata_Parziale[i, n] == model.Binary_A[n] * (1 - model.Binary_Turbines_A[i, n]) * model.Binary_Parz[i] * model.Q_Parziale[i]


''''''


def V_Somma_Portate(model, i):
    return model.Somma_portate[i] == sum(model.Portata_A[i, n] + model.Portata_B[i, n] + model.Portata_Parziale[i, n] for n in model.nmax)


def V_Qavailable(model, i):
    return model.Somma_portate[i] <= model.Duration_Curve[i]


def V_Hnet_A(model, i, n):
    return model.Hnet_A[i, n] == model.Hgross[i] - model.Coeff * (model.Portata_A[i, n]**2)


def V_Hnet_B(model, i, n):
    return model.Hnet_B[i, n] == model.Hgross[i] - model.Coeff * (model.Portata_B[i, n]**2)


'''Hnet_P'''


def V_Separo_Hnet_P(model, i, n):
    return model.Portata_Quadratica[i, n] == (model.Portata_Parziale[i, n]**2)


def V_Hnet_P(model, i, n):
    return model.Hnet_P[i, n] == model.Hgross[i] - model.Coeff * model.Portata_Quadratica[i, n]


'''Eta_p'''


def V_p(model, i, n):
    return model.Qp[i, n] == model.Portata_Parziale[i, n]/model.Portata_Nom[1]


def V_Eta_P(model, i, n):
    coefs = []
    for t in range(1, len(model.PolyCoefs) + 1):
        coefs += [model.PolyCoefs[t]]
    return model.Eta_P[i, n] == poly.polyval(model.Qp[i, n], coefs)


''''''


def V_Potenza_A(model, i):
    return model.Potenza_giorn_A[i] == (10**3) * 9.81 * sum(model.Portata_A[i, n] * model.Hnet_A[i, n] * model.Etas[1] for n in model.nmax)


def V_Potenza_B(model, i):
    return model.Potenza_giorn_B[i] == (10**3) * 9.81 * sum(model.Portata_B[i, n] * model.Hnet_B[i, n] * model.Etas[2] for n in model.nmax)


'''Potenza_P'''


def V_Potenza_P(model, i):
    return model.Potenza_giorn_P[i] == (10**3) * 9.81 * sum(model.Portata_Parziale[i, n] * model.Hnet_P[i, n] + model.Eta_P[i, n]*1e-2 for n in model.nmax)


''''''


def V_EnergiaAnnua(model):
    return model.EnergiaAnnua == sum(model.Potenza_giorn_A[i] + model.Potenza_giorn_B[i] + model.Potenza_giorn_P[i] for i in model.giorni)*24*model.Eta_aux*1e-6


def V_Costo_Turbine_Variabile(model):
    return model.Costo_Turbine_Variabile == sum(model.Binary_A[n] * model.Cost_turb[1] + model.Binary_B[n] * model.Cost_turb[2] for n in model.nmax)


def Separo_INV_COST(model):
    return model.INV_COST == model.Inv_Cost + model.Costo_Turbine_Variabile


''''''

def V_foo1(model):
    return model.Revenues == model.EnergiaAnnua * model.Revenues_Specific
def V_foo2(model):
    return model.Costs_forTax == model.INV_COST * (model.Perc_OeM + (1 / model.Ammortization))
def V_foo3(model):
    return model.Costs_forCF == model.INV_COST * model.Perc_OeM
def V_foo4(model):
    return model.Taxes_first == (model.Revenues - model.Costs_forTax) * model.Taxes
def V_foo5(model):
    return model.Taxes_second == (model.Revenues - model.Costs_forCF) * model.Taxes
def V_foo6(model):
    return model.CF_first == model.Revenues - model.Costs_forCF - model.Taxes_first
def V_foo7(model):
    return model.CF_second == model.Revenues - model.Costs_forCF - model.Taxes_second

def V_forNPV(model):
    return model.cf == model.Act_1 * model.CF_first + model.Act_2 * model.CF_second
def Net_Present_Value(model): #objective!!
    return - model.INV_COST + model.cf


#vincoli per irr (ma troppo non-lineare perché riesca a risolverlo...)
def V_forIRR1(model):
    return model.att1 == sum(1 / ((1 + model.irr_rate) ** i) for i in range(1, model.Ammortization + 1))
def V_forIRR2(model):
    return model.att2 == sum(1 / ((1 + model.irr_rate) ** i) for i in range(model.Ammortization + 1, model.Lifetime + 1))
def V_forIRR3(model):
    return model.cf_irr == model.att1 * model.CF_first + model.att2 * model.CF_second
def V_forIRR4(model):
    return - model.INV_COST + model.cf_irr == 0
def IRR(model): #objective!!
    return model.irr_rate
