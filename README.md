# Discord Solar System Generator Bot

Bot generador de sistemas solares para servidores de roleplay de naciones espaciales.

## Archivos del Proyecto

- `main.py` - Archivo principal para ejecutar el bot
- `bot.py` - Lógica del bot de Discord y comandos
- `solar_system_generator.py` - Generador de sistemas solares
- `config.py` - Configuración de probabilidades y constantes
- `railway_requirements.txt` - Dependencias para Railway
- `Procfile` - Comando de inicio para Railway
- `railway.json` - Configuración de Railway

## Comandos del Bot

### Comandos Slash
- `/generar_sistema` - Genera un sistema solar aleatorio
- `/ayuda_sistema` - Muestra información de ayuda

### Comandos Tradicionales
- `!generar` (o `!sistema`, `!solar`) - Genera un sistema solar aleatorio
- `!ayuda` (o `!info`) - Muestra información de ayuda

## Variables de Entorno Requeridas

- `DISCORD_BOT_TOKEN` - Token del bot de Discord

## Despliegue en Railway

1. Sube todos los archivos a un repositorio de GitHub
2. Conecta Railway a tu repositorio
3. Configura la variable de entorno DISCORD_BOT_TOKEN
4. Railway detectará automáticamente la configuración