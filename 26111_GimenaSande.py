import pandas as pd

ventas_path = r"C:\Users\gimen\OneDrive\Documentos\Python\Entrega\datasets\ventas.csv"
marketing_path = r"C:\Users\gimen\OneDrive\Documentos\Python\Entrega\datasets\marketing.csv"
clientes_path = r"C:\Users\gimen\OneDrive\Documentos\Python\Entrega\datasets\clientes.csv"

ventas = pd.read_csv(ventas_path)
marketing = pd.read_csv(marketing_path)
clientes = pd.read_csv(clientes_path)

# Función para análisis exploratorio
def eda(df, nombre):
    print(f"=== {nombre} ===")
    print("shape:", df.shape)
    print("columnas:", list(df.columns))
    print("dtypes:")
    print(df.dtypes)
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nPrimeras filas:")
    print(df.head(5))  # reemplaza display por print
    print("\nDescribe (numérico):")
    print(df.describe(include='number'))
    print("-"*100)

# -------------------------------------------------
# 1️⃣ Crear copias independientes para no modificar los  dataframes originales
# -------------------------------------------------
ventas_clean = ventas.copy()
clientes_clean = clientes.copy()
marketing_clean = marketing.copy()

# NORMALIZAMOS TEXTOS: evita errores por may/min y espacios extra, facilitando conteos, agrupaciones y análisis confiables
# Columna producto

ventas_clean["producto"] = (
    ventas_clean["producto"]
    .astype(str) # convierte a texto
    .str.title() # mayúscula inicial en cada palabra
    .str.strip() # quita espacios al inicio y final
    .str.replace( " +"," ", regex=True)  #  reemplaza espacios múltiples por uno solo
)
# Columna categoria
ventas_clean["categoria"] = (
    ventas_clean["categoria"]
    .astype(str) # convierte a texto
    .str.title() # mayúscula inicial en cada palabra
    .str.strip() # quita espacios al inicio y final
    .str.replace(" +", " ", regex=True)  #  reemplaza espacios múltiples por uno solo
)

# NORMALIZAMOS FECHAS: con pd.to_datetime
ventas_clean["fecha_venta"] = pd.to_datetime(ventas_clean["fecha_venta"], errors="coerce", dayfirst=True)
marketing_clean["fecha_inicio"] = pd.to_datetime(marketing_clean["fecha_inicio"], errors="coerce", dayfirst=True)
marketing_clean["fecha_fin"] = pd.to_datetime(marketing_clean["fecha_fin"], errors="coerce", dayfirst=True)

# NORMALIZAMOS PRECIO, sacandole el $
ventas_clean["precio"] = (
        ventas_clean["precio"]
        .astype(str)
        .str.replace("$", "", regex=False)  # Elimina el símbolo
        .str.replace(",", "", regex=False)  # Elimina comas
        .str.strip() # Quita espacios sobrantes
    )
# Lo convierto a dato numerico
ventas_clean["precio"] = pd.to_numeric(ventas_clean["precio"], errors="coerce")

#-----------------------------------------------
# 3 Completar valores null con 0
#-----------------------------------------------

# .fillna(0) reemplaza todos los valores NaN en la columna cantidad por 0.
ventas_clean["cantidad"] = ventas_clean["cantidad"].fillna(0)
# Completar precio con promedio por producto
ventas_clean["precio"] = ventas_clean.groupby("producto")["precio"].transform(
    lambda x: x.fillna(x.mean())
)
'''
1 groupby("producto")["precio"]
Agrupa el DataFrame por cada producto y selecciona la columna precio.
Cada grupo contiene todas las filas del mismo producto.
.transform(lambda x: x.fillna(x.mean()))
transform() devuelve un resultado del mismo tamaño que el DataFrame original, fila por fila.
Dentro de la lambda:
x.fillna(x.mean()) reemplaza los NaN del grupo por el promedio de los precios de ese producto.
'''

ventas_clean = ventas_clean.drop_duplicates()
clientes_clean = clientes_clean.drop_duplicates()
marketing_clean = marketing_clean.drop_duplicates()

# Llamamos a la función para cada DataFrame
for dataframe, name in [(ventas_clean, "Ventas"), (marketing_clean, "Marketing"), (clientes_clean, "Clientes")]:
    eda(dataframe, f"Análisis exploratorio de {name}")
