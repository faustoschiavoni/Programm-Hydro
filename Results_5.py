import pandas as pd
import csv
import xlsxwriter

def Risultati(instance, Optimization_Goal):

    EE = instance.EnergiaAnnua.value  # [MWh]

    x = instance.INV_COST.value
    y = instance.cf.value

    lt = instance.Lifetime.value
    am = instance.Ammortization.value
    dr = instance.Discount_Rate.value
    cf_1 = instance.CF_first.value
    cf_2 = instance.CF_second.value

    npv = - x
    pbt = 0
    for t in range(1, am + 1):
        npv += cf_1 * (1 / (1 + dr) ** t)
        if npv >= 0:
            pbt = t
            break
    if pbt == 0:
        for g in range(am + 1, lt + 1):
            npv += cf_2 * (1 / (1 + dr) ** g)
            if npv >= 0:
                pbt = g
                break
    if pbt == 0:
        PBT = 'Never reached'
    else:
        PBT = str(pbt) + ' [y]'


    print('\n Energia Annua:', round(EE, 2), "[MWh]", '\n Net Present Value:', round(-x+y, 2), '[€]', '\n Pay Back Time:', PBT)

    def z_irr(irr):
        npvi = - x
        for ti in range(1, am + 1):
            npvi += cf_1 * (1 / (1 + irr) ** ti)
        for gi in range(am + 1, lt + 1):
            npvi += cf_2 * (1 / (1 + irr) ** gi)
        return npvi

    def goal_seek(a, b, itmax, toll):#non mettere un intervallo la cui media è 0
        import numpy as np
        it = -1
        err = toll + 1
        while it < itmax and err > toll:
            xx = (b+a)/2
            if xx == 0:
                xx += 0.00001
            if abs(z_irr(xx)) < np.finfo(float).eps:
                err = 0
            else:
                err = abs(b-a)/2
            it += 1
            if z_irr(xx)*z_irr(a) < 0:
                b = xx
            else:
                a = xx
        return xx, it

    IRR, itt = goal_seek(-1 + 0.001, 1, 100, 1e-5)

    print(' IRR:', round(IRR*100, 2), '[%] (in', itt, 'iterazioni)')


    binaria1 = instance.Binary_A.get_values()
    binaria2 = instance.Binary_B.get_values()
    nmax = range(1, instance.Nmax.value + 1)
    count_1 = 0
    count_2 = 0
    for k in nmax:
        count_1 += binaria1[k]
        count_2 += binaria2[k]

    print('\n\nQuante ne compro del tipo A:', count_1, '(', binaria1, ')', '\nQuante ne compro del tipo B:', count_2, '(', binaria2, ')')


    if Optimization_Goal == "IRR":
        irr = instance.irr_rate.value
        print('\nL\'IRR è:', irr)


    #Creo CSV ed Excel per visualizzare i dati
    #Valori da stampare su Excel
    giorni = range(1, instance.Giorni.value + 1)
    #nmax = range(1, instance.Nmax.value + 1) #già implementato su per il numero totale di turbine per tipo

    Portata_A = instance.Portata_A.get_values()#model.Portata_A[i, n]
    Portata_B = instance.Portata_B.get_values()
    Portata_Parziale = instance.Portata_Parziale.get_values()#model.Portata_Parziale[i, n]
    Somma_portate = instance.Somma_portate.get_values()#model.Somma_portate[i]
    Duration_Curve = instance.Duration_Curve.extract_values()
    Eta_P = instance.Eta_P.get_values()#model.Eta_P[i, n]
    Potenza_giorn_A = instance.Potenza_giorn_A.get_values()#model.Potenza_giorn_A[i]
    Potenza_giorn_B = instance.Potenza_giorn_B.get_values()
    Potenza_giorn_P = instance.Potenza_giorn_P.get_values()

    #CSV
    dw = None
    df = open("Output/Risultati.csv", mode='w')
    dw = csv.writer(df, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dw.writerow(['Giorno', 'n', 'Portata A', 'Portata B', 'Portata P', 'Somma Portate', 'Duration Curve', 'Eta P',
                  'Potenza A', 'Potenza B', 'Potenza P'])
    for i in giorni:
        for n in nmax:
            dw.writerow(
                [i, n, Portata_A[i, n], Portata_B[i, n], Portata_Parziale[i, n], Somma_portate[i], Duration_Curve[i],
                 round(Eta_P[i, n], 1), Potenza_giorn_A[i], Potenza_giorn_B[i], Potenza_giorn_P[i]])
    df.close()

    #Excel
    excel_name = "Output/Risultati.xlsx"
    read_file = pd.read_csv("Output/Risultati.csv")
    df = pd.DataFrame(read_file)
    writer = pd.ExcelWriter(excel_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Foglio1', startrow=1, index=None, header=False)
    workbook = writer.book
    worksheet1 = writer.sheets['Foglio1']

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': False,
        'valign': 'vcenter',
        'fg_color': '#7FFFD4',
        'center_across': True,
        'shrink': False,
        'border_color': '#C36241', 
        'border': 2})

    worksheet1.set_row(0, 17)
    worksheet1.set_column('A:C', 8)
    worksheet1.set_column('C:K', 18)
    for col_num, value in enumerate(df.columns.values):
        worksheet1.write(0, col_num, value, header_format)

    writer.save()

    return
