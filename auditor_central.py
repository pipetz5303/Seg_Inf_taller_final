#Programa para que el auditor genere llaves publicas y privadas; como comprobar que la imagen no fue alterada
import json
import os
import hashlib

# Librerias de criptografia 
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

def calcular_sha256(ruta_archivo):
    #Calcula la huella digital (Hash) de un archivo
    with open(ruta_archivo, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def menu():
    print('''Generador de llaves RSA 
    1. Generar pareja de llaves RSA (Pública/Privada)
    2. Procesar y verificar evidencias recibidas
    3. Salir''')
    return input("Selecciona una opcion: ")

while True:
    opcion = menu()
    
    if opcion == "1":
        print("\nGenerando llaves RSA de 2048 bits...")
        llave = RSA.generate(2048)
        
        # Guarda Llave Privada
        with open("llave_privada.pem", "wb") as f:
            f.write(llave.export_key())
            
        # Guarda Llave Pública 
        with open("llave_publica.pem", "wb") as f:
            f.write(llave.publickey().export_key())
            
        print("Llaves generadas.")
        print(" -> 'llave_publica.pem' Para prueba")
        print(" -> 'llave_privada.pem' Para auditor\n")
        
    elif opcion == "2":
        print("\nIniciando desencriptacion y control de integridad...")
        
        # Verifica que existan todos los archivos necesarios
        archivos_requeridos = ["llave_privada.pem", "evidencia.jpg.enc", "metadatos.json.enc", "clave_aes.key.enc"]
        faltantes = [a for a in archivos_requeridos if not os.path.exists(a)]
        
        if faltantes:
            print(f"ERROR Faltan archivos obligatorios para el proceso: {faltantes}")
            print("INFO Asegurate de que el tecnico ya haya generado las evidencias (.enc).\n")
            continue
            
        # 1. Carga la llave privada del auditor
        with open("llave_pirvada.pem" if os.path.exists("llave_pirvada.pem") else "llave_privada.pem", "rb") as f:
            llave_privada = RSA.import_key(f.read())
            
        # 2. Lee la clave AES cifrada y recuperarla con RSA Privada
        with open("clave_aes.key.enc", "rb") as f:
            clave_aes_cifrada = f.read()
            
        cipher_rsa = PKCS1_OAEP.new(llave_privada)
        try:
            clave_aes_recuperada = cipher_rsa.decrypt(clave_aes_cifrada)
            print("-> [RSA] Clave AES recuperada exitosamente usando la llave privada.")
        except Exception as e:
            print("[CRÍTICO] Error al descifrar con RSA. Llave privada incorrecta o datos corruptos.")
            continue
            
        # 3. Desencripta la imagen y el JSON usando la clave AES recuperada
        iv_fijo = b"1234567812345678"
        
        # Desencriptar Imagen
        cipher_aes_img = AES.new(clave_aes_recuperada, AES.MODE_CBC, iv=iv_fijo)
        with open("evidencia.jpg.enc", "rb") as f:
            img_datos_cifrados = f.read()
        imagen_original_bytes = unpad(cipher_aes_img.decrypt(img_datos_cifrados), AES.block_size)
        
        # Guardar la imagen recuperada legible en la central
        ruta_imagen_recuperada = "auditoria_evidencia_recuperada.jpg"
        with open(ruta_imagen_recuperada, "wb") as f:
            f.write(imagen_original_bytes)
            
        # Desencriptar JSON
        cipher_aes_json = AES.new(clave_aes_recuperada, AES.MODE_CBC, iv=iv_fijo)
        with open("metadatos.json.enc", "rb") as f:
            json_datos_cifrados = f.read()
        json_original_bytes = unpad(cipher_aes_json.decrypt(json_datos_cifrados), AES.block_size)
        
        metadatos_legibles = json.loads(json_original_bytes.decode('utf-8'))
        print("-> [AES] Imagen y archivo JSON de metadatos descifrados correctamente.")
        
        # 4. CONTROL DE INTEGRIDAD (VALIDACIÓN DEL HASH SHA-256)
        hash_esperado = metadatos_legibles["hash_verificacion"]
        hash_calculado_servidor = calcular_sha256(ruta_imagen_recuperada)
        
        print(f'''\n      RESULTADO DEL CONTROL DE CALIDAD             
        Fecha/Hora Captura: {metadatos_legibles['fecha_hora']}
        Origen:             {metadatos_legibles['dispositivo']}
        Detecciones YOLO:   {metadatos_legibles['yolo_detecciones']}
        Hash en el JSON (Origen):   {hash_esperado}
        Hash Calculado (Destino):  {hash_calculado_servidor}''')
        
        if hash_esperado == hash_calculado_servidor:
            print("\n[ÉXITO] >>> VERIFICACIÓN POSITIVA <<<")
            print("[INFO] Los hashes coinciden exactamente. La imagen NO fue modificada.")
            print("[INFO] Cadena de custodia garantizada (Control A.10 ISO 27001).\n")
        else:
            print("\n[ALERTA CRÍTICA] >>> VERIFICACIÓN FALLIDA <<<")
            print("[PELIGRO] Los hashes NO coinciden. La evidencia fue alterada en el trayecto.\n")
            
    elif opcion == "3":
        print("Saliendo del sistema de auditoria.")
        break
    else:
        print("Opcion invalida.\n")
2
