import os
import requests
import time
import random
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()

# --- CONFIGURACIÓN ---
API_TOKEN = os.getenv("API_TOKEN")
SERVER_ID = os.getenv("SERVER_ID")

# Validar que sí se cargaron las variables correctamente
if not API_TOKEN or not SERVER_ID:
    print("Error: Faltan credenciales")
    exit()

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def ejecutar_comando(comando):
    """ACTUADOR: Envía la orden al servidor por la API"""
    url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/command/"
    requests.post(url, headers=HEADERS, json={"command": comando})

def agente_reactivo():
    url_estado = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/"
    print("Agente Reactivo listo y monitoreando el servidor...")
    
    jugadores_anteriores = []
    ciclos = 0
    
    while True:
        try:
            # SENSOR: Lee cómo está el mundo en este momento exacto
            respuesta = requests.get(url_estado, headers=HEADERS)
            
            if respuesta.status_code != 200:
                time.sleep(15)
                continue
                
            datos = respuesta.json().get("data", {})
            
            if datos.get("status") != 2:
                print("⏳ Servidor apagado o iniciando. Esperando...")
                time.sleep(15)
                continue
                
            # Extraemos lo que nos interesa percibir
            ram_usada = datos.get("ram", {}).get("usage", 0)
            lista_jugadores = datos.get("players", {}).get("list", [])
            num_jugadores = len(lista_jugadores)
            
            print(f"Escaneo -> RAM: {ram_usada / 1000000:.2f} MB | Jugadores: {num_jugadores}")
            
            # ==========================================
            # LAS 6 ACCIONES DEL AGENTE
            # ==========================================
            
            # 1. LIMPIEZA DE LAG: Si la RAM sube a más de 1GB
            if ram_usada > 1000000000:
                print("ACCIÓN 1: Limpiando entidades por RAM alta.")
                ejecutar_comando("kill @e[type=item]")
                ejecutar_comando("say [Agente] Limpieza automatica por sobrecarga de RAM.")

            # Detectamos quién acaba de entrar comparando con el escaneo anterior
            jugadores_nuevos = [j for j in lista_jugadores if j not in jugadores_anteriores]
            
            # 2. EL KIT DE BIENVENIDA
            for jugador in jugadores_nuevos:
                print(f"ACCIÓN 2: Bienvenida a {jugador}.")
                ejecutar_comando(f"say ¡Bienvenido a la partida, {jugador}!")
                ejecutar_comando(f"give {jugador} stone_pickaxe 1")
                ejecutar_comando(f"give {jugador} cooked_beef 10")

            # 3. DIFICULTAD DINÁMICA (Modo Horda)
            if num_jugadores >= 3:
                # Si hay 3 o más, subimos la dificultad
                ejecutar_comando("difficulty hard")
            elif num_jugadores > 0:
                # Si son 1 o 2, la dejamos normal
                ejecutar_comando("difficulty normal")

            # Aumentamos el contador de ciclos para los eventos de tiempo
            ciclos += 1

            # Eventos que solo ocurren si hay gente conectada
            if num_jugadores > 0:
                
                # 4. EL SUSTO DIVINO (Rayo aleatorio cada ~2 minutos)
                if ciclos % 8 == 0:
                    victima = random.choice(lista_jugadores)
                    print(f"ACCIÓN 4: Rayo asustando a {victima}.")
                    ejecutar_comando(f"execute at {victima} run summon lightning_bolt ~ ~ ~5")
                    ejecutar_comando(f"say Ups, casi te doy, {victima}...")

                # 5. RULETA DE SUPERPODERES (Cada ~3.5 minutos)
                if ciclos % 14 == 0:
                    afortunado = random.choice(lista_jugadores)
                    poderes = [
                        {"efecto": "jump_boost", "nombre": "Super Salto", "nivel": 3},
                        {"efecto": "speed", "nombre": "Velocidad Extrema", "nivel": 3},
                        {"efecto": "haste", "nombre": "Super Mineria", "nivel": 3}
                    ]
                    poder_elegido = random.choice(poderes)
                    
                    print(f"ACCIÓN 5: {afortunado} recibió {poder_elegido['nombre']}.")
                    ejecutar_comando(f"say ¡La ruleta giro! {afortunado} recibe {poder_elegido['nombre']} por 1 minuto.")
                    ejecutar_comando(f"effect give {afortunado} {poder_elegido['efecto']} 60 {poder_elegido['nivel']}")

                # 6. AIRDROP SORPRESA (Lotería cada ~5 minutos)
                if ciclos % 20 == 0:
                    if random.choice([True, False]): # 50% de probabilidad de que caiga el premio
                        print("ACCIÓN 6: ¡Airdrop lanzado!")
                        ejecutar_comando("say ¡El Agente ha lanzado un Airdrop sorpresa!")
                        ejecutar_comando("give @a diamond 1")

            # Actualizamos la memoria a corto plazo
            jugadores_anteriores = lista_jugadores
            
        except Exception as e:
            print(f"Error en los sensores: {e}")
            
        # Espera 15 segundos para no saturar la API
        time.sleep(15) 

if __name__ == "__main__":
    agente_reactivo()