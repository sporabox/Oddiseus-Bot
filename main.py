import os
import asyncio
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

async def main():
    """Función principal para ejecutar el bot"""
    # Obtener token del bot desde variables de entorno
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        logging.error("No se encontró el token del bot. Asegúrate de establecer DISCORD_BOT_TOKEN en las variables de entorno.")
        return
    
    # Crear e iniciar el bot
    bot = SolarSystemBot()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logging.info("Bot detenido por el usuario")
    except Exception as e:
        logging.error(f"Error al ejecutar el bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
