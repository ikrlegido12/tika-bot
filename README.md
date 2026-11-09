# tika-bot
Bot de Discord con DiscordPY para CDPC

## Prerequisitos
- Python 3.12 para Docker. para desarrollo local, Python 3.8 o superior
## Requisitos
Librerías: discord.py, python-dotenv (se instalan desde `requirements.txt`)

## Ejecución local

Crea un archivo `.env` en la raíz con las variables necesarias:

```env
DISCORD_TOKEN=tu_token_del_bot
CLIENT_ID=tu_client_id
```

Instala las dependencias y ejecuta el bot:

```powershell
.\tika-env\Scripts\python.exe -m pip install -r requirements.txt
.\tika-env\Scripts\python.exe .\src\index.py
```

## Docker y Dockge

El `Dockerfile` crea una imagen para `linux/amd64` y `linux/arm64`. GitHub Actions publica la imagen en GHCR al hacer push. No despliega en la Raspberry Pi: la actualización del stack se hace manualmente desde Dockge (interfaz web de Docker), descargando la nueva imagen y recreando el contenedor.

Al detener o recrear el contenedor, Docker envía `SIGTERM`; el bot cierra su conexión con Discord antes de salir. Compose espera hasta 30 segundos para que termine el cierre.

La Raspberry debe poder descargar la imagen de GHCR. Si el paquete es privado, inicia sesión en GHCR en la Raspberry con un token que tenga permiso `read:packages`; si es público, no hace falta.

## Variables de entorno
- `DISCORD_TOKEN` (obligatoria): token del bot de Discord.
- `CLIENT_ID` (opcional): ID de la aplicación de Discord.

## Créditos
ikrlegido12 - Desarrollador y host del bot

treyunova301 - Desarrollador
