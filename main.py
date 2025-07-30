
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="🛠️ Registro de Mantenimiento ULTRONA", layout="centered")
st.title("🛠️ Registro de Mantenimiento Mensual - ULTRONA")

EXCEL_FILE = "registro_mant_ultrona.xlsx"
BACKUP_DIR = "respaldo"

# Crear carpeta de respaldo si no existe
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Cargar datos
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Fecha y Hora", "Mantenimiento Realizado", "Operador"])

# Fecha y hora por separado
fecha = st.date_input("📅 Fecha", value=datetime.now().date())
hora = st.time_input("🕒 Hora", value=datetime.now().time())
fecha_hora = datetime.combine(fecha, hora)

mantenimiento = st.selectbox("🧹 Mantenimiento", [
    "Remover y limpiar el deposito de basura",
    "Limpiar la plataforma de la tira y del deposito de residuos",
    "Limpieza del transportador de tira",
    "Limpieza y desinfeccion externa",
    "Calibracion",
    "Cambio de papel",
    "Cambio de fusibles"
])

operador = st.selectbox("👨‍🔧 Operador", [
    "Anibal Saavedra", "Juan Ramos", "Nycole Farias", "Stefanie Maureira", "Maria J.Vera",
    "Felipe Fernandez", "Paula Gutierrez", "Paola Araya", "Maria Rodriguez", "Pamela Montenegro"
])

if st.button("✅ Guardar Registro"):
    nueva_fila = {
        "Fecha y Hora": fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
        "Mantenimiento Realizado": mantenimiento,
        "Operador": operador
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    # respaldo automático
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    respaldo_path = os.path.join(BACKUP_DIR, f"respaldo_mant_{now}.xlsx")
    df.to_excel(respaldo_path, index=False)
    st.success("✅ Registro guardado y respaldado correctamente.")

# Filtro por mes
st.markdown("### 🔍 Buscar registros por mes")
mes_seleccionado = st.selectbox("📆 Mes", sorted(df["Fecha y Hora"].str[:7].unique(), reverse=True))
df_filtrado = df[df["Fecha y Hora"].str.startswith(mes_seleccionado)]
st.dataframe(df_filtrado, use_container_width=True)

# Descargar registros filtrados
def to_excel_memory(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Descargar registros filtrados",
    data=to_excel_memory(df_filtrado),
    file_name=f"mant_ultrona_{mes_seleccionado}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
