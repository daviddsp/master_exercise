#!/usr/bin/env python3
"""
Script para cargar datos de MIOTI en Neo4j Sandbox
Adaptado para usar con https://sandbox.neo4j.com/
"""

import json
from neo4j import GraphDatabase, basic_auth
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_mioti_data():
    """Cargar datos de MIOTI en Neo4j Sandbox"""
    
    # CONFIGURA AQUÍ TUS CREDENCIALES DE SANDBOX
    # Reemplaza con los valores de tu sandbox específico
    URI = "bolt://44.201.223.174:7687"  # Tu URI del sandbox
    USERNAME = "neo4j"
    PASSWORD = "nuts-accounts-boxcars"  # Tu contraseña del sandbox
    
    print("🚀 Iniciando carga de datos de MIOTI en Neo4j Sandbox...")
    
    # Conectar a Neo4j Sandbox
    driver = GraphDatabase.driver(URI, auth=basic_auth(USERNAME, PASSWORD))
    
    try:
        with driver.session(database="neo4j") as session:
            # 1. Limpiar base de datos
            print("🧹 Limpiando base de datos...")
            session.run("MATCH (n) DETACH DELETE n")
            
            # 2. Crear restricciones
            print("📋 Creando restricciones...")
            constraints = [
                "CREATE CONSTRAINT estudiante_id IF NOT EXISTS FOR (e:Estudiante) REQUIRE e.id IS UNIQUE",
                "CREATE CONSTRAINT profesor_id IF NOT EXISTS FOR (p:Profesor) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT asignatura_codigo IF NOT EXISTS FOR (a:Asignatura) REQUIRE a.codigo IS UNIQUE"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception:
                    pass  # La restricción ya existe
            
            # 3. Cargar datos desde JSON
            print("📊 Cargando datos...")
            with open('sample_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar estudiantes
            for estudiante in data['estudiantes']:
                session.run("""
                    CREATE (e:Estudiante {
                        id: $id, nombre: $nombre, email: $email,
                        fecha_ingreso: date($fecha_ingreso),
                        especialidad: $especialidad, empresa_origen: $empresa_origen,
                        pais: $pais
                    })
                """, **estudiante)
            
            # Cargar profesores
            for profesor in data['profesores']:
                session.run("""
                    CREATE (p:Profesor {
                        id: $id, nombre: $nombre, email: $email,
                        titulo: $titulo, especialidad: $especialidad,
                        años_experiencia: $años_experiencia, tipo: $tipo
                    })
                """, **profesor)
            
            # Cargar asignaturas
            for asignatura in data['asignaturas']:
                session.run("""
                    CREATE (a:Asignatura {
                        codigo: $codigo, nombre: $nombre, creditos: $creditos,
                        semestre: $semestre, tipo: $tipo, descripcion: $descripcion
                    })
                """, **asignatura)
            
            # Cargar proyectos
            for proyecto in data['proyectos']:
                session.run("""
                    CREATE (proy:Proyecto {
                        id: $id, titulo: $titulo, descripcion: $descripcion,
                        fecha_inicio: date($fecha_inicio), fecha_fin: date($fecha_fin),
                        tipo: $tipo, estado: $estado
                    })
                """, **proyecto)
            
            # Cargar departamentos
            for departamento in data['departamentos']:
                session.run("""
                    CREATE (d:Departamento {
                        id: $id, nombre: $nombre, area: $area, presupuesto: $presupuesto
                    })
                """, **departamento)
            
            # 4. Crear relaciones principales
            print("🔗 Creando relaciones...")
            
            # Estudiantes estudian asignaturas obligatorias
            session.run("""
                MATCH (e:Estudiante), (a:Asignatura)
                WHERE a.codigo IN ['IOT101', 'ML201']
                CREATE (e)-[:ESTUDIA {fecha_matricula: date('2024-09-01'), estado: 'cursando'}]->(a)
            """)
            
            # Profesores imparten asignaturas
            relationships = [
                ("PROF001", "IOT101"),
                ("PROF002", "ML201"),
                ("PROF003", "NET301"),
                ("PROF004", "SEC401"),
                ("PROF005", "EDGE501"),
                ("PROF006", "DATA601")
            ]
            
            for prof_id, asig_codigo in relationships:
                session.run("""
                    MATCH (p:Profesor {id: $prof_id}), (a:Asignatura {codigo: $asig_codigo})
                    CREATE (p)-[:IMPARTE {fecha_inicio: date('2024-09-01'), horas_semanales: 4}]->(a)
                """, prof_id=prof_id, asig_codigo=asig_codigo)
            
            # Colaboraciones entre estudiantes
            session.run("""
                MATCH (e1:Estudiante {id: 'EST001'}), (e2:Estudiante {id: 'EST002'})
                CREATE (e1)-[:COLABORA_CON {tipo: 'compañero_clase', intensidad: 'alta'}]->(e2)
            """)
            
            session.run("""
                MATCH (e1:Estudiante {id: 'EST003'}), (e2:Estudiante {id: 'EST005'})
                CREATE (e1)-[:COLABORA_CON {tipo: 'proyecto_conjunto', intensidad: 'alta'}]->(e2)
            """)
            
            # Estudiantes participan en proyectos
            proyecto_participaciones = [
                ("EST001", "PROY001", "Desarrollo del sistema de sensores"),
                ("EST002", "PROY002", "Algoritmos de predicción"),
                ("EST007", "PROY003", "Arquitectura de seguridad"),
                ("EST004", "PROY004", "Implementación edge AI")
            ]
            
            for est_id, proy_id, contribucion in proyecto_participaciones:
                session.run("""
                    MATCH (e:Estudiante {id: $est_id}), (proy:Proyecto {id: $proy_id})
                    CREATE (e)-[:PARTICIPA_EN {rol: 'director', contribucion: $contribucion}]->(proy)
                """, est_id=est_id, proy_id=proy_id, contribucion=contribucion)
            
            # Profesores dirigen proyectos
            session.run("""
                MATCH (p:Profesor {id: 'PROF001'}), (proy:Proyecto {id: 'PROY001'})
                CREATE (p)-[:DIRIGE {tipo_direccion: 'director'}]->(proy)
            """)
            
            session.run("""
                MATCH (p:Profesor {id: 'PROF002'}), (proy:Proyecto {id: 'PROY002'})
                CREATE (p)-[:DIRIGE {tipo_direccion: 'director'}]->(proy)
            """)
            
            # 5. Verificar carga
            result = session.run("MATCH (n) RETURN labels(n)[0] as tipo, count(n) as cantidad ORDER BY cantidad DESC")
            
            print("\n✅ ¡Datos cargados exitosamente!")
            print("\n📊 Resumen del grafo:")
            for record in result:
                print(f"   {record['tipo']}: {record['cantidad']} nodos")
            
            print(f"\n🎯 Próximos pasos:")
            print(f"1. Abre el navegador Neo4j de tu sandbox")
            print(f"2. Ejecuta queries de ejemplo:")
            print(f"   MATCH (e:Estudiante) RETURN e.nombre, e.especialidad")
            print(f"   MATCH (e:Estudiante)-[r:COLABORA_CON]->(e2:Estudiante) RETURN e.nombre, e2.nombre, r.tipo")
            print(f"3. Explora las queries del archivo queries.cypher")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Verifica que:")
        print("- Las credenciales del sandbox sean correctas")
        print("- El archivo sample_data.json esté disponible")
        print("- Tu conexión a internet funcione")
    
    finally:
        driver.close()
        print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    load_mioti_data() 
