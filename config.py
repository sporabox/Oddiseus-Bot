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
    'Estrella de Neutrones': 100, # Muy peligrosa
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
    'Estrella de Neutrones',
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
DEPOSITOS_PROBABILITY = 15  # 15% de chance de tener depósitos

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

# Configuración de Sondeo
SONDEO_PROBABILITY = 5  # 5% chance de sondeo exitoso (muy, muy bajo)

# Configuración de Leviatanes
LEVIATANES_PROBABILITY = 20  # 20% chance de leviatanes (raro pero no tanto)

# Leviatanes y sus restricciones
LEVIATANES = [
    "Nubes de Vacío",
    "Dragones espaciales", 
    "Amebas espaciales",
    "Entidades cristalinas",
    "Tiyankis",
    "Colmenas de asteroides",
    "Calamares fantasma",
    "Estelaritas",
    "Engendros del vacío",
    "Horrores dimensionales", 
    "Drones mineros antiguos",
    "Cutoloides",
    "Gusanos del vacío"
]

# Restricciones de leviatanes por tipo de sistema
LEVIATANES_RESTRICCIONES = {
    # No pueden aparecer en ciertos sistemas
    "Dragones espaciales": {
        "prohibidos": ["Agujero Negro", "Magnetar", "Pulsar", "Estrella de Neutrones"]
    },
    "Estelaritas": {
        "prohibidos": ["Agujero Negro", "Magnetar", "Pulsar", "Estrella de Neutrones"]
    },
    
    # Solo pueden aparecer en ciertos sistemas
    "Entidades cristalinas": {
        "solo_en": ["Estrella de Neutrones", "Pulsar", "Magnetar"]
    },
    "Calamares fantasma": {
        "solo_en": ["Estrella de Neutrones", "Pulsar", "Magnetar"]
    },
    "Engendros del vacío": {
        "solo_en": ["Tipo G"]
    },
    "Gusanos del vacío": {
        "solo_en": ["Agujero Negro"]
    }
}

# Megaestructuras y sus probabilidades
MEGAESTRUCTURAS = {
    'comunes': {
        'probabilidad': 70,
        'estructuras': [
            "Mundo Anillo", "Asamblea Interestelar", "Megainstalacion de Artes", 
            "Centro de Coordinación Estratégica", "Esfera Dyson", "Gran archivo", 
            "Forja de Arco", "Ecumenópolis"
        ]
    },
    'poco_comunes': {
        'probabilidad': 25,
        'estructuras': [
            "Catapulta Cuántica", "Nexo Científico", "Matriz Centinela", "Megastillero"
        ]
    },
    'muy_raras': {
        'probabilidad': 5,
        'estructuras': [
            "Cerebro Matriohska", "Descompresor de Materia"
        ]
    }
}

# Megaestructuras con restricciones de sistema
MEGAESTRUCTURAS_RESTRICCIONES = {
    'Esfera Dyson': ['Tipo F', 'Tipo G', 'Tipo K', 'Tipo O'],
    'Catapulta Cuántica': ['Estrella de Neutrones', 'Pulsar', 'Magnetar'],
    'Descompresor de Materia': ['Agujero Negro']
}

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

# Configuración de Especies
ESPECIES_PROBABILITY = 10  # 10% chance de especies (muy, muy raro)

# Tipos de especies
TIPOS_ESPECIES = [
    "Maquina", "Mamiferas", "Toxoides", "Necronas", "Reptilianas", 
    "Acuaticas", "Moluscoides", "Aviares", "Litoideas", "Fungicas", 
    "Plantoides", "Antropodas"
]

# Niveles tecnológicos
NIVELES_TECNOLOGICOS = [
    "Edad de Piedra", "Edad de Bronce", "Edad de Hierro", "Renacimiento",
    "Edad del Vapor", "Era Industrial", "Edad de las Máquinas", 
    "Era Atómica", "Era Espacial Inicial"
]

# Rasgos positivos y sus restricciones
RASGOS_POSITIVOS = {
    "Agrarios": [],
    "Ingeniosos": [],
    "Laboriosos": [],
    "Inteligentes": [],
    "Negociantes natos": [],
    "Ingenieros natos": [],
    "Físicos natos": [],
    "Sociólogos natos": [],
    "Muy adaptables": ["Litoideas", "Toxoides", "Maquina", "Necronas"],
    "Adaptables": [],
    "Reproductores rápidos": ["Necronas", "Fungicas", "Maquina", "Antropodas"],
    "Talentosos": [],
    "Aprendizaje rápido": [],
    "Tradicionistas": [],
    "Dóciles": [],
    "Muy fuertes": ["Maquina", "Litoideas"],
    "Fuertes": [],
    "Nómadas": [],
    "Comunales": [],
    "Carismáticos": [],
    "Conformistas": [],
    "Venerables": ["Maquina", "Litoideas"],
    "Duraderos": ["Plantoides", "Fungicas", "Moluscoides", "Acuaticas", "Necronas"],
    "Resilientes": [],
    "Conservacionistas": []
}

# Rasgos negativos y sus restricciones
RASGOS_NEGATIVOS = {
    "Poco adaptables": [],
    "Reproductores lentos": ["Acuaticas", "Litoideas"],
    "Aprendizaje lento": [],
    "Beligerantes": [],
    "Rebeldes": [],
    "Débiles": [],
    "Sedentarios": [],
    "Solitarios": [],
    "Repugnantes": [],
    "Desviados": [],
    "Efímeros": ["Mamiferas", "Reptilianas", "Aviares", "Antropodas"],
    "Decadentes": [],
    "Derrochadores": []
}

# Rasgos que se excluyen mutuamente
RASGOS_EXCLUSIVOS = {
    "Inteligentes": ["Ingenieros natos", "Físicos natos", "Sociólogos natos"],
    "Ingenieros natos": ["Inteligentes"],
    "Físicos natos": ["Inteligentes"],
    "Sociólogos natos": ["Inteligentes"]
}

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
