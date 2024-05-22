import os
import shutil

def copy_limited_images(src_dir, dest_dir, num_images):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        # Skip the root directory
        if root == src_dir:
            continue

        # Create the corresponding destination directory
        rel_path = os.path.relpath(root, src_dir)
        dest_path = os.path.join(dest_dir, rel_path)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        # Get all image files in the current directory
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        # Sort the image files to get a consistent order
        image_files.sort()

        # Copy the first num_images files
        for i, image_file in enumerate(image_files[:num_images]):
            src_file = os.path.join(root, image_file)
            dest_file = os.path.join(dest_path, image_file)
            shutil.copy2(src_file, dest_file)

if __name__ == "__main__":
    src_main_dir = "originales_resized"  # Nombre de la carpeta principal de origen
    dest_main_dir = "originales_resized_limited"  # Nombre de la carpeta principal de destino
    train_folder = "train"  # Nombre de la carpeta train
    valid_folder = "valid"  # Nombre de la carpeta valid
    num_images_train = 400  # Número de imágenes a copiar por subcarpeta en train
    num_images_valid = num_images_train // 4  # Número de imágenes a copiar por subcarpeta en valid

    copy_limited_images(os.path.join(src_main_dir, train_folder), os.path.join(dest_main_dir, train_folder), num_images_train)
    copy_limited_images(os.path.join(src_main_dir, valid_folder), os.path.join(dest_main_dir, valid_folder), num_images_valid)
