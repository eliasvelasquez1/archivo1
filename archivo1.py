from googletrans import Translator # Libreria de google para traducir texto (GUIA)
import urllib.parse #Permite codificar paremetros de URL
import requests #Permite realizar solitudes HTTP

translator = Translator() # crea una instancia para el traductor de google

"""
Se definen las url necesarias para el funcionamiento del codigo
y las claves para las API de Mapquest y Google Cloud
Las variables estan en Ingles por buenas practicas
"""

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "RVA9r2c4w2TDXkMXEjKwQ3xUVaIw1Zhf"
google_translate_api_key = "AIzaSyDID5ycBqiM5eUDihfwa2uMp7xkRPjAxw4"

#While crea una repeticion continua para que el usario ingrese pares de ciudades y obtenga indicaciones
while True:

    #Instrucciones generales para el usuario
    print("======================= ADVERTENCIA ==========================")
    print("Entregue las direcciones especificando el País de origen")
    print("Respete el siguiente formato de EJEMPLO: Concepcion, Chile")
    print("Para salir del programa ejecute 'S' o la palabra 'salida'")
    print("==============================================================")

    start = input("Ciudad de origen: ")
    if start == "salida" or start == "S": #Formato para salir del programa
        break
    end = input("Ciudad de destino: ")
    if end == "salida" or end == "S": #Formato para salir del programa
        break 
    #La primera línea codifica los parametros generales para hacer una correcta solicitus a la API
    #La segunda línea hace solicitud de HTTP GET por medio de requests
    #La cuarta linea indica el resultado de la solicitud y en base a ello se ejecuta el codigo
    url = main_api + urllib.parse.urlencode({"key": key, "from": start, "to": end})
    json_data = requests.get(url).json()
    print("URL: " + url)
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        #Si la llamada a la ruta es igual a cero esta fue exitosa. Entregando los parametros generales
        #json_data es un objeto que contiene la propiedad (route); de esta se extrae Time y distance
        #{:.1}.format imprime los resultados de distancia con un decimal
        print("Estado de la API: " + str(json_status) + " = La llamada a la ruta fue exitosa.\n")
        print("====================== PARAMETROS GENERALES =========================")        
        print("Inicio de trayecto desde " + (start) + " hasta " + (end))      
        print("Tiempo estimado del viaje:  " + (json_data["route"]["formattedTime"]))  
        print("Kilómetros: {:.1f}".format(json_data["route"]["distance"] * 1.61))  
        print("============================== GUIA =================================")
        #maneuvers son las maniobras o indicaciones que se encuentran en la json_data
        #each itera las intrucciones de 1 en 1
        #En narrative se guardan las iteraciones impartidas por each y translation las traduce
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            narrative = each["narrative"]
            translation = translator.translate(each["narrative"], dest='es').text  
            print(translation + "(" + str("{:.1f}".format(each["distance"] * 1.61)) + "km)")
        print("=====================================================================\n")
    #Si el estado da un error es lo concatena como un string
    elif json_status == 402:        
        print("***********************************************")
        print("Código de estado:" + str (json_status) + "; Entradas de usuario no válidas para una o ambas ubicaciones.")    
        print("***********************************************\n")    
    elif json_status == 611:        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Código de estado:" + str (json_status) + "; Falta una entrada para una o ambas ubicaciones.")    
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")    
    else:      
        print( "/////////////////////////////////////////////////////////")        
        print("Para el código:" + str (json_status) + "; consulte:")        
        print(" https://developer.mapquest.com/documentation/directions-api/status-codes ")
        print("///////////////////////////////////////////////////////////\n")