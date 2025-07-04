import discord
from discord.ext import commands
import logging
from solar_system_generator import SolarSystemGenerator
from database import SystemDatabase

class SolarSystemBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable message content intent for ! commands

        super().__init__(
            command_prefix='!',
            intents=intents,
            description='Bot generador de sistemas solares para roleplay espacial'
        )

        self.generator = SolarSystemGenerator()
        self.database = SystemDatabase()

    async def setup_hook(self):
        """Se ejecuta cuando el bot se está configurando"""
        # Add slash commands directly to tree
        self.tree.add_command(generar_sistema_slash)
        self.tree.add_command(ficha_sistema_slash)
        self.tree.add_command(stats_exploracion_slash)
        self.tree.add_command(ayuda_sistema_slash)

        # Sync commands immediately
        try:
            synced = await self.tree.sync()
            logging.info(f'Comandos sincronizados en setup_hook: {len(synced)}')
        except Exception as e:
            logging.error(f'Error en setup_hook sync: {e}')

    async def on_ready(self):
        """Evento que se ejecuta cuando el bot está listo"""
        logging.info(f'{self.user} se ha conectado a Discord!')
        logging.info(f'Bot está en {len(self.guilds)} servidores')

        # Force sync commands again on ready
        try:
            synced = await self.tree.sync()
            logging.info(f'Comandos sincronizados en on_ready: {len(synced)}')
            for cmd in synced:
                logging.info(f'Comando sincronizado: {cmd.name}')
        except Exception as e:
            logging.error(f'Error al sincronizar comandos en on_ready: {e}')

    async def on_guild_join(self, guild):
        """Evento cuando el bot se une a un servidor"""
        logging.info(f'Bot se unió al servidor: {guild.name} (ID: {guild.id})')

    async def on_guild_remove(self, guild):
        """Evento cuando el bot sale de un servidor"""
        logging.info(f'Bot salió del servidor: {guild.name} (ID: {guild.id})')

# Función para crear embed del sistema
def crear_embed_sistema(sistema, nombre_sistema=None):
    """Crea un embed para mostrar el sistema solar generado"""
    title = f"🌌 Sistema Solar: {nombre_sistema}" if nombre_sistema else "🌌 Sistema Solar Generado"
    embed = discord.Embed(
        title=title,
        color=0x1E88E5,
        description="Sistema generado para roleplay de naciones espaciales"
    )

    # Añadir información del tipo de sistema
    embed.add_field(
        name="📊 Tipo de Sistema",
        value=sistema['tipo_sistema'],
        inline=True
    )

    # Añadir información de las estrellas
    estrellas_texto = "\n".join([f"• {estrella}" for estrella in sistema['estrellas']])
    embed.add_field(
        name="⭐ Estrellas",
        value=estrellas_texto,
        inline=True
    )

    # Añadir habitabilidad
    habitabilidad_emoji = "✅" if sistema['habitabilidad'] == "Habitable" else "❌"
    embed.add_field(
        name="🏠 Habitabilidad",
        value=f"{habitabilidad_emoji} {sistema['habitabilidad']}",
        inline=True
    )

    # Añadir información de cuerpos celestes si aplica
    if sistema['generar_cuerpos']:
        # Mostrar distribución por estrella
        if 'cuerpos_por_estrella' in sistema and sistema['cuerpos_por_estrella']:
            distribuciones = []
            for estrella, cuerpos in sistema['cuerpos_por_estrella'].items():
                if cuerpos['planetas'] > 0 or cuerpos['lunas'] > 0:
                    distribuciones.append(f"**{estrella}**\n🪐 {cuerpos['planetas']} planetas\n🌙 {cuerpos['lunas']} lunas")

            if distribuciones:
                embed.add_field(
                    name="🌌 Distribución de Cuerpos Celestes",
                    value="\n\n".join(distribuciones),
                    inline=False
                )

        # Totales y asteroides
        embed.add_field(
            name="📊 Totales del Sistema",
            value=f"🪐 {sistema.get('total_planetas', 0)} planetas totales\n🌙 {sistema.get('total_lunas', 0)} lunas totales\n🌌 {sistema['asteroides']} cinturones de asteroides",
            inline=True
        )
    else:
        embed.add_field(
            name="⚠️ Cuerpos Celestes",
            value="No se generan debido a condiciones extremas del sistema",
            inline=False
        )

    # Agregar información de depósitos de recursos
    depositos = sistema.get('depositos', {})
    embed.add_field(
        name="💎 Depósitos",
        value=depositos.get('mensaje', 'No hay información disponible'),
        inline=False
    )

    if depositos.get('tiene_depositos'):
        embed.add_field(
            name="🔹 Recurso Estratégico",
            value=depositos.get('recurso', 'Desconocido'),
            inline=True
        )

    # Agregar información de evento especial
    evento = sistema.get('evento_especial', {})
    if evento.get('tiene_evento'):
        embed.add_field(
            name="⚡ Evento Especial en el Sistema",
            value=f"**{evento.get('tipo_evento')}**",
            inline=False
        )
        embed.add_field(
            name="📋 Recordatorio",
            value="Recuerda reclamar tu evento poniendo la ficha del sistema + que tipo de evento tienes en el canal de \"Eventos Pendientes\"",
            inline=False
        )
    else:
        embed.add_field(
            name="⚡ Evento Especial",
            value="No hay eventos especiales en este sistema",
            inline=False
        )

    # Agregar información de planetas habitables
    if sistema['habitabilidad'] == "Habitable":
        planetas_habitables = sistema.get('planetas_habitables', 0)
        embed.add_field(
            name="🌍 Planetas Habitables",
            value=f"**{planetas_habitables}** planetas habitables en el sistema",
            inline=True
        )

        # Agregar tipos de planetas
        tipos_planetas = sistema.get('tipos_planetas', [])
        if tipos_planetas:
            tipos_texto = []
            for i, planeta in enumerate(tipos_planetas, 1):
                tipos_texto.append(f"**Planeta {i}**: {planeta['tipo']} ({planeta['categoria']})")

            embed.add_field(
                name="🪐 Tipo de Planetas",
                value="\n".join(tipos_texto),
                inline=False
            )
    else:
        # Mostrar tipos de planetas inhabitables
        tipos_planetas = sistema.get('tipos_planetas_inhabitables', [])
        if tipos_planetas:
            tipos_texto = []
            for i, planeta in enumerate(tipos_planetas, 1):
                if planeta == "Planeta Gaseoso":
                    # Agregar lunas para planetas gaseosos
                    lunas = sistema.get('lunas_planeta_gaseoso', [])
                    if lunas:
                        luna_texto = "\n".join([f"    {luna}" for luna in lunas])
                        tipos_texto.append(f"**Planeta {i}**: {planeta}\n{luna_texto}")
                    else:
                        tipos_texto.append(f"**Planeta {i}**: {planeta}")
                else:
                    tipos_texto.append(f"**Planeta {i}**: {planeta}")

            embed.add_field(
                name="🪐 Planetas del Sistema",
                value="\n".join(tipos_texto),
                inline=False
            )

    # Agregar información de sondeo
    sondeo = sistema.get('sondeo', {})
    if sondeo.get('sondeo_exitoso'):
        embed.add_field(
            name="🔍 Sondeo",
            value=f"**{sondeo.get('mensaje')}**",
            inline=True
        )
        embed.add_field(
            name="🏗️ Megaestructura Detectada",
            value=f"**{sondeo.get('megaestructura')}**",
            inline=True
        )
    else:
        embed.add_field(
            name="🔍 Sondeo",
            value=sondeo.get('mensaje', 'Sondeo no exitoso'),
            inline=True
        )

    # Agregar información de leviatanes
    leviatanes = sistema.get('leviatanes', {})
    if leviatanes.get('tiene_leviatanes'):
        embed.add_field(
            name="🐉 Leviatanes",
            value=f"**{leviatanes.get('leviatan')}** detectado en el sistema",
            inline=False
        )
    else:
        embed.add_field(
            name="🐉 Leviatanes",
            value="No se detectaron leviatanes en el sistema",
            inline=False
        )

    # Agregar información de especies (muy raro)
    especies = sistema.get('especies', {})
    if especies.get('tiene_especies'):
        embed.add_field(
            name="👽 Especies Detectadas",
            value=f"**Tipo:** {especies.get('tipo_especie')}\n**Nivel Tecnológico:** {especies.get('nivel_tecnologico')}",
            inline=False
        )

        # Rasgos positivos
        rasgos_positivos = especies.get('rasgos_positivos', [])
        if rasgos_positivos:
            embed.add_field(
                name="✅ Rasgos Positivos",
                value="\n".join([f"• {rasgo}" for rasgo in rasgos_positivos]),
                inline=True
            )

        # Rasgos negativos
        rasgos_negativos = especies.get('rasgos_negativos', [])
        if rasgos_negativos:
            embed.add_field(
                name="❌ Rasgos Negativos",
                value="\n".join([f"• {rasgo}" for rasgo in rasgos_negativos]),
                inline=True
            )

    # Añadir footer
    embed.set_footer(
        text="Generado para servidor de roleplay espacial",
        icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
    )

    return embed

# Configurar comandos slash
@discord.app_commands.command(name="generar_sistema", description="Genera un sistema solar aleatorio para roleplay")
@discord.app_commands.describe(nombre="Nombre del sistema (opcional) - se guardará en la base de datos")
async def generar_sistema_slash(interaction: discord.Interaction, nombre: str = None):
    """Comando slash para generar un sistema solar aleatorio"""
    try:
        # Generar el sistema solar
        bot_instance = interaction.client
        if hasattr(bot_instance, 'generator'):
            sistema = bot_instance.generator.generar_sistema_completo()
        else:
            # Fallback: crear un generador temporal
            from solar_system_generator import SolarSystemGenerator
            generator = SolarSystemGenerator()
            sistema = generator.generar_sistema_completo()

        # Si se proporcionó un nombre, guardar en la base de datos
        if nombre:
            if bot_instance.database.system_exists(nombre):
                # Advertir pero permitir duplicados
                embed = crear_embed_sistema(sistema, nombre)
                embed.add_field(
                    name="⚠️ Advertencia",
                    value=f"Ya existe un sistema con el nombre '{nombre}', pero se ha permitido el duplicado.",
                    inline=False
                )
            else:
                embed = crear_embed_sistema(sistema, nombre)
            
            # Guardar en la base de datos
            bot_instance.database.add_system(nombre, interaction.user.id, interaction.user.name, sistema)
            
            embed.add_field(
                name="💾 Sistema Guardado",
                value=f"Sistema '{nombre}' guardado exitosamente. Usa `/ficha_sistema {nombre}` para verlo más tarde.",
                inline=False
            )
        else:
            embed = crear_embed_sistema(sistema)

        await interaction.response.send_message(embed=embed)

        # Log del sistema generado
        guild_name = interaction.guild.name if interaction.guild else "DM"
        nombre_log = f" - {nombre}" if nombre else ""
        logging.info(f"Sistema generado para {interaction.user.name} en {guild_name}: {sistema['tipo_sistema']}{nombre_log}")

    except Exception as e:
        logging.error(f"Error al generar sistema: {e}")
        await interaction.response.send_message(
            "❌ Ocurrió un error al generar el sistema solar. Por favor, inténtalo de nuevo.", 
            ephemeral=True
        )

@discord.app_commands.command(name="ficha_sistema", description="Muestra la ficha detallada de un sistema guardado")
@discord.app_commands.describe(nombre="Nombre del sistema a consultar")
async def ficha_sistema_slash(interaction: discord.Interaction, nombre: str):
    """Comando slash para mostrar la ficha de un sistema guardado"""
    try:
        bot_instance = interaction.client
        
        # Buscar el sistema en la base de datos
        sistema_info = bot_instance.database.get_system(nombre)
        
        if not sistema_info:
            await interaction.response.send_message(
                f"❌ No se encontró el sistema '{nombre}' en la base de datos.",
                ephemeral=True
            )
            return
        
        # Crear embed con la información del sistema
        sistema_data = sistema_info['system_data']
        embed = crear_embed_sistema(sistema_data, sistema_info['original_name'])
        
        # Añadir información de exploración
        embed.add_field(
            name="🧭 Información de Exploración",
            value=f"**Explorador:** {sistema_info['explorer_name']}\n**Fecha:** {sistema_info['timestamp'][:10]}\n**Hora:** {sistema_info['timestamp'][11:19]}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log
        guild_name = interaction.guild.name if interaction.guild else "DM"
        logging.info(f"Ficha de sistema '{nombre}' consultada por {interaction.user.name} en {guild_name}")
        
    except Exception as e:
        logging.error(f"Error al consultar ficha de sistema: {e}")
        await interaction.response.send_message(
            "❌ Ocurrió un error al consultar la ficha del sistema.", 
            ephemeral=True
        )

@discord.app_commands.command(name="stats_exploracion", description="Muestra estadísticas del servidor y ranking de exploradores")
async def stats_exploracion_slash(interaction: discord.Interaction):
    """Comando slash para mostrar estadísticas de exploración"""
    try:
        bot_instance = interaction.client
        
        # Obtener estadísticas
        total_systems = bot_instance.database.get_total_systems()
        top_explorers = bot_instance.database.get_top_explorers(5)
        
        embed = discord.Embed(
            title="📊 Estadísticas de Exploración",
            color=0x4CAF50,
            description="Estadísticas de sistemas explorados en este servidor"
        )
        
        embed.add_field(
            name="🌌 Total de Sistemas Explorados",
            value=f"**{total_systems}** sistemas han sido explorados y guardados",
            inline=False
        )
        
        if top_explorers:
            explorer_text = ""
            for i, (user_id, data) in enumerate(top_explorers, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                explorer_text += f"{medal} **{data['name']}** - {data['systems_explored']} sistemas\n"
            
            embed.add_field(
                name="🏆 Top Exploradores",
                value=explorer_text,
                inline=False
            )
        else:
            embed.add_field(
                name="🏆 Top Exploradores",
                value="No hay datos de exploradores aún",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
        
        # Log
        guild_name = interaction.guild.name if interaction.guild else "DM"
        logging.info(f"Estadísticas consultadas por {interaction.user.name} en {guild_name}")
        
    except Exception as e:
        logging.error(f"Error al consultar estadísticas: {e}")
        await interaction.response.send_message(
            "❌ Ocurrió un error al consultar las estadísticas.", 
            ephemeral=True
        )

@discord.app_commands.command(name="ayuda_sistema", description="Muestra información sobre los tipos de sistemas y estrellas")
async def ayuda_sistema_slash(interaction: discord.Interaction):
    """Comando slash de ayuda que explica los tipos de sistemas y estrellas"""
    embed = discord.Embed(
        title="📚 Guía de Sistemas Solares",
        color=0x4CAF50,
        description="Información sobre la generación de sistemas solares"
    )

    embed.add_field(
        name="🌟 Tipos de Sistema",
        value="• **Unario** (50%): Un solo sol\n• **Binario** (25%): Dos soles\n• **Trinario** (25%): Tres soles",
        inline=False
    )

    embed.add_field(
        name="⭐ Tipos de Estrellas",
        value="• **Más Comunes**: Estrella Clase M, Tipo K, G, F\n• **Menos Comunes**: Tipo A, Tipo T\n• **Raras**: Gigante Roja, Pulsar, Agujero Negro\n• **Muy Raras**: Magnetar, Estrella Extraña, Tipo O",
        inline=False
    )

    embed.add_field(
        name="🏠 Habitabilidad",
        value="• **Habitable**: Sistemas con estrellas Tipo K, G, F o A\n• **Inhabitable**: Sistemas con Gigante Roja, Pulsar, Agujero Negro, Estrella Extraña, Magnetar o Tipo O",
        inline=False
    )

    embed.add_field(
        name="🪐 Cuerpos Celestes",
        value="• **Planetas**: 1-16 por sistema\n• **Lunas**: 1-27 por sistema\n• **Asteroides**: 0-3 cinturones\n• *No se generan en sistemas con Agujero Negro o Estrella Extraña*",
        inline=False
    )

    embed.add_field(
        name="📝 Comandos Disponibles",
        value="• `/generar_sistema [nombre]` - Genera un sistema completo\n• `/ficha_sistema <nombre>` - Muestra ficha detallada\n• `/stats_exploracion` - Estadísticas del servidor\n• `/ayuda_sistema` - Muestra esta ayuda",
        inline=False
    )

    embed.add_field(
        name="🗃️ Base de Datos",
        value="Los sistemas con nombre se guardan automáticamente y pueden consultarse más tarde. Se lleva registro de quién exploró cada sistema y cuándo.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

# Comandos tradicionales con !
@commands.command(name='generar', aliases=['sistema', 'solar'])
async def generar_comando(ctx):
    """Comando tradicional para generar un sistema solar aleatorio"""
    try:
        # Generar el sistema solar
        sistema = ctx.bot.generator.generar_sistema_completo()
        embed = crear_embed_sistema(sistema)

        await ctx.send(embed=embed)

        # Log del sistema generado
        guild_name = ctx.guild.name if ctx.guild else "DM"
        logging.info(f"Sistema generado para {ctx.author.name} en {guild_name}: {sistema['tipo_sistema']}")

    except Exception as e:
        logging.error(f"Error al generar sistema: {e}")
        await ctx.send("❌ Ocurrió un error al generar el sistema solar. Por favor, inténtalo de nuevo.")



@commands.command(name='ayuda', aliases=['info'])
async def ayuda_comando(ctx):
    """Comando tradicional de ayuda que explica los tipos de sistemas y estrellas"""
    embed = discord.Embed(
        title="📚 Guía de Sistemas Solares",
        color=0x4CAF50,
        description="Información sobre la generación de sistemas solares"
    )

    embed.add_field(
        name="🌟 Tipos de Sistema",
        value="• **Unario** (50%): Un solo sol\n• **Binario** (25%): Dos soles\n• **Trinario** (25%): Tres soles",
        inline=False
    )

    embed.add_field(
        name="⭐ Tipos de Estrellas",
        value="• **Más Comunes**: Estrella Clase M, Tipo K, G, F\n• **Menos Comunes**: Tipo A, Tipo T\n• **Raras**: Gigante Roja, Pulsar, Agujero Negro\n• **Muy Raras**: Magnetar, Estrella Extraña, Tipo O",
        inline=False
    )

    embed.add_field(
        name="🏠 Habitabilidad",
        value="• **Habitable**: Sistemas con estrellas Tipo K, G, F o A\n• **Inhabitable**: Sistemas con Gigante Roja, Pulsar, Agujero Negro, Estrella Extraña, Magnetar o Tipo O",
        inline=False
    )

    embed.add_field(
        name="🪐 Cuerpos Celestes",
        value="• **Planetas**: 1-16 por sistema\n• **Lunas**: 1-27 por sistema\n• **Asteroides**: 0-3 cinturones\n• *No se generan en sistemas con Agujero Negro o Estrella Extraña*",
        inline=False
    )

    embed.add_field(
        name="📝 Comandos Disponibles",
        value="• `/generar_sistema [nombre]` - Genera un sistema completo\n• `/ficha_sistema <nombre>` - Muestra ficha detallada\n• `/stats_exploracion` - Estadísticas del servidor\n• `/ayuda_sistema` - Muestra esta ayuda",
        inline=False
    )

    embed.add_field(
        name="🗃️ Base de Datos",
        value="Los sistemas con nombre se guardan automáticamente y pueden consultarse más tarde. Se lleva registro de quién exploró cada sistema y cuándo.",
        inline=False
    )

    await ctx.send(embed=embed)

# This function is no longer needed - commands are registered in setup_hook