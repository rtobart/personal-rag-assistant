# 🧠 Taller: Crea tu propio Asistente Personal con IA Generativa (RAG + Notion + Obsidian)

**Duración:** 3 horas  
**Nivel:** Intermedio (nociones básicas de programación)  
**Requisitos:**
- Python instalado
- Cuenta en OpenAI
- Cuenta en Notion
- Obsidian instalado

---

## 🌟 Objetivo

Guiar a les participantes en la creación de un chatbot personalizado con capacidades de **Recuperación Aumentada por Generación (RAG)**, capaz de integrarse con herramientas de notas como **Notion** y **Obsidian**.

Al finalizar, cada asistente tendrá su propio wrapper de IA generativa que puede consultar su información personal, tomar notas, organizar ideas y responder preguntas como un asistente real.

---

## 🧹 ¿Qué vamos a construir?

Un **chatbot local o deployable** que:

- Se conecta a fuentes personales de conocimiento (Notion y Obsidian).
- Usa un pipeline RAG para responder preguntas con contexto real del usuario.
- Funciona como asistente personal para tareas diarias.

---

## 🔧 Tecnologías que usaremos

- Python
- LangChain o LlamaIndex
- OpenAI API (u otro modelo generativo)
- API de Notion
- Lectura de archivos Markdown (Obsidian)
- FastAPI o Streamlit (opcional para la interfaz)

---

## 🧠 Contenido del taller (3 horas)

| Tiempo        | Contenido                                                            |
|---------------|----------------------------------------------------------------------|
| 0:00 - 0:15    | Introducción a RAG y asistentes personales                          |
| 0:15 - 0:45    | Setup del entorno y explicación de arquitectura                     |
| 0:45 - 1:30    | Integración con Notion y Obsidian (extracción de datos)             |
| 1:30 - 2:15    | Implementación del motor RAG con búsqueda semántica                 |
| 2:15 - 2:45    | Creación de la interfaz del chatbot (CLI o web)                     |
| 2:45 - 3:00    | Demo final, feedback y próximos pasos                               |

---

## 💡 ¿Qué se llevan les participantes?

- Un asistente personalizado que consulta su base de conocimiento.
- Código reutilizable y extendible.
- Bases para crear herramientas de productividad con IA.

---

## 🚀 Próximos pasos sugeridos

- Añadir más fuentes (Google Drive, Gmail, RSS, etc.)
- Usar modelos locales para mayor privacidad
- Convertir el asistente en una app móvil o web

---

## 📂 Estructura sugerida del repositorio

```
personal-ai-assistant/
│
├── data_sources/
│   ├── notion_client.py
│   └── obsidian_parser.py
│
├── rag_engine/
│   ├── retriever.py
│   └── generator.py
│
├── interface/
│   ├── cli.py
│   └── web_app.py
│
├── main.py
└── README.md
```

---