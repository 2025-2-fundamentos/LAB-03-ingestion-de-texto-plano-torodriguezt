"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd
    import re
    
    # Read the file
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Initialize lists to store data
    clusters = []
    cantidad_palabras = []
    porcentajes = []
    palabras_clave = []
    
    # Find the separator line
    i = 0
    while i < len(lines):
        if '---' in lines[i]:
            i += 1
            break
        i += 1
    
    # Parse the data
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a cluster line (starts with a number)
        match = re.match(r'^\s+(\d+)\s+(\d+)\s+([\d,]+)\s+%\s+(.+)', line)
        
        if match:
            # Save previous cluster if exists
            if current_cluster is not None:
                clusters.append(current_cluster)
                cantidad_palabras.append(current_cantidad)
                porcentajes.append(current_porcentaje)
                # Clean up keywords
                keywords_text = ' '.join(current_keywords)
                keywords_text = re.sub(r'\s+', ' ', keywords_text)
                keywords_text = re.sub(r'\s*,\s*', ', ', keywords_text)
                keywords_text = keywords_text.strip().rstrip('.')
                palabras_clave.append(keywords_text)
            
            # Start new cluster
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            current_porcentaje = float(match.group(3).replace(',', '.'))
            current_keywords = [match.group(4).strip()]
        
        elif line.strip() and current_cluster is not None:
            # This is a continuation of keywords
            current_keywords.append(line.strip())
        
        elif not line.strip() and current_cluster is not None:
            # Empty line might indicate end of current cluster
            pass
        
        i += 1
    
    # Don't forget the last cluster
    if current_cluster is not None:
        clusters.append(current_cluster)
        cantidad_palabras.append(current_cantidad)
        porcentajes.append(current_porcentaje)
        keywords_text = ' '.join(current_keywords)
        keywords_text = re.sub(r'\s+', ' ', keywords_text)
        keywords_text = re.sub(r'\s*,\s*', ', ', keywords_text)
        keywords_text = keywords_text.strip().rstrip('.')
        palabras_clave.append(keywords_text)
    
    # Create DataFrame
    df = pd.DataFrame({
        'cluster': clusters,
        'cantidad_de_palabras_clave': cantidad_palabras,
        'porcentaje_de_palabras_clave': porcentajes,
        'principales_palabras_clave': palabras_clave
    })
    
    return df
