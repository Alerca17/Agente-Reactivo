# Agente Reactivo para Minecraft (Exaroton API)

Este proyecto implementa un **Agente Reactivo Simple** desarrollado en Python, diseñado para monitorear y gestionar de forma autónoma un servidor de Minecraft alojado en la plataforma Exaroton. 

El agente percibe el estado del entorno en tiempo real (jugadores conectados) a través de la API REST de Exaroton y toma decisiones automatizadas de mantenimiento, interacción y control de dificultad sin necesidad de intervención humana.

## ⚙️ Características Principales (Reglas del Agente)

El agente opera en un ciclo continuo y ejecuta las siguientes 6 acciones basadas en las condiciones del entorno:

1. **Mantenimiento Preventivo:** Cada 10 ciclos (aprox. 2.5 minutos), limpia los objetos tirados en el suelo (`kill @e[type=item]`) y despeja el clima para evitar sobrecarga y lag en el servidor.
2. **Bienvenida con Memoria:** Detecta nuevos jugadores y les entrega un "Kit PRO" (herramientas de hierro, escudo, armadura básica y zanahorias doradas). Utiliza una lista histórica para asegurar que el kit se entregue solo una vez por sesión.
3. **Dificultad Dinámica:** Escala la dificultad del juego a "Difícil" si hay 3 o más jugadores conectados simultáneamente, fomentando el trabajo en equipo. Regresa a "Normal" si hay menos.
4. **El Susto Divino:** Cada cierto tiempo, elige a un jugador al azar de la sesión y hace caer un rayo cerca de su posición (sin causarle daño directo) para mantener la tensión en el juego.
5. **Ruleta de Superpoderes:** Aleatoriamente, otorga a un jugador un efecto positivo temporal de nivel 3 (Super Salto, Velocidad Extrema o Super Minería).
6. **Airdrop Sorpresa:** Ejecuta un evento de lotería periódicamente donde existe un 50% de probabilidad de que todos los jugadores reciban un diamante.

## Tecnologías y Requisitos

* **Python 3.x**
* Librería `requests` (para peticiones a la API).
* Librería `python-dotenv` (para manejo seguro de variables de entorno).
* Un servidor de Minecraft activo en Exaroton.

## Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Alerca17/Agente-Reactivo.git](https://github.com/Alerca17/Agente-Reactivo.git)
   cd Agente-Reactivo

2. **Crear y activar un entorno virtual**
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

3. **Instalar dependencias**
   pip install requests python-doten

4. **Configurar variables de entorno**

  Crea un archivo llamado .env en la raíz del proyecto.
  Agrega tus credenciales de Exaroton sin comillas:
  
  API_TOKEN=tu_token_aqui
  SERVER_ID=tu_id_del_servidor_aqui

5. **Ejecutar el Agente**
  python agente.py


Autor
Alejandro Correa Arias
