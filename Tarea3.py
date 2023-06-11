import pandas as pd
import numpy as np
from sympy import symbols, Eq, solve
from sympy.vector import CoordSys3D

diametros = []

def leer_datos_excel():
    # Lee el archivo de Excel
    df = pd.read_excel('Datos_engranajes.xlsx')

    # Crea los vectores con los nombres de las filas
    Numero_dientes = df.iloc[0, 1:].tolist()
    Angulo_presion = df.iloc[1, 1:].tolist()
    Angulo_paso_helice = df.iloc[2, 1:].tolist()
    Paso_diametral = df.iloc[3, 1:].tolist()
    Ancho_cara = df.iloc[4, 1:].tolist()

    return Numero_dientes,Angulo_presion, Angulo_paso_helice, Paso_diametral, Ancho_cara

# Función para calcular la velocidad de salida del sistema de transmisión
def velocidad_salida(velocidad_entrada,N2,N3,N4,N5,N6,N7):
    return velocidad_entrada*(N2/N3)*(N4/N5)*(N6/N7)

# Función para calcular el diametro de paso a partir del numero de dientes y paso diametral
def diametro_paso(num_dientes, P):
    diametro_paso = num_dientes/P 
    return diametro_paso

# Función para encontrar la velocidad lineal en cada engrane
def velocidad_linea(w,d):
    return (np.pi*d*w)/12

# Función para encontrar la fuerza tangencial 'Wt' en cada engrane a partir de su potencia y velocidad lineal
def fuerza_tangencial(p,v):
    return (33000*p)/v

def Esfuerzo(Wt, F, P, num_dien):
    indice = y_dict["Numero de dientes"].index(num_dien)
    y = y_dict["Y"][indice]
    Es = (Wt * P)/(F * y)
    print("Esfuerzo en el engranaje 4:", Es, " psi")
    return Es

if __name__ == "__main__":
    Numero_dientes,Angulo_presion, Angulo_paso_helice, Paso_diametral, Ancho_cara = leer_datos_excel()
    velocidad_entrada = float(input("Ingrese la velocidad de entrada (V2) en rpm: "))
    potecia_entrada = float(input("Ingrese la potencia de entrada (H2) en HP: "))
    l5 = float(input("Ingrese el valor de l5: "))
    l6 = float(input("Ingrese el valor de l6: "))
    l7 = float(input("Ingrese el valor de l7: "))
    # Imprime los vectores
    print("Numero_dientes:", Numero_dientes)
    print("Angulo_presion:", Angulo_presion)
    print("Angulo_paso_helice:", Angulo_paso_helice)
    print("Paso_diametral:", Paso_diametral)
    print("Ancho_cara:", Ancho_cara)

    # Nombres
    N2, N3, N4, N5, N6, N7 = Numero_dientes
    sigma_2, sigma_3,sigma_4, sigma_5, sigma_6, sigma_7 = Angulo_presion
    psi_2, psi_3 = Angulo_paso_helice[:2]
    gamma_4, gamma_5 = Angulo_paso_helice[2:4]
    P_2, P_3, P_4, P_5, P_6, P_7 = Paso_diametral
    F_2, F_3, F_4, F_5, F_6, F_7 = Ancho_cara

    #Velocidad de salida
    print('La velocidad de salida V7 es:', velocidad_salida(velocidad_entrada,N2,N3,N4,N5,N6,N7))

    #Calcula los diámetros de los engranajes
    for i in range(6):
        diametro = diametro_paso(Numero_dientes[i],Paso_diametral[i])
        diametros.append(diametro)

    #Velocidad angular de los engranajes necesario
    w_5 = velocidad_entrada*(N2/N3)*(N4/N5)
    w_6 = w_5

    #Velocidad de línea de los engranajes necesarios
    v_5 = velocidad_linea(w_5,diametros[3]) #Velocidad angular de 5 usando relación de engranes
    v_6 = velocidad_linea(w_6,diametros[4]) #Al estar en el mismo eje
    ##Encontradas las velocidades, procedemos a encontrar las fuerzas.
    
    #Fuerzas para engrane cónico 5
    ft_5 = fuerza_tangencial(potecia_entrada,v_5)        #Fuerza tangencial del engrane cónico 5 
    fr_5 = ft_5*np.tan(np.deg2rad(Angulo_presion[3]))*np.cos(np.deg2rad(Angulo_paso_helice[3]))    #Fuerza radial del engrane cónico 5 , a partir del angulo de presion y de paso obtenidos de excel
    fa_5 = fr_5*np.tan(np.deg2rad(Angulo_presion[3]))*np.sin(np.deg2rad(Angulo_paso_helice[3]))    #Fuerza axial del engrane cónico 5 , a partir del angulo de presion y de paso obtenidos de excel    

    #Fuerzas para engrane recto 6
    ft_6 = fuerza_tangencial(potecia_entrada,v_6)        #Fuerza tangencial del engrane recto 6  
    fr_6 = ft_6*np.tan(np.deg2rad(Angulo_presion[4]))   

    
    ## Encontradas las fuerzas de los engranes involucradas, realizaremos análisis estático para encontrar reacciones en los cojinetes.
    
    # Asignamos nuestros vectores fuerza en los cojinetes
    # E= [Ex,Ey,0]     pues por dato solo tendrá fuerza radial y axial
    # F= [0,Fy,0]      pues por dato solo tendrá fuerza radial

    # Definir las variables desconocidas como simbólicas
    Ey, Fy = symbols('Ey Fy')
    # Definir el sistema de coordenadas
    N = CoordSys3D('N')

    #Inicamos el análisis estático con Sumatoria de fuerzas en X: Ex - fa_5 = 0
    Ex = fa_5
    
    #Sumatoria de fuerzas en Y: 
        # Ey + fr_5 - fr_6 + Fy = 0        Ec1 (su mención es solo como guía para proseguir con el desarollo)
    
    #Sumatoria de momentos en E: 
         #  FE x F + f6E x f6 + f5E x f5 = 0        Ec2 (su mención es solo como guía para proseguir con el desarollo)
    
    #Creamos los vectores de Fuerzas de los engranes en forma vectorial:
    f6 = -fr_6*N.j + ft_6*N.k
    f5 = -fa_5*N.i + fr_5*N.j + ft_5*N.k
    F = Fy*N.j
    
    #Creamos los vectores de posición desde el cojinete E a cada una de las fuerzas: 
    F_E = (l5+l6)*N.i
    f6_E = -l7*N.i + (diametros[4]/2)*N.j
    f5_E = (l6-diametros[2])*N.i - diametros[3]*N.j

    # Definimos las ecuaciones Ec1 y Ec2 que se mencionaron anteriormente:
    eq1 = Eq(Ey + fr_5 - fr_6 + Fy, 0)
    eq2 = Eq(F_E.dot(N.i) * F.dot(N.j) + f6_E.dot(N.i) * f6.dot(N.j) + f5_E.dot(N.i) * f5.dot(N.k), 0)

    # Resolvemos el sistema de ecuaciones para encontrar Ey , Fy
    sol = solve((eq1, eq2), (Ey, Fy))

    # Obtener las soluciones
    Ey_sol = sol[Ey]
    Fy_sol = sol[Fy]

    # Imprimir las soluciones
    print("Ey =", Ey_sol)
    print("Fy =", Fy_sol)
    
    ###########################################3
    #Cálculo de esfuerzo Lewis para el engranaje 4
    y_dict = {"Numero de dientes":[12	, 13	, 14	, 15	, 16	, 17	, 18	, 19	, 20	, 21	, 22	, 24	, 26	, 28	, 30	, 34	, 38	, 43	, 50	, 60	, 75	, 100	, 150	, 300	, 400	, "Rack"],
          "Y": [0.245	, 0.261	, 0.277	, 0.29	, 0.296	, 0.303	, 0.309	, 0.314	, 0.322	, 0.328	, 0.331	, 0.337	, 0.346	, 0.353	, 0.359	, 0.371	, 0.384	, 0.397	, 0.409	, 0.422	, 0.435	, 0.447	, 0.46	, 0.472	, 0.48	, 0.485]}

    #La fuerza tangencial del engranaje 4 es la misma que del engranaje 5
    ft_4 = ft_5
    
    #Esfuerzo en el engranje 4
    print("Para poner obtener el valor correcto del esfuerzo lewis es necesario que el ángulo de presión sea de 20º")
    Esfuerzo(ft_4, Ancho_cara[2], Paso_diametral[2], Numero_dientes[2])