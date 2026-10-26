import pandas as pd
import glob
import os

def calcular_metricas(patron_archivos, nombre_configuracion):
    # Buscar todos los archivos que coincidan con el patrón
    archivos = glob.glob(patron_archivos)
    
    if not archivos:
        print(f"⚠️ No se encontraron archivos para {nombre_configuracion}")
        return

    # Leer y unir todos los archivos en una sola tabla
    dfs = [pd.read_csv(archivo) for archivo in archivos]
    df_total = pd.concat(dfs, ignore_index=True)

    # Calcular promedios y desviaciones estándar
    ttft_promedio = df_total['ttft'].mean()
    ttft_desviacion = df_total['ttft'].std()
    tokens_promedio = df_total['tokens_por_segundo'].mean()
    tokens_desviacion = df_total['tokens_por_segundo'].std()

    print(f"\n📊 --- Resultados para {nombre_configuracion} ---")
    print(f"Archivos analizados: {len(archivos)} (Total de respuestas: {len(df_total)})")
    print(f"🔹 TTFT Promedio: {ttft_promedio:.3f} s  (Desviación Estándar: {ttft_desviacion:.3f})")
    print(f"🔹 Tokens/s Promedio: {tokens_promedio:.3f}  (Desviación Estándar: {tokens_desviacion:.3f})")

if __name__ == "__main__":
    print("Iniciando análisis de desempeño...")
    
    # Analizar los archivos de Windows
    calcular_metricas('results/nativo_*.csv', 'Nativo (Windows)')
    
    # Analizar los archivos de Docker
    calcular_metricas('results/docker_*.csv', 'Docker')