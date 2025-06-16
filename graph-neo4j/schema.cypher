// ========================================
// ESQUEMA DEL GRAFO MIOTI - NEO4J
// ========================================

// Crear restricciones de unicidad
CREATE CONSTRAINT estudiante_id IF NOT EXISTS FOR (e:Estudiante) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT profesor_id IF NOT EXISTS FOR (p:Profesor) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT empleado_id IF NOT EXISTS FOR (emp:Empleado) REQUIRE emp.id IS UNIQUE;
CREATE CONSTRAINT asignatura_codigo IF NOT EXISTS FOR (a:Asignatura) REQUIRE a.codigo IS UNIQUE;
CREATE CONSTRAINT programa_id IF NOT EXISTS FOR (pr:Programa) REQUIRE pr.id IS UNIQUE;
CREATE CONSTRAINT departamento_id IF NOT EXISTS FOR (d:Departamento) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT proyecto_id IF NOT EXISTS FOR (proy:Proyecto) REQUIRE proy.id IS UNIQUE;

// Crear índices para mejorar el rendimiento
CREATE INDEX estudiante_email IF NOT EXISTS FOR (e:Estudiante) ON (e.email);
CREATE INDEX profesor_email IF NOT EXISTS FOR (p:Profesor) ON (p.email);
CREATE INDEX asignatura_nombre IF NOT EXISTS FOR (a:Asignatura) ON (a.nombre);
CREATE INDEX estudiante_nombre IF NOT EXISTS FOR (e:Estudiante) ON (e.nombre);
CREATE INDEX profesor_nombre IF NOT EXISTS FOR (p:Profesor) ON (p.nombre);

// ========================================
// ESTRUCTURA DE NODOS
// ========================================

/*
ESTUDIANTE:
- id: Identificador único
- nombre: Nombre completo
- email: Correo electrónico
- fecha_ingreso: Fecha de inicio en MIOTI
- especialidad: Área de especialización
- empresa_origen: Empresa de procedencia (opcional)
- pais: País de origen
*/

/*
PROFESOR:
- id: Identificador único
- nombre: Nombre completo
- email: Correo electrónico
- titulo: Título académico más alto
- especialidad: Área de especialización
- años_experiencia: Años de experiencia docente
- tipo: "titular", "asociado", "colaborador"
*/

/*
EMPLEADO:
- id: Identificador único
- nombre: Nombre completo
- email: Correo electrónico
- cargo: Posición en la organización
- fecha_ingreso: Fecha de contratación
- area: Área de trabajo
*/

/*
ASIGNATURA:
- codigo: Código único de la asignatura
- nombre: Nombre de la asignatura
- creditos: Número de créditos ECTS
- semestre: Semestre en que se imparte
- tipo: "obligatoria", "optativa", "proyecto"
- descripcion: Descripción breve
*/

/*
PROGRAMA:
- id: Identificador único
- nombre: Nombre del programa
- tipo: "master", "curso", "especialización"
- duracion_meses: Duración en meses
- modalidad: "presencial", "online", "híbrida"
*/

/*
DEPARTAMENTO:
- id: Identificador único
- nombre: Nombre del departamento
- area: Área de responsabilidad
- presupuesto: Presupuesto anual (opcional)
*/

/*
PROYECTO:
- id: Identificador único
- titulo: Título del proyecto
- descripcion: Descripción del proyecto
- fecha_inicio: Fecha de inicio
- fecha_fin: Fecha de finalización
- tipo: "TFM", "grupal", "investigacion"
- estado: "planificacion", "desarrollo", "finalizado"
*/

// ========================================
// ESTRUCTURA DE RELACIONES
// ========================================

/*
ESTUDIA: Estudiante -> Asignatura
- fecha_matricula: Fecha de matrícula
- calificacion: Nota obtenida (opcional)
- estado: "cursando", "aprobada", "suspensa"

IMPARTE: Profesor -> Asignatura
- fecha_inicio: Inicio del período docente
- tipo_participacion: "titular", "colaborador"
- horas_semanales: Horas dedicadas por semana

COLABORA_CON: Estudiante -> Estudiante
- tipo: "compañero_clase", "proyecto_conjunto", "estudio_grupo"
- fecha_inicio: Inicio de la colaboración
- intensidad: "alta", "media", "baja"

TRABAJA_EN: Empleado -> Departamento
- fecha_inicio: Fecha de inicio en el departamento
- rol: Rol específico en el departamento

PERTENECE_A: Profesor -> Departamento
- fecha_inicio: Fecha de adscripción
- dedicacion: "completa", "parcial"

FORMA_PARTE_DE: Asignatura -> Programa
- orden: Orden en el plan de estudios
- caracter: "obligatoria", "optativa"

PARTICIPA_EN: Estudiante -> Proyecto
- rol: "director", "participante"
- fecha_inicio: Fecha de inicio de participación
- contribucion: Descripción de la contribución

DIRIGE: Profesor -> Proyecto
- tipo_direccion: "director", "codirector", "tutor"
- fecha_inicio: Fecha de inicio de la dirección
*/ 
