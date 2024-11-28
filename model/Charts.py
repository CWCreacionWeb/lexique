import sys
# Añadir el directorio de la clase
sys.path.append('/home/guille/UOC/lexique/')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
# import ipywidgets as widgets
# from IPython.display import display
import random

class Charts:

    def __init__(self, file, encoding='latin1', **kwargs):
        data = pd.read_csv(file, encoding=encoding, on_bad_lines='skip')
        self.df = pd.DataFrame(data)
        self.plt = plt
        self.sns = sns
        self.px = px

        # Configuro el label de todas las gráficas con los nombres de las regiones
        self.seasonal_decompose = seasonal_decompose

        # Formatear columnas como fechas si se especifican
        for column in kwargs.get('date_columns', []):
            self.formatDate(column)

    def showData(self, key=None):
        if key:
            return self.df[key]
        else:
            return self.df

    def selectedKeys(self, keys):
        return self.df[keys]

    def makeFrame(data):
        return pd.DataFrame(data)

    def showColumns(self):
        return self.df.columns

    def isNull(self):
        return self.df.isnull().sum()

    def clearData(self, column_name):
        """
        Elimina una columna si existe en el DataFrame.
        Muestra un mensaje si no se encuentra la columna.
        """
        if column_name in self.df.columns:
            self.df = self.df.drop(columns=[column_name])
            print(f"Columna eliminada: {column_name}")
        else:
            print(f"Columna no encontrada: {column_name}")

    def formatDate(self, column_name):
        """
        Convierte una columna en formato datetime, eliminando microsegundos y zona horaria.
        """
        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce')  # Asegurar formato datetime
        self.df[column_name] = self.df[column_name].dt.strftime('%Y-%m-%d %H:%M:%S')  # Formato simplificado

    def show(self):
        plt.show()

    def temporada(self, fecha):
        if fecha in [12, 1, 2]:
            return 'Invierno'
        elif fecha in [3, 4, 5]:
            return 'Primavera'
        elif fecha in [6, 7, 8]:
            return 'Verano'
        else:
            return 'Otoño'

    def to_excel(self, data, filename):
        # Guardar como archivo Excel
        excel_file = filename + '.xlsx'  # Nombre del archivo Excel a crear
        data.to_excel(excel_file, index=False)  # index=False para no incluir el índice como una columna

    def topRegions(self, num=5, exclude=None):
        if exclude:
            self.df = self.df[self.df['region'].isin(self.df.groupby('region')['Total Volume'].sum().sort_values(ascending=False).head(num).index)]
            self.df = self.df[self.df['region'] != exclude]
        else:
            self.df = self.df[self.df['region'].isin(self.df.groupby('region')['Total Volume'].sum().sort_values(ascending=False).head(num).index)]

# Nuevo método para limpiar columnas específicas
    def cleanColumns(self, columns_to_remove):
        """
        Elimina columnas específicas si existen en el DataFrame.
        Args:
            columns_to_remove (list): Lista de nombres de columnas a eliminar.
        """
        for col in columns_to_remove:
            if col in self.df.columns:
                self.df = self.df.drop(columns=[col])
                print(f"Columna eliminada: {col}")
            else:
                print(f"Columna no encontrada: {col}")


    def saveChart(self, nombre):
        """
        Guarda la gráfica en un archivo PNG.
        """
        filename = f'graficas/{nombre}_chart_{random.randint(0, 1000)}.png'
        self.plt.savefig(filename)
        print(f"Gráfica guardada como {filename}")
