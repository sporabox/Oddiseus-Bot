"""
Configuración de probabilidades y constantes para el generador de sistemas solares
"""

# Probabilidades de tipos de sistema (deben sumar a 100 para facilidad de cálculo)
SYSTEM_PROBABILITIES = [50, 25, 25]  # Unario, Binario, Trinario

# Probabilidades de tipos de estrellas (valores relativos)
# Valores más altos = mayor probabilidad
STAR_PROBABILITIES = {
    # Estrellas más comunes - No habitables
    'Estrella Clase M': 4000,   # La más común
    'Tipo T': 1500,             # Enana marrón
    
    # Estrellas habitables - Menos comunes
    'Tipo K': 800,              # Habitable pero menos común
    'Tipo G': 700,              # Como nuestro Sol
    'Tipo F': 600,              # Habitable pero menos común
    'Tipo A': 400,              # Habitable pero rara
    
    # Estrellas raras
    'Gigante Roja': 150,        # Peligrosa
    'Pulsar': 100,              # Muy peligrosa
    'Agujero Negro': 30,        # Extremadamente peligrosa
    'Magnetar': 10,             # Muy rara y peligrosa
    
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
EVENTO_ESPECIAL_PROBABILITY = 15  # 15% de chance de evento especial

# Probabilidades de recursos estratégicos
DEPOSITOS_PROBABILITY = 25  # 25% de chance de tener depósitos

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

# Tipos de planetas y sus probabilidades
TIPOS_PLANETAS = {
    'Helados': {
        'probabilidad': 30,
        'planetas': [
            "tundra", "alpino", "ártico", "Tormentoso", "Icebergs", "Glacial", 
            "Antártico", "Eólico", "Desertico Frio", "Dunas de Hielo", "Grietas", 
            "Púas de Hielo", "Crioflora", "Líquenes", "Pantanos", "Micelio", 
            "Barro", "Basalto", "Tuya", "Criovolcánico", "Treelines", 
            "Glaciovolcánico", "Lantánidos", "Borealis", "Nevado", 
            "Mundo de las Alturas", "Bosques de Duna", "Fiordos", "Floreciente", "Taiga"
        ]
    },
    'Secos': {
        'probabilidad': 30,
        'planetas': [
            "desértico", "árido", "sabana", "Salado", "Acuífero", "Oasis", "Duna", 
            "Outbacks", "Costero", "Hongos", "Arena de Hierro", "Cactus", "Coral", 
            "Primitivo", "Mesa", "Desierto de Niebla", "Mediterráneo", "Badlands", 
            "Suculentas", "Rayado, Amatista", "Sumideros", "Estepa", "Pradera", 
            "Calcita", "Semiárido", "Álamos", "Turquesa"
        ]
    },
    'Humedos': {
        'probabilidad': 30,
        'planetas': [
            "continental", "megafloriano", "Petrificado", "Supercontinental", "Lagos", 
            "boscoso", "tropical", "oceánico", "fungal", "musgoso", "arrecife", 
            "cascadiano", "pantanico", "archipiélago", "riscoso", "niebla", 
            "Mundo de alga", "pilares", "alganiano rosa", "geotérmico", 
            "bioluminiscente", "atolonico", "tepuico", "manglares", "cenótico", 
            "fúngico", "aereo"
        ]
    },
    'Otros': {
        'probabilidad': 7,
        'planetas': [
            "Tumba", "Reliquia", "Gaia", "Gaia seco", "Gaia frio", 
            "Superhabitable humedo", "Superhabitable Frio", "Superhabitable Seco"
        ]
    },
    'Exoticos': {
        'probabilidad': 3,
        'planetas': [
            "Acido", "Radiotropical", "Hiceano", "Metanico", "Ceniza", 
            "Amoniaco", "Sulfurico", "Pandorico", "cristalino"
        ]
    }
}

# Rangos para generación de cuerpos celestes
PLANETS_RANGE = (1, 16)
MOONS_RANGE = (1, 27)
ASTEROID_BELTS_RANGE = (0, 3)

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
