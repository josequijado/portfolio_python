from PIL import Image, ImageEnhance, ImageOps
import os
import random
import numpy as np
import struct  # Importar el módulo struct

# Función para rotar la imagen en los tres ejes cartesianos
def rotate_image(image):
    rotated_images = []
    # Rotaciones en el eje X
    for angle_x in [0, 90, 180, 270]:
        rotated_x = image.rotate(angle_x, expand=True)
        rotated_images.append(rotated_x)
    # Rotaciones en el eje Y
    for angle_y in [0, 90, 180, 270]:
        rotated_y = image.transpose(Image.FLIP_LEFT_RIGHT).rotate(angle_y, expand=True)
        rotated_images.append(rotated_y)
    # Rotaciones en el eje Z
    for angle_z in [0, 90, 180, 270]:
        rotated_z = image.transpose(Image.FLIP_TOP_BOTTOM).rotate(angle_z, expand=True)
        rotated_images.append(rotated_z)
    return rotated_images

# Función para aplicar el volteo horizontal y vertical
def apply_flip(image):
    flipped_images = [image.transpose(Image.FLIP_LEFT_RIGHT), image.transpose(Image.FLIP_TOP_BOTTOM)]
    return flipped_images

# Función para aplicar el cambio de brillo y contraste
def apply_brightness_contrast(image):
    enhanced_images = []
    for brightness_factor in [0.5, 1.5]:
        for contrast_factor in [0.5, 1.5]:
            enhancer = ImageEnhance.Brightness(image)
            brightened_image = enhancer.enhance(brightness_factor)
            enhancer = ImageEnhance.Contrast(brightened_image)
            contrasted_image = enhancer.enhance(contrast_factor)
            enhanced_images.append(contrasted_image)
    return enhanced_images

# Función para aplicar el cambio de tono y saturación
def apply_color_adjust(image):
    enhanced_images = []
    for color_factor in [0.5, 1.5]:
        for saturation_factor in [0.5, 1.5]:
            enhancer = ImageEnhance.Color(image)
            colored_image = enhancer.enhance(color_factor)
            enhancer = ImageEnhance.Contrast(colored_image)
            saturated_image = enhancer.enhance(saturation_factor)
            enhanced_images.append(saturated_image)
    return enhanced_images

# Función para aplicar el aumento de ruido
def apply_noise(image):
    noised_images = []
    if image.mode in ['RGB', 'RGBA']:
        image = image.convert('RGB')  # Convertir la imagen a modo RGB si es RGBA
        for _ in range(2):  # Aplicamos ruido a dos versiones de la imagen
            np_image = np.array(image)
            noise = np.random.normal(loc=0, scale=20, size=np_image.shape[:2])
            noised_image = np.clip(np_image + noise[..., np.newaxis], 0, 255).astype(np.uint8)
            noised_image = Image.fromarray(noised_image, mode='RGB')
            noised_images.append(noised_image)
    else:
        noised_images.append(image)  # Si el modo de la imagen no es compatible, simplemente agregamos la imagen original
    return noised_images

# Directorio de entrada (donde están las carpetas train y valid)
input_dir = "originales"

# Directorio de salida (donde se guardarán las imágenes aumentadas)
output_dir = "DA"

# Crear la carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterar sobre todas las subcarpetas y archivos en el directorio de entrada
for carpeta in ['valid']:
    carpeta_input = os.path.join(input_dir, carpeta)
    carpeta_output = os.path.join(output_dir, carpeta)
    
    # Crear la carpeta de salida para esta carpeta si no existe
    if not os.path.exists(carpeta_output):
        os.makedirs(carpeta_output)
    
    # Iterar sobre todas las subcarpetas en el directorio de entrada
    for subcarpeta in os.listdir(carpeta_input):
        subcarpeta_input = os.path.join(carpeta_input, subcarpeta)
        
        # Verificar si es una carpeta
        if os.path.isdir(subcarpeta_input):
            subcarpeta_output = os.path.join(carpeta_output, subcarpeta)
            
            # Crear la subcarpeta de salida para esta subcarpeta si no existe
            if not os.path.exists(subcarpeta_output):
                os.makedirs(subcarpeta_output)
            
            # Iterar sobre todas las imágenes en la subcarpeta de entrada
            for imagen in os.listdir(subcarpeta_input):
                imagen_input_path = os.path.join(subcarpeta_input, imagen)
                imagen_output_base_name = os.path.splitext(imagen)[0]  # Nombre de archivo sin extensión
                
                try:
                    # Cargar la imagen original
                    original_image = Image.open(imagen_input_path)
                    
                    # Aplicar todas las transformaciones y guardar las imágenes aumentadas
                    augmented_images = []
                    augmented_images.extend(rotate_image(original_image))
                    augmented_images.extend(apply_flip(original_image))
                    augmented_images.extend(apply_brightness_contrast(original_image))
                    augmented_images.extend(apply_color_adjust(original_image))
                    augmented_images.extend(apply_noise(original_image))
                    
                    for idx, augmented_image in enumerate(augmented_images):
                        imagen_output_name = f"{imagen_output_base_name}_aug_{idx}.png"  # Cambiamos a formato PNG
                        imagen_output_path = os.path.join(subcarpeta_output, imagen_output_name)
                        augmented_image.save(imagen_output_path, format='PNG')  # Guardamos como PNG en lugar de JPEG
                except (OSError, struct.error) as e:
                    print(f"Error al procesar {imagen_input_path}: {e}")
