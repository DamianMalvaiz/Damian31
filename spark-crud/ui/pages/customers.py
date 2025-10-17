# ui/pages/customers.py
# Página de gestión de customers con CRUD completo
# ================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import time

def render():
    """Renderiza la página de gestión de customers"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            👥 Gestión de Customers Épica
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo de customers
    @st.cache_data
    def generate_customers_data():
        np.random.seed(42)  # Para datos consistentes
        
        names = [
            "Ana García", "Luis Rodríguez", "María López", "Carlos Martín", "Laura Sánchez",
            "Diego Fernández", "Sofia Ruiz", "Javier Moreno", "Carmen Jiménez", "Pablo Álvarez",
            "Elena Romero", "Miguel Torres", "Isabel Navarro", "Andrés Ramos", "Cristina Vega",
            "Fernando Gil", "Natalia Serrano", "Roberto Blanco", "Mónica Castro", "Alejandro Ortega"
        ]
        
        jobs = [
            "Desarrollador", "Diseñador", "Manager", "Analista", "Consultor",
            "Arquitecto", "DevOps", "QA Tester", "Product Owner", "Scrum Master"
        ]
        
        data = []
        for i in range(100):
            data.append({
                'id': i + 1,
                'name': np.random.choice(names) + f" {i+1}",
                'email': f"user{i+1}@brutal.com",
                'phone': f"+34 {np.random.randint(600, 700)} {np.random.randint(100, 999)} {np.random.randint(100, 999)}",
                'sex': np.random.choice(['M', 'F']),
                'job_title': np.random.choice(jobs),
                'balance': np.random.uniform(100, 10000),
                'created_at': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 365)),
                'dob': date(1980, 1, 1) + pd.Timedelta(days=np.random.randint(0, 15000))
            })
        
        return pd.DataFrame(data)
    
    customers_df = generate_customers_data()
    
    # Formulario de creación/edición
    with st.expander("➕ Agregar/Editar Customer", expanded=False):
        st.markdown("### 📝 Formulario de Customer")
        
        with st.form("customer_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                name = st.text_input("👤 Nombre Completo", placeholder="Ej: Ana García")
                email = st.text_input("📧 Email", placeholder="ana@ejemplo.com")
                phone = st.text_input("📱 Teléfono", placeholder="+34 600 123 456")
            
            with col2:
                sex = st.selectbox("⚧ Sexo", ["M", "F"])
                job_title = st.text_input("💼 Puesto de Trabajo", placeholder="Desarrollador")
                balance = st.number_input("💰 Balance", min_value=0.0, value=1000.0, step=100.0)
            
            with col3:
                dob = st.date_input("🎂 Fecha de Nacimiento", value=date(1990, 1, 1))
                created_at = st.date_input("📅 Fecha de Registro", value=date.today())
                
                # Botón de envío
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("💾 Guardar Customer", use_container_width=True)
        
        if submitted and name and email:
            # Simular guardado
            with st.spinner("Guardando customer..."):
                time.sleep(1)
            st.success(f"✅ Customer '{name}' guardado exitosamente!")
            st.balloons()
    
    # Filtros avanzados
    st.markdown("### 🎯 Filtros Avanzados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_name = st.text_input("🔍 Buscar por nombre", placeholder="Ingresa nombre...")
    
    with col2:
        filter_sex = st.selectbox("⚧ Filtrar por sexo", ["Todos", "M", "F"])
    
    with col3:
        min_balance = st.number_input("💰 Balance mínimo", min_value=0.0, value=0.0, step=100.0)
    
    with col4:
        job_filter = st.selectbox("💼 Filtrar por trabajo", 
                                 ["Todos"] + sorted(customers_df['job_title'].unique().tolist()))
    
    # Aplicar filtros
    filtered_df = customers_df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
    
    if filter_sex != "Todos":
        filtered_df = filtered_df[filtered_df['sex'] == filter_sex]
    
    if min_balance > 0:
        filtered_df = filtered_df[filtered_df['balance'] >= min_balance]
    
    if job_filter != "Todos":
        filtered_df = filtered_df[filtered_df['job_title'] == job_filter]
    
    # Estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Customers", len(filtered_df), delta=f"de {len(customers_df)}")
    
    with col2:
        avg_balance = filtered_df['balance'].mean() if len(filtered_df) > 0 else 0
        st.metric("💰 Balance Promedio", f"€{avg_balance:,.0f}")
    
    with col3:
        male_count = len(filtered_df[filtered_df['sex'] == 'M'])
        st.metric("👨 Hombres", male_count)
    
    with col4:
        female_count = len(filtered_df[filtered_df['sex'] == 'F'])
        st.metric("👩 Mujeres", female_count)
    
    # Tabla principal
    st.markdown(f"### 📋 Lista de Customers ({len(filtered_df)} resultados)")
    
    if len(filtered_df) > 0:
        # Configurar columnas para mostrar
        display_df = filtered_df.copy()
        display_df['balance'] = display_df['balance'].apply(lambda x: f"€{x:,.2f}")
        display_df['created_at'] = display_df['created_at'].dt.strftime('%d/%m/%Y')
        display_df['dob'] = pd.to_datetime(display_df['dob']).dt.strftime('%d/%m/%Y')
        
        # Agregar columna de selección
        display_df.insert(0, '✅', False)
        
        # Editor de datos
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            height=400,
            hide_index=True,
            column_config={
                "✅": st.column_config.CheckboxColumn("Seleccionar"),
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "name": st.column_config.TextColumn("Nombre"),
                "email": st.column_config.TextColumn("Email"),
                "phone": st.column_config.TextColumn("Teléfono"),
                "sex": st.column_config.SelectboxColumn("Sexo", options=["M", "F"]),
                "job_title": st.column_config.TextColumn("Trabajo"),
                "balance": st.column_config.TextColumn("Balance"),
                "created_at": st.column_config.TextColumn("Creado"),
                "dob": st.column_config.TextColumn("Nacimiento")
            }
        )
        
        # Botones de acción
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("✅ Guardar Cambios", use_container_width=True):
                with st.spinner("Guardando cambios..."):
                    time.sleep(1)
                st.success("💾 Cambios guardados exitosamente!")
        
        with col2:
            selected_count = edited_df['✅'].sum()
            if st.button(f"🗑️ Eliminar Seleccionados ({selected_count})", use_container_width=True):
                if selected_count > 0:
                    with st.spinner(f"Eliminando {selected_count} customers..."):
                        time.sleep(1)
                    st.success(f"🗑️ {selected_count} customers eliminados!")
                else:
                    st.warning("⚠️ Selecciona al menos un customer")
        
        with col3:
            if st.button("📊 Generar Reporte", use_container_width=True):
                with st.spinner("Generando reporte..."):
                    time.sleep(2)
                st.success("📈 Reporte generado exitosamente!")
        
        with col4:
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📤 Exportar CSV",
                data=csv_data,
                file_name=f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        st.info("🔍 No se encontraron customers con los filtros aplicados")
    
    # Analytics rápidos
    if len(filtered_df) > 0:
        st.markdown("### 📊 Analytics Rápidos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Distribución de Balance")
            
            # Crear bins para el histograma
            balance_bins = pd.cut(filtered_df['balance'], bins=5, precision=0)
            balance_counts = balance_bins.value_counts().sort_index()
            
            chart_data = pd.DataFrame({
                'Rango': [f"€{int(interval.left):,}-€{int(interval.right):,}" for interval in balance_counts.index],
                'Cantidad': balance_counts.values
            })
            
            st.bar_chart(chart_data.set_index('Rango'))
        
        with col2:
            st.markdown("#### 👥 Distribución por Trabajo")
            
            job_counts = filtered_df['job_title'].value_counts().head(8)
            
            st.bar_chart(job_counts)
        
        # Tabla de estadísticas
        st.markdown("#### 📈 Estadísticas Detalladas")
        
        stats_data = {
            'Métrica': [
                'Total Customers',
                'Balance Total',
                'Balance Promedio',
                'Balance Máximo',
                'Balance Mínimo',
                'Edad Promedio (aprox)',
                'Registros este mes',
                'Tasa de crecimiento'
            ],
            'Valor': [
                f"{len(filtered_df):,}",
                f"€{filtered_df['balance'].sum():,.2f}",
                f"€{filtered_df['balance'].mean():,.2f}",
                f"€{filtered_df['balance'].max():,.2f}",
                f"€{filtered_df['balance'].min():,.2f}",
                f"{np.random.randint(25, 45)} años",
                f"{np.random.randint(15, 35)}",
                f"+{np.random.uniform(8, 15):.1f}%"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)