from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
import firebase_admin  
from firebase_admin import credentials, auth  

# Inicializa la aplicación FastAPI  
app = FastAPI()  

# Configuración de Firebase

cred = credentials.Certificate("./prueba-karen.json")  
firebase_admin.initialize_app(cred)  

# Conexión a la base de datos RDS de AWS  
 
@app.get("/Usuario/{uid}")  
async def obtener_usuario():  
    # Obtener todos los usuarios de Firebase  
    try:  
        users = auth.list_users().users  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios de Firebase: {str(e)}")  

    # Crear una lista de pacientes  
    pacientes = []  
    for user in users:  
        paciente = {  
            "nombre": user.display_name or "Sin nombre",  
            "apellido": "Sin apellido",  # Firebase no tiene apellido por defecto  
            "telefono": "Sin teléfono",  # Puedes agregar lógica para obtener el teléfono  
            "email": user.email or "Sin email"  
        }  
        pacientes.append(paciente)  

    return {"pacientes": pacientes}

# Modelo de datos para el paciente  
class Paciente(BaseModel):  
    nombres: str  
    apellidos: str  
    telefono: str  
    email: str  
    rol: str  

"""@app.post("/insertar_paciente/{uid}")  
async def insertar_paciente(uid: str):  
    # Obtener el usuario de Firebase por UID  

    if rol=="Paciente":
        try:  
            user = auth.get_user(uid)  
        except Exception as e:  
            raise HTTPException(status_code=404, detail=f"Usuario no encontrado: {str(e)}")  

    # Crear un objeto Paciente  
    paciente = Paciente(  
        nombres=user.display_name or "Sin nombre",  
        apellidos="Reyes",  # Puedes modificar esto según la estructura de tu base de datos  
        telefono="123123123213",  # Puedes modificar esto según la estructura de tu base de datos  
        email=user.email or "Sin email",  
        rol="fisioterapeuta"  # Puedes modificar esto según la estructura de tu base de datos  
    )  

    # Insertar en la base de datos  
    cursor = db_connection.cursor()  
    try:  
        cursor.execute(  
            "INSERT INTO paciente (Nombres, Apellidos, Telefono, Email) VALUES (%s, %s, %s, %s)",  
            (paciente.nombres, paciente.apellidos, paciente.telefono, paciente.email)  
        )  
        db_connection.commit()  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Error al insertar paciente: {str(e)}")  
    finally:  
        cursor.close()  

    return {"message": "Paciente insertado con éxito", "paciente": paciente}"""