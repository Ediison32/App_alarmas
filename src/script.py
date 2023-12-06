import pywhatkit
import datetime
import json
from datetime import timedelta
from time import sleep
import serial
from threading import Thread

info = open("config.json", "r")
send = json.loads(info.read())

#pywhatkit.sendwhatmsg_to_group(id_grupo, "mensaje prueba",10,36)

def fechaActual():
    fecha_hora_actual = datetime.datetime.now()
    format = "%d-%m-%Y  %H:%M"
    fecha_hora_formateada = fecha_hora_actual.strftime(format)

    hora = datetime.datetime.now().time().hour
    minuto=datetime.datetime.now().time().minute

    return fecha_hora_formateada,hora,minuto



arduino = serial.Serial('COM6', 9600)  
print("ARRANCA")

def listen_to_arduino():
    try:
        
        while True:
            data = arduino.readline().decode().strip()
            print(f"Dato recibido desde Arduino: {data}")
            if data == "Se apago la caldera":
                fecha,hora,minuto= fechaActual()
                mensaje = " caldera apagada el: "+ fecha
                pywhatkit.sendwhatmsg_to_group(send["id_grupo"],mensaje, hora, minuto+1)
               # pywhatkit.sendwhatmsg(id_grupo,mensaje, datetime.now().hour, datetime.now().minute + 1)
                print("MENSAJE ENVIADO ")
    except KeyboardInterrupt:
        print("Programa terminado.")
        arduino.close()

    

if __name__ == '__main__':
    
    arduino_thread = Thread(target=listen_to_arduino)
    arduino_thread.start()  # Inicia el hilo para escuchar datos desde Arduino
    

