"""
Configuración de probabilidades y constantes para el generador de sistemas solares
"""

# Probabilidades de tipos de sistema (deben sumar a 100 para facilidad de cálculo)
SYSTEM_PROBABILITIES = [50, 25, 25]  # Unario, Binario, Trinario

# Probabilidades de tipos de estrellas (valores relativos)
# Valores más altos = mayor probabilidad
STAR_PROBABILITIES = {
    # Estrellas más comunes
    'Estrella Clase M': 3500,   # La más común
    'Tipo K': 2000,             # Común y habitable
    'Tipo G': 2000,             # Como nuestro Sol
    'Tipo F': 1500,             # Habitable pero menos común
    
    # Estrellas menos comunes
    'Tipo A': 500,              # Menos común
    'Tipo T': 300,              # Enana marrón
    
    # Estrellas raras
    'Gigante Roja': 100,        # Peligrosa
    'Pulsar': 70,               # Muy peligrosa
    'Agujero Negro': 20,        # Extremadamente peligrosa
    'Magnetar': 5,              # Muy rara y peligrosa
    
    # Estrellas extremadamente raras
    'Estrella Extraña': 3,      # Hipotética
    'Tipo O': 2                 # Muy masiva y rara
}

# Estrellas que hacen habitable un sistema
HABITABLE_STARS = [
    'Tipo K',
    'Tipo G', 
    'Tipo F',
    'Tipo A'
]

# Estrellas que hacen inhabitable un sistema (anulan habitabilidad)
DANGEROUS_STARS = [
    'Gigante Roja',
    'Pulsar',
    'Agujero Negro',
    'Estrella Extraña',
    'Magnetar',
    'Tipo O'
]

# Estrellas que impiden la generación de planetas, lunas y asteroides
NO_BODIES_STARS = [
    'Agujero Negro',
    'Estrella Extraña'
]

# Probabilidades para eventos especiales
EVENTO_ESPECIAL_PROBABILITY = 30  # 30% de chance de evento especial

# Probabilidades de recursos estratégicos
DEPOSITOS_PROBABILITY = 50  # 50% de chance de tener depósitos

RECURSOS_ESTRATEGICOS = {
    # Recursos más comunes
    'Gases Exóticos': 30,
    'Cristales Raros': 30,
    'Polvo Zro': 25,
    
    # Recursos poco comunes
    'Motas Volátiles': 10,
    
    # Recursos muy poco comunes
    'Metal Vivo': 4,
    
    # Recursos extremadamente raros
    'Nanitos': 1
}

# Recursos especiales solo para agujeros negros
RECURSOS_AGUJERO_NEGRO = ['Materia Oscura']

# Tipos de eventos especiales
EVENTOS_ESPECIALES = ['Yacimiento Arqueológico', 'Anomalía']

# Rangos para planetas habitables en sistemas habitables
PLANETAS_HABITABLES_RANGE = (1, 3)

# Rangos para generación de cuerpos celestes
PLANETS_RANGE = (1, 16)
MOONS_RANGE = (1, 27)
ASTEROID_BELTS_RANGE = (0, 2)

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'solar_system_bot.log'

# Configuración del bot
BOT_DESCRIPTION = 'Bot generador de sistemas solares para roleplay de naciones espaciales'
COMMAND_PREFIX = '!'

# Colores para embeds de Discord (en hexadecimal)
EMBED_COLORS = {
    'success': 0x4CAF50,      # Verde
    'info': 0x1E88E5,         # Azul
    'warning': 0xFF9800,      # Naranja
    'error': 0xF44336,        # Rojo
    'habitable': 0x4CAF50,    # Verde para sistemas habitables
    'inhabitable': 0xF44336   # Rojo para sistemas inhabitables
}

# Emojis para el bot
EMOJIS = {
    'star': '⭐',
    'planet': '🪐',
    'moon': '🌙',
    'asteroid': '🌌',
    'habitable': '✅',
    'inhabitable': '❌',
    'system': '🌌',
    'info': 'ℹ️',
    'warning': '⚠️',
    'danger': '☢️'
}

# Mensajes del bot
MESSAGES = {
    'system_generated': 'Sistema solar generado exitosamente',
    'generation_error': 'Error al generar el sistema solar',
    'no_bodies_warning': 'No se generan cuerpos celestes debido a condiciones extremas',
    'bot_ready': 'Bot de sistemas solares listo para usar',
    'help_title': 'Guía de Sistemas Solares',
    'help_description': 'Información sobre la generación de sistemas solares para roleplay'
}

# Información adicional sobre tipos de estrellas para el comando de ayuda
STAR_INFO = {
    'common_stars': ['Estrella Clase M', 'Tipo K', 'Tipo G', 'Tipo F'],
    'uncommon_stars': ['Tipo A', 'Tipo T'],
    'rare_stars': ['Gigante Roja', 'Pulsar', 'Agujero Negro'],
    'very_rare_stars': ['Magnetar', 'Estrella Extraña', 'Tipo O']
}
