# Grafo Neo4j - MIOTI (Máster en Internet de las Cosas e Inteligencia Artificial)

## Descripción del Proyecto

Este proyecto implementa un grafo de conocimiento en Neo4j que modela la estructura organizacional y académica de MIOTI, incluyendo estudiantes, profesores, empleados, asignaturas y sus relaciones.

## Estructura del Grafo

### Entidades (Nodos)
- **Estudiante**: Compañeros del máster
- **Profesor**: Profesores que imparten asignaturas
- **Empleado**: Personal administrativo y de gestión
- **Asignatura**: Materias del plan de estudios
- **Programa**: Programas académicos (Máster, Cursos, etc.)
- **Departamento**: Departamentos organizacionales
- **Proyecto**: Proyectos fin de máster y trabajos grupales

### Relaciones
- Estudiante **ESTUDIA** Asignatura
- Profesor **IMPARTE** Asignatura
- Estudiante **COLABORA_CON** Estudiante
- Empleado **TRABAJA_EN** Departamento
- Profesor **PERTENECE_A** Departamento
- Asignatura **FORMA_PARTE_DE** Programa
- Estudiante **PARTICIPA_EN** Proyecto
- Profesor **DIRIGE** Proyecto

## Archivos del Proyecto

- `schema.cypher`: Definición del esquema y restricciones
- `data_loader.py`: Script Python para cargar datos de ejemplo
- `sample_data.json`: Datos de ejemplo en formato JSON
- `queries.cypher`: Queries de ejemplo y análisis
- `requirements.txt`: Dependencias de Python

## Instalación y Uso

### Opción 1: Neo4j Sandbox (Recomendado - No requiere instalación)

🚀 **Inicio rápido con Neo4j Sandbox:**

1. **Crear cuenta** en [https://sandbox.neo4j.com/](https://sandbox.neo4j.com/)
2. **Crear un "Blank Sandbox"**
3. **Instalar dependencia:** `pip3 install neo4j-driver`
4. **Configurar credenciales** en `sandbox_loader.py`
5. **Ejecutar:** `python3 sandbox_loader.py`
6. **Explorar** en el navegador Neo4j de tu sandbox

## Queries Destacadas

El proyecto incluye queries para:
- Análisis de colaboraciones entre estudiantes
- Carga académica de profesores
- Estructura departamental
- Relaciones interdisciplinarias
- Análisis de proyectos colaborativos 
