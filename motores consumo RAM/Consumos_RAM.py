import pandas as pd
import matplotlib.pyplot as plt
import math
import os

carpetas=os.getcwd()+'/motores consumo RAM/datos/'
archivo=os.listdir(carpetas)

df = pd.read_csv(carpetas+archivo[0],sep=',')

inf_der = pd.DataFrame(df, columns=['TimeSeconds',
                                    's3_tcs_ram_actcurbsls_C1074135149',
                                    's3_tcs_ram_actcurbsrs_C1074135150',
                                    's3_tcs_ram_actcurtsls_C1074135151',
                                    's3_tcs_ram_actcurtsrs_C1074135152',
                                    's3_an2l_ramzustand_alt_C1075314736'])


inf_der=inf_der[inf_der['s3_an2l_ramzustand_alt_C1075314736']==176]


fecha=[]
sentido=[]

for s in range(1,len(df)):
    
    if df.loc[s,'s3_an2l_ramzustand_alt_C1075314736'] == 176: 
    
        if df.loc[s,'s3_an2e_ramrefautocoldwidthhmi_C2185'] < df.loc[s,'s3_an2l_ramactwidthboc_C1547']:
            fecha.append(df.loc[s,'TimeSeconds'])
            sentido.append('achicando')

        elif df.loc[s,'s3_an2e_ramrefautocoldwidthhmi_C2185'] > df.loc[s,'s3_an2l_ramactwidthboc_C1547']:
            fecha.append(df.loc[s,'TimeSeconds'])
            sentido.append('agrandando')

        elif df.loc[s,'s3_an2e_ramrefautocoldwidthhmi_C2185'] == df.loc[s,'s3_an2l_ramactwidthboc_C1547']:
            fecha.append(df.loc[s,'TimeSeconds'])
            sentido.append('detenido')


direccion={'fecha':fecha,'sentido':sentido}

df_direccion = pd.DataFrame(data=direccion)


fecha=[]
ancho=[]

for s in range(1,len(df)):
    
    if df.loc[s,'s3_an2l_ramzustand_alt_C1075314736'] == 176: 

            fecha.append(df.loc[s,'TimeSeconds'])
            decimal,entero=math.modf(df.loc[s,'s3_an2l_ramactwidthboc_C1547']/100)
            ancho.append(int(entero*100))


#Armo el DataFrame --- Rango

rangos={'fecha':fecha,'ancho':ancho}

df_ancho = pd.DataFrame(data=rangos)

consumos=df_ancho.set_index('fecha').join(df_direccion.set_index('fecha')).join(inf_der.set_index('TimeSeconds'), on='fecha')



ax = consumos.boxplot(column=['s3_tcs_ram_actcurtsls_C1074135151','s3_tcs_ram_actcurtsrs_C1074135152',
                              's3_tcs_ram_actcurbsls_C1074135149','s3_tcs_ram_actcurbsrs_C1074135150'],by='ancho',
                    layout=(2, 2),
                    showmeans=True, 
                    showbox=True,
                    figsize=(20,15),
                    boxprops={'color':'blue'},
                    medianprops={'color':'red'},
                    whiskerprops={'color':'blue'},
                    meanprops={'marker':'o','mec':'black','mfc':'grey'})

#Titulos:

num_molde=3

fecha = pd.to_datetime(df['TimeSeconds'])
fecha = fecha.dt.strftime('%d/%m/%Y') 
fecha = f"{fecha[min(fecha.index)]} al {fecha[max(fecha.index)]}" 

fig = ax[0][0].get_figure()
fig.canvas.set_window_title('Consumos Motores RAM')
fig.suptitle(f'\n\nLinea 3 --- Molde N°: {num_molde} --- Periodo: {fecha}')

ax[0][0].set_title("Sup_Izq")
ax[0][1].set_title("Sup_Der")
ax[1][0].set_title("Inf_Izq")
ax[1][1].set_title("Inf_Der")

ax[0][0].set_ylabel("Corriente")
ax[1][0].set_ylabel("Corriente")


ax[1][0].set_xlabel("Ancho")
ax[1][1].set_xlabel("Ancho")


# visualizza sullo schermo e crea un'immagine chiamata "Consumos Motores RAM L3.png" nella directory.

plt.show()
plt.savefig(f'{os.getcwd()}/motores consumo RAM/Consumos Motores RAM L3.png',facecolor='w')


######### il ritardo è perché ci sono 808.580 record ########