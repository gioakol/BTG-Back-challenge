# BTG-Back-Challenge

## Descripción
Challenge diseñado para validar conocimientos técnicos en python y AWS, por ello para el back-end se diseña una API que permite:
- Realizar suscripciones (FIC y FPV).
- Cancelar suscripciones (FIC y FPV).
- Historial de transacciones

## Tecnologías Utilizadas
- **Lenguaje de Programación:** Python
- **Frameworks y Librerías:**
  - **FastAPI**: Construcción de APIs
  - **Uvicorn**: Servidor ASGI para FastAPI
  - **Boto3**: Interacción con AWS
  - **python-dotenv**: Gestión de variables de entorno
  - **Pydantic**: Validación de datos
  - **pytest**: Pruebas
  - **httpx**: Cliente HTTP asíncrono
- **Servicios en la Nube:**
  - **AWS DynamoDB:** Bases de datos no relacionales
  - **AWS SNS:** Servicio de notificación simple (envio de sms o correos de notificación bajo suscripción)
  - **AWS Secrets Manager:** Almacenamiento y administración de secretos (como credenciales y claves API) de manera segura.
  - **AWS CloudFormation:** Herramienta para gestionar y aprovisionar recursos en la nube mediante plantillas en formato JSON o YAML.
  - **AWS EC2:** Servidores virtuales en la nube para ejecutar aplicaciones con configuración y escalabilidad flexible.

## Instalación
Para instalar y configurar el entorno de desarrollo, sigue los siguientes pasos:

1. **Clona el repositorio:**
    ```bash
    git clone https://github.com/gioakol/BTG-Back-challenge.git
    cd BTG-Back-challenge

2. **Crea un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt

4. Ejecución dev
    ```bash
    uvicorn main:app --reload --env-file=".env"



## Instalación
Para realizar la instalación en un ambiente productivo/pruebas, asegúrate de seguir estos pasos:

1. Crear VM en EC2 Linux
2. Instalar todas las dependencias en la VM
    ```bash
    sudo apt update
    sudo apt install nginx
    sudo apt install python3.12-venv
    
3. Inciar entorno virtual
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

2. **Ejecuta la aplicación:**
    ```bash
    uvicorn main:app --reload --env-file=".env"

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

  ```bash
    BTG-Back-challenge/
    │
    ├── app/
    │   ├── database/
    │   │   ├── __init__.py
    │   │   ├── clients.py
    │   │   └── db.py
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   └── clients.py
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   └── helpers.py
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── test_clients.py
    │
    ├── .env
    ├── .gitignore
    ├── main.py
    └── requirements.txt
  ```

## Infraestructura Cloud

![image](https://github.com/user-attachments/assets/a215636f-e24a-466d-8eb3-2767d55d7e4d)

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.













