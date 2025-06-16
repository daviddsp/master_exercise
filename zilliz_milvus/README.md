# 🛍️ Base de Datos Vectorial de Productos de Moda - Milvus

Esta carpeta contiene scripts para crear y usar una base de datos vectorial con productos de moda usando **Milvus** y **embeddings semánticos**.

## 📋 Requisitos

```bash
# Activar entorno mioti_env
conda activate mioti_env

# Instalar dependencias
pip install pymilvus-model tqdm pandas
```

## 📁 Archivos Incluidos

- **`load-data.py.py`** - Carga **2000 productos** (recomendado para pruebas)
- **`P4. Zilliz (Milvus).ipynb`** - Contiene el codigo para conectarse a Milvus y realizar búsquedas

## 🚀 Uso Rápido

### Paso 1: Cargar datos (solo 2000 productos - recomendado si se quiere en un nuevo entorno)

```bash
cd master_exercise/zilliz_milvus/README.md
python load-data.py
```

**Tiempo estimado**: 3-5 minutos


## 🔍 Ejemplos de Búsqueda

Una vez cargados los datos, puedes realizar búsquedas semánticas como:

```python
from pymilvus import MilvusClient
from pymilvus_model import DefaultEmbeddingFunction

client = MilvusClient(uri="...", token="...")
embedding_fn = DefaultEmbeddingFunction()

# Búsqueda básica
query_vector = embedding_fn.encode_queries(["camisa azul para hombre"])
results = client.search(
    collection_name="flipkart_fashion_sample",
    data=query_vector,
    limit=5,
    output_fields=["title", "brand", "selling_price"]
)
```

## 🎯 Tipos de Búsqueda Soportados

### 1. Búsqueda Semántica
- "ropa casual para hombre"
- "zapatos deportivos para correr"
- "vestido elegante para fiesta"

### 2. Búsqueda con Filtros
```python
# Solo productos baratos
search_products("camiseta", filters="selling_price < 500")

# Solo productos bien valorados
search_products("zapatos", filters="average_rating > 4.0")

# Solo productos disponibles
search_products("jeans", filters="out_of_stock == false")
```

### 3. Filtros Combinados
```python
search_products(
    "vestido", 
    filters="selling_price < 1000 and average_rating > 4.0"
)
```

## ⚙️ Configuración

Los scripts están configurados para usar:
- **Cluster**: Milvus Cloud (credenciales incluidas)
- **Modelo de embeddings**: sentence-transformers (768 dimensiones)
- **Métrica**: Similitud coseno
- **Dataset**: 30K productos de moda de Flipkart

## 📊 Estadísticas del Dataset

- **Total productos**: 30,000
- **Campos principales**: título, descripción, marca, categoría, precio, rating
- **Categorías**: Ropa, zapatos, accesorios
- **Marcas**: Nike, Adidas, Puma, y muchas más

## 🔧 Solución de Problemas

### Error de importación `model`
```bash
pip install pymilvus-model
```

### Error de conexión
Verifica que las credenciales de Milvus sean correctas en los scripts.

### Memoria insuficiente
Usa `milvus_fashion_loader_sample.py` en lugar del loader completo.

## 💡 Consejos

1. **Empezar con muestra**: Usa siempre el script de muestra (2000 productos) para pruebas
2. **Búsquedas semánticas**: No necesitas palabras exactas, la búsqueda entiende el contexto
3. **Filtros**: Combina búsqueda semántica con filtros estructurados para mejores resultados
4. **Experimentar**: Prueba diferentes tipos de consultas para ver la potencia del sistema

## 📈 Rendimiento

- **Muestra (2000 productos)**: ~3-5 minutos de carga
- **Dataset completo (30K)**: ~15-30 minutos de carga
- **Búsquedas**: < 1 segundo por consulta
- **Memoria**: ~2-4 GB para el dataset completo 