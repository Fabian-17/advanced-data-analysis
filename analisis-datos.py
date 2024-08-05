import mysql.connector as mysql
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a la base de datos
try:
    db = mysql.connect(
        host='localhost',
        user='root',
        password='',
        database='CompanyData'
    )
except mysql.Error as e:
    print(f"Error al conectar a MySQL: {e}")
    exit(1)

try:
    # Crear un cursor para ejecutar consultas
    cursor = db.cursor()

    # Ejecutar consulta para extraer los datos de la tabla
    cursor.execute("SELECT * FROM EmployeePerformance")
    
    # Obtener los nombres de las columnas
    columns = [desc[0] for desc in cursor.description]
    
    # Cargar los datos en un DataFrame de pandas
    data = pd.DataFrame(cursor.fetchall(), columns=columns)
    
    # Cerrar el cursor y la conexión
    cursor.close()
    db.close()

    # Verificar si se cargaron los datos
    if data.empty:
        print("No se encontraron datos en la tabla 'EmployeePerformance'.")
        exit(1)

    # Calcular las estadísticas por departamento
    stats = data.groupby('department').agg({
        'performance_score': ['mean', 'median', 'std'],
        'salary': ['mean', 'median', 'std'],
        'employee_id': 'count'
    }).rename(columns={'count': 'total_employees'})

    # Calcular las correlaciones
    correlation_years_performance = data[['years_with_company', 'performance_score']].corr().iloc[0, 1]
    correlation_salary_performance = data[['salary', 'performance_score']].corr().iloc[0, 1]

    # Mostrar los resultados
    print("Estadísticas por departamento:")
    print(stats)

    print("\nCorrelación entre years_with_company y performance_score:")
    print(correlation_years_performance)

    print("\nCorrelación entre salary y performance_score:")
    print(correlation_salary_performance)

    # Visualizaciones con matplotlib
    departments = data['department'].unique()

    # Histograma del performance_score para cada departamento
    for department in departments:
        dept_data = data[data['department'] == department]
        plt.hist(dept_data['performance_score'], bins=10, alpha=0.7)
        plt.title(f'Histograma del Performance Score - {department}')
        plt.xlabel('Performance Score')
        plt.ylabel('Frecuencia')
        plt.grid(True)
        plt.show()

    # Gráfico de dispersión de years_with_company vs. performance_score
    plt.scatter(data['years_with_company'], data['performance_score'])
    plt.title('Years with Company vs. Performance Score')
    plt.xlabel('Years with Company')
    plt.ylabel('Performance Score')
    plt.grid(True)
    plt.show()

    # Gráfico de dispersión de salary vs. performance_score
    plt.scatter(data['salary'], data['performance_score'])
    plt.title('Salary vs. Performance Score')
    plt.xlabel('Salary')
    plt.ylabel('Performance Score')
    plt.grid(True)
    plt.show()

except mysql.Error as e:
    print(f"Error al procesar la tabla: {e}")