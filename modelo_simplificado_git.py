# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 10:44:46 2019

@author: Fede
"""
import math
import numpy as np


def interaccion(tamanio,persona, polo1,polo2,d, noticia):
    
    if noticia is "positiva":
        
        if (polo1[1]-persona[1]) == 0:
            alfa = math.pi/2  #angulo del movimiento
        else:   
            alfa = math.atan((polo1[0]-persona[0])/(polo1[1]-persona[1]))        
        dx = math.sin(alfa)*d*np.sign(polo1[1]-persona[1]) #mobimiento en X
        dy = math.cos(alfa)*d*np.sign(polo1[1]-persona[1]) #mobimiento en Y
            
        if acepta(persona,polo1,polo2,noticia):
            x = [persona[0] + dx if persona[0] + dx < tamanio[2] and  persona[0] + dx > tamanio[1] else tamanio[2] if persona[0] + dx>tamanio[2] else tamanio[1]][0]
            y = [persona[1] + dy if persona[1] + dy < tamanio[4] and  persona[1] + dy > tamanio[3] else tamanio[4] if persona[1] + dy>tamanio[4] else tamanio[3]][0]

            persona = [x,y]
            return persona
        else:
            x = [persona[0] - dx if persona[0] - dx < tamanio[2] and  persona[0] - dx > tamanio[1] else tamanio[2] if persona[0] - dx>tamanio[2] else tamanio[1]][0]
            y = [persona[1] - dy if persona[1] - dy < tamanio[4] and  persona[1] - dy > tamanio[3] else tamanio[4] if persona[1] - dy>tamanio[4] else tamanio[3]][0]

            persona = [x,y]
            return persona
    else:
        if (polo2[1]-persona[1]) == 0:
            alfa = math.pi/2  #angulo del movimiento
        else:   
            alfa = math.atan((polo2[0]-persona[0])/(polo2[1]-persona[1]))        
        dx = math.sin(alfa)*d*np.sign(polo2[1]-persona[1]) #mobimiento en X
        dy = math.cos(alfa)*d*np.sign(polo2[1]-persona[1]) #mobimiento en Y        
        
        if acepta(persona,polo1,polo2,noticia):
            x = [persona[0] - dx if persona[0] - dx < tamanio[2] and  persona[0] - dx > tamanio[1] else tamanio[2] if persona[0] - dx>tamanio[2] else tamanio[1]][0]
            y = [persona[1] - dy if persona[1] - dy < tamanio[4] and  persona[1] - dy > tamanio[3] else tamanio[4] if persona[1] - dy>tamanio[4] else tamanio[3]][0]

            persona = [x,y]
            return persona
        else:
            x = [persona[0] + dx if persona[0] + dx < tamanio[2] and  persona[0] + dx > tamanio[1] else tamanio[2] if persona[0] + dx>tamanio[2] else tamanio[1]][0]
            y = [persona[1] + dy if persona[1] + dy < tamanio[4] and  persona[1] + dy > tamanio[3] else tamanio[4] if persona[1] + dy>tamanio[4] else tamanio[3]][0]

            persona = [x,y]
            return persona



def acepta(persona,polo1,polo2,noticia):
    d1=(polo1[0]-persona[0])**2+(polo1[1]-persona[1])**2
    d2=(polo2[0]-persona[0])**2+(polo2[1]-persona[1])**2
    return d1<=d2



def iterar(personas,Medio1_polo1,Medio1_polo2,Medio1_d_C,Medio1_d_T,Medio2_polo1,Medio2_polo2,Medio2_d_C,Medio2_d_T,Medio3_polo1,Medio3_polo2,Medio3_d_C,Medio3_d_T,iteraciones,tamanio,votos_C,votos_T):
    for iteracion in range(iteraciones):
        for i in range(len(personas)):
            d1=dist_punto_recta(personas[i],Medio1_polo1,Medio1_polo2) #distancia a cada uno de los ejes de polarizacion
            d2=dist_punto_recta(personas[i],Medio2_polo1,Medio2_polo2) #         veo con que medio interactua cada persona
            d3=dist_punto_recta(personas[i],Medio3_polo1,Medio3_polo2)
            
            if d2>=d1 and d3>=d1:  
                personas[i] = interaccion(tamanio,personas[i],Medio1_polo1,Medio1_polo2,Medio1_d_C[iteracion],"positiva")
                personas[i] = interaccion(tamanio,personas[i],Medio1_polo1,Medio1_polo2,Medio1_d_T[iteracion],"negativa") 
            elif d1>=d2 and d3>=d2:
                personas[i] = interaccion(tamanio,personas[i],Medio2_polo1,Medio2_polo2,Medio2_d_C[iteracion],"positiva") 
                personas[i] = interaccion(tamanio,personas[i],Medio1_polo1,Medio1_polo2,Medio1_d_T[iteracion],"negativa") 
            else:
                personas[i] = interaccion(tamanio,personas[i],Medio3_polo1,Medio3_polo2,Medio3_d_C[iteracion],"positiva")
                personas[i] = interaccion(tamanio,personas[i],Medio1_polo1,Medio1_polo2,Medio1_d_T[iteracion],"negativa") 
       
        votos_C[iteracion],votos_T[iteracion] = A_quien_vota(personas,Medio1_polo1,Medio1_polo2,Medio2_polo1,Medio2_polo2,Medio3_polo1,Medio3_polo2, False)
    return personas,votos_C,votos_T
 


def dist_punto_recta(punto,puntoRecta_1,puntoRecta_2):
    nom = np.abs((puntoRecta_2[1]-puntoRecta_1[1])*punto[0]-(puntoRecta_2[0]-puntoRecta_1[0])*punto[1]+puntoRecta_2[0]*puntoRecta_1[1]-puntoRecta_2[1]*puntoRecta_1[0])
    den = np.sqrt((puntoRecta_2[1]-puntoRecta_1[1])**2+(puntoRecta_2[0]-puntoRecta_1[0])**2)
    RV= nom/den     
    return RV




def A_quien_vota(personas,Medio1_polo1,Medio1_polo2,Medio2_polo1,Medio2_polo2,Medio3_polo1,Medio3_polo2, printear):
    Votos_C_1, Votos_T_1, Votos_C_2, Votos_T_2, Votos_C_3, Votos_T_3, Votos_C_T, Votos_T_T,Votos_C_votan,Votos_T_votan = 0,0,0,0,0,0,0,0,0,0
    cant_personas_votan = 0.000001
    trsh = 0.25
    
    for persona in personas:
        d1=dist_punto_recta(persona,Medio1_polo1,Medio1_polo2) 
        d2=dist_punto_recta(persona,Medio2_polo1,Medio2_polo2)
        d3=dist_punto_recta(persona,Medio3_polo1,Medio3_polo2)
        if d2>=d1 and d3>=d1:
            d_p1=(Medio1_polo1[0]-persona[0])**2+(Medio1_polo1[1]-persona[1])**2
            d_p2=(Medio1_polo2[0]-persona[0])**2+(Medio1_polo2[1]-persona[1])**2
            if d_p1>d_p2:
                 Votos_T_1 += 1
                 Votos_T_T += 1
                 if d_p2< trsh:
                     cant_personas_votan+=1
                     Votos_T_votan +=1
            else:
                 Votos_C_1 += 1
                 Votos_C_T += 1
                 if d_p1< trsh:
                     cant_personas_votan+=1
                     Votos_C_votan +=1
                
        elif d1>=d2 and d3>=d2:
            d_p1=(Medio2_polo1[0]-persona[0])**2+(Medio2_polo1[1]-persona[1])**2
            d_p2=(Medio2_polo2[0]-persona[0])**2+(Medio2_polo2[1]-persona[1])**2
            if d_p1>d_p2:
                 Votos_T_2 += 1
                 Votos_T_T += 1
                 if d_p2< trsh:
                     cant_personas_votan+=1
                     Votos_T_votan +=1
            else:
                 Votos_C_2 += 1
                 Votos_C_T += 1
                 if d_p1< trsh:
                     cant_personas_votan+=1
                     Votos_C_votan +=1
        else:
            d_p1=(Medio3_polo1[0]-persona[0])**2+(Medio3_polo1[1]-persona[1])**2
            d_p2=(Medio3_polo2[0]-persona[0])**2+(Medio3_polo2[1]-persona[1])**2
            if d_p1>d_p2:
                 Votos_T_3 += 1
                 Votos_T_T += 1
                 if d_p2< trsh:
                     cant_personas_votan+=1
                     Votos_T_votan +=1
            else:
                 Votos_C_3 += 1
                 Votos_C_T += 1
                 if d_p1< trsh:
                     cant_personas_votan+=1
                     Votos_C_votan +=1
                 
    cant_personas = len(personas)  
    if printear:           
        print('--------')    
        print('vota',cant_personas/len(personas),'% de la población')
        print('Votos a Clinton por FN:',Votos_C_1/cant_personas,'%')
        print('Votos a Trump por FN:',Votos_T_1/cant_personas,'%')
        print('Votos a Clinton por NYT:',Votos_C_2/cant_personas,'%')
        print('Votos a Trump  por NYT:',Votos_T_2/cant_personas,'%')
        print('Votos a Clinton por Breitbart:',Votos_C_3/cant_personas,'%')
        print('Votos a Trump por Breitbart:',Votos_T_3/cant_personas,'%')
        print('Votos a Clinton totales:',Votos_C_T/cant_personas,'%')
        print('Votos a Trump totales:',Votos_T_T/cant_personas,'%')  
        print('Votos a Clinton totales (voto optativo):',Votos_C_votan/cant_personas_votan,'%')
        print('Votos a Trump totales (voto optativo):',Votos_T_votan/cant_personas_votan,'%')  
        print('--------')  
        
    return [Votos_C_votan/cant_personas_votan,Votos_T_votan/cant_personas_votan]

