import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Función para mostrar gráficos
def show_graphs(df, file_name):
    st.subheader("Gráficos")

    if file_name == 'train.csv':
        # Verificar columnas necesarias
        if 'Ticket' not in df.columns or 'Embarked' not in df.columns:
            st.error("El archivo CSV debe contener las columnas 'Ticket' y 'Embarked'.")
            return

        # Gráfico de distribución de Embarked
        st.subheader("Distribución de Embarked")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='Embarked', ax=ax)
        ax.set_title("Distribución de Embarked")
        ax.set_xlabel("Embarked")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

        # Gráfico de torta de Ticket
        st.subheader("Distribución de Ticket")
        ticket_counts = df['Ticket'].value_counts().head(10)  # Muestra las 10 categorías más frecuentes
        fig, ax = plt.subplots()
        ax.pie(ticket_counts, labels=ticket_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Distribución de Ticket")
        st.pyplot(fig)

        # Gráfico de cascada de Embarked
        st.subheader("Gráfico de Cascada de Embarked")
        embarked_counts = df['Embarked'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(embarked_counts.index, embarked_counts.values, color='skyblue')
        ax.set_title("Gráfico de Cascada de Embarked")
        ax.set_xlabel("Embarked")
        ax.set_ylabel("Cantidad")
        
        # Agregar etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')
        
        st.pyplot(fig)

        # Gráfico de líneas de Ticket
        st.subheader("Gráfico de Líneas de Ticket")
        ticket_data = df[['Ticket', 'Embarked']].dropna()
        ticket_counts = ticket_data['Ticket'].value_counts()
        sorted_ticket_counts = ticket_counts.sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(sorted_ticket_counts.index, sorted_ticket_counts.values, marker='o', linestyle='-', color='b')
        ax.set_title("Gráfico de Líneas de Ticket")
        ax.set_xlabel("Ticket")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

    elif file_name == 'test.csv':
        # Verificar columnas necesarias
        if 'PassengerId' not in df.columns or 'Age' not in df.columns:
            st.error("El archivo CSV debe contener las columnas 'PassengerId' y 'Age'.")
            return

        # Gráfico de distribución de Age
        st.subheader("Distribución de Age")
        fig, ax = plt.subplots()
        sns.histplot(df['Age'].dropna(), bins=30, kde=True, ax=ax)
        ax.set_title("Distribución de Edad")
        ax.set_xlabel("Edad")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

        # Gráfico de torta de Sex
        if 'Sex' in df.columns:
            st.subheader("Porcentaje de Sex")
            sex_counts = df['Sex'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title("Porcentaje de Sex")
            st.pyplot(fig)
        else:
            st.warning("El archivo CSV no contiene la columna 'Sex'.")

        # Gráfico de cascada de Age
        st.subheader("Gráfico de Cascada de Age")
        age_data = df['Age'].dropna().value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(age_data.index, age_data.values, color='skyblue')
        ax.set_title("Gráfico de Cascada de Edad")
        ax.set_xlabel("Edad")
        ax.set_ylabel("Cantidad")
        
        # Agregar etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')
        
        st.pyplot(fig)

        # Gráfico de líneas de Age
        st.subheader("Gráfico de Líneas de Age")
        age_data = df[['PassengerId', 'Age']].dropna().sort_values(by='PassengerId')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(age_data['PassengerId'], age_data['Age'], marker='o', linestyle='-', color='b')
        ax.set_title("Gráfico de Líneas de Edad")
        ax.set_xlabel("PassengerId")
        ax.set_ylabel("Edad")
        st.pyplot(fig)

# Función para mostrar la tabla y los controles
def show_table_and_controls(df, file_name):
    st.subheader(f"Datos de {file_name}")
    st.dataframe(df)

    # Botón para guardar en Excel
    if st.button("Guardar en Excel", key="save_excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        st.download_button(
            label="Descargar archivo Excel",
            data=output.getvalue(),
            file_name='datos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # Eliminar datos
    if st.button("Eliminar Datos", key="delete_data"):
        row_to_delete = st.number_input("Número de fila a eliminar:", min_value=0, max_value=len(df)-1, value=0)
        if row_to_delete < len(df):
            df = df.drop(index=row_to_delete).reset_index(drop=True)
            st.success(f"Fila {row_to_delete} eliminada.")
            st.dataframe(df)
        else:
            st.error("Número de fila inválido.")

    # Editar datos
    if st.button("Editar Datos", key="edit_data"):
        row_to_edit = st.number_input("Número de fila a editar:", min_value=0, max_value=len(df)-1, value=0)
        if row_to_edit < len(df):
            edited_data = {}
            for col in df.columns:
                edited_data[col] = st.text_input(f"Editar {col} en fila {row_to_edit}:", value=str(df.at[row_to_edit, col]))
            
            if st.button("Guardar Edición", key="save_edit"):
                df.loc[row_to_edit] = pd.Series(edited_data)
                st.success(f"Fila {row_to_edit} editada.")
                st.dataframe(df)
        else:
            st.error("Número de fila inválido.")

    # Mostrar gráficos si el archivo es test.csv o train.csv
    if file_name in ['test.csv', 'train.csv']:
        show_graphs(df, file_name)

# Aplicación principal
def main():
    st.title("Visualización de Datos y Controles")

    st.subheader("Carga de Archivos CSV")
    
    # Botón para subir archivos CSV
    uploaded_files = st.file_uploader("Selecciona los archivos CSV:", type=["csv"], accept_multiple_files=True)
    
    if uploaded_files:
        file_names = [file.name for file in uploaded_files]
        selected_file = st.selectbox("Selecciona el archivo CSV para analizar:", file_names)
        
        # Cargar datos
        for uploaded_file in uploaded_files:
            if uploaded_file.name == selected_file:
                df = pd.read_csv(uploaded_file)
                show_table_and_controls(df, uploaded_file.name)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
