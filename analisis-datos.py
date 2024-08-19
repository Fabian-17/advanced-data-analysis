import mysql.connector as mysql
import pandas as pd
import matplotlib.pyplot as plt

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

class EmployeePerformanceAnalyzer:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.data = None

    def fetch_data(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM EmployeePerformance")
            columns = [desc[0] for desc in cursor.description]
            self.data = pd.DataFrame(cursor.fetchall(), columns=columns)
            cursor.close()
            self.db_connection.close()

            if self.data.empty:
                print("No se encontraron datos en la tabla 'EmployeePerformance'.")
                exit(1)
        except mysql.Error as e:
            print(f"Error al procesar la tabla: {e}")
            exit(1)

    def calculate_statistics(self):
        stats = self.data.groupby('department').agg({
            'performance_score': ['mean', 'median', 'std'],
            'salary': ['mean', 'median', 'std'],
            'employee_id': 'count'
        }).rename(columns={'count': 'total_employees'})

        correlation_years_performance = self.data[['years_with_company', 'performance_score']].corr().iloc[0, 1]
        correlation_salary_performance = self.data[['salary', 'performance_score']].corr().iloc[0, 1]

        return stats, correlation_years_performance, correlation_salary_performance

    def display_statistics(self, stats, correlation_years_performance, correlation_salary_performance):
        print("Estadísticas por departamento:")
        print(stats)

        print("\nCorrelación entre years_with_company y performance_score:")
        print(correlation_years_performance)

        print("\nCorrelación entre salary y performance_score:")
        print(correlation_salary_performance)

    def plot_histograms(self):
        departments = self.data['department'].unique()
        for department in departments:
            dept_data = self.data[self.data['department'] == department]
            plt.hist(dept_data['performance_score'], bins=10, alpha=0.7)
            plt.title(f'Histograma del Performance Score - {department}')
            plt.xlabel('Performance Score')
            plt.ylabel('Frecuencia')
            plt.grid(True)
            plt.show()

    def plot_scatter_plots(self):
        plt.scatter(self.data['years_with_company'], self.data['performance_score'])
        plt.title('Years with Company vs. Performance Score')
        plt.xlabel('Years with Company')
        plt.ylabel('Performance Score')
        plt.grid(True)
        plt.show()

        plt.scatter(self.data['salary'], self.data['performance_score'])
        plt.title('Salary vs. Performance Score')
        plt.xlabel('Salary')
        plt.ylabel('Performance Score')
        plt.grid(True)
        plt.show()

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

# Crea una instancia de EmployeePerformanceAnalyzer
analyzer = EmployeePerformanceAnalyzer(db_connector.connection)
    
# Extrae los datos de la tabla
analyzer.fetch_data()

# Calcula las estadísticas y correlaciones
stats, correlation_years_performance, correlation_salary_performance = analyzer.calculate_statistics()

# Muestra las estadísticas y correlaciones
analyzer.display_statistics(stats, correlation_years_performance, correlation_salary_performance)

# Genera las visualizaciones
analyzer.plot_histograms()
analyzer.plot_scatter_plots()