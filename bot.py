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
        self.tree.add_command(generar_ficha_slash)
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
async def generar_comando(ctx, *, nombre: str = None):
    """Comando tradicional para generar un sistema solar aleatorio"""
    try:
        # Generar el sistema solar
        sistema = ctx.bot.generator.generar_sistema_completo()
        
        # Si se proporcionó un nombre, guardar en la base de datos
        if nombre:
            if ctx.bot.database.system_exists(nombre):
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
            ctx.bot.database.add_system(nombre, ctx.author.id, ctx.author.name, sistema)
            
            embed.add_field(
                name="💾 Sistema Guardado",
                value=f"Sistema '{nombre}' guardado exitosamente. Usa `!ficha {nombre}` o `/ficha_sistema {nombre}` para verlo más tarde.",
                inline=False
            )
        else:
            embed = crear_embed_sistema(sistema)

        await ctx.send(embed=embed)

        # Log del sistema generado
        guild_name = ctx.guild.name if ctx.guild else "DM"
        nombre_log = f" - {nombre}" if nombre else ""
        logging.info(f"Sistema generado para {ctx.author.name} en {guild_name}: {sistema['tipo_sistema']}{nombre_log}")

    except Exception as e:
        logging.error(f"Error al generar sistema: {e}")
        await ctx.send("❌ Ocurrió un error al generar el sistema solar. Por favor, inténtalo de nuevo.")

@commands.command(name='ficha')
async def ficha_comando(ctx, *, nombre: str):
    """Comando tradicional para mostrar la ficha de un sistema guardado"""
    try:
        # Buscar el sistema en la base de datos
        sistema_info = ctx.bot.database.get_system(nombre)
        
        if not sistema_info:
            await ctx.send(f"❌ No se encontró el sistema '{nombre}' en la base de datos.")
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
        
        await ctx.send(embed=embed)
        
        # Log
        guild_name = ctx.guild.name if ctx.guild else "DM"
        logging.info(f"Ficha de sistema '{nombre}' consultada por {ctx.author.name} en {guild_name}")
        
    except Exception as e:
        logging.error(f"Error al consultar ficha de sistema: {e}")
        await ctx.send("❌ Ocurrió un error al consultar la ficha del sistema.")

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
        value="• `!generar [nombre]` / `/generar_sistema [nombre]` - Genera un sistema completo\n• `!ficha <nombre>` / `/ficha_sistema <nombre>` - Muestra ficha detallada\n• `/generar_ficha <nombre>` - Genera ficha con nombres detallados\n• `/stats_exploracion` - Estadísticas del servidor\n• `!ayuda` / `/ayuda_sistema` - Muestra esta ayuda",
        inline=False
    )

    embed.add_field(
        name="🗃️ Base de Datos",
        value="Los sistemas con nombre se guardan automáticamente y pueden consultarse más tarde. Se lleva registro de quién exploró cada sistema y cuándo.",
        inline=False
    )

    await ctx.send(embed=embed)

def crear_embed_ficha_detallada(sistema, nombre_sistema):
    """Crea un embed detallado con nombres específicos para cuerpos celestes"""
    from datetime import datetime, timezone, timedelta
    
    # GMT-6 timezone
    gmt_minus_6 = timezone(timedelta(hours=-6))
    fecha_hora = datetime.now(gmt_minus_6).strftime("%Y-%m-%d %H:%M:%S GMT-6")
    
    embed = discord.Embed(
        title=f"📋 Ficha Detallada del Sistema: {nombre_sistema}",
        color=0x2E7D32,
        description=f"Ficha completa generada el {fecha_hora}"
    )

    # Información básica del sistema
    embed.add_field(
        name="📊 Información del Sistema",
        value=f"**Tipo:** {sistema['tipo_sistema']}\n**Habitabilidad:** {sistema['habitabilidad']}",
        inline=True
    )

    # Estrellas con nombres
    estrellas_texto = ""
    for i, estrella in enumerate(sistema['estrellas']):
        if len(sistema['estrellas']) == 1:
            estrellas_texto += f"⭐ **{nombre_sistema}** ({estrella})\n"
        else:
            letra = chr(65 + i)  # A, B, C
            estrellas_texto += f"⭐ **{nombre_sistema} {letra}** ({estrella})\n"

    embed.add_field(
        name="🌟 Estrellas del Sistema",
        value=estrellas_texto,
        inline=True
    )

    # Generar nombres detallados de planetas y lunas
    if sistema['generar_cuerpos'] and sistema.get('total_planetas', 0) > 0:
        planetas_detalle = generar_nombres_planetas_lunas(nombre_sistema, sistema)
        
        if planetas_detalle:
            embed.add_field(
                name="🪐 Planetas y Lunas del Sistema",
                value=planetas_detalle,
                inline=False
            )
    else:
        embed.add_field(
            name="🪐 Cuerpos Celestes",
            value="⚠️ No se generan cuerpos celestes debido a condiciones extremas del sistema",
            inline=False
        )

    # Cinturones de asteroides
    if sistema.get('asteroides', 0) > 0:
        asteroides_texto = ""
        for i in range(sistema['asteroides']):
            asteroides_texto += f"🌌 **Cinturón de Asteroides {nombre_sistema}-{i+1}**\n"
        
        embed.add_field(
            name="☄️ Cinturones de Asteroides",
            value=asteroides_texto,
            inline=True
        )

    # Recursos estratégicos
    depositos = sistema.get('depositos', {})
    if depositos.get('tiene_depositos'):
        embed.add_field(
            name="💎 Recursos Estratégicos",
            value=f"**{depositos.get('recurso')}** detectado en el sistema",
            inline=True
        )

    # Eventos especiales
    evento = sistema.get('evento_especial', {})
    if evento.get('tiene_evento'):
        embed.add_field(
            name="⚡ Evento Especial",
            value=f"**{evento.get('tipo_evento')}** detectado",
            inline=True
        )

    # Megaestructuras
    sondeo = sistema.get('sondeo', {})
    if sondeo.get('sondeo_exitoso'):
        embed.add_field(
            name="🏗️ Megaestructura",
            value=f"**{sondeo.get('megaestructura')}** detectada mediante sondeo",
            inline=True
        )

    # Leviatanes
    leviatanes = sistema.get('leviatanes', {})
    if leviatanes.get('tiene_leviatanes'):
        embed.add_field(
            name="🐉 Leviatan",
            value=f"**{leviatanes.get('leviatan')}** detectado en el sistema",
            inline=True
        )

    # Especies
    especies = sistema.get('especies', {})
    if especies.get('tiene_especies'):
        rasgos_pos = especies.get('rasgos_positivos', [])
        rasgos_neg = especies.get('rasgos_negativos', [])
        
        especies_info = f"**Tipo:** {especies.get('tipo_especie')}\n"
        especies_info += f"**Nivel Tecnológico:** {especies.get('nivel_tecnologico')}\n"
        
        if rasgos_pos:
            especies_info += f"**Rasgos Positivos:** {', '.join(rasgos_pos)}\n"
        if rasgos_neg:
            especies_info += f"**Rasgos Negativos:** {', '.join(rasgos_neg)}"
        
        embed.add_field(
            name="👽 Especies Inteligentes",
            value=especies_info,
            inline=False
        )

    embed.set_footer(
        text=f"Ficha detallada generada para {nombre_sistema}",
        icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
    )

    return embed

def generar_nombres_planetas_lunas(nombre_sistema, sistema):
    """Genera nombres detallados para planetas y lunas usando números romanos"""
    def numero_a_romano(num):
        valores = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]
        resultado = ''
        for valor, letra in valores:
            count = num // valor
            resultado += letra * count
            num -= valor * count
        return resultado

    total_planetas = sistema.get('total_planetas', 0)
    if total_planetas == 0:
        return "No hay planetas en este sistema"

    resultado = ""
    
    # Distribuir lunas entre planetas de manera realista
    total_lunas = sistema.get('total_lunas', 0)
    lunas_por_planeta = []
    
    if total_lunas > 0:
        # Distribuir lunas aleatoriamente entre planetas
        import random
        lunas_restantes = total_lunas
        for i in range(total_planetas):
            if i == total_planetas - 1:  # Último planeta obtiene lunas restantes
                lunas_por_planeta.append(lunas_restantes)
            else:
                max_lunas = min(lunas_restantes, random.randint(0, 4))
                lunas_por_planeta.append(max_lunas)
                lunas_restantes -= max_lunas
    else:
        lunas_por_planeta = [0] * total_planetas

    # Generar información de planetas
    for i in range(min(total_planetas, 10)):  # Máximo 10 planetas mostrados
        romano = numero_a_romano(i + 1)
        nombre_planeta = f"**{nombre_sistema} {romano}**"
        
        # Determinar tipo de planeta
        tipo_planeta = "Planeta"
        if sistema['habitabilidad'] == "Habitable":
            tipos_planetas = sistema.get('tipos_planetas', [])
            if i < len(tipos_planetas):
                tipo_planeta = tipos_planetas[i]['tipo']
        else:
            tipos_inhabitables = sistema.get('tipos_planetas_inhabitables', [])
            if i < len(tipos_inhabitables):
                tipo_planeta = tipos_inhabitables[i]

        resultado += f"🪐 {nombre_planeta} ({tipo_planeta})\n"
        
        # Añadir lunas si las tiene
        num_lunas = lunas_por_planeta[i] if i < len(lunas_por_planeta) else 0
        if num_lunas > 0:
            for j in range(num_lunas):
                letra_luna = chr(97 + j)  # a, b, c, d...
                resultado += f"   🌙 {nombre_sistema} {romano}{letra_luna}\n"
        else:
            resultado += f"   No tiene lunas\n"
        
        resultado += "\n"

    if total_planetas > 10:
        resultado += f"... y {total_planetas - 10} planetas adicionales\n"

    return resultado

@discord.app_commands.command(name="generar_ficha", description="Genera una ficha detallada con nombres específicos para un sistema guardado")
@discord.app_commands.describe(nombre="Nombre del sistema para generar la ficha detallada")
async def generar_ficha_slash(interaction: discord.Interaction, nombre: str):
    """Comando slash para generar ficha detallada con nombres específicos"""
    try:
        bot_instance = interaction.client
        
        # Buscar el sistema en la base de datos
        sistema_info = bot_instance.database.get_system(nombre)
        
        if not sistema_info:
            await interaction.response.send_message(
                f"❌ No se encontró el sistema '{nombre}' en la base de datos. Primero genera un sistema con ese nombre usando `/generar_sistema {nombre}`",
                ephemeral=True
            )
            return
        
        # Crear embed detallado
        sistema_data = sistema_info['system_data']
        embed = crear_embed_ficha_detallada(sistema_data, sistema_info['original_name'])
        
        # Añadir información del explorador
        embed.add_field(
            name="🧭 Información de Exploración",
            value=f"**Explorador Original:** {sistema_info['explorer_name']}\n**Fecha de Descubrimiento:** {sistema_info['timestamp'][:10]}\n**Hora:** {sistema_info['timestamp'][11:19]}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log
        guild_name = interaction.guild.name if interaction.guild else "DM"
        logging.info(f"Ficha detallada de sistema '{nombre}' generada por {interaction.user.name} en {guild_name}")
        
    except Exception as e:
        logging.error(f"Error al generar ficha detallada: {e}")
        await interaction.response.send_message(
            "❌ Ocurrió un error al generar la ficha detallada del sistema.", 
            ephemeral=True
        )

# This function is no longer needed - commands are registered in setup_hook