import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1. Carregar dados via URLs do GitHub
base_url = "https://raw.githubusercontent.com/eduardosocek/supply-chain-inventory-analytics/main/data/"
products = pd.read_csv(base_url + "products.csv")
inventory = pd.read_csv(base_url + "inventory.csv")
orders = pd.read_csv(base_url + "orders.csv")

# 2. Processar com SQLite para Curva ABC
conn = sqlite3.connect(":memory:")
products.to_sql("products", conn, index=False, if_exists="replace")
inventory.to_sql("inventory", conn, index=False, if_exists="replace")
orders.to_sql("orders", conn, index=False, if_exists="replace")

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

# Cálculo da Curva ABC
abc_df['cum_revenue'] = abc_df['total_revenue'].cumsum()
abc_df['total_rev_sum'] = abc_df['total_revenue'].sum()
abc_df['cum_perc'] = (abc_df['cum_revenue'] / abc_df['total_rev_sum']) * 100

def get_abc_class(perc):
    if perc <= 70:
        return 'Classe A'
    elif perc <= 90:
        return 'Classe B'
    else:
        return 'Classe C'

abc_df['classe_abc'] = abc_df['cum_perc'].apply(get_abc_class)

# 3. Criar Gráfico Plotly com a identidade visual SA (Tons de Azul Escuro e Teal)
fig = px.bar(
    abc_df, 
    x='product_name', 
    y='total_revenue', 
    color='classe_abc',
    title="Curva ABC de Faturamento por Produto",
    labels={'product_name': 'Produto', 'total_revenue': 'Faturamento (R$)', 'classe_abc': 'Classe'},
    color_discrete_map={
        'Classe A': '#0f172a',  # Azul escuro sofisticado
        'Classe B': '#0ea5e9',  # Azul moderno
        'Classe C': '#10b981'   # Verde / Teal de destaque
    }
)
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Inter, sans-serif", color="#334155"),
    title_font=dict(size=18, color="#0f172a", family="Inter, sans-serif")
)

# Converter gráfico para HTML embutido
chart_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

# 4. Montar o HTML completo com a marca SA e Estilo Profissional
html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Supply Chain & Inventory Analytics | SA</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 0;
        }}
        header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            padding: 20px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .brand-container {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .sa-logo {{
            background-color: #0ea5e9;
            color: white;
            font-weight: 800;
            font-size: 24px;
            letter-spacing: 1px;
            padding: 10px 16px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .header-title h1 {{
            margin: 0;
            font-size: 22px;
            font-weight: 700;
        }}
        .header-title p {{
            margin: 4px 0 0 0;
            font-size: 13px;
            color: #94a3b8;
        }}
        .container {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border-left: 4px solid #0ea5e9;
        }}
        .kpi-card h3 {{
            margin: 0;
            font-size: 14px;
            color: #64748b;
            text-transform: uppercase;
        }}
        .kpi-card .value {{
            margin: 10px 0 0 0;
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #94a3b8;
            font-size: 12px;
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand-container">
            <div class="sa-logo">SA</div>
            <div class="header-title">
                <h1>Supply Chain & Inventory Analytics</h1>
                <p>Socek Analytics • Painel Executivo de Gestão de Estoque</p>
            </div>
        </div>
        <div style="font-size: 13px; color: #94a3b8;">
            Status: <span style="color: #10b981; font-weight: bold;">● Online / Atualizado</span>
        </div>
    </header>

    <div class="container">
        <!-- KPIs Principais -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <h3>Faturamento Total</h3>
                <div class="value">R$ {abc_df['total_revenue'].sum():,.2f}</div>
            </div>
            <div class="kpi-card" style="border-left-color: #10b981;">
                <h3>Total de Peças Vendidas</h3>
                <div class="value">{abc_df['total_units_sold'].sum():,.0f} un</div>
            </div>
            <div class="kpi-card" style="border-left-color: #0f172a;">
                <h3>Produtos Classe A</h3>
                <div class="value">{len(abc_df[abc_df['classe_abc'] == 'Classe A'])} itens</div>
            </div>
        </div>

        <!-- Gráfico Interativo -->
        <div class="card">
            {chart_html}
        </div>
    </div>

    <footer>
        Desenvolvido por Socek Analytics (SA) • Dados integrados via Pipeline SQLite & GitHub
    </footer>

</body>
</html>
"""

# Salvar o arquivo HTML
with open("supply_chain_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Relatório HTML gerado com sucesso como 'supply_chain_report.html'!")
