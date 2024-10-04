#Programa para capturar las fotos con el intervalo
import cv2
import os
import time 

class CapturaFotos:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.cam = cv2.VideoCapture(1)
        self.inicio = time.time()

    def capturar(self):
        try:
            i = 0
            while True:
                # Calcular el tiempo desde el inicio
                tiempo_transcurrido = time.time() - self.inicio
                
                # Determinar el intervalo de tiempo entre fotos
                if tiempo_transcurrido < 5 * 60:
                    intervalo_entre_fotos = 1
                elif tiempo_transcurrido < 60 * 60:
                    intervalo_entre_fotos = 60
                else:
                    intervalo_entre_fotos = 3600

                # Capturar imagen
                ret, frame = self.cam.read()
                if not ret:
                    print("No se pudo capturar la imagen.")
                    break
                
                # Guardar imagen
                cv2.imwrite(os.path.join(self.output_dir, f"{i}.jpg"), frame)
                
                # Mostrar progreso
                print(f"Tomada foto {i + 1}")
                i += 1
                
                # Comprobar si se ha presionado la tecla 'x' para salir
                if cv2.waitKey(1) & 0xFF == ord('x'):
                    print("Captura detenida por el usuario.")
                    break
                
                # Esperar el intervalo de tiempo entre fotos
                time.sleep(intervalo_entre_fotos)
                
        finally:
            # Liberar la cámara
            self.cam.release()
            cv2.destroyAllWindows()

# Ejecutamos el codigo pasandole una ruta donde se guardaran las imágenes 
capturador = CapturaFotos(image_folder = "C:\\Users\\Dione\\Downloads\\1. CIDIMEC\\PresentaciónFinal\\prueba")

capturador.capturar()
