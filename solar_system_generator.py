import random
import secrets
from config import (STAR_PROBABILITIES, SYSTEM_PROBABILITIES, HABITABLE_STARS, DANGEROUS_STARS, 
                   NO_BODIES_STARS, DEPOSITOS_PROBABILITY, RECURSOS_ESTRATEGICOS, 
                   RECURSOS_AGUJERO_NEGRO, EVENTO_ESPECIAL_PROBABILITY, EVENTOS_ESPECIALES,
                   PLANETAS_HABITABLES_RANGE, TIPOS_PLANETAS, SONDEO_PROBABILITY,
                   MEGAESTRUCTURAS, MEGAESTRUCTURAS_RESTRICCIONES)

class SolarSystemGenerator:
    def __init__(self):
        """Inicializa el generador de sistemas solares"""
        self.system_types = ['Unario', 'Binario', 'Trinario']
        self.system_probabilities = SYSTEM_PROBABILITIES
        self.star_probabilities = STAR_PROBABILITIES
        self.habitable_stars = HABITABLE_STARS
        self.dangerous_stars = DANGEROUS_STARS
        self.no_bodies_stars = NO_BODIES_STARS
    
    def _weighted_choice(self, choices, weights):
        """Selección aleatoria basada en pesos/probabilidades"""
        # Usar secrets para mayor seguridad en la aleatoriedad
        total = sum(weights)
        r = secrets.randbelow(total)
        upto = 0
        for choice, weight in zip(choices, weights):
            if upto + weight >= r:
                return choice
            upto += weight
        return choices[-1]  # Fallback
    
    def generar_tipo_sistema(self):
        """Genera el tipo de sistema solar (Unario, Binario, Trinario)"""
        return self._weighted_choice(
            self.system_types, 
            self.system_probabilities
        )
    
    def generar_estrella(self):
        """Genera una estrella individual con probabilidades específicas"""
        estrellas = list(self.star_probabilities.keys())
        probabilidades = list(self.star_probabilities.values())
        
        return self._weighted_choice(estrellas, probabilidades)
    
    def generar_estrellas_sistema(self, tipo_sistema):
        """Genera las estrellas para un sistema según su tipo"""
        num_estrellas = {
            'Unario': 1,
            'Binario': 2,
            'Trinario': 3
        }
        
        estrellas = []
        for _ in range(num_estrellas[tipo_sistema]):
            estrellas.append(self.generar_estrella())
        
        return estrellas
    
    def determinar_habitabilidad(self, estrellas):
        """Determina si el sistema es habitable o inhabitable"""
        # Verificar si hay estrellas peligrosas
        for estrella in estrellas:
            if estrella in self.dangerous_stars:
                return "Inhabitable"
        
        # Verificar si hay estrellas habitables
        for estrella in estrellas:
            if estrella in self.habitable_stars:
                return "Habitable"
        
        # Si no hay estrellas habitables ni peligrosas, es inhabitable
        return "Inhabitable"
    
    def puede_generar_cuerpos(self, estrellas):
        """Determina si se pueden generar planetas, lunas y asteroides"""
        for estrella in estrellas:
            if estrella in self.no_bodies_stars:
                return False
        return True
    
    def generar_cuerpos_celestes(self, estrellas):
        """Genera planetas, lunas y cinturones de asteroides organizados por estrella"""
        total_planetas = random.randint(1, 16)
        total_lunas = random.randint(1, 27)
        asteroides = random.randint(0, 3)
        
        # Distribuir planetas entre las estrellas
        cuerpos_por_estrella = {}
        num_estrellas = len(estrellas)
        
        for i, estrella in enumerate(estrellas):
            # Calcular cuántos planetas y lunas para esta estrella
            if i == len(estrellas) - 1:  # Última estrella obtiene los restantes
                planetas_estrella = total_planetas
                lunas_estrella = total_lunas
            else:
                # Distribuir proporcionalmente
                planetas_estrella = random.randint(0, max(1, total_planetas // num_estrellas + 2))
                lunas_estrella = random.randint(0, max(1, total_lunas // num_estrellas + 5))
                total_planetas -= planetas_estrella
                total_lunas -= lunas_estrella
            
            cuerpos_por_estrella[estrella] = {
                'planetas': max(0, planetas_estrella),
                'lunas': max(0, lunas_estrella)
            }
        
        return {
            'cuerpos_por_estrella': cuerpos_por_estrella,
            'asteroides': asteroides,
            'total_planetas': sum(data['planetas'] for data in cuerpos_por_estrella.values()),
            'total_lunas': sum(data['lunas'] for data in cuerpos_por_estrella.values())
        }
    
    def generar_sistema_completo(self):
        """Genera un sistema solar completo con todas sus características"""
        # Generar tipo de sistema
        tipo_sistema = self.generar_tipo_sistema()
        
        # Generar estrellas
        estrellas = self.generar_estrellas_sistema(tipo_sistema)
        
        # Determinar habitabilidad
        habitabilidad = self.determinar_habitabilidad(estrellas)
        
        # Verificar si se pueden generar cuerpos celestes
        generar_cuerpos = self.puede_generar_cuerpos(estrellas)
        
        # Crear el resultado base
        resultado = {
            'tipo_sistema': tipo_sistema,
            'estrellas': estrellas,
            'habitabilidad': habitabilidad,
            'generar_cuerpos': generar_cuerpos
        }
        
        # Generar cuerpos celestes si es posible
        if generar_cuerpos:
            cuerpos = self.generar_cuerpos_celestes(estrellas)
            resultado.update(cuerpos)
        else:
            resultado.update({
                'cuerpos_por_estrella': {},
                'asteroides': 0,
                'total_planetas': 0,
                'total_lunas': 0
            })
        
        # Generar eventos y recursos
        depositos = self.generar_depositos_recursos(estrellas)
        evento = self.generar_evento_especial()
        planetas_habitables = self.generar_planetas_habitables(habitabilidad)
        tipos_planetas = self.generar_tipos_planetas(planetas_habitables)
        sondeo = self.generar_sondeo(estrellas)
        
        resultado.update({
            'depositos': depositos,
            'evento_especial': evento,
            'planetas_habitables': planetas_habitables,
            'tipos_planetas': tipos_planetas,
            'sondeo': sondeo
        })
        
        return resultado
    
    def generar_sistemas_multiples(self, cantidad):
        """Genera múltiples sistemas solares"""
        sistemas = []
        for _ in range(cantidad):
            sistemas.append(self.generar_sistema_completo())
        return sistemas
    
    def obtener_estadisticas_estrella(self, estrella):
        """Obtiene información adicional sobre una estrella específica"""
        info_estrellas = {
            'Estrella Clase M': {
                'descripcion': 'Enana roja, la más común en la galaxia',
                'temperatura': 'Baja (2300-3800K)',
                'longevidad': 'Muy alta (billones de años)'
            },
            'Tipo K': {
                'descripcion': 'Enana naranja, ideal para la vida',
                'temperatura': 'Moderada (3700-5200K)',
                'longevidad': 'Alta (15-45 mil millones años)'
            },
            'Tipo G': {
                'descripcion': 'Como nuestro Sol',
                'temperatura': 'Media (5200-6000K)',
                'longevidad': 'Media (10 mil millones años)'
            },
            'Tipo F': {
                'descripcion': 'Estrella blanco-amarilla',
                'temperatura': 'Alta (6000-7500K)',
                'longevidad': 'Baja (2-7 mil millones años)'
            },
            'Tipo A': {
                'descripcion': 'Estrella blanca y caliente',
                'temperatura': 'Muy alta (7500-10000K)',
                'longevidad': 'Muy baja (1-3 mil millones años)'
            },
            'Tipo T': {
                'descripcion': 'Enana marrón fría',
                'temperatura': 'Muy baja (<1300K)',
                'longevidad': 'Extremadamente alta'
            },
            'Gigante Roja': {
                'descripcion': 'Estrella en fase final, expandida',
                'temperatura': 'Variable',
                'longevidad': 'Fase terminal'
            },
            'Pulsar': {
                'descripcion': 'Estrella de neutrones en rotación',
                'temperatura': 'Extrema',
                'longevidad': 'Millones de años'
            },
            'Agujero Negro': {
                'descripcion': 'Objeto con gravedad extrema',
                'temperatura': 'N/A',
                'longevidad': 'Prácticamente eterna'
            },
            'Magnetar': {
                'descripcion': 'Estrella de neutrones con campo magnético extremo',
                'temperatura': 'Extrema',
                'longevidad': 'Miles de años activo'
            },
            'Estrella Extraña': {
                'descripcion': 'Objeto hipotético de materia extraña',
                'temperatura': 'Desconocida',
                'longevidad': 'Desconocida'
            },
            'Tipo O': {
                'descripcion': 'Estrella azul, la más masiva y caliente',
                'temperatura': 'Extrema (>30000K)',
                'longevidad': 'Muy corta (1-10 millones años)'
            }
        }
        
        return info_estrellas.get(estrella, {
            'descripcion': 'Información no disponible',
            'temperatura': 'Desconocida',
            'longevidad': 'Desconocida'
        })
    
    def generar_depositos_recursos(self, estrellas):
        """Genera depósitos de recursos estratégicos"""
        # Verificar si hay chance de depósitos
        if random.randint(1, 100) > DEPOSITOS_PROBABILITY:
            return {
                'tiene_depositos': False,
                'recurso': None,
                'mensaje': "No hay ningún depósito de recursos estratégicos en el sistema"
            }
        
        # Verificar si hay agujero negro para materia oscura
        if 'Agujero Negro' in estrellas:
            return {
                'tiene_depositos': True,
                'recurso': 'Materia Oscura',
                'mensaje': "Recursos estratégicos presentes en el sistema"
            }
        
        # Seleccionar recurso normal
        recursos = list(RECURSOS_ESTRATEGICOS.keys())
        probabilidades = list(RECURSOS_ESTRATEGICOS.values())
        recurso = self._weighted_choice(recursos, probabilidades)
        
        return {
            'tiene_depositos': True,
            'recurso': recurso,
            'mensaje': "Recursos estratégicos presentes en el sistema"
        }
    
    def generar_evento_especial(self):
        """Genera evento especial en el sistema"""
        # 30% chance de evento especial
        if random.randint(1, 100) > EVENTO_ESPECIAL_PROBABILITY:
            return {
                'tiene_evento': False,
                'tipo_evento': None
            }
        
        # Seleccionar tipo de evento (50% cada uno)
        evento = random.choice(EVENTOS_ESPECIALES)
        
        return {
            'tiene_evento': True,
            'tipo_evento': evento
        }
    
    def generar_planetas_habitables(self, habitabilidad):
        """Genera número de planetas habitables si el sistema es habitable"""
        if habitabilidad != "Habitable":
            return 0
        
        return random.randint(*PLANETAS_HABITABLES_RANGE)
    
    def generar_tipos_planetas(self, num_planetas_habitables):
        """Genera los tipos de planetas habitables"""
        if num_planetas_habitables == 0:
            return []
        
        tipos_planetas = []
        
        # Obtener categorías y sus probabilidades
        categorias = list(TIPOS_PLANETAS.keys())
        probabilidades = [TIPOS_PLANETAS[cat]['probabilidad'] for cat in categorias]
        
        for _ in range(num_planetas_habitables):
            # Seleccionar categoría
            categoria = self._weighted_choice(categorias, probabilidades)
            
            # Seleccionar planeta específico de la categoría
            planetas_categoria = TIPOS_PLANETAS[categoria]['planetas']
            planeta = random.choice(planetas_categoria)
            
            tipos_planetas.append({
                'categoria': categoria,
                'tipo': planeta
            })
        
        return tipos_planetas
    
    def generar_sondeo(self, estrellas):
        """Genera resultado de sondeo con posible megaestructura"""
        # Muy, muy baja probabilidad de sondeo exitoso
        if random.randint(1, 100) > SONDEO_PROBABILITY:
            return {
                'sondeo_exitoso': False,
                'megaestructura': None,
                'mensaje': "Sondeo no exitoso"
            }
        
        # Sondeo exitoso - generar megaestructura
        megaestructura = self.generar_megaestructura(estrellas)
        
        return {
            'sondeo_exitoso': True,
            'megaestructura': megaestructura,
            'mensaje': "Sondeo exitoso"
        }
    
    def generar_megaestructura(self, estrellas):
        """Genera una megaestructura según las restricciones del sistema"""
        # Obtener todas las megaestructuras disponibles
        megaestructuras_disponibles = []
        probabilidades = []
        
        for categoria, datos in MEGAESTRUCTURAS.items():
            for estructura in datos['estructuras']:
                # Verificar restricciones
                if estructura in MEGAESTRUCTURAS_RESTRICCIONES:
                    tipos_permitidos = MEGAESTRUCTURAS_RESTRICCIONES[estructura]
                    if not any(estrella in tipos_permitidos for estrella in estrellas):
                        continue  # Saltar esta megaestructura
                
                megaestructuras_disponibles.append(estructura)
                probabilidades.append(datos['probabilidad'])
        
        # Si no hay megaestructuras disponibles, seleccionar una común genérica
        if not megaestructuras_disponibles:
            estructuras_comunes = [e for e in MEGAESTRUCTURAS['comunes']['estructuras'] 
                                 if e not in MEGAESTRUCTURAS_RESTRICCIONES]
            return random.choice(estructuras_comunes)
        
        # Seleccionar megaestructura con probabilidades ponderadas
        return self._weighted_choice(megaestructuras_disponibles, probabilidades)
