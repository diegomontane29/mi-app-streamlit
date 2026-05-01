import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Proyecto Streamlit", layout="wide")

# Menú lateral
menu = st.sidebar.selectbox(
    "Menú de navegación",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

if menu == "Home":
    st.title("Aplicación en Streamlit")

    st.subheader("Fundamentos de programación")

    #ruta=r"C:\Users\DIEGO\OneDrive\Documents\trabajo DMC\logo.png"
    st.image("logo.png", width=150)
    st.write("### Información del estudiante")
    st.write("**Nombre:** Diego Eduardo Montané Quintana")
    st.write("**Módulo:** Módulo 1 - Fundamentos de Programación")
    st.write("**Año:** 2026")

    st.write("### Descripción del proyecto")
    st.write("""
    Esta aplicación fue desarrollada utilizando Streamlit como parte del curso de 
    Fundamentos de Programación. El objetivo es aplicar conceptos como:
    
    - Variables
    - Estructuras de datos
    - Control de flujo
    - Funciones
    - Programación orientada a objetos
    """)

    st.write("### Tecnologías utilizadas")
    st.markdown("""
    - Python  
    - Streamlit  
    """)

# ---------------- EJERCICIO 1 ----------------
elif menu == "Ejercicio 1":
    st.title("💰 Flujo de Caja con Listas")

    st.markdown("""
    Este módulo permite registrar movimientos financieros (ingresos y gastos).
    
    Puedes ingresar un concepto, seleccionar el tipo de movimiento y su valor.
    El sistema calculará automáticamente el flujo de caja.
    """)
    
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []
    
    concepto = st.text_input("Concepto")
    tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
    valor = st.number_input("Valor", min_value=0.0, step=1.0)

    if st.button("Agregar movimiento"):
        if concepto != "" and valor > 0:
            movimiento = {
                "Concepto": concepto,
                "Tipo": tipo,
                "Valor": valor
            }
            st.session_state.movimientos.append(movimiento)
            st.success("Movimiento agregado correctamente")
        else:
            st.error("Debes completar todos los campos correctamente")

    if st.session_state.movimientos:
        st.subheader("📋 Movimientos registrados")
        st.dataframe(st.session_state.movimientos)

        ingresos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
        gastos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
        saldo = ingresos - gastos

        st.subheader("📊 Resumen financiero")

        col1, col2, col3 = st.columns(3)

        col1.metric("Ingresos", f"S/ {ingresos:.2f}")
        col2.metric("Gastos", f"S/ {gastos:.2f}")
        col3.metric("Saldo", f"S/ {saldo:.2f}")

        if saldo > 0:
            st.success("El flujo de caja está A FAVOR ✅")
        elif saldo < 0:
            st.error("El flujo de caja está EN CONTRA ❌")
        else:
            st.info("El flujo de caja está equilibrado ⚖️")
    else:
        st.info("No hay movimientos registrados aún")

# ---------------- EJERCICIO 2 ----------------
elif menu == "Ejercicio 2":
    st.title("📦 Registro de Productos con NumPy y DataFrame")

    st.markdown("""
    Este módulo permite registrar productos usando arrays de NumPy y visualizar los datos en un DataFrame actualizado.
    """)



    # Inicializar array en session_state
    if "productos" not in st.session_state:
        st.session_state.productos = np.empty((0, 5), dtype=object)

    # Inputs con key para evitar duplicación
    nombre = st.text_input("Nombre del producto", key="nombre_producto")
    categoria = st.selectbox("Categoría", ["Abarrotes", "Tecnología", "Ropa", "Otros"], key="categoria_producto")
    precio = st.number_input("Precio", min_value=0.0, step=1.0, key="precio_producto")
    cantidad = st.number_input("Cantidad", min_value=0, step=1, key="cantidad_producto")

    # Cálculo del total
    total = precio * cantidad

    st.write(f"💰 Total calculado: **{total}**")

    # Botón agregar (controlado)
    if st.button("Agregar producto", key="btn_agregar_producto"):

        if nombre != "" and precio > 0 and cantidad > 0:

            nuevo_registro = np.array([[nombre, categoria, precio, cantidad, total]])

            st.session_state.productos = np.vstack([
                st.session_state.productos,
                nuevo_registro
            ])

            st.success("Producto agregado correctamente")

        else:
            st.error("Completa todos los campos correctamente")

    # Mostrar DataFrame
    if st.session_state.productos.shape[0] > 0:

        df = pd.DataFrame(
            st.session_state.productos,
            columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"]
        )

        st.subheader("📊 Inventario de productos")
        st.dataframe(df)



# ---------------- EJERCICIO 3 ----------------
elif menu == "Ejercicio 3":
    st.title("📊 Cálculo de Margen Neto (Función Externa)")

    st.markdown("""
    Este ejercicio utiliza una función externa para calcular el margen neto de una empresa.
    """)

    import libreria_funciones_proyecto1 as lf

    import pandas as pd

    # Inicializar historial
    if "historial_margen" not in st.session_state:
        st.session_state.historial_margen = []

    # Inputs
    ingresos = st.number_input("Ingresos", min_value=0.0, step=100.0)
    costos = st.number_input("Costos", min_value=0.0, step=100.0)
    gastos_operativos = st.number_input("Gastos operativos", min_value=0.0, step=100.0)
    impuestos = st.number_input("Impuestos", min_value=0.0, step=100.0)

    # Botón con key (evita problemas de rerun)
    if st.button("Calcular margen neto", key="btn_margen_neto"):

        try:
            resultado = lf.calcular_margen_neto(
                float(ingresos),
                float(costos),
                float(gastos_operativos),
                float(impuestos)
            )

            st.success("Cálculo realizado correctamente")

            st.write("### 📌 Resultados")
            st.write(f"💰 Utilidad bruta: {resultado['utilidad_bruta']}")
            st.write(f"📉 Utilidad neta: {resultado['utilidad_neta']}")
            st.write(f"📊 Margen neto (%): {resultado['margen_neto_pct']}%")

            # Evitar duplicados exactos
            nuevo = {
                "Ingresos": ingresos,
                "Costos": costos,
                "Gastos Operativos": gastos_operativos,
                "Impuestos": impuestos,
                "Utilidad Bruta": resultado["utilidad_bruta"],
                "Utilidad Neta": resultado["utilidad_neta"],
                "Margen %": resultado["margen_neto_pct"]
            }

            if nuevo not in st.session_state.historial_margen:
                st.session_state.historial_margen.append(nuevo)

        except Exception as e:
            st.error(f"Error al calcular: {e}")

    # Mostrar historial
    if len(st.session_state.historial_margen) > 0:
        st.subheader("📊 Historial de cálculos")

        df = pd.DataFrame(st.session_state.historial_margen)
        st.dataframe(df)

# ---------------- EJERCICIO 4 ----------------
elif menu == "Ejercicio 4":
    st.title("📈 Evaluación de Proyectos de Inversión")

    st.markdown("""
    Este módulo utiliza una clase externa para evaluar proyectos mediante VPN, ROI y Payback.
    """)

    from libreria_clases_proyecto1 import ProyectoInversion

    # ---------------- HISTORIAL ----------------
    if "historial_proyectos" not in st.session_state:
        st.session_state.historial_proyectos = []

    # ---------------- INPUTS ----------------
    nombre = st.text_input("Nombre del proyecto", key="nombre_proyecto")

    inversion = st.number_input("Inversión inicial", min_value=0.0, step=100.0, key="inversion")

    tasa = st.number_input("Tasa de descuento (%)", min_value=0.0, step=1.0, key="tasa")

    flujos_texto = st.text_area(
        "Flujos de caja (separados por coma)",
        key="flujos",
        placeholder="Ejemplo: 1000,1200,1500"
    )

    # Convertir flujos de forma segura
    flujos = []
    if flujos_texto:
        try:
            flujos = [float(x.strip()) for x in flujos_texto.split(",") if x.strip() != ""]
        except:
            st.error("❌ Error: los flujos deben ser números separados por coma")

    # ---------------- BOTÓN ----------------
    if st.button("Evaluar proyecto", key="btn_proyecto"):

        if nombre and len(flujos) > 0:

            try:
                proyecto = ProyectoInversion(
                    nombre,
                    float(inversion),
                    flujos,
                    float(tasa)
                )

                resultado = proyecto.resumen()

                st.success("Evaluación completada")

                # Mostrar resultados
                st.write("### 📊 Resultados")
                st.write(f"📌 Proyecto: {resultado['proyecto']}")
                st.write(f"💰 VPN: {resultado['vpn']}")
                st.write(f"📈 ROI: {resultado['roi_pct']}%")
                st.write(f"⏳ Payback: {resultado['payback_anios']} años")
                st.write(f"🎯 Decisión: {resultado['decision']}")

                # ---------------- EVITAR DUPLICADOS ----------------
                if resultado not in st.session_state.historial_proyectos:
                    st.session_state.historial_proyectos.append(resultado)

            except Exception as e:
                st.error(f"Error en el cálculo: {e}")

        else:
            st.warning("Completa todos los campos correctamente")

    # ---------------- HISTORIAL ----------------
    if len(st.session_state.historial_proyectos) > 0:

        st.subheader("📋 Historial de proyectos")

        df = pd.DataFrame(st.session_state.historial_proyectos)
        st.dataframe(df)
