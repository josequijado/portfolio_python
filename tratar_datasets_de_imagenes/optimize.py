import os
from PIL import Image

def optimizar_imagen(input_path, output_path, formato_salida):
    try:
        with Image.open(input_path) as img:
            print(f"Abriendo imagen: {input_path}")
            # Convertir al formato de salida
            img = img.convert("RGB")
            
            if formato_salida.lower() == 'jpeg':
                # Guardar la imagen optimizada como JPEG
                img.save(output_path, format=formato_salida, optimize=True, quality=85)
            elif formato_salida.lower() == 'png':
                # Guardar la imagen optimizada como PNG
                img.save(output_path, format=formato_salida, optimize=True)
            
            print(f"Imagen guardada en {output_path} en formato {formato_salida}")
    except Exception as e:
        print(f"Error al procesar la imagen {input_path}: {e}")

def copiar_y_convertir_imagenes(ruta_origen, ruta_salida, formato_salida):
    for root, dirs, files in os.walk(ruta_origen):
        print(f"Recorriendo directorio: {root}")
        # Crear la estructura de directorios en la ruta de salida
        relative_path = os.path.relpath(root, ruta_origen)
        directorio_destino = os.path.join(ruta_salida, relative_path)
        os.makedirs(directorio_destino, exist_ok=True)
        
        for file in files:
            input_path = os.path.join(root, file)
            output_file = os.path.splitext(file)[0] + '.' + formato_salida.lower()
            output_path = os.path.join(directorio_destino, output_file)
            
            print(f"Procesando archivo: {input_path} -> {output_path}")
            
            # Convertir y optimizar la imagen
            optimizar_imagen(input_path, output_path, formato_salida)

# Establecer las variables
ruta_origen = "original"
formato_salida = "JPEG"  # Puede ser "JPEG", "PNG", etc.
ruta_salida = "optimizado"

# Verificar si las rutas de origen y salida existen
if not os.path.exists(ruta_origen):
    print(f"La ruta de origen '{ruta_origen}' no existe.")
elif not os.path.isdir(ruta_origen):
    print(f"La ruta de origen '{ruta_origen}' no es un directorio.")
else:
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)
    # Llamar a la función para copiar y convertir las imágenes
    copiar_y_convertir_imagenes(ruta_origen, ruta_salida, formato_salida)
