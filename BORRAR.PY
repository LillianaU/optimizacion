import os  # Importa el módulo para interactuar con el sistema de archivos
import shutil  # Importa el módulo para operaciones de alto nivel con archivos y carpetas
import datetime  # Importa el módulo para trabajar con fechas y horas
from pathlib import Path  # Importa la clase Path para manejar rutas de archivos de manera más simple

# Función para borrar el contenido de una carpeta
def borrar_contenido_carpeta(carpeta):
    # Recorre todos los archivos y carpetas en la carpeta especificada
    for filename in os.listdir(carpeta):
        file_path = os.path.join(carpeta, filename)  # Genera la ruta completa del archivo/carpeta
        try:
            # Verifica si es un archivo o un enlace simbólico y lo borra
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Elimina el archivo o enlace simbólico
            # Si es una carpeta, la borra junto con su contenido
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Borra la carpeta de forma recursiva
        except PermissionError:
            print(f'Acceso denegado: {file_path}')  # Muestra un mensaje específico para permisos denegados
        except Exception as e:
            print(f'Error al borrar {file_path}. Razón: {e}')  # Muestra un mensaje en caso de error

# Función para borrar descargas de la fecha actual
def borrar_descargas_hoy(carpeta_descargas):
    hoy = datetime.datetime.now().date()  # Obtiene la fecha actual
    # Recorre todos los archivos en la carpeta de descargas
    for filename in os.listdir(carpeta_descargas):
        file_path = os.path.join(carpeta_descargas, filename)  # Genera la ruta completa del archivo
        try:
            if os.path.isfile(file_path):  # Verifica si es un archivo
                archivo_fecha = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date()  # Obtiene la fecha de creación del archivo
                if archivo_fecha == hoy:  # Si el archivo fue creado hoy, lo elimina
                    os.unlink(file_path)  # Elimina el archivo
            elif os.path.isdir(file_path):  # Si es una carpeta, la elimina
                shutil.rmtree(file_path)  # Borra la carpeta de forma recursiva
        except PermissionError:
            print(f'Acceso denegado: {file_path}')  # Muestra un mensaje específico para permisos denegados
        except Exception as e:
            print(f'Error al borrar {file_path}. Razón: {e}')  # Muestra un mensaje en caso de error

# Función para limpiar la caché del navegador (Google Chrome y Firefox en este caso)
def limpiar_cache_navegadores():
    # Ruta de la caché de Chrome en Windows
    chrome_cache = Path(os.getenv('LOCALAPPDATA')) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'Cache'
    # Ruta de la caché de Firefox en Windows (requiere navegar por perfiles)
    firefox_cache = Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox' / 'Profiles'
    
    # Limpiar caché de Chrome
    if chrome_cache.exists():  # Verifica si la carpeta de caché de Chrome existe
        borrar_contenido_carpeta(chrome_cache)  # Llama a la función para borrar el contenido de la caché
        print("Caché de Chrome limpiada.")  # Imprime un mensaje confirmando que la caché fue limpiada
    
    # Limpiar caché de Firefox
    for profile in firefox_cache.glob('*'):  # Recorre cada perfil de usuario en Firefox
        cache_path = profile / 'cache2' / 'entries'  # Especifica la ruta de la caché de Firefox
        if cache_path.exists():  # Verifica si la carpeta de caché existe
            borrar_contenido_carpeta(cache_path)  # Llama a la función para borrar el contenido de la caché
            print(f'Caché de Firefox perfil {profile.name} limpiada.')  # Imprime un mensaje para cada perfil limpiado

# Función para limpiar archivos temporales
def limpiar_temporales():
    temp_folder = Path(os.getenv('TEMP'))  # Obtiene la ruta de la carpeta temporal del sistema
    borrar_contenido_carpeta(temp_folder)  # Llama a la función para borrar el contenido de la carpeta temporal
    print("Archivos temporales limpiados.")  # Imprime un mensaje confirmando que los temporales fueron limpiados

# Función principal para limpiar todo el sistema
def limpiar_sistema():
    # Limpiar carpeta de descargas
    descargas_path = Path.home() / 'Downloads'  # Obtiene la ruta de la carpeta de descargas
    borrar_descargas_hoy(descargas_path)  # Llama a la función para borrar las descargas de hoy
    
    # Limpiar caché de navegadores
    limpiar_cache_navegadores()  # Llama a la función para limpiar la caché de los navegadores
    
    # Limpiar archivos temporales
    limpiar_temporales()  # Llama a la función para limpiar los archivos temporales

# Menú interactivo
def mostrar_menu():
    # Muestra las opciones disponibles para el usuario
    print("\nSeleccione una opción:")
    print("1. Limpiar descargas de hoy")
    print("2. Limpiar caché de navegadores")
    print("3. Limpiar archivos temporales")
    print("4. Realizar todas las funciones")
    print("5. Salir")

    # Solicita al usuario que ingrese una opción
    opcion = input("\nIngrese el número de la opción deseada: ")
    return opcion  # Retorna la opción seleccionada por el usuario

# Función principal que ejecuta el menú y las acciones correspondientes
def main():
    while True:  # Bucle que permite repetir el menú hasta que el usuario decida salir
        opcion = mostrar_menu()  # Llama a la función para mostrar el menú

        if opcion == '1':  # Si el usuario elige la opción 1
            descargas_path = Path.home() / 'Downloads'  # Obtiene la ruta de descargas
            borrar_descargas_hoy(descargas_path)  # Borra las descargas de hoy
            print("Descargas de hoy eliminadas.")  # Confirma la acción
        elif opcion == '2':  # Si el usuario elige la opción 2
            limpiar_cache_navegadores()  # Limpia la caché de los navegadores
            print("Caché de navegadores limpiada.")  # Confirma la acción
        elif opcion == '3':  # Si el usuario elige la opción 3
            limpiar_temporales()  # Limpia los archivos temporales
            print("Archivos temporales eliminados.")  # Confirma la acción
        elif opcion == '4':  # Si el usuario elige la opción 4
            limpiar_sistema()  # Realiza todas las acciones de limpieza
            print("Todas las funciones ejecutadas.")  # Confirma la acción
        elif opcion == '5':  # Si el usuario elige la opción 5
            print("Saliendo del programa...")  # Imprime un mensaje y termina el programa
            break  # Sale del bucle
        else:  # Si el usuario ingresa una opción inválida
            print("Opción no válida. Por favor, elija una opción del menú.")  # Informa de la opción no válida

# Punto de entrada del programa
if __name__ == "__main__":
    main()  # Ejecuta la función principal
