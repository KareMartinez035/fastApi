class configuracion():

    host="terapp.c3m0606uy54o.us-east-1.rds.amazonaws.com",
    user= "admin",
    password= "resstech04",
    database= "terapp"

config= {
    'config': configuracion
    }
db_connection = mysql.connector.connect(  
    host="terapp.c3m0606uy54o.us-east-1.rds.amazonaws.com",
    user= "admin",
    password= "resstech04",
    database= "terapp"  
) 