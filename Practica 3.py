import os
import re

# Función para extraer el año
def extract_year(file_content):
    match = re.search(r"Popularity in (\d{4})", file_content)
    if match:
        return match.group(1)
    return None

# Función para extraer nombres y rankings
def extract_names(file_content):
    # Encuentra todas las coincidencias de rank, boy_name, girl_name
    matches = re.findall(r"<tr align=\"right\"><td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>", file_content)
    return matches

# Función para crear un diccionario de nombres y rankings
def create_name_dict(matches):
    name_dict = {}
    for rank, boy_name, girl_name in matches:
        if boy_name not in name_dict:
            name_dict[boy_name] = rank
        if girl_name not in name_dict:
            name_dict[girl_name] = rank
    return name_dict

# Función para crear una lista de nombres ordenados alfabéticamente
def create_sorted_name_list(name_dict):
    return sorted(name_dict.keys())

# Función para crear la lista con formato específico
def create_year_name_list(year, name_dict):
    sorted_names = sorted(name_dict.items())
    name_list = [f"{name} {rank}" for name, rank in sorted_names]
    return [year] + name_list

# Procesar archivos HTML
def process_files(data_dir):
    results = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".html"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                year = extract_year(content)
                matches = extract_names(content)
                name_dict = create_name_dict(matches)
                sorted_names = create_sorted_name_list(name_dict)
                year_name_list = create_year_name_list(year, name_dict)
                
                # Imprimir resultados
                print(f"Año: {year}")
                print("Nombres ordenados alfabéticamente:", sorted_names[:10], "...")  # Mostrar los primeros 10
                print("Lista con formato:", year_name_list[:10], "...")
                
                # Guardar resultados para otros usos
                results.append((year, name_dict, sorted_names, year_name_list))
    return results

# Directorio de datos
data_dir = "../data"

# Procesar archivos
all_results = process_files(data_dir)

# Si quieres guardar los resultados en un archivo
for year, name_dict, sorted_names, year_name_list in all_results:
    output_file = f"output_{year}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(year_name_list))
    print(f"Guardado en {output_file}")
