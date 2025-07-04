import os
import logging
from bot import SolarSystemBot

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Función principal para iniciar el bot"""
    # Obtener token del bot desde las variables de entorno
    token = os.getenv('DISCORD_BOT_TOKEN')

    if not token:
        logging.error("DISCORD_BOT_TOKEN no está configurado en las variables de entorno")
        return

    # Crear y ejecutar el bot
    bot = SolarSystemBot()

    # Add traditional commands
    from bot import generar_comando, ayuda_comando, ficha_comando
    bot.add_command(generar_comando)
    bot.add_command(ayuda_comando)
    bot.add_command(ficha_comando)

    try:
        bot.run(token)
    except Exception as e:
        logging.error(f"Error al ejecutar el bot: {e}")

if __name__ == "__main__":
    main()