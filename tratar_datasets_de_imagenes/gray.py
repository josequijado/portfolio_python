import os
import shutil
from PIL import Image
import logging

# Configuración del logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

# Variables de configuración
ORIGINALS_DIR = "originales_resized"  # Nombre de la carpeta principal
SUBFOLDERS = ["train", "valid"]  # Subcarpetas de primer nivel
RESIZED_SUFFIX = "_grayscale"  # Sufijo para la carpeta de destino
OUTPUT_FORMAT = "png"  # Formato de las imágenes de salida (jpg, png, gif, bmp)

def convert_to_grayscale(image_path, output_path, output_format):
    """Convierte una imagen a escala de grises y la guarda en la ruta especificada."""
    try:
        with Image.open(image_path) as img:
            grayscale_img = img.convert("L")
            if output_format.lower() in ['jpg', 'jpeg']:
                grayscale_img = grayscale_img.convert("RGB")  # Convertir a RGB si el formato es JPG/JPEG
            output_path = os.path.splitext(output_path)[0] + f".{output_format}"
            grayscale_img.save(output_path, format=output_format.upper())
    except Exception as e:
        logging.error(f"Error al procesar {image_path}: {e}")

def process_directory(source_dir, dest_dir, output_format):
    """Procesa recursivamente una carpeta, convirtiendo imágenes a escala de grises y replicando la estructura de directorios."""
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(dest_dir, relative_path)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                source_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_path, file)
                convert_to_grayscale(source_file_path, dest_file_path, output_format)

def main(originals_dir, subfolders, resized_suffix, output_format):
    """Función principal que coordina el proceso."""
    if os.path.exists(originals_dir):
        dest_directory = f"{originals_dir}{resized_suffix}"
        if os.path.exists(dest_directory):
            shutil.rmtree(dest_directory)
        os.makedirs(dest_directory)

        for subfolder in subfolders:
            source_subfolder_path = os.path.join(originals_dir, subfolder)
            dest_subfolder_path = os.path.join(dest_directory, subfolder)

            if os.path.exists(source_subfolder_path):
                print(f"Procesando {source_subfolder_path}...")
                process_directory(source_subfolder_path, dest_subfolder_path, output_format)
            else:
                logging.error(f"La subcarpeta {source_subfolder_path} no existe.")
    else:
        logging.error(f"La carpeta {originals_dir} no existe.")

if __name__ == "__main__":
    # Ejecutar el script principal
    main(ORIGINALS_DIR, SUBFOLDERS, RESIZED_SUFFIX, OUTPUT_FORMAT)
