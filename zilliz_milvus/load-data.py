#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cargador de muestra de productos de moda Flipkart para Milvus (2000 productos)
Este script carga una muestra del dataset JSON de productos de moda en Milvus
"""

import json
import pandas as pd
from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema
# Importación correcta para el módulo model
from pymilvus.model import DefaultEmbeddingFunction
import re
from typing import List, Dict, Any
from tqdm import tqdm
import time

class MilvusFashionLoaderSample:
    def __init__(self, cluster_endpoint: str, token: str):
        """
        Inicializa el cargador con las credenciales de Milvus
        
        Args:
            cluster_endpoint: URL del cluster de Milvus
            token: Token de autenticación
        """
        self.client = MilvusClient(uri=cluster_endpoint, token=token)
        self.embedding_fn = DefaultEmbeddingFunction()
        self.collection_name = "flipkart_fashion_sample"
        
    def clean_text(self, text: str) -> str:
        """
        Limpia y normaliza el texto para mejor procesamiento
        
        Args:
            text: Texto a limpiar
            
        Returns:
            Texto limpio
        """
        if not text or pd.isna(text):
            return ""
        
        # Convertir a string si no lo es
        text = str(text)
        
        # Remover caracteres especiales y normalizar espacios
        text = re.sub(r'\s+', ' ', text)  # Múltiples espacios a uno solo
        text = re.sub(r'[^\w\s\-\.,!?()]', ' ', text)  # Remover caracteres especiales
        text = text.strip()
        
        return text
    
    def parse_price(self, price_str: str) -> float:
        """
        Convierte string de precio a float
        
        Args:
            price_str: String del precio (ej: "2,999")
            
        Returns:
            Precio como float
        """
        if not price_str or pd.isna(price_str):
            return 0.0
        
        # Remover comas y convertir a float
        try:
            return float(str(price_str).replace(',', ''))
        except:
            return 0.0
    
    def parse_rating(self, rating_str: str) -> float:
        """
        Convierte string de rating a float
        
        Args:
            rating_str: String del rating
            
        Returns:
            Rating como float
        """
        if not rating_str or pd.isna(rating_str):
            return 0.0
        
        try:
            return float(rating_str)
        except:
            return 0.0
    
    def extract_product_details(self, product_details: List[Dict]) -> str:
        """
        Extrae detalles del producto como texto concatenado
        
        Args:
            product_details: Lista de diccionarios con detalles
            
        Returns:
            String con todos los detalles concatenados
        """
        if not product_details:
            return ""
        
        details = []
        for detail_dict in product_details:
            if isinstance(detail_dict, dict):
                for key, value in detail_dict.items():
                    details.append(f"{key}: {value}")
        
        return " | ".join(details)
    
    def prepare_data_batch(self, products: List[Dict[str, Any]], start_id: int = 0) -> List[Dict[str, Any]]:
        """
        Prepara un lote de productos para inserción en Milvus
        
        Args:
            products: Lista de productos del dataset
            start_id: ID inicial para este lote
            
        Returns:
            Lista de productos preparados para Milvus
        """
        prepared_data = []
        
        # Preparar textos para vectorización
        texts_for_embedding = []
        for product in products:
            title = self.clean_text(product.get('title', ''))
            description = self.clean_text(product.get('description', ''))
            product_details = self.extract_product_details(product.get('product_details', []))
            
            # Combinar título, descripción y detalles para mejor representación vectorial
            combined_text = f"{title}. {description}. {product_details}"
            texts_for_embedding.append(combined_text)
        
        # Generar embeddings
        print("Generando embeddings vectoriales...")
        vectors = self.embedding_fn.encode_documents(texts_for_embedding)
        
        # Preparar datos estructurados
        for i, product in enumerate(products):
            try:
                prepared_item = {
                    "id": start_id + i,  # ID secuencial para Milvus
                    "vector": vectors[i],
                    "product_id": product.get('_id', ''),
                    "pid": product.get('pid', ''),
                    "title": self.clean_text(product.get('title', ''))[:500],  # Limitar longitud
                    "description": self.clean_text(product.get('description', ''))[:1000],  # Limitar longitud
                    "brand": self.clean_text(product.get('brand', ''))[:100],
                    "category": self.clean_text(product.get('category', ''))[:100],
                    "sub_category": self.clean_text(product.get('sub_category', ''))[:100],
                    "actual_price": self.parse_price(product.get('actual_price', 0)),
                    "selling_price": self.parse_price(product.get('selling_price', 0)),
                    "discount": self.clean_text(product.get('discount', ''))[:50],
                    "average_rating": self.parse_rating(product.get('average_rating', 0)),
                    "seller": self.clean_text(product.get('seller', ''))[:100],
                    "out_of_stock": bool(product.get('out_of_stock', False)),
                    "product_details": self.extract_product_details(product.get('product_details', []))[:500],
                    "crawled_at": product.get('crawled_at', ''),
                    "url": product.get('url', '')[:500]  # Limitar longitud de URL
                }
                prepared_data.append(prepared_item)
            except Exception as e:
                print(f"Error procesando producto {i}: {e}")
                continue
        
        return prepared_data
    
    def create_collection(self):
        """
        Crea la colección en Milvus con el esquema apropiado
        """
        # Eliminar colección existente si existe
        if self.client.has_collection(collection_name=self.collection_name):
            print(f"Eliminando colección existente: {self.collection_name}")
            self.client.drop_collection(collection_name=self.collection_name)
        
        # Crear nueva colección con dimensión de 768 (default del modelo de embeddings)
        print(f"Creando colección: {self.collection_name}")
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=768,  # Dimensión del modelo de embeddings
            metric_type="COSINE",  # Métrica de similitud coseno
            primary_field_name="id",
            vector_field_name="vector"
        )
        
        print(f"Colección '{self.collection_name}' creada exitosamente!")
    
    def load_sample_dataset(self, dataset_path: str, sample_size: int = 2000, batch_size: int = 100):
        """
        Carga una muestra del dataset en Milvus
        
        Args:
            dataset_path: Ruta al archivo JSON del dataset
            sample_size: Número de productos a cargar (default: 2000)
            batch_size: Tamaño del lote para procesamiento
        """
        print(f"Cargando muestra de {sample_size} productos desde: {dataset_path}")
        
        # Cargar datos del JSON
        with open(dataset_path, 'r', encoding='utf-8') as f:
            all_products = json.load(f)
        
        # Tomar solo una muestra
        products = all_products[:sample_size]
        print(f"Total de productos a cargar: {len(products)} de {len(all_products)} disponibles")
        
        # Crear colección
        self.create_collection()
        
        # Procesar en lotes
        total_inserted = 0
        
        for i in tqdm(range(0, len(products), batch_size), desc="Cargando datos"):
            batch = products[i:i + batch_size]
            
            # Preparar datos del lote
            prepared_batch = self.prepare_data_batch(batch, start_id=total_inserted)
            
            if prepared_batch:
                try:
                    # Insertar en Milvus
                    res = self.client.insert(
                        collection_name=self.collection_name,
                        data=prepared_batch
                    )
                    total_inserted += len(prepared_batch)
                    print(f"Lote insertado. Total insertados: {total_inserted}")
                    
                except Exception as e:
                    print(f"Error insertando lote {i//batch_size + 1}: {e}")
                    continue
            
            # Pequeña pausa para no sobrecargar el sistema
            time.sleep(0.1)
        
        print(f"\n¡Carga completada! Total de productos insertados: {total_inserted}")
        
        # Crear índice para mejorar rendimiento de búsqueda
        print("Creando índice para optimizar búsquedas...")
        try:
            self.client.create_index(
                collection_name=self.collection_name,
                field_name="vector",
                index_type="IVF_FLAT",
                params={"nlist": 128}  # Menor para dataset más pequeño
            )
            print("Índice creado exitosamente!")
        except Exception as e:
            print(f"Advertencia: No se pudo crear el índice: {e}")
    
    def search_products(self, query: str, limit: int = 10, filters: str = None):
        """
        Busca productos similares basado en una consulta de texto
        
        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            filters: Filtros adicionales (opcional)
            
        Returns:
            Resultados de búsqueda
        """
        print(f"Buscando: '{query}'")
        
        # Generar vector de la consulta
        query_vector = self.embedding_fn.encode_queries([query])
        
        # Realizar búsqueda
        results = self.client.search(
            collection_name=self.collection_name,
            data=query_vector,
            limit=limit,
            filter=filters,
            output_fields=["title", "description", "brand", "category", "selling_price", "average_rating"]
        )
        
        return results
    
    def get_collection_stats(self):
        """
        Obtiene estadísticas de la colección
        """
        try:
            # Obtener información básica
            if self.client.has_collection(self.collection_name):
                # Contar total de elementos
                total_count = self.client.query(
                    collection_name=self.collection_name,
                    filter="id >= 0",
                    output_fields=["id"]
                )
                
                print(f"Colección: {self.collection_name}")
                print(f"Total de productos: {len(total_count) if total_count else 0}")
                print(f"Dimensión de vectores: 768")
                
            else:
                print(f"La colección '{self.collection_name}' no existe")
                
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")


def main():
    """
    Función principal para ejecutar la carga de datos
    """
    print("🚀 CARGADOR DE MUESTRA DE PRODUCTOS DE MODA")
    print("=" * 50)
    print("Cargando solo 2000 productos para pruebas rápidas")
    print("=" * 50)
    
    # Configuración de Milvus (usar las mismas credenciales del notebook)
    CLUSTER_ENDPOINT = "https://in03-fc51ec1067f53e7.serverless.gcp-us-west1.cloud.zilliz.com"
    TOKEN = "e1a5f13be33e07ef22a239ffbc7ddffb08ada6250f4c7edfa0221784b304ac41627ed2db02a0e8be6e26c4e2f6b0db0d2ba2da09"
    
    # Ruta del dataset
    DATASET_PATH = "./flipkart_fashion_products_dataset_2k.json"
    
    # Crear cargador
    loader = MilvusFashionLoaderSample(CLUSTER_ENDPOINT, TOKEN)
    
    try:
        # Cargar muestra de 2000 productos
        loader.load_sample_dataset(DATASET_PATH, sample_size=2000, batch_size=50)
        
        # Mostrar estadísticas
        loader.get_collection_stats()
        
        # Ejemplo de búsqueda
        print("\n" + "="*60)
        print("EJEMPLO DE BÚSQUEDA")
        print("="*60)
        
        results = loader.search_products("camiseta azul para hombre", limit=3)
        
        print("\nResultados de búsqueda para 'camiseta azul para hombre':")
        for i, result in enumerate(results[0], 1):
            product = result['entity']
            print(f"\n{i}. {product['title']}")
            print(f"   Marca: {product['brand']}")
            print(f"   Categoría: {product['category']}")
            print(f"   Precio: ${product['selling_price']}")
            print(f"   Rating: {product['average_rating']}")
            print(f"   Similitud: {1 - result['distance']:.4f}")
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        raise


if __name__ == "__main__":
    main() 