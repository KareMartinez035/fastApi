from fastapi import FastAPI, Depends, HTTPException  
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  
import firebase_admin  
from firebase_admin import credentials, auth  
import mysql.connector  
import bcrypt  
import uuid  
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig  
from pydantic import BaseModel  
from typing import Optional  

app = FastAPI()  

# Configuración de Firebase  
cred = credentials.Certificate("./terapp-firebase.json")  
firebase_admin.initialize_app(cred)  

# Conexión a la base de datos RDS de AWS  
db_connection = mysql.connector.connect(  
    host="terapp.c3m0606uy54o.us-east-1.rds.amazonaws.com",  
    user="admin",  
    password="resstech04",  
    database="terapp"  
)  

# Configuración del envío de correos  
class MailConfig(BaseModel):  
    MAIL_USERNAME: str  
    MAIL_PASSWORD: str  
    MAIL_FROM: str  
    MAIL_PORT: int  
    MAIL_SERVER: str  
    MAIL_FROM_NAME: str  
    MAIL_STARTTLS: bool  
    MAIL_SSL_TLS: bool  
    USE_CREDENTIALS: bool  

conf = MailConfig(  
    MAIL_USERNAME="TerApp",  
    MAIL_PASSWORD="bxpk ahav orpu tjuu",  
    MAIL_FROM="terapp.rehabilitacion@gmail.com",  
    MAIL_PORT=587,  
    MAIL_SERVER="smtp.gmail.com",  
    MAIL_FROM_NAME="TerApp",  
    MAIL_STARTTLS=True,  
    MAIL_SSL_TLS=False,  
    USE_CREDENTIALS=True  
)  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

class Paciente(BaseModel):  
    nombre: str  
    apellido: str  
    tel: int  
    email: str  
    passw: str  

@app.post("/token")  
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  
    try:  
        user = auth.get_user_by_email(form_data.username)  
    except Exception:  
        raise HTTPException(status_code=401, detail="Usuario no encontrado")  
    
    return {"access_token": user.uid, "token_type": "bearer"}  

@app.post("/insertar_paciente/")  
async def insertar_paciente(paciente: Paciente, token: str = Depends(oauth2_scheme)):  
    uid = verify_token(token)  

    hashed_password = bcrypt.hashpw(paciente.passw.encode('utf-8'), bcrypt.gensalt())  
    
    cursor = db_connection.cursor()  
    cursor.execute("INSERT INTO paciente (Nombres, Apellidos, Telefono, Email, Contrasena) VALUES (%s, %s, %s, %s, %s)",  
                   (paciente.nombre, paciente.apellido, paciente.tel, paciente.email, hashed_password))  
    db_connection.commit()  
    cursor.close()  

    return {"message": "Paciente insertado con éxito", "uid": uid}  

class RecuperarContrasena(BaseModel):  
    email: str  

@app.post("/recuperar_contrasena/")  
async def recuperar_contrasena(data: RecuperarContrasena):  
    cursor = db_connection.cursor()  
    cursor.execute("SELECT * FROM paciente WHERE Email = %s", (data.email,))  
    user = cursor.fetchone()  

    if not user:  
        raise HTTPException(status_code=404, detail="Usuario no encontrado")  

    token = str(uuid.uuid4())  
    reset_link = f"http://tu_dominio.com/restablecer_contrasena/{token}"  

    message = MessageSchema(  
        subject="Restablecer contraseña",  
        recipients=[data.email],  
        body=f"Para restablecer tu contraseña, por favor haz clic en el siguiente enlace: {reset_link}",  
        subtype="html",  
    )  

    fm = FastMail(conf)  
    await fm.send_message(message)  

    return {"message": "Enlace de restablecimiento de contraseña enviado a tu correo electrónico."}  

@app.post("/restablecer_contrasena/")  
async def restablecer_contrasena(token: str, nueva_contrasena: str):  
    hashed_password = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())  

    cursor = db_connection.cursor()    
    cursor.execute("UPDATE paciente SET Contrasena = %s WHERE Email = %s", (hashed_password, email))  
    db_connection.commit()  
    cursor.close()  

    return {"message": "Contraseña restablecida con éxito."} 