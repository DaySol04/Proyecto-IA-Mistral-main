FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 appuser

# Crear la carpeta results y darle permisos al usuario
RUN mkdir -p results && chown appuser:appuser results

USER appuser

COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser prompts/ ./prompts/

ENTRYPOINT ["python", "src/inference.py"]