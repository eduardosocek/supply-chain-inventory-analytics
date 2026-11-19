🇧🇷 Português · [🇺🇸 English](README.md)

# 📦 Supply Chain & Inventory Analytics

Painel de estoque que roda direto no navegador. Você aponta para os CSVs do armazém e vê faturamento, Curva ABC, risco de ruptura e saldo de cada item. Sem servidor, sem instalação, sem login.

**Acesse:** https://eduardosocek.github.io/supply-chain-inventory-analytics/

## 🎯 Problema que resolve

Armazéns sofrem com pouca visibilidade do estoque: ruptura que ninguém previu, excesso parado e decisão tomada com planilha desatualizada. Painéis tradicionais também são difíceis de compartilhar. Aqui, quem tem o link e os arquivos já tem o painel.

## ✨ O que o painel faz

- **Indicadores:** faturamento, peças vendidas, produtos Classe A, margem bruta, prazo médio de envio e estoque crítico/atenção.
- **Curva ABC** de faturamento, com linha de percentual acumulado e guias de 70% e 90%.
- **Filtro cruzado, como no Power BI:** clique numa barra, categoria ou classe e todo o painel se refaz. Clique de novo para limpar.
- **Alertas de estoque** com cobertura em dias.
- **Detalhe do produto:** histórico diário de estoque com as faixas de segurança e reposição, mais a lista de pedidos.
- **Tabela de saldos** de todos os itens, com busca e ordenação.
- **Atualização automática** a cada 10, 30 ou 60 segundos.

## 📂 Fontes de dados

| Fonte | Como funciona |
|---|---|
| **Exemplo** | Lê os CSVs fictícios de `data/sample/`. |
| **Pasta do PC** | Você escolhe a pasta e a página lê todos os CSVs dela. Relê sozinha com a atualização automática. Só Chrome e Edge. |
| **Google Sheets** | Publique cada aba como CSV (Arquivo › Compartilhar › Publicar na Web) e cole os links. |
| **Escolher CSVs** | Selecione os arquivos manualmente. Não atualiza sozinho. |

**Os arquivos não precisam ter nome fixo.** O tipo é reconhecido pelas colunas. Vários arquivos do mesmo tipo (por exemplo, um por mês) são somados, e linhas repetidas são removidas.

### Colunas esperadas

| Tipo | Colunas obrigatórias |
|---|---|
| Produtos | `product_id`, `product_name`, `category`, `unit_price`, `reorder_point`, `safety_stock` (`unit_cost` é opcional, usado na margem) |
| Estoque | `snapshot_date`, `product_id`, `quantity_on_hand` |
| Pedidos | `order_id`, `order_date`, `product_id`, `quantity_ordered`, `order_status`, `shipping_days` |

## 🧮 Regras de cálculo

- **Faturamento:** pedidos `Shipped` e `Delivered`, quantidade × `unit_price`. Pedidos `Cancelled` ficam de fora.
- **Curva ABC:** o produto entra na Classe A se o faturamento acumulado *antes* dele for menor que 70%, na B se for menor que 90%, e na C no restante.
- **Status de estoque:** `CRÍTICO` quando o saldo é menor ou igual ao estoque de segurança. `ATENÇÃO` quando é menor ou igual ao ponto de reposição. `OK` nos demais casos.
- **Cobertura (dias):** saldo atual ÷ venda média diária, usando o período entre o primeiro e o último pedido.
- **Margem bruta:** (faturamento − unidades × `unit_cost`) ÷ faturamento.
- **Prazo médio de envio:** média de `shipping_days` dos pedidos expedidos e entregues.
- **Saldo atual:** última posição de cada produto em `snapshot_date`.
- Valores exibidos em **R$**.

## 🔒 Privacidade

Todo o cálculo acontece no navegador. Os arquivos da pasta ou do upload **não são enviados a nenhum servidor**. O link compartilha a ferramenta, não os dados: cada pessoa abre com a própria fonte.

> Não coloque dados reais de empresa neste repositório público. Os arquivos de `data/sample/` são fictícios.

## ⚠️ Limitações

- Servidor de empresa como fonte de dados ainda não é suportado (esbarra em CORS, HTTP misto e firewall).
- Os nomes das colunas precisam ser os da tabela acima.
- Excel (`.xlsx`) não é lido. Exporte para CSV.
- Escolher pasta exige Chrome ou Edge. O navegador bloqueia pastas como Downloads, Documentos e Área de trabalho; use uma subpasta. Em redes corporativas, a política da TI pode bloquear o recurso. Nesse caso, use "Escolher CSVs".
- Os dados de exemplo são fictícios e criados para testar as funções.

## 🛠️ Tecnologias

HTML, CSS e JavaScript puros, sem bibliotecas externas. Gráficos em SVG. Publicado no GitHub Pages. Consultas SQL de apoio em `scripts/`.

## 📁 Estrutura

```text
supply-chain-inventory-analytics/
├── index.html          # Painel completo (um único arquivo)
├── data/
│   └── sample/         # CSVs fictícios de exemplo
│       ├── products.csv
│       ├── inventory.csv
│       └── orders.csv
├── scripts/
│   └── analysis_queries.sql   # Consultas SQL de referência
├── legacy/             # Versões anteriores (Streamlit e relatório estático)
└── README.md
```

## 💻 Rodar localmente

A fonte "Exemplo" usa `fetch`, que não funciona abrindo o arquivo direto no navegador. Sirva a pasta:

```bash
python -m http.server 8000
```

Depois abra `http://localhost:8000`. As outras fontes funcionam mesmo sem servidor.

## 👤 Autor

**Socek Analytics (SA)** · Eduardo Socek
