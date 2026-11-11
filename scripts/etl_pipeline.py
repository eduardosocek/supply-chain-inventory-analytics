import os
import sqlite3
import pandas as pd

# 1. Definir caminhos relativos ao projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "supply_chain.db")

print("🔍 Lendo arquivos da pasta data...")

# 2. Ingestão dos CSVs
df_products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
df_inventory = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))
df_orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))

# 3. Conexão com o banco SQLite
conn = sqlite3.connect(DB_PATH)

# 4. Gravação no banco de dados
df_products.to_sql("products", conn, if_exists="replace", index=False)
df_inventory.to_sql("inventory", conn, if_exists="replace", index=False)
df_orders.to_sql("orders", conn, if_exists="replace", index=False)

print("✅ Banco 'supply_chain.db' criado e atualizado com sucesso!")
conn.close()
