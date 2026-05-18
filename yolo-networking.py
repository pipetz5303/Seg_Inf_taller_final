#Programa para YOLO, captura de imagen y encriptacion
import cv2
import json
import os
import hashlib
from datetime import datetime
from ultralytics import YOLO

# Librerias de criptografia
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

# Calcula la huella digital (Hash) de la imagen para garantizar INTEGRIDAD
def calcular_sha256(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

print("Cargando modelo YOLO para hardware de IT...")

model = YOLO("best.pt") 

# Importar la llave pública que previamente nos dio el auditor
if not os.path.exists("llave_publica.pem"):
    print("[ERROR] No se encuentra el archivo 'llave_publica.pem'.")
    print("[INFO] Ejecuta primero el script del auditor para generar las llaves.")
    exit()

with open("llave_publica.pem", "rb") as f:
    llave_publica_auditor = RSA.import_key(f.read())

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("\n=== CÁMARA EN VIVO INICIADA ===")
print("Presiona la tecla 'E' para capturar la evidencia y protegerla.")
print("Presiona la tecla 'Q' para salir.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # Inferencia en tiempo real con YOLO
    results = model(frame)
    annotated_frame = results[0].plot()
    
    cv2.imshow("Captura de evidencias equipos redes", annotated_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):
        
        print("\n[!] Capturando fotograma actual...")
        
        # 1. Guardar la imagen original limpia (sin los recuadros dibujados)
        foto_temporal = "evidencia_original.jpg"
        cv2.imwrite(foto_temporal, frame)
        
        # 2. INTEGRIDAD: Calcular el Hash SHA-256 de la foto original
        hash_imagen = calcular_sha256(foto_temporal)
        print(f"-> [SHA-256] Huella digital calculada: {hash_imagen}")
        
        # 3. METADATOS: Extraer resultados de YOLO y estructurar el JSON
        detecciones = []
        for box in results[0].boxes:
            clase_id = int(box.cls[0])
            detecciones.append({
                "clase": model.names[clase_id],
                "confianza": round(float(box.conf[0]), 2)
            })
            
        metadatos = {
            "fecha_hora": datetime.now().isoformat(),
            "dispositivo": "Laptop_Tecnico_Campo_01",
            "hash_verificacion": hash_imagen,
            "yolo_detecciones": detecciones
        }
        
        # Guardar metadatos temporalmente en JSON
        json_temporal = "metadatos.json"
        with open(json_temporal, "w") as f:
            json.dump(metadatos, f, indent=4)
            
        # 4. CONFIDENCIALIDAD (AES): Generar clave simétrica efímera de 16 bytes
        clave_aes = os.urandom(16)
        iv_fijo = b"1234567812345678" # IV estático para simplicidad del laboratorio académico
        
        # Cifrar la imagen con AES
        cipher_aes_img = AES.new(clave_aes, AES.MODE_CBC, iv=iv_fijo)
        with open(foto_temporal, "rb") as f:
            imagen_cifrada = cipher_aes_img.encrypt(pad(f.read(), AES.block_size))
            
        # Cifrar el JSON con AES
        cipher_aes_json = AES.new(clave_aes, AES.MODE_CBC, iv=iv_fijo)
        with open(json_temporal, "rb") as f:
            json_cifrado = cipher_aes_json.encrypt(pad(f.read(), AES.block_size))
            
        # Guardar los archivos cifrados ilegibles (.enc)
        with open("evidencia.jpg.enc", "wb") as f: f.write(imagen_cifrada)
        with open("metadatos.json.enc", "wb") as f: f.write(json_cifrado)
        print("-> [AES-128-CBC] Imagen y JSON cifrados exitosamente.")
        
        # Borrar archivos temporales legibles del entorno inseguro
        if os.path.exists(foto_temporal): os.remove(foto_temporal)
        if os.path.exists(json_temporal): os.remove(json_temporal)
        print("-> Archivos temporales borrados para evitar fugas de informacion.")
        
        # 5. GESTIÓN DE CLAVES (RSA): Cifrar la clave AES usando la Pública del Auditor
        cipher_rsa = PKCS1_OAEP.new(llave_publica_auditor)
        clave_aes_cifrada = cipher_rsa.encrypt(clave_aes)
        
        with open("clave_aes.key.enc", "wb") as f: f.write(clave_aes_cifrada)
        print("-> [RSA-2048] Clave AES cifrada con la llave publica del Auditor.")
        print("[OK] Paquete de evidencia protegido y listo para enviar al Auditor.\n")
        
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
