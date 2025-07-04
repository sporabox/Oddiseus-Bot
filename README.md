
# Discord Solar System Generator Bot

Bot generador de sistemas solares para servidores de roleplay de naciones espaciales. Genera sistemas completos con estrellas, planetas, recursos, eventos especiales, leviatanes, especies y más.

## Características

- **Generación de Sistemas Solares**: Sistemas unarios, binarios y trinarios con diferentes tipos de estrellas
- **Base de Datos**: Registro automático de sistemas explorados con nombre, explorador y fecha
- **Estadísticas**: Contador de sistemas explorados por servidor y ranking de exploradores
- **Fichas de Sistema**: Visualización detallada de sistemas guardados
- **Eventos Especiales**: Yacimientos arqueológicos y anomalías
- **Recursos Estratégicos**: Diversos materiales raros y estratégicos
- **Leviatanes**: Criaturas espaciales con restricciones según el tipo de sistema
- **Especies**: Generación de especies inteligentes con rasgos únicos
- **Megaestructuras**: Detectables mediante sondeo exitoso

## Archivos del Proyecto

- `main.py` - Archivo principal para ejecutar el bot
- `bot.py` - Lógica del bot de Discord y comandos
- `solar_system_generator.py` - Generador de sistemas solares
- `config.py` - Configuración de probabilidades y constantes
- `database.py` - Manejo de base de datos SQLite para sistemas explorados
- `railway_requirements.txt` - Dependencias para Railway
- `Procfile` - Comando de inicio para Railway
- `railway.json` - Configuración de Railway

## Comandos del Bot

### Comandos Slash
- `/generar_sistema [nombre]` - Genera un sistema solar aleatorio (opcional: con nombre para guardar)
- `/ficha_sistema <nombre>` - Muestra la ficha detallada de un sistema guardado
- `/stats_exploracion` - Muestra estadísticas del servidor y ranking de exploradores
- `/ayuda_sistema` - Muestra información de ayuda completa

### Comandos Tradicionales
- `!generar` (o `!sistema`, `!solar`) - Genera un sistema solar aleatorio
- `!ayuda` (o `!info`) - Muestra información de ayuda

## Tipos de Estrellas

### Comunes
- **Estrella Clase M**: Enana roja, la más común
- **Tipo K, G, F**: Estrellas habitables
- **Tipo A**: Estrella habitable pero menos común

### Raras
- **Tipo T**: Enana marrón
- **Gigante Roja**: Estrella en expansión
- **Pulsar**: Estrella de neutrones en rotación
- **Estrella de Neutrones**: Remanente estelar ultra-denso

### Muy Raras
- **Agujero Negro**: Gravedad extrema
- **Magnetar**: Campo magnético extremo
- **Estrella Extraña**: Materia exótica hipotética
- **Tipo O**: Estrella azul masiva

## Recursos Estratégicos

- **Comunes**: Gases Exóticos, Cristales Raros, Polvo Zro
- **Poco Comunes**: Motas Volátiles
- **Raros**: Metal Vivo
- **Muy Raros**: Nanitos
- **Únicos**: Materia Oscura (solo en sistemas con Agujero Negro)

## Leviatanes

Criaturas espaciales que aparecen según el tipo de sistema:
- **Universales**: Nubes de Vacío, Amebas espaciales, Tiyankis, etc.
- **Restringidos**: Algunos solo aparecen en ciertos tipos de sistemas
- **Prohibidos**: Algunos no pueden aparecer en sistemas peligrosos

## Base de Datos

El bot mantiene un registro automático de:
- Sistemas explorados con nombre
- Usuario que exploró cada sistema
- Fecha y hora de exploración
- Estadísticas por servidor
- Ranking de exploradores más activos

## Variables de Entorno Requeridas

- `DISCORD_BOT_TOKEN` - Token del bot de Discord

## Despliegue en Replit

1. Configura la variable de entorno `DISCORD_BOT_TOKEN` en los Secrets de Replit
2. El bot se ejecutará automáticamente con el botón Run
3. La base de datos SQLite se crea automáticamente al iniciar

## Características Especiales

- **Habitabilidad**: Determinada por tipos de estrellas presentes
- **Cuerpos Celestes**: Planetas, lunas y asteroides distribuidos por estrella
- **Eventos Especiales**: 15% de probabilidad de yacimientos o anomalías
- **Sondeo**: 5% de probabilidad de detectar megaestructuras
- **Especies**: 10% de probabilidad en sistemas habitables
- **Advertencias**: El bot advierte si un nombre de sistema ya existe pero permite duplicados

## Probabilidades

- **Sistemas**: 50% Unario, 25% Binario, 25% Trinario
- **Recursos**: 15% de probabilidad de depósitos estratégicos
- **Leviatanes**: 20% de probabilidad de aparición
- **Especies**: 10% solo en sistemas habitables
- **Eventos**: 15% de probabilidad de eventos especiales
