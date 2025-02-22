
---

# SynthECBE

El proyecto procesa documentos PDF extrayendo texto, fragmentándolo y generando incrustaciones vectoriales (embeddings) para habilitar búsquedas semánticas avanzadas.

## Tabla de Contenidos

- [Introducción](#introducción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Introducción

SynthECBE utiliza técnicas modernas de Procesamiento de Lenguaje Natural (NLP) y embeddings vectoriales para realizar búsquedas semánticas en una colección de documentos PDF. Gracias a Flask para el desarrollo de la API RESTful y PostgreSQL (con extensiones vectoriales) para el almacenamiento, SynthECBE ofrece una solución robusta y segura para la recuperación y consulta de documentos.

## Características

- **Búsqueda Semántica:** Permite realizar consultas en lenguaje natural y obtener resultados relevantes basados en la similitud vectorial.
- **Procesamiento de PDFs:** Extrae y fragmenta el texto de documentos PDF en párrafos para facilitar la indexación y búsqueda.
- **API REST:** Desarrollada con Flask, proporcionando endpoints para el procesamiento de documentos y búsquedas.
- **Seguridad en la Base de Datos:** Utiliza PostgreSQL con políticas de seguridad a nivel de fila (RLS) para proteger los datos.
- **Arquitectura Extensible:** Fácil integración de nuevos modelos y ampliación de funcionalidades.

## Instalación

### Requisitos Previos

- Python 3.9 o superior
- PostgreSQL 12 o superior (con la extensión vector instalada, por ejemplo [pgvector](https://github.com/pgvector/pgvector))
- pip

### Clonar el Repositorio

```bash
git clone https://github.com/brrodriguezd/SynthECBE-Backend
cd SynthECBE
```

### Configurar el Entorno Virtual

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: venv\Scripts\activate
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y añade las variables de configuración necesarias, por ejemplo:

```env
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_JWT_SECRET=
```

## Uso

### Ejecutar la Aplicación

Inicia el servidor de desarrollo de Flask con el siguiente comando:

```bash
flask --app main run
```

La aplicación estará disponible en `http://localhost:5000`.

### Procesamiento de PDFs

Envía un documento PDF (o la ruta al archivo) al endpoint correspondiente. El sistema extraerá el texto, lo fragmentará en párrafos y lo indexará para que esté disponible en la búsqueda semántica.

## Endpoints de la API

Esta documentación actualizada asume que el endpoint ha sido modificado para aceptar archivos a través de la clave `pdf_file` en lugar de un JSON con la clave `pdf_content`. Asegúrate de que el código de tu endpoint en Flask procese correctamente las peticiones de tipo `multipart/form-data` y extraiga el archivo enviado.
- **POST /process_pdf**
  Procesa un documento PDF y lo sube a la base de datos.
  **Parametros**
  - pdf_file (archivo):
  El documento PDF que se desea procesar. Este archivo debe enviarse en la petición utilizando el formato multipart/form-data.
  Ejemplo de Solicitud con cURL:
  ```bash
  curl -X POST "http://localhost:5000/process_pdf" \
    -H "accept: application/json" \
    -H "Content-Type: multipart/form-data" \
    -F "pdf_file=@/ruta/al/archivo.pdf"
  ```
- **POST /semantic_search**
  Realiza una búsqueda semántica en los documentos procesados.
  **Cuerpo de la solicitud (JSON):**
  ```json
  {
    "query": "Tu consulta de búsqueda",
    "threshold": 0.7,    // opcional
    "limit": 5           // opcional
  }
  ```
  **Respuesta:**
  ```json
  {
    "results": [
      {
        "id": "uuid_del_fragmento",
        "content": "Texto coincidente",
        "document_id": "uuid_del_documento",
        "filename": "archivo.pdf",
        "similarity": 0.85
      },
      ...
    ]
  }
  ```

- **GET /documents**
  Recupera una lista de documentos procesados.

## Configuración de la Base de Datos

### Creación de la Base de Datos

El archivo SQL está en la carpeta `sql`. Puedes ejecutarlo en tu base de datos para configurar el esquema y las políticas de seguridad.

```sql
/db/config.sql
```

### Uso de la Extensión Vectorial

Verifica que la extensión [pgvector](https://github.com/pgvector/pgvector) esté instalada y configurada en tu base de datos, ya que se utilizará para almacenar e indexar los embeddings vectoriales.

## Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
