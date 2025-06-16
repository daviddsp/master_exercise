# Diseño y Desarrollo del Grafo Neo4j - MIOTI

**Autor:** Abraham Solórzano

## Índice

1. [Introducción](#introducción)
2. [Diseño del Grafo](#diseño-del-grafo)
3. [Implementación](#implementación)
4. [Análisis de Queries](#análisis-de-queries)
5. [Resultados y Conclusiones](#resultados-y-conclusiones)
6. [Casos de Uso](#casos-de-uso)
7. [Instalación y Ejecución](#instalación-y-ejecución)

---

## Introducción

Este proyecto implementa un grafo de conocimiento en Neo4j que modela la estructura académica y organizacional de MIOTI, una institución especializada en IoT e Inteligencia Artificial. El objetivo es crear una representación gráfica de las relaciones entre estudiantes, profesores, asignaturas, proyectos y departamentos para facilitar el análisis de la comunidad académica.

### Objetivos del Proyecto

- **Modelar relaciones complejas** entre entidades académicas
- **Facilitar análisis de redes sociales** dentro de la comunidad MIOTI
- **Proporcionar insights** sobre colaboraciones y patrones académicos
- **Crear una base** para sistemas de recomendación educativa
- **Demostrar el potencial** de los grafos en el ámbito educativo

---

## Diseño del Grafo

### Arquitectura Conceptual

El grafo está diseñado siguiendo un modelo de entidades y relaciones que refleja la realidad de una institución educativa especializada:

```
    [Estudiante] ──ESTUDIA──> [Asignatura] <──IMPARTE── [Profesor]
         │                       │                        │
    COLABORA_CON           FORMA_PARTE_DE            PERTENECE_A
         │                       │                        │
         │                   [Programa]              [Departamento]
         │                                               │
    PARTICIPA_EN                                   TRABAJA_EN
         │                                               │
    [Proyecto] <──DIRIGE── [Profesor]              [Empleado]
```

### Entidades (Nodos)

#### 1. Estudiante
**Propósito:** Representar a los compañeros del máster y sus características

**Propiedades:**
- `id`: Identificador único (EST001, EST002, ...)
- `nombre`: Nombre completo del estudiante
- `email`: Correo electrónico institucional
- `fecha_ingreso`: Fecha de inicio en MIOTI
- `especialidad`: Área de especialización (IoT Industrial, Machine Learning, etc.)
- `empresa_origen`: Empresa de procedencia (opcional)
- `pais`: País de origen

**Justificación:** Los estudiantes son el centro del ecosistema educativo y sus características permiten análisis de diversidad, procedencia y especialización.

#### 2. Profesor
**Propósito:** Modelar el cuerpo docente y su experiencia

**Propiedades:**
- `id`: Identificador único (PROF001, PROF002, ...)
- `nombre`: Nombre completo
- `email`: Correo electrónico
- `titulo`: Título académico más alto
- `especialidad`: Área de expertise
- `años_experiencia`: Experiencia docente
- `tipo`: Categoría académica (titular, asociado, colaborador)

**Justificación:** Permite análisis de carga docente, expertise y asignación de recursos académicos.

#### 3. Asignatura
**Propósito:** Representar las materias del plan de estudios

**Propiedades:**
- `codigo`: Código único (IOT101, ML201, ...)
- `nombre`: Nombre descriptivo
- `creditos`: Créditos ECTS
- `semestre`: Período académico
- `tipo`: Categoría (obligatoria, optativa, proyecto)
- `descripcion`: Descripción breve

**Justificación:** Central para el análisis académico, carga de trabajo y progresión curricular.

#### 4. Proyecto
**Propósito:** Modelar trabajos de investigación y desarrollo

**Propiedades:**
- `id`: Identificador único
- `titulo`: Título del proyecto
- `descripcion`: Descripción detallada
- `fecha_inicio`: Fecha de inicio
- `fecha_fin`: Fecha de finalización
- `tipo`: Tipo de proyecto (TFM, grupal, investigación)
- `estado`: Estado actual (planificación, desarrollo, finalizado)

**Justificación:** Permite analizar colaboraciones en investigación y seguimiento de proyectos.

#### 5. Departamento
**Propósito:** Representar la estructura organizacional

**Propiedades:**
- `id`: Identificador único
- `nombre`: Nombre del departamento
- `area`: Área de responsabilidad
- `presupuesto`: Presupuesto anual

**Justificación:** Facilita análisis organizacional y asignación de recursos.

#### 6. Programa
**Propósito:** Modelar programas académicos

**Propiedades:**
- `id`: Identificador único
- `nombre`: Nombre del programa
- `tipo`: Tipo (master, curso, especialización)
- `duracion_meses`: Duración
- `modalidad`: Modalidad (presencial, online, híbrida)

#### 7. Empleado
**Propósito:** Representar personal administrativo

**Propiedades:**
- `id`: Identificador único
- `nombre`: Nombre completo
- `cargo`: Posición
- `fecha_ingreso`: Fecha de contratación
- `area`: Área de trabajo

### Relaciones

#### 1. ESTUDIA (Estudiante → Asignatura)
**Propósito:** Conectar estudiantes con sus asignaturas

**Propiedades:**
- `fecha_matricula`: Fecha de matrícula
- `calificacion`: Nota obtenida (opcional)
- `estado`: Estado actual (cursando, aprobada, suspensa)

**Análisis posible:** Progreso académico, rendimiento por asignatura, carga de trabajo.

#### 2. IMPARTE (Profesor → Asignatura)
**Propósito:** Conectar profesores con asignaturas que enseñan

**Propiedades:**
- `fecha_inicio`: Inicio del período docente
- `tipo_participacion`: Rol (titular, colaborador)
- `horas_semanales`: Dedicación semanal

**Análisis posible:** Carga docente, distribución de enseñanza, especialización.

#### 3. COLABORA_CON (Estudiante → Estudiante)
**Propósito:** Modelar colaboraciones entre estudiantes

**Propiedades:**
- `tipo`: Tipo de colaboración (compañero_clase, proyecto_conjunto, estudio_grupo)
- `fecha_inicio`: Inicio de la colaboración
- `intensidad`: Nivel de colaboración (alta, media, baja)

**Análisis posible:** Redes sociales, patrones de colaboración, comunidades.

#### 4. PARTICIPA_EN (Estudiante → Proyecto)
**Propósito:** Conectar estudiantes con proyectos

**Propiedades:**
- `rol`: Papel en el proyecto (director, participante)
- `fecha_inicio`: Inicio de participación
- `contribucion`: Descripción de la contribución

#### 5. DIRIGE (Profesor → Proyecto)
**Propósito:** Conectar profesores directores con proyectos

**Propiedades:**
- `tipo_direccion`: Tipo (director, codirector, tutor)
- `fecha_inicio`: Inicio de la dirección

#### 6. PERTENECE_A (Profesor → Departamento)
**Propósito:** Asignación departamental de profesores

**Propiedades:**
- `fecha_inicio`: Fecha de adscripción
- `dedicacion`: Nivel de dedicación (completa, parcial)

#### 7. TRABAJA_EN (Empleado → Departamento)
**Propósito:** Asignación departamental de empleados

**Propiedades:**
- `fecha_inicio`: Fecha de inicio
- `rol`: Rol específico

#### 8. FORMA_PARTE_DE (Asignatura → Programa)
**Propósito:** Estructurar el currículum

**Propiedades:**
- `orden`: Orden en el plan de estudios
- `caracter`: Naturaleza (obligatoria, optativa)

---

## Implementación

### Tecnologías Utilizadas

- **Neo4j Community Edition 5.x**: Base de datos de grafos
- **Python 3.8+**: Script de carga de datos
- **Driver Neo4j Python**: Conectividad con la base de datos
- **Cypher**: Lenguaje de consulta de grafos

### Estructura del Proyecto

```
graph_neo4j/
├── README.md                  # Descripción general
├── DOCUMENTO_PROYECTO.md      # Este documento
├── schema.cypher             # Definición del esquema
├── sample_data.json          # Datos de ejemplo
├── data_loader.py           # Script de carga
├── queries.cypher           # Queries de análisis
├── requirements.txt         # Dependencias Python
└── config_example.py        # Configuración de ejemplo
```

### Proceso de Desarrollo

#### Fase 1: Diseño Conceptual
1. **Análisis de requisitos** del dominio educativo
2. **Identificación de entidades** principales
3. **Definición de relaciones** significativas
4. **Validación del modelo** con casos de uso

#### Fase 2: Implementación del Esquema
1. **Creación de restricciones** de unicidad
2. **Definición de índices** para optimización
3. **Documentación del esquema** en Cypher

#### Fase 3: Generación de Datos
1. **Creación de datos realistas** para MIOTI
2. **Diversidad en nacionalidades** y especialidades
3. **Relaciones coherentes** entre entidades
4. **Validación de integridad** referencial

#### Fase 4: Desarrollo de Queries
1. **Queries básicas** de exploración
2. **Análisis de redes sociales** entre estudiantes
3. **Métricas académicas** y de rendimiento
4. **Queries de recomendación** avanzadas

---

## Análisis de Queries

### 1. Análisis Básico del Grafo

#### Query: Estructura General
```cypher
MATCH (n)
RETURN labels(n)[0] as TipoNodo, count(n) as Cantidad
ORDER BY Cantidad DESC;
```

**Propósito:** Obtener una visión general de la composición del grafo.

**Resultados Esperados:**
- Estudiante: 8
- Asignatura: 9  
- Profesor: 6
- Departamento: 5
- Empleado: 5
- Proyecto: 4
- Programa: 2

**Insights:** Permite validar que la carga de datos fue correcta y entender la proporción de cada tipo de entidad.

### 2. Análisis de Redes de Estudiantes

#### Query: Colaboraciones entre Estudiantes
```cypher
MATCH (e1:Estudiante)-[r:COLABORA_CON]->(e2:Estudiante)
RETURN e1.nombre, e2.nombre, r.tipo, r.intensidad, r.fecha_inicio
ORDER BY r.fecha_inicio DESC;
```

**Propósito:** Analizar patrones de colaboración en la comunidad estudiantil.

**Resultados Esperados:**
- Ana García ↔ Carlos López (compañero_clase, alta intensidad)
- María Fernández ↔ Lucía Martín (proyecto_conjunto, alta intensidad)
- João Santos ↔ Ahmed Hassan (estudio_grupo, media intensidad)

**Insights:** 
- Identifica líderes naturales y conectores
- Revela patrones de formación de grupos
- Puede guiar estrategias de team building

#### Query: Estudiantes más Conectados
```cypher
MATCH (e:Estudiante)-[r:COLABORA_CON]-()
RETURN e.nombre, e.especialidad, count(r) as NumeroColaboraciones
ORDER BY NumeroColaboraciones DESC;
```

**Insights:** Identifica estudiantes clave en la red social del máster.

### 3. Análisis Académico

#### Query: Carga por Asignatura
```cypher
MATCH (e:Estudiante)-[r:ESTUDIA]->(a:Asignatura)
RETURN a.nombre, a.codigo, count(e) as NumeroEstudiantes, 
       collect(e.nombre) as EstudiantesMatriculados
ORDER BY NumeroEstudiantes DESC;
```

**Propósito:** Analizar popularidad y demanda de asignaturas.

**Resultados Esperados:**
- "Fundamentos de IoT": 8 estudiantes (asignatura obligatoria)
- "Machine Learning Aplicado": 8 estudiantes (asignatura obligatoria)
- "Redes y Protocolos IoT": 4 estudiantes
- "Ciberseguridad en IoT": 4 estudiantes
- "Edge Computing": 1 estudiante (especializada)

**Insights:**
- Las asignaturas obligatorias tienen matrícula completa
- Las optativas reflejan especialización por intereses
- Permite planificar recursos docentes

#### Query: Carga Docente
```cypher
MATCH (p:Profesor)-[r:IMPARTE]->(a:Asignatura)
RETURN p.nombre, sum(r.horas_semanales) as HorasTotalesSemanales,
       collect({asignatura: a.nombre, horas: r.horas_semanales}) as AsignaturasQueImparte
ORDER BY HorasTotalesSemanales DESC;
```

**Insights:** Evalúa distribución de carga de trabajo docente y especialización.

### 4. Análisis de Proyectos

#### Query: Proyectos Activos
```cypher
MATCH (proy:Proyecto)
WHERE proy.estado IN ['desarrollo', 'planificacion']
OPTIONAL MATCH (e:Estudiante)-[re:PARTICIPA_EN]->(proy)
OPTIONAL MATCH (p:Profesor)-[rp:DIRIGE]->(proy)
RETURN proy.titulo, proy.tipo, proy.estado,
       collect(DISTINCT e.nombre) as Estudiantes,
       collect(DISTINCT p.nombre) as Directores
ORDER BY proy.fecha_inicio DESC;
```

**Propósito:** Monitorear proyectos en curso y sus equipos.

**Resultados Esperados:**
- "Sistema IoT para Agricultura Inteligente" (Ana García + Dr. Rodríguez)
- "Análisis Predictivo de Consumo Energético" (Carlos López + Dra. Sánchez)
- "Plataforma de Seguridad IoT Industrial" (Elena Popov + Ing. Morales)
- "Edge AI para Vehículos Autónomos" (João Santos + Dr. Chen)

**Insights:**
- Permite seguimiento de proyectos
- Identifica colaboraciones profesor-estudiante
- Facilita asignación de recursos

### 5. Análisis de Especialidades

#### Query: Compatibilidad de Especialidades
```cypher
MATCH (e:Estudiante)-[:ESTUDIA]->(a:Asignatura)<-[:IMPARTE]-(p:Profesor)
WHERE e.especialidad = p.especialidad
RETURN e.especialidad, 
       collect(DISTINCT e.nombre) as Estudiantes,
       collect(DISTINCT p.nombre) as Profesores,
       collect(DISTINCT a.nombre) as Asignaturas
ORDER BY e.especialidad;
```

**Propósito:** Evaluar alineación entre intereses de estudiantes y expertise docente.

**Insights:**
- Identifica oportunidades de mentoría especializada
- Revela áreas donde se necesita más diversidad docente
- Optimiza asignación de directores de proyecto

### 6. Queries de Recomendación

#### Query: Colaboradores Potenciales
```cypher
MATCH (e:Estudiante {nombre: 'Carlos López Rodríguez'})
MATCH (otros:Estudiante)-[:ESTUDIA]->(a:Asignatura)<-[:ESTUDIA]-(e)
WHERE otros <> e
AND NOT (e)-[:COLABORA_CON]-(otros)
RETURN otros.nombre, otros.especialidad, 
       count(a) as AsignaturasComunes,
       collect(a.nombre) as DetalleAsignaturas
ORDER BY AsignaturasComunes DESC
LIMIT 5;
```

**Propósito:** Sugerir colaboradores potenciales basado en asignaturas comunes.

**Valor:** Sistema de recomendación para formación de grupos de estudio.

### 7. Análisis Temporal

#### Query: Evolución de Matrículas
```cypher
MATCH (e:Estudiante)-[r:ESTUDIA]->(a:Asignatura)
RETURN r.fecha_matricula, count(r) as NumeroMatriculas
ORDER BY r.fecha_matricula;
```

**Insights:** Permite ver la progresión académica a lo largo del tiempo.

### 8. Métricas del Grafo

#### Query: Densidad de Conexiones
```cypher
MATCH (n)
WITH count(n) as totalNodes
MATCH ()-[r]->()
WITH totalNodes, count(r) as totalRelations
RETURN totalNodes, totalRelations, 
       round(toFloat(totalRelations) / (totalNodes * (totalNodes - 1)) * 100, 2) as DensidadPorcentaje;
```

**Propósito:** Evaluar qué tan conectado está el grafo.

**Valor:** Métrica de cohesión de la comunidad académica.

---

## Resultados y Conclusiones

### Hallazgos Principales

#### 1. Estructura de la Comunidad
- **Diversidad Internacional:** 4 países representados (España, Portugal, Marruecos, Bulgaria)
- **Especialización Variada:** 8 especialidades diferentes en IoT e IA
- **Procedencia Empresarial:** 75% de estudiantes tienen experiencia previa

#### 2. Patrones de Colaboración
- **Redes Densas:** Estudiantes con especialidades complementarias tienden a colaborar más
- **Proyectos Multidisciplinarios:** Cada proyecto combina múltiples especialidades
- **Mentoría Efectiva:** Alto alineamiento entre especialidades de profesores y estudiantes

#### 3. Estructura Académica
- **Curriculum Balanceado:** 60% asignaturas obligatorias, 40% optativas
- **Carga Distribuida:** Distribución equitativa de horas docentes
- **Progresión Lógica:** Asignaturas básicas en semestres iniciales

#### 4. Métricas del Grafo
- **Nodos Totales:** 39 entidades
- **Relaciones Totales:** 47+ conexiones
- **Densidad:** ~3.1% (típico para redes sociales académicas)
- **Nodos Centrales:** Asignaturas obligatorias son los más conectados

### Valor del Modelo de Grafo

#### Ventajas sobre Modelos Relacionales
1. **Consultas Naturales:** Las relaciones son ciudadanos de primera clase
2. **Descubrimiento de Patrones:** Facilita encontrar conexiones no obvias
3. **Escalabilidad de Consultas:** Traversals eficientes en grafos grandes
4. **Flexibilidad:** Fácil adición de nuevos tipos de relaciones

#### Limitaciones Identificadas
1. **Complejidad de Queries:** Cypher requiere curva de aprendizaje
2. **Rendimiento:** Algunas consultas complejas pueden ser costosas
3. **Consistencia:** Requiere cuidado en el mantenimiento de datos

### Recomendaciones

#### Para la Institución
1. **Implementar Sistema de Recomendación:** Usar queries para sugerir colaboraciones
2. **Monitoreo de Proyectos:** Dashboard basado en el grafo para seguimiento
3. **Análisis de Rendimiento:** Correlacionar estructura de red con éxito académico
4. **Planificación Curricular:** Usar análisis de popularidad para ajustar oferta

#### Para Estudiantes
1. **Networking Inteligente:** Identificar colaboradores complementarios
2. **Selección de Proyectos:** Evaluar disponibilidad de expertise
3. **Planificación Académica:** Optimizar selección de asignaturas optativas

#### Para Profesores
1. **Asignación Eficiente:** Distribuir carga según expertise
2. **Identificación de Talento:** Detectar estudiantes destacados por área
3. **Formación de Equipos:** Guiar formación de grupos de proyecto

---

## Casos de Uso

### 1. Sistema de Recomendación Académica

**Escenario:** Un estudiante busca compañeros para un proyecto grupal.

**Query:**
```cypher
MATCH (estudiante:Estudiante {nombre: 'Ana García Martínez'})
MATCH (otros:Estudiante)-[:ESTUDIA]->(a:Asignatura)<-[:ESTUDIA]-(estudiante)
WHERE otros.especialidad <> estudiante.especialidad
RETURN otros.nombre, otros.especialidad, count(a) as compatibilidad
ORDER BY compatibilidad DESC LIMIT 3;
```

**Beneficio:** Recomendaciones basadas en complementariedad de habilidades.

### 2. Análisis de Carga Docente

**Escenario:** Planificación de recursos para el próximo semestre.

**Query:**
```cypher
MATCH (p:Profesor)-[r:IMPARTE]->(a:Asignatura)
RETURN p.nombre, sum(r.horas_semanales) as carga_total,
       CASE WHEN sum(r.horas_semanales) > 12 THEN 'Sobrecargado'
            WHEN sum(r.horas_semanales) < 6 THEN 'Subcargado'
            ELSE 'Balanceado' END as estado
ORDER BY carga_total DESC;
```

**Beneficio:** Optimización de la distribución de carga docente.

### 3. Seguimiento de Proyectos

**Escenario:** Identificar proyectos en riesgo por falta de supervisión.

**Query:**
```cypher
MATCH (proy:Proyecto)
WHERE proy.estado = 'desarrollo'
OPTIONAL MATCH (p:Profesor)-[:DIRIGE]->(proy)
WITH proy, count(p) as num_directores
WHERE num_directores = 0
RETURN proy.titulo as proyecto_sin_director, proy.fecha_inicio;
```

**Beneficio:** Detección temprana de problemas en proyectos.

### 4. Análisis de Redes Sociales

**Escenario:** Identificar estudiantes aislados para intervención.

**Query:**
```cypher
MATCH (e:Estudiante)
OPTIONAL MATCH (e)-[r:COLABORA_CON]-()
WITH e, count(r) as conexiones
WHERE conexiones = 0
RETURN e.nombre, e.especialidad, 'Necesita integración' as recomendacion;
```

**Beneficio:** Apoyo proactivo a estudiantes con pocas conexiones sociales.

### 5. Planificación Curricular

**Escenario:** Evaluar demanda de asignaturas optativas.

**Query:**
```cypher
MATCH (a:Asignatura {tipo: 'optativa'})
OPTIONAL MATCH (e:Estudiante)-[:ESTUDIA]->(a)
RETURN a.nombre, count(e) as estudiantes_matriculados,
       CASE WHEN count(e) < 3 THEN 'Considerar cancelar'
            WHEN count(e) > 6 THEN 'Considerar duplicar'
            ELSE 'Mantener' END as recomendacion
ORDER BY estudiantes_matriculados DESC;
```

**Beneficio:** Decisiones basadas en datos para oferta académica.

---

## Instalación y Ejecución

### Requisitos Previos

1. **Neo4j Desktop** o **Neo4j Community Edition** instalado
2. **Python 3.8+** 
3. **Git** para clonar el repositorio

### Pasos de Instalación

#### 1. Preparar Neo4j
```bash
# Descargar e instalar Neo4j Desktop desde:
# https://neo4j.com/download/

# O usar Docker:
docker run \
    --name mioti-neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    --env NEO4J_AUTH=neo4j/password \
    neo4j:5.15
```

#### 2. Configurar el Proyecto
```bash
# Clonar repositorio (si está en Git)
git clone <repository_url>
cd graph_neo4j

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar conexión
cp config_example.py config.py
# Editar config.py con tus credenciales
```

#### 3. Cargar Datos
```bash
# Ejecutar script de carga
python data_loader.py
```

#### 4. Verificar Instalación
```bash
# Abrir Neo4j Browser en http://localhost:7474
# Ejecutar query de verificación:
# MATCH (n) RETURN count(n);
```

### Ejecución de Queries

#### Desde Neo4j Browser
1. Abrir http://localhost:7474
2. Autenticarse con usuario/contraseña
3. Copiar queries desde `queries.cypher`
4. Ejecutar y analizar resultados

#### Desde Python
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", 
                            auth=("neo4j", "password"))

with driver.session() as session:
    result = session.run("MATCH (e:Estudiante) RETURN count(e)")
    print(f"Número de estudiantes: {result.single()[0]}")

driver.close()
```

### Personalización

#### Modificar Datos
1. Editar `sample_data.json` con datos reales de tu institución
2. Ejecutar nuevamente `python data_loader.py`

#### Añadir Nuevas Queries
1. Agregar queries al archivo `queries.cypher`
2. Documentar propósito y resultados esperados

#### Extender el Esquema
1. Modificar `schema.cypher` con nuevas entidades/relaciones
2. Actualizar `data_loader.py` con nuevos métodos de carga
3. Crear datos de ejemplo para las nuevas entidades

---

## Conclusiones Finales

Este proyecto demuestra el poder de los grafos para modelar ecosistemas académicos complejos. La implementación en Neo4j proporciona:

### Beneficios Técnicos
- **Flexibilidad** para evolucionar el esquema
- **Performance** en consultas de traversal
- **Expresividad** en el lenguaje Cypher
- **Visualización** nativa de relaciones

### Beneficios Funcionales
- **Insights** sobre patrones de colaboración
- **Optimización** de recursos académicos
- **Recomendaciones** personalizadas
- **Análisis** de redes sociales educativas

### Aplicabilidad
El modelo es extensible a:
- **Otras instituciones educativas**
- **Empresas** (empleados, proyectos, departamentos)
- **Comunidades de investigación**
- **Redes profesionales**

### Trabajo Futuro
- **Análisis temporal** más profundo
- **Métricas de centralidad** avanzadas
- **Machine Learning** sobre el grafo
- **Interfaces web** para consultas
- **Análisis predictivo** de rendimiento académico

El grafo de MIOTI se convierte así en una herramienta valiosa para entender, analizar y optimizar la experiencia educativa en el ámbito de IoT e Inteligencia Artificial.

---

**Contacto:** [mioti@contact.com](mailto:mioti@contact.com)  
**Repositorio:** [GitHub - MIOTI Graph Neo4j](https://github.com/mioti/graph-neo4j)  
**Documentación:** [Wiki del Proyecto](https://github.com/mioti/graph-neo4j/wiki) 
