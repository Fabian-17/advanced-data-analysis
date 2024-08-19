import mysql.connector as mysql
import csv

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            exit(1)

    def close(self):
        if self.connection:
            self.connection.close()

class EmployeePerformanceTable:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = self.db_connection.cursor()

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS EmployeePerformance (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    employee_id INT, 
                    department VARCHAR(255),
                    performance_score DECIMAL(10, 2),
                    years_with_company INT,
                    salary DECIMAL(10, 2)
                )
            """)
            print("Tabla 'EmployeePerformance' creada.")
        except mysql.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insert_data_from_csv(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Omite la fila de encabezados
                for row in reader:
                    try:
                        self.cursor.execute("""
                            INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
                            VALUES (%s, %s, %s, %s, %s)
                        """, row)
                    except mysql.Error as e:
                        print(f"Error al insertar datos: {e}")
            self.db_connection.commit()
            print("Datos insertados correctamente.")
        except mysql.Error as e:
            print(f"Error al procesar el archivo CSV: {e}")
        except FileNotFoundError:
            print(f"Archivo {csv_file_path} no encontrado.")

    def close(self):
        self.cursor.close()

# Uso de las clases
if __name__ == "__main__":
    # Crea una instancia de DatabaseConnector
    db_connector = DatabaseConnector(
        host='localhost',
        user='root',
        password='',
        database='CompanyData'
    )
    
    # Conecta a la base de datos
    db_connector.connect()
    
    # Crea una instancia de EmployeePerformanceTable
    performance_table = EmployeePerformanceTable(db_connector.connection)
    
    # Crea la tabla e insertar los datos del CSV
    performance_table.create_table()
    performance_table.insert_data_from_csv('employee_performance.csv')
    
    # Cierra las conexiones
    performance_table.close()
    db_connector.close()