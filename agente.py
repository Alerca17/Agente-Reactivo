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

if not API_TOKEN or not SERVER_ID:
    print("Error: Faltan credenciales. Revisa tu archivo .env")
    exit()

HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}


def ejecutar_comando(comando):
    """ACTUADOR: Envía la orden al servidor por la API"""
    url = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/command/"
    respuesta = requests.post(url, headers=HEADERS, json={"command": comando})
    if respuesta.status_code != 200:
        print(f"Error enviando comando: {respuesta.text}")


def agente_reactivo():
    url_estado = f"https://api.exaroton.com/v1/servers/{SERVER_ID}/"
    print("Agente Reactivo listo y monitoreando el servidor...")

    jugadores_conocidos = []
    ciclos = 0

    while True:
        try:
            # SENSOR PRINCIPAL
            respuesta = requests.get(url_estado, headers=HEADERS)

            if respuesta.status_code != 200:
                print(f"Error de conexión a Exaroton: Código {respuesta.status_code}")
                time.sleep(15)
                continue

            datos = respuesta.json().get("data", {})
            estado_actual = datos.get("status")

            if estado_actual != 1:
                print(f"Servidor no está listo (Estado: {estado_actual}). Esperando...")
                time.sleep(15)
                continue

            # Extraemos lo que nos interesa percibir de la realidad
            lista_jugadores = datos.get("players", {}).get("list", [])
            num_jugadores = len(lista_jugadores)

            print(f"Escaneo -> Jugadores conectados: {num_jugadores}")

            # LAS ACCIONES DEL AGENTE

            # Aumentamos el contador de tiempo del agente
            ciclos += 1

            # 1. MANTENIMIENTO PREVENTIVO (Cada 2.5 minutos)
            if ciclos % 10 == 0:
                print("ACCIÓN 1: Ejecutando mantenimiento preventivo.")
                ejecutar_comando("kill @e[type=item]")
                ejecutar_comando("say [Agente] Limpieza de objetos.")

            # Detectamos quién acaba de entrar
            jugadores_nuevos = [
                j for j in lista_jugadores if j not in jugadores_conocidos
            ]

            # 2. EL KIT DE BIENVENIDA
            for jugador in lista_jugadores:
                if jugador not in jugadores_conocidos:
                    print(f"👋 ACCIÓN 2: Bienvenida PRO a {jugador}.")
                    ejecutar_comando(
                        f"say ¡Bienvenido al servidor, {jugador}! Revisa tu inventario para empezar con toda."
                    )

                    # Herramientas de hierro
                    ejecutar_comando(f"give {jugador} iron_pickaxe 1")
                    ejecutar_comando(f"give {jugador} iron_sword 1")
                    ejecutar_comando(f"give {jugador} iron_axe 1")

                    # Defensa esencial
                    ejecutar_comando(f"give {jugador} shield 1")
                    ejecutar_comando(f"give {jugador} iron_chestplate 1")
                    ejecutar_comando(f"give {jugador} iron_leggings 1")

                    # Comida premium
                    ejecutar_comando(f"give {jugador} golden_carrot 32")

                    # Anotamos al jugador en la memoria para no repetirle el kit
                    jugadores_conocidos.append(jugador)

            # 3. DIFICULTAD DINÁMICA
            if num_jugadores >= 3:
                ejecutar_comando("difficulty hard")
            elif num_jugadores > 0:
                ejecutar_comando("difficulty normal")

            # Eventos que solo pasan si hay gente conectada
            if num_jugadores > 0:

                # 4. EL SUSTO DIVINO (Rayo aleatorio cada ~2 minutos)
                if ciclos % 8 == 0:
                    victima = random.choice(lista_jugadores)
                    print(f"ACCIÓN 4: Rayo asustando a {victima}.")
                    ejecutar_comando(
                        f"execute at {victima} run summon lightning_bolt ~ ~ ~5"
                    )
                    ejecutar_comando(f"say Ups, casi te doy, {victima}...")

                # 5. RULETA DE SUPERPODERES (Cada ~3.5 minutos)
                if ciclos % 14 == 0:
                    afortunado = random.choice(lista_jugadores)
                    poderes = [
                        {"efecto": "jump_boost", "nombre": "Super Salto", "nivel": 3},
                        {"efecto": "speed", "nombre": "Velocidad Extrema", "nivel": 3},
                        {"efecto": "haste", "nombre": "Super Mineria", "nivel": 3},
                    ]
                    poder_elegido = random.choice(poderes)

                    print(f"ACCIÓN 5: {afortunado} recibió {poder_elegido['nombre']}.")
                    ejecutar_comando(
                        f"say ¡La ruleta giro! {afortunado} recibe {poder_elegido['nombre']} por 1 minuto."
                    )
                    ejecutar_comando(
                        f"effect give {afortunado} {poder_elegido['efecto']} 60 {poder_elegido['nivel']}"
                    )

                # 6. AIRDROP SORPRESA (Lotería cada ~5 minutos)
                if ciclos % 20 == 0:
                    if random.choice([True, False]):  # 50% de probabilidad
                        print("ACCIÓN 6: ¡Airdrop lanzado!")
                        ejecutar_comando(
                            "say ¡El Agente ha lanzado un Airdrop sorpresa!"
                        )
                        ejecutar_comando("give @a diamond 1")

        except Exception as e:
            print(f"Error en los sensores: {e}")

        time.sleep(15)


if __name__ == "__main__":
    agente_reactivo()
