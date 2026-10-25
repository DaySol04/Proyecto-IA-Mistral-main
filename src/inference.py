import argparse
import json
import time
import requests
import os
import pandas as pd

# URL de la API local de Ollama
OLLAMA_API = "http://localhost:11434/api/generate"

def medir_inferencia(modelo, prompt, temperatura, max_tokens):
    payload = {
        "model": modelo,
        "prompt": prompt,
        "temperature": temperatura,
        "stream": True,
        "options": {"num_predict": max_tokens}
    }
    
    start_time = time.time()
    ttft = None
    tokens_generados = 0
    respuesta_completa = ""
    
    try:
        with requests.post(OLLAMA_API, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        if ttft is None:
                            ttft = time.time() - start_time
                        respuesta_completa += chunk['response']
                        tokens_generados += 1
    except Exception as e:
        print(f"Error al conectar con Ollama: {e}")
        return None
    
    end_time = time.time()
    tiempo_total = end_time - start_time
    
    # Calculo de tokens/s
    tiempo_generacion = tiempo_total - ttft if ttft else tiempo_total
    tokens_por_segundo = tokens_generados / tiempo_generacion if tiempo_generacion > 0 else 0
    
    return {
        "modelo": modelo,                
        "temperatura": temperatura,
        "prompt": prompt,
        "respuesta": respuesta_completa.strip(),
        "ttft": round(ttft, 3) if ttft else None,
        "tokens_por_segundo": round(tokens_por_segundo, 2),
        "tiempo_total": round(tiempo_total, 3)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de inferencia para Ollama")
    parser.add_argument("--modelo", default="mistral", help="Nombre del modelo")
    parser.add_argument("--prompts", default="prompts/suite.json", help="Ruta al archivo JSON")
    parser.add_argument("--temperatura", type=float, default=0.7, help="Temperatura")
    parser.add_argument("--max_tokens", type=int, default=256, help="Máximo de tokens")
    parser.add_argument("--output", default="results/resultados.csv", help="Archivo CSV de salida")
    args = parser.parse_args()
    
    # Crear la carpeta results si no existe
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Leer el archivo suite.json
    with open(args.prompts, 'r', encoding='utf-8') as f:
        suite = json.load(f)
        
    resultados = []
    for item in suite:
        print(f"Ejecutando prompt ID {item['id']} ({item['categoria']})...")
        res = medir_inferencia(args.modelo, item['prompt'], args.temperatura, args.max_tokens)
        if res:
            res['id'] = item['id']
            res['categoria'] = item['categoria']
            resultados.append(res)
            print(f"  -> TTFT: {res['ttft']}s | Velocidad: {res['tokens_por_segundo']} tokens/s")
        else:
            print(f"  -> Falló el prompt ID {item['id']}")

    # Guardar resultados en el CSV
    df = pd.DataFrame(resultados)
    df.to_csv(args.output, index=False, encoding='utf-8')
    print(f"\n¡Listo! Resultados guardados exitosamente en {args.output}")