import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Supply Chain & Inventory Analytics",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Supply Chain & Inventory Health Dashboard")
st.markdown("Visão integrada de saúde de estoque, rastreabilidade de itens e Curva ABC.")

# 1. Carregar dados (Lê os CSVs da pasta data/)
@st.cache_data
def load_data():
    products = pd.read_csv("data/products.csv")
    inventory = pd.read_csv("data/inventory.csv")
    orders = pd.read_csv("data/orders.csv")
    
    # Criar conexão com SQLite em memória para queries dinâmicas
    conn = sqlite3.connect(":memory:")
    products.to_sql("products", conn, index=False, if_exists="replace")
    inventory.to_sql("inventory", conn, index=False, if_exists="replace")
    orders.to_sql("orders", conn, index=False, if_exists="replace")
    
    return products, inventory, orders, conn

df_products, df_inventory, df_orders, conn = load_data()

# Aba 1: Curva ABC & Visão Geral | Aba 2: Rastreio por Item (Drill-down)
tab1, tab2 = st.tabs(["📊 Visão Geral & Curva ABC", "🔍 Rastreio Individual de Item"])

# ============================================================
# ABA 1: VISÃO GERAL & CURVA ABC
# ============================================================
with tab1:
    # Query para Curva ABC
    query_abc = """
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(o.quantity_ordered) AS total_units_sold,
        ROUND(SUM(o.quantity_ordered * p.unit_price), 2) AS total_revenue
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    WHERE o.order_status IN ('Shipped', 'Delivered')
    GROUP BY p.product_id, p.product_name, p.category
    ORDER BY total_revenue DESC;
    """
    abc_df = pd.read_sql_query(query_abc, conn)
    
    # Cálculo da Curva ABC em Python
    abc_df['cum_revenue'] = abc_df['total_revenue'].cumsum()
    abc_df['total_rev_sum'] = abc_df['total_revenue'].sum()
    abc_df['cum_perc'] = (abc_df['cum_revenue'] / abc_df['total_rev_sum']) * 100
    
    def get_abc_class(perc):
        if perc <= 70:
            return 'Classe A (Alto Impacto)'
        elif perc <= 90:
            return 'Classe B (Médio Impacto)'
        else:
            return 'Classe C (Baixo Impacto)'
            
    abc_df['classe_abc'] = abc_df['cum_perc'].apply(get_abc_class)
    
    # KPIs Topo
    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {abc_df['total_revenue'].sum():,.2f}")
    col2.metric("Total de Peças Expedidas", f"{abc_df['total_units_sold'].sum():,.0f} un")
    col3.metric("Produtos em Classe A", len(abc_df[abc_df['classe_abc'] == 'Classe A (Alto Impacto)']))
    
    st.divider()
    
    # Gráfico Curva ABC (Pareto)
    st.subheader("📈 Classificação Curva ABC (Faturamento Acumulado)")
    fig_abc = px.bar(
        abc_df, 
        x='product_name', 
        y='total_revenue', 
        color='classe_abc',
        title="Faturamento por Produto e Classificação ABC",
        labels={'product_name': 'Produto', 'total_revenue': 'Faturamento (R$)', 'classe_abc': 'Classe ABC'},
        color_discrete_map={
            'Classe A (Alto Impacto)': '#2ecc71',
            'Classe B (Médio Impacto)': '#f1c40f',
            'Classe C (Baixo Impacto)': '#e74c3c'
        }
    )
    st.plotly_chart(fig_abc, use_container_width=True)
    
    st.dataframe(abc_df[['product_id', 'product_name', 'category', 'total_revenue', 'cum_perc', 'classe_abc']], use_container_width=True)

# ============================================================
# ABA 2: DRILL-DOWN / RASTREIO INDIVIDUAL DO ITEM
# ============================================================
with tab2:
    st.subheader("🔎 Consulta Detalhada por Código / Nome do Produto")
    
    # Dropdown de seleção de produto
    selected_product_name = st.selectbox(
        "Selecione o produto para analisar o histórico completo:",
        df_products['product_name'].unique()
    )
    
    # Dados do produto selecionado
    prod_info = df_products[df_products['product_name'] == selected_product_name].iloc[0]
    p_id = prod_info['product_id']
    
    # Métricas do produto
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("SKU / ID", p_id)
    m2.metric("Categoria", prod_info['category'])
    m3.metric("Preço Unitário", f"R$ {prod_info['unit_price']:.2f}")
    m4.metric("Estoque de Segurança", f"{prod_info['safety_stock']} un")
    
    st.divider()
    
    col_inv, col_orders = st.columns(2)
    
    with col_inv:
        st.subheader("📦 Evolução Diária do Estoque (Snapshot)")
        inv_prod = df_inventory[df_inventory['product_id'] == p_id].sort_values('snapshot_date')
        
        fig_inv = px.line(
            inv_prod, 
            x='snapshot_date', 
            y='quantity_on_hand',
            markers=True,
            title=f"Histórico de Estoque: {selected_product_name}",
            labels={'snapshot_date': 'Data', 'quantity_on_hand': 'Qtd em Mão'}
        )
        # Linha de alerta de Safety Stock
        fig_inv.add_hline(y=prod_info['safety_stock'], line_dash="dash", line_color="red", annotation_text="Safety Stock")
        st.plotly_chart(fig_inv, use_container_width=True)
        
    with col_orders:
        st.subheader("🚚 Histórico de Saídas e Expedição")
        orders_prod = df_orders[df_orders['product_id'] == p_id].sort_values('order_date', ascending=False)
        st.write(f"Total de pedidos encontrados: **{len(orders_prod)}**")
        st.dataframe(orders_prod[['order_id', 'order_date', 'quantity_ordered', 'order_status', 'shipping_days']], use_container_width=True)
