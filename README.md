# Agente Reactivo para Minecraft con Exaroton API

Un **Agente Reactivo Simple** desarrollado en **Python** para monitorear y administrar automáticamente un servidor de Minecraft alojado en Exaroton.

El agente observa continuamente el estado del servidor mediante la API REST de Exaroton y ejecuta acciones automáticas basadas en reglas predefinidas, mejorando la experiencia de juego sin intervención humana.

---

## Descripción

Este proyecto implementa un agente reactivo basado en reglas simples. El agente percibe el entorno mediante consultas periódicas a la API de Exaroton y responde automáticamente según el estado actual del servidor y los jugadores conectados.

Su objetivo es automatizar tareas de mantenimiento, interacción con jugadores y ajustes dinámicos de la dificultad para mejorar la experiencia de juego.

---

## Funcionalidades

El agente opera en un ciclo continuo y ejecuta las siguientes acciones:

---

## Arquitectura del Agente

Percepción → Evaluación de Reglas → Acción

1. El agente consulta el estado del servidor mediante la API de Exaroton.
2. Evalúa las reglas definidas.
3. Ejecuta acciones utilizando comandos de Minecraft.
4. Espera el siguiente ciclo de monitoreo.
5. Repite el proceso indefinidamente.

---

### 1. Mantenimiento Preventivo

Cada 10 ciclos (aproximadamente cada 2.5 minutos):

- Elimina los objetos tirados en el suelo.
- Limpia el clima del servidor.

**Comandos utilizados:**

```mcfunction
kill @e[type=item]
weather clear
```

### 2. Bienvenida con Memoria

Cuando un jugador se conecta por primera vez durante la sesión:

- Recibe un Kit PRO compuesto por:
  - Herramientas de hierro.
  - Escudo.
  - Armadura básica.
  - Zanahorias doradas.

El agente mantiene un registro interno para evitar entregar el kit más de una vez por sesión.

### 3. Dificultad Dinámica

La dificultad del servidor se ajusta automáticamente según la cantidad de jugadores conectados:

| Jugadores conectados | Dificultad |
|----------------------|------------|
| Menos de 3           | Normal     |
| 3 o más              | Difícil    |

### 4. El Susto Divino

Periódicamente:

- Se selecciona un jugador aleatorio.
- Se genera un rayo cerca de su ubicación.
- El evento no produce daño directo.

Este comportamiento busca agregar momentos inesperados y mantener la atención de los jugadores.

### 5. Ruleta de Superpoderes

De forma aleatoria, un jugador recibe temporalmente uno de los siguientes efectos de nivel III:

- Super Salto.
- Velocidad Extrema.
- Super Minería.

### 6. Airdrop Sorpresa

Cada cierto tiempo se ejecuta una lotería global:

- Existe un 50% de probabilidad de activación.
- Todos los jugadores conectados reciben un diamante.

---

## Tecnologías Utilizadas

- Python 3.x
- Requests
- Python Dotenv
- API REST de Exaroton
- Minecraft Java Edition

---

## Requisitos

Antes de ejecutar el proyecto es necesario contar con:

- Python 3.x instalado.
- Un servidor activo en Exaroton.
- Token de acceso a la API de Exaroton.
- Identificador (ID) del servidor.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Alerca17/Agente-Reactivo.git
cd Agente-Reactivo
```

### 2. Crear y activar un entorno virtual

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install requests python-dotenv
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
API_TOKEN=tu_token_aqui
SERVER_ID=tu_id_del_servidor_aqui
```

---

## Ejecución

Iniciar el agente con el siguiente comando:

```bash
python agente.py
```

Una vez ejecutado, el agente comenzará a monitorear el servidor y aplicará automáticamente las reglas definidas.

---

## Estructura del Proyecto

```text
Agente-Reactivo/
│
├── agente.py
├── .env
```

---

**Alejandro Correa Arias**

GitHub: https://github.com/Alerca17
