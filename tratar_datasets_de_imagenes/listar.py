import os

def listar_contenido_directorio(ruta, nivel=0, resumen=None):
    if resumen is None:
        resumen = {}
    
    try:
        # Obtener la lista de directorios y archivos en la ruta actual
        contenido = os.listdir(ruta)
    except PermissionError:
        print(" " * nivel * 4 + "Permiso denegado: " + ruta)
        return resumen

    # Inicializar el contador de subdirectorios y archivos
    num_subdirectorios = 0
    num_archivos = 0

    # Ordenar contenido para que los directorios aparezcan primero
    contenido.sort()

    # Recorrer el contenido
    for item in contenido:
        # Construir la ruta completa del ítem
        item_ruta = os.path.join(ruta, item)
        
        # Imprimir el ítem con sangría según el nivel
        if os.path.isdir(item_ruta):
            print(" " * nivel * 4 + "|-- " + item + "/")
            # Contar el subdirectorio
            num_subdirectorios += 1
            # Si el ítem es un directorio, llamar recursivamente a la función
            resumen = listar_contenido_directorio(item_ruta, nivel + 1, resumen)
        else:
            print(" " * nivel * 4 + "|-- " + item)
            # Contar el archivo
            num_archivos += 1
    
    # Guardar el resumen para el directorio actual
    resumen[ruta] = {'subdirectorios': num_subdirectorios, 'archivos': num_archivos}
    
    return resumen

def imprimir_resumen(resumen):
    print("\nResumen del contenido del directorio:\n")
    for directorio, conteo in resumen.items():
        print(f"Directorio: {directorio}")
        print(f"  Subdirectorios: {conteo['subdirectorios']}")
        print(f"  Archivos: {conteo['archivos']}\n")

# Establecer la ruta del directorio inicial
ruta_inicial = "or_resized"

# Llamar a la función para listar el contenido del directorio
resumen = listar_contenido_directorio(ruta_inicial)

# Imprimir el informe resumen
imprimir_resumen(resumen)
