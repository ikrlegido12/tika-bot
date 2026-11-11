# tika-bot
Bot de Discord con DiscordPY para CDPC

## Prerequisitos
- Python 3.12
## Requisitos
Librerías: discord.py, python-dotenv (se instalan desde `requirements.txt`)

## Ejecución local

Crea un archivo `.env` en la raíz con las variables necesarias:

```env
DISCORD_TOKEN=tu_token_del_bot
TEST_GUILD_ID=id_de_tu_servidor_de_pruebas
DEV_USER_IDS=123456789012345678,987654321098765432
```

`TEST_GUILD_ID` es opcional. Si se configura, los slash commands se sincronizan
solo con ese servidor y los cambios aparecen rápidamente durante el desarrollo.
Si se deja vacío, se sincronizan globalmente; Discord puede tardar un tiempo en
propagarlos. Invita la aplicación con los scopes `bot` y `applications.commands`.

El código está organizado bajo `src/`: `commands/` contiene comandos, `events/`
contendrá listeners de Discord y `utils/` las funciones auxiliares compartidas.

Puedes crear embeds reutilizables con `create_embed`:

```python
from utils import create_embed

embed = create_embed(
    title="Ticket creado",
    description="El equipo de soporte te atenderá pronto.",
    fields=[("Número", "#42", True)],
    footer="Tika Bot",
)
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
- `TEST_GUILD_ID` (opcional): ID del servidor donde sincronizar comandos para pruebas.
- `DEV_USER_IDS` (opcional): IDs de usuario de Discord autorizados para `/restart`, separados por comas. Si está vacío, nadie puede usarlo.

`/restart` cierra el bot ordenadamente. En Docker, la política `restart: unless-stopped`
de Compose vuelve a iniciar el contenedor. Al ejecutarlo localmente, el proceso termina
y tendrás que iniciarlo de nuevo manualmente.

## Créditos
ikrlegido12 - Desarrollador y host del bot

treyunova301 - Desarrollador
