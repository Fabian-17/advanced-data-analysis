import MySQLdb as mysql
import csv

# Conexión a la base de datos
try:
    db = mysql.connect('localhost', 'root', '', 'CompanyData')
except mysql.Error as e:
    print(f"Error al conectar a MySQL: {e}")
    exit(1)

try:
    # Crear un cursor para ejecutar consultas
    cursor = db.cursor()

    # Crear la tabla 'EmployeePerformance'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EmployeePerformance (
                id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                employee_id INT(11), 
                department VARCHAR(255),
                performance_score FLOAT, 
                years_with_company INT(11),
                salary FLOAT
        )
    """)
    print("Tabla 'EmployeePerformance' creada.")

    # Leer el archivo CSV
    with open('employee_performance.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Omitir la fila de encabezados
        next(reader)
        
        for row in reader:
            try:
                # Insertar datos en la tabla
                cursor.execute("""
                    INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
                    VALUES (%s, %s, %s, %s, %s)
                """, row)
                
            except mysql.Error as e:
                print(f"Error al insertar datos: {e}")
    
    # Confirmar los cambios
    db.commit()
    print("Datos insertados correctamente.")

except mysql.Error as e:
    print(f"Error al procesar el archivo CSV: {e}")
finally:
    # Cerrar la conexión
    db.close()