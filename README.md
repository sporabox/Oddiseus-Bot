
# 🌌 Bot Generador de Sistemas Solares

Bot de Discord para generar sistemas solares aleatorios para roleplay de naciones espaciales.

## 📋 Características

- **Generación de sistemas completos** con múltiples tipos de estrellas
- **Base de datos integrada** para guardar y consultar sistemas
- **Sistema de nomenclatura detallado** con nombres específicos para cuerpos celestes
- **Múltiples tipos de comandos** (slash y tradicionales)
- **Estadísticas de exploración** y ranking de usuarios
- **Eventos especiales** y recursos estratégicos
- **Leviatanes y especies inteligentes** raras
- **Megaestructuras** detectables mediante sondeo

## 🎮 Comandos del Bot

### Comandos Slash (/)
- `/generar_sistema [nombre]` - Genera un sistema solar aleatorio (opcional: con nombre para guardar)
- `/ficha_sistema <nombre>` - Muestra la ficha básica de un sistema guardado
- `/generar_ficha <nombre>` - Genera ficha detallada con nombres específicos (GMT-6)
- `/stats_exploracion` - Muestra estadísticas del servidor y ranking de exploradores
- `/ayuda_sistema` - Muestra información de ayuda completa

### Comandos Tradicionales (!)
- `!generar [nombre]` (o `!sistema`, `!solar`) - Genera un sistema solar aleatorio
- `!ficha <nombre>` - Muestra la ficha básica de un sistema guardado
- `!ayuda` (o `!info`) - Muestra información de ayuda

## ⭐ Tipos de Estrellas

### Comunes (Habitables)
- **Estrella Clase M**: Enana roja, la más común en la galaxia
- **Tipo K**: Enana naranja, ideal para la vida
- **Tipo G**: Como nuestro Sol, estable y habitable
- **Tipo F**: Estrella blanco-amarilla, habitable pero más caliente
- **Tipo A**: Estrella blanca y caliente, habitable pero menos duradera

### Comunes (No Habitables)
- **Tipo T**: Enana marrón fría, sin fusión nuclear

### Raras (Peligrosas)
- **Gigante Roja**: Estrella en expansión, fase terminal
- **Pulsar**: Estrella de neutrones en rotación rápida
- **Estrella de Neutrones**: Remanente estelar ultra-denso

### Muy Raras (Extremas)
- **Agujero Negro**: Gravedad extrema, deforma el espacio-tiempo
- **Magnetar**: Campo magnético extremo, muy peligroso
- **Estrella Extraña**: Materia exótica hipotética
- **Tipo O**: Estrella azul masiva, vida muy corta

## 🌟 Tipos de Sistemas

- **Unario** (50%): Un solo sol
- **Binario** (25%): Dos soles
- **Trinario** (25%): Tres soles

## 🏠 Habitabilidad

- **Habitable**: Sistemas con estrellas Tipo K, G, F o A
- **Inhabitable**: Sistemas con estrellas peligrosas o extremas
- **Sin Cuerpos Celestes**: Agujeros Negros y Estrellas Extrañas

## 🪐 Cuerpos Celestes

### Generación
- **Planetas**: 1-16 por sistema
- **Lunas**: 1-27 por sistema  
- **Asteroides**: 0-3 cinturones
- *No se generan en sistemas con Agujero Negro o Estrella Extraña*

### Nomenclatura en Fichas Detalladas
- **Estrellas**: `Nombre del Sistema` + `(Tipo de Estrella)`
  - Ejemplo: `Porin (Tipo G)`
- **Planetas**: `Nombre del Sistema` + `Número Romano` + `(Tipo de Planeta)`
  - Ejemplo: `Porin I (Planeta Gaseoso)`, `Porin II (Gaia)`
- **Lunas**: `Nombre del Planeta` + `letra minúscula`
  - Ejemplo: `Porin Ia`, `Porin Ib`, `Porin IIIa`

## 💎 Recursos Estratégicos

### Comunes
- **Gases Exóticos**: Útiles para tecnología avanzada
- **Cristales Raros**: Componentes para equipamiento
- **Polvo Zro**: Material psiónico

### Poco Comunes
- **Motas Volátiles**: Energía especializada

### Raros
- **Metal Vivo**: Tecnología auto-reparadora

### Muy Raros
- **Nanitos**: Tecnología de vanguardia

### Únicos
- **Materia Oscura**: Solo en sistemas con Agujero Negro

## ⚡ Eventos Especiales (30% probabilidad)

- **Tormenta Psiónica**: Fenómeno mental en el sistema
- **Lluvia Meteórica**: Bombardeo constante de meteoritos

## 🏗️ Megaestructuras (3% probabilidad mediante sondeo)

### Comunes
- Estación Espacial Abandonada
- Plataforma de Investigación
- Puesto de Observación

### Raras  
- Mundo Anillo
- Esfera de Dyson Parcial
- Portal Dimensional

### Muy Raras
- Esfera de Dyson Completa
- Matrioshka Brain
- Computadora Cuántica Galáctica

## 🐉 Leviatanes (7% probabilidad)

### Generales
- Guardián Estelar
- Bestia del Vacío
- Devorador de Mundos

### Específicos por Tipo de Estrella
- **Estelaritas**: Solo en sistemas normales
- **Entidades Cristalinas**: Solo en Pulsares, Neutrones, Magnetar

## 👽 Especies Inteligentes (2% probabilidad en sistemas habitables)

### Tipos
- Humanoides, Reptilianos, Insectoides, Acuáticos, Gaseosos, Máquinas, Energía Pura

### Niveles Tecnológicos
- Pre-espacial, Espacial Primitivo, Espacial Avanzado, Tecnología Arcana

### Rasgos
- **3 Rasgos Positivos** y **2 Rasgos Negativos** por especie
- Restricciones y exclusiones entre ciertos rasgos

## 🗃️ Base de Datos

- **Almacenamiento automático** de sistemas con nombre
- **Tracking de exploradores** y fecha de descubrimiento
- **Estadísticas del servidor** y ranking de usuarios
- **Consulta posterior** de sistemas guardados
- **Fichas detalladas** con nomenclatura específica

## 🕐 Zona Horaria

Las fichas detalladas (`/generar_ficha`) muestran la fecha y hora en **GMT-6**.

## 🚀 Uso Recomendado

1. **Exploración básica**: Usa `/generar_sistema` o `!generar` para exploración rápida
2. **Sistemas importantes**: Añade un nombre para guardar en la base de datos
3. **Consulta rápida**: Usa `/ficha_sistema` para ver información básica
4. **Ficha oficial**: Usa `/generar_ficha` para crear documentación detallada con nombres específicos
5. **Estadísticas**: Revisa `/stats_exploracion` para ver el progreso del servidor

## 📊 Probabilidades del Sistema

- **Habitabilidad**: ~45% de sistemas habitables
- **Recursos**: 25% probabilidad de depósitos estratégicos
- **Eventos**: 30% probabilidad de eventos especiales
- **Megaestructuras**: 3% probabilidad mediante sondeo exitoso
- **Leviatanes**: 7% probabilidad de aparición
- **Especies**: 2% probabilidad en sistemas habitables

---

*Bot desarrollado para servidores de roleplay de naciones espaciales*
