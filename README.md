Fundacion Universitaria Compensar\
Facultad de Ingenieria\
Ingeniería de Sistemas\
Seguridad de la información\
Felipe Castellanos Sánchez\
código 1030576147
## Proyecto Final
## Sistema de inventario visual y auditoria de seguridad para Telecomunicaciones
Objetivo: Desarrollar un sistema automatizado que detecte activos de telecomunicaciones mediante YOLO, asegure su transmisión mediante cifrado y evalue el cumplimiento de la norma ISO27001.\
Modulo 1: Detección YOLO\
1.	Entrenamiento del modelo\
Utilizamos 10 imágenes de cada categoría de dispositivo, en este caso servidor, firewall, switch, router y hub.
 
2.	Subimos el modelo a Roboflow
 
3.	Entrenamos el modelo
 
 
4.	Descargamos el archivo best.py una vez entrenado con colab de google
 
5.	Programa en Python YOLO
 
6.	Creacion de entorno virtual

 
7.	Pruebas de reconocimiento
 

 
Modulo 2: Criptografia
8.	Adicion al programa y funciones para encriptar

9.	Programa del auditor para llaves publicas y privadas RSA
 
 



10.	Funcion de comprobar imagen encriptada

 

11.	Prueba

 
Lado de auditor
 
 
 

Modulo 3: Auditoria ISO27001
12.	Inventario de activos: Logro listar todos los routers y switches? Ayuda a mantener el inventario actualizado?
Control 5.9 (ISO/IEC 27001:2022) / A.8.1.1 (ISO 27001:2013) – Inventario de Información y otros Activos Asociados
Estado: APLICA

Justificación de Aplicabilidad: Toda organización que gestione infraestructura crítica de redes de datos debe mantener un registro actualizado, exacto y centralizado de sus componentes de hardware (activos físicos) para prevenir brechas de seguridad, accesos no autorizados o pérdidas de control sobre la topología de la red.

El algoritmo detecta de forma visual y clasifica en tiempo real cada activo presente frente a la cámara (generando etiquetas precisas de Router, Switch, Firewall, Servidor).

13.	Uso aceptable de activos: el software de detección solo se usa para inventario?

Control 5.10 (ISO/IEC 27001:2022) / A.8.1.3 (ISO 27001:2013) – Uso Aceptable de Activos
Estado: APLICA

Justificación de Aplicabilidad: Los activos de software que procesan información visual y topológica de la infraestructura de red corporativa (Data Centers, racks, firewalls, servidores) manejan datos de alta confidencialidad. Se debe garantizar que el uso del software esté restringido estrictamente a funciones de auditoría e inventario autorizadas, evitando que sea desviado para espionaje industrial, fuga de información o mapeo no autorizado de vulnerabilidades físicas.

Restricción por Política (Alcance Organizacional): El software de detección con YOLO (yolo-networking.py) está definido en la organización con un propósito único y exclusivo: la recolección automatizada de datos para el Inventario de Activos. No está autorizado su uso en dispositivos personales ni para capturas que no correspondan a una orden de auditoría vigente.

el software no permite almacenar datos en texto plano en la zona no segura. Obliga a que el activo (el software) funcione exclusivamente como un canalizador ciego: captura, cifra y destruye el residuo local, alineándose de forma estricta con el principio de uso aceptable y seguro.

14.	Transferencia de información: se aplica el cifrado al enviar los datos?

Control 8.12 (ISO/IEC 27001:2022) / A.13.2.1 (ISO 27001:2013) – Transferencia de Información
Estado: APLICA

Justificación de Aplicabilidad: Cuando un técnico recopila información sobre la infraestructura crítica de la red en el campo y la envía hacia la central (ya sea por correo electrónico, redes Wi-Fi, canales compartidos o almacenamiento en la nube), los datos están expuestos a riesgos de interceptación (man-in-the-middle), espionaje o modificaciones no autorizadas. Es mandatorio garantizar que la información viaje blindada de extremo a extremo.
Evidencia de cumplimiento: Los archivos generados listos para la transferencia son exclusivamente de extensión cifrada (.enc), garantizando que ningún dato confidencial viaje expuesto por la red.



15.	Etiquetado de los activos: las fotos sirven como etiqueta visual del equipo?

Control 5.13 (ISO/IEC 27001:2022) / A.8.2.2 (ISO 27001:2013) – Etiquetado de los Activos
Estado: APLICA (Bajo enfoque digital)

Justificación de Aplicabilidad: La organización requiere un mecanismo para identificar de forma unívoca la clasificación y el estado de sus activos de información en la infraestructura de red. Tradicionalmente esto se hace con etiquetas físicas autoadhesivas; sin embargo, en entornos de alta disponibilidad (como racks o centros de datos), las etiquetas pueden deteriorarse, caerse o ser manipuladas maliciosamente, perdiendo la trazabilidad del activo.

Esa huella digital de 64 caracteres viaja cifrada y amarrada a la topología. Si un atacante intenta suplantar el equipo o cambiar la foto, el script auditor_central.py detectará que los hashes no coinciden. Esto actúa como un sello o etiqueta digital de seguridad que garantiza el origen del activo inspeccionado.

16.	Protección contra malware: El ordenador donde corre YOLO tiene antivirus?
Control 8.7 (ISO/IEC 27001:2022) / A.12.2.1 (ISO 27001:2013) – Protección contra Malware
Estado: NO APLICA (Al alcance del desarrollo del software) / REQUISITO EXTERNO PARA EL ENTORNO
Justificación de Exclusión en el Código: Los scripts de software desarrollados (yolo-networking.py y auditor_central.py) tienen como alcance exclusivo la detección de objetos por visión artificial, la recolección de métricas de auditoría y la protección criptográfica híbrida de la información. El sistema de software no cuenta con funciones nativas de un Antivirus, E
Matriz de Riesgos

ID Riesgo	Amenaza / Evento	Impacto Inicial	Control ISO 27001 Aplicado	Mitigación Técnica en tu Proyecto	Impacto Residual
R-01	Un tercero intercepta la red inalámbrica en campo y roba las fotos de los routers del Data Center.	ALTO (Fuga de topología crítica)	8.24 (Criptografía) y 8.12 (Transferencia)	Cifrado inmediato de la imagen y metadatos con AES-128-CBC. Los archivos interceptados son ilegibles.	BAJO
R-02	Un técnico malicioso altera el archivo JSON para reportar un firewall inexistente o modificar la hora.	MEDIO (Fraude en auditoría)	5.9 (Inventario) y 8.24 (Integridad)	El Hash SHA-256 se calcula antes de cifrar. Si el archivo se edita, el hash calculado en el destino fallará.	BAJO
R-03	Pérdida o robo de la clave de cifrado durante el tránsito hacia el servidor de auditoría.	ALTO (Descifrado total expuesto)	5.15 (Gestión de llaves criptográficas)	La clave AES no se envía en texto plano; viaja protegida con la Llave Pública RSA-2048 del auditor.	BAJO
R-04	Acceso no autorizado a la base de datos de evidencias almacenadas históricamente.	ALTO (Exposición de vulnerabilidades)	8.24 (Criptografía en reposo)	El auditor mantiene almacenados los datos en su formato cifrado, usando su Llave Privada para consultas bajo demanda.	BAJO


