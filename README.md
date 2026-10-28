# Proyecto de Investigación: Inferencia Local con Mistral AI

Este proyecto implementa la ejecución local del modelo de lenguaje Mistral 7B utilizando Ollama y Python, empaquetado en un contenedor Docker para garantizar su reproducibilidad.

## Requisitos previos
* Tener instalado [Ollama](https://ollama.com/).
* Tener instalado Python 3.11 o superior.
* Tener instalado Docker Desktop (opcional, para ejecución en contenedor).

## 1. Descarga del modelo
Abre una terminal y ejecuta:
```bash
ollama run mistral

## 2. Clona el repositorio y navega a la carpeta del proyecto. Instala las dependencias de Python
pip install -r requirements.txt


## 3. Ejecuta el script de inferencia    Nota: Asegurarse de que Ollama esté corriendo en segundo plano.
python src/inference.py --modelo mistral --output results/nativo.csv

## 4. Contruir la imagen
docker build -t mistral-inference .    #El punto final es muy importante


## 5. Ejecuta el contenedor
docker run --rm -v "${PWD}/results:/app/results" mistral-inference --output results/docker.csv

## EJEMPLO DE SALIDA
Ejecutando prompt ID 1 (Generación de texto)...
  -> TTFT: 0.614s | Velocidad: 15.11 tokens/s
...
¡Listo! Resultados guardados exitosamente en results/nativo.csv

***


