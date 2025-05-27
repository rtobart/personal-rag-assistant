# 🧠 Asistente Personal con IA Generativa: RAG + Notion + Qdrant

**Duración:** 2 horas  
**Nivel:** Intermedio  
**Requisitos:**
- Python 3.11+ instalado
- Cuenta en Notion
- Cuenta en Qdrant Cloud (gratuita)
- API Key de OpenAI, OpenRouter o acceso a Vertex AI

---

## � Objetivo del Taller

Construir un **asistente personal inteligente** que puede consultar tu información de Notion usando tecnología RAG (Retrieval-Augmented Generation), proporcionando respuestas contextualizadas basadas en tu propia base de conocimiento.

---

## 🧩 ¿Qué es RAG y por qué es importante?

**RAG (Retrieval-Augmented Generation)** es una técnica que combina:
- **Recuperación**: Buscar información relevante en una base de datos
- **Generación**: Usar un LLM para crear respuestas contextualizadas

### 🚀 Ventajas del RAG:
- ✅ **Información actualizada**: No limitado al entrenamiento del modelo
- ✅ **Respuestas precisas**: Basadas en datos específicos del usuario
- ✅ **Transparencia**: Se puede rastrear la fuente de la información
- ✅ **Personalización**: Adaptado a tu contenido personal
- ✅ **Costo-efectivo**: No requiere reentrenamiento de modelos

---

## 🔧 Arquitectura del Sistema

```
[Notion] → [Extracción] → [Chunks] → [Embeddings] → [Qdrant DB]
                                                           ↓
[Usuario] → [Pregunta] → [RAG Pipeline] → [LLM] → [Respuesta]
```

---

## 📚 Agenda del Taller (2 horas)

| Tiempo     | Contenido                                                        |
|------------|------------------------------------------------------------------|
| 0:00-0:20  | **Introducción**: ¿Qué es RAG? Ventajas y casos de uso         |
| 0:20-0:50  | **Extracción de Notion**: API, estructura de datos, chunking   |
| 0:50-1:20  | **Base de Datos Vectorial**: ¿Qué es? Configuración de Qdrant |
| 1:20-1:45  | **LLM como Servicio**: OpenAI, OpenRouter, Vertex AI          |
| 1:45-2:00  | **Demo y Conexiones**: Configurar cuentas personales          |

---

## 📖 Conceptos Clave

### 🗃️ ¿Qué es una Base de Datos Vectorial?

Una **base de datos vectorial** almacena información como vectores numéricos (embeddings) que representan el significado semántico del texto.

**¿Por qué Qdrant?**
- 🔥 Alto rendimiento
- 🌐 API REST fácil de usar
- ☁️ Versión cloud gratuita
- 🔍 Búsqueda semántica avanzada
- 📊 Filtros y metadatos

### 🤖 LLM como Servicio

En lugar de ejecutar modelos localmente, usamos APIs de proveedores:

**Opciones soportadas:**
- **OpenAI**: GPT-4, GPT-3.5 (más conocido)
- **OpenRouter**: Acceso a múltiples modelos (económico)
- **Vertex AI**: Modelos de Google (Gemini)
- **Ollama**: Modelos locales (privacidad)

---

## 🛠️ Configuración Inicial

### 1. Clona el repositorio
```bash
git clone <tu-repo>
cd personal-rag-assistant
```

### 2. Instala dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

### 4. Ejecuta el servidor
```bash
python run.py
```

---

## 📝 Extracción de Información de Notion

### Configuración de Notion API

1. **Crear integración en Notion**:
   - Ve a [developers.notion.com](https://developers.notion.com)
   - Crea una nueva integración
   - Copia el token de API

2. **Compartir página con la integración**:
   - Abre tu página de Notion
   - Clic en menu de tres puntos (...) en la esquina superior derecha
   - Selecciona "Conexiones"
   - Busca tu integración y dale acceso

3. **Configurar en el código**:
```python
# En .env
NOTION_API_KEY=tu_token_aqui
NOTION_PAGE_ID=id_de_tu_pagina
```

### Cómo funciona la extracción

El servicio [`NotionService`](app/services/notion_service.py) extrae contenido de manera recursiva:
- 📄 Obtiene todos los bloques de una página
- 🔄 Procesa bloques anidados recursivamente
- 📝 Extrae texto plano de diferentes tipos de contenido
- 📊 Mantiene metadatos para trazabilidad

---

## �️ Configuración de Qdrant

### 1. Crear cuenta en Qdrant Cloud
- Ve a [cloud.qdrant.io](https://cloud.qdrant.io)
- Crea una cuenta gratuita
- Obtén tu API key y URL del cluster

### 2. Configuración en el proyecto
```python
# En .env
QDRANT_HOST=tu-cluster-url
QDRANT_PORT=6333
QDRANT_API_KEY=tu_api_key
```

### 3. Cómo funciona el almacenamiento vectorial

1. **Chunking**: Dividimos el texto en fragmentos manejables
2. **Embeddings**: Convertimos texto a vectores con modelos de embeddings
3. **Almacenamiento**: Guardamos vectores + metadatos en Qdrant
4. **Búsqueda**: Encontramos fragmentos similares usando distancia coseno

---

## 🚀 Uso del Sistema

### 1. Cargar datos desde Notion
```bash
POST /personal-assistant/api/v1/agent/bulk-insert
{
  "collection_name": "notion",
  "embedding_algorithm": "sentence-transformer"
}
```

### 2. Hacer una consulta
```bash
POST /personal-assistant/api/v1/agent/inference
{
  "text": "¿Qué proyectos tengo pendientes?",
  "embeddingAlgorithm": "sentence-transformer",
  "vectorsTopK": 5,
  "llmAgentDescription": "base64_encoded_instructions",
  "modelProvider": "openrouter"
}
```

---

## � Componentes Principales

### Pipeline RAG
El flujo principal se maneja en [`AgentChatServices`](app/services/agent_chat_services.py):
1. **Pre-inferencia**: Busca vectores similares con [`PreHookService`](app/services/pre_hook_service.py)
2. **Contextualización**: Crea prompt con contexto usando [`ContexChatbotService`](app/services/contex_chatbot.py)
3. **Generación**: Envía a LLM usando [`AIFactory`](app/factory/ai_factory.py)

### Procesamiento de Datos
- **Chunking**: [`DataProcessor`](app/services/data_processing.py) divide texto en fragmentos
- **Embeddings**: [`EmbeddingProcess`](app/services/embeddings_service.py) convierte texto a vectores
- **Almacenamiento**: [`VectorDBServiceQdrant`](app/services/vector_db_service_qdrant.py) maneja Qdrant

---

## 🎯 Demo y Configuración Personal

### Conecta tu Notion:
1. Sigue los pasos de configuración de Notion API
2. Actualiza tu archivo `.env`
3. Ejecuta el endpoint de bulk-insert

### Conecta tu Qdrant:
1. Crea tu cluster en Qdrant Cloud
2. Actualiza las credenciales en `.env`
3. El sistema creará automáticamente las colecciones

### Elige tu LLM:
- Para **OpenRouter**: Obtén API key en [openrouter.ai](https://openrouter.ai)
- Para **OpenAI**: Usa tu API key existente
- Para **Vertex AI**: Configura autenticación de Google Cloud

---

## � Estructura del Proyecto

```
personal-rag-assistant/
├── app/
│   ├── controllers/          # Endpoints de la API
│   ├── services/            # Lógica de negocio
│   │   ├── notion_service.py       # Extracción de Notion
│   │   ├── agent_chat_services.py  # Pipeline RAG principal
│   │   └── pre_hook_service.py     # Búsqueda vectorial
│   ├── database/            # Conexión a Qdrant
│   ├── facade/             # Integraciones con LLMs
│   └── models/             # Modelos de datos
├── run.py                  # Servidor principal
└── requirements.txt        # Dependencias
```

---

## 🎉 Conclusiones y Próximos Pasos

### ✅ Lo que hemos logrado:
- **Sistema RAG funcional** que consulta tu información personal
- **Integración con Notion** para extraer conocimiento
- **Base vectorial** para búsqueda semántica eficiente
- **Flexibilidad** para usar diferentes proveedores de LLM

### 🚀 Extensiones posibles:
- 📱 **Interfaz web** con Streamlit o React
- 📚 **Más fuentes**: Google Drive, Obsidian, PDFs
- 🔒 **Modelos locales** para mayor privacidad
- 🤖 **Agentes especializados** por tipo de consulta
- 📊 **Analytics** de uso y efectividad

### 💡 Casos de uso reales:
- **Asistente de productividad personal**
- **Base de conocimiento empresarial**
- **Tutor personalizado** basado en tus notas
- **Organizador de ideas y proyectos**

---

## 🔗 Recursos Útiles

- [Documentación de Notion API](https://developers.notion.com/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenRouter Models](https://openrouter.ai/models)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)

---

**¡Felicidades!** 🎉 Ahora tienes tu propio asistente personal con IA que puede consultar tu información de Notion y responder preguntas contextualizadas.