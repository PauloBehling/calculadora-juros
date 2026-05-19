import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from calculadora import calcular_simulacao

# Configuração da Página
st.set_page_config(
    page_title="Calculadora de Juros Pro | SAC & Price",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega e injeta o CSS original para manter a identidade visual premium
if os.path.exists("style.css"):
    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()
    # Adicionamos pequenas correções para harmonizar o CSS original com a estrutura do Streamlit
    custom_css = f"""
    <style>
    {css}
    
    /* Ajustes específicos para harmonizar com Streamlit */
    .stApp {{
        background: #0f172a;
        color: #f8fafc;
        font-family: 'Outfit', sans-serif;
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 30%, rgba(79, 172, 254, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, rgba(127, 0, 255, 0.15) 0%, transparent 40%);
        z-index: -1;
    }}
    
    /* Remove padding padrão excessivo do Streamlit */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }}
    
    /* Estilização personalizada de inputs do Streamlit para combinar com o tema */
    div[data-baseweb="input"], div[data-baseweb="select"], div[role="combobox"] {{
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }}
    
    div[data-baseweb="input"] input, div[data-baseweb="select"] select {{
        color: white !important;
        font-family: 'Outfit', sans-serif;
    }}
    
    label {{
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        font-family: 'Outfit', sans-serif;
    }}
    
    /* Estilo do botão de exportação */
    .stDownloadButton button {{
        background: linear-gradient(135deg, #10b981, #059669) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2) !important;
        width: 100%;
        margin-top: 1rem;
    }}
    
    .stDownloadButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.3) !important;
    }}
    
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Helper para formatar moeda em real brasileiro (BRL)
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Título Principal da Aplicação
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #00f2fe, #7f00ff); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">Calculadora Pro 🐍</h1>
    <p style="color: #94a3b8; font-size: 1.15rem; margin-top: 0.25rem;">Simulação Avançada de Financiamento e Antecipação (Versão Python)</p>
</div>
""", unsafe_allow_html=True)

# Grid Layout Principal: 1 Coluna Lateral para Inputs, 1 Coluna Grande para Resultados
col_inputs, col_resultados = st.columns([1.1, 2.9], gap="large")

with col_inputs:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Configurações")
    
    # Campo 1: Valor do Bem
    asset_value = st.number_input(
        "Valor do Bem (R$)",
        min_value=0.0,
        value=150000.00,
        step=1000.00,
        format="%.2f"
    )
    
    # Campo 2: Taxa de Juros
    interest_rate = st.number_input(
        "Taxa de Juros (% a.m.)",
        min_value=0.0,
        value=1.25,
        step=0.01,
        format="%.2f"
    )
    
    # Campo 3: Número de Parcelas
    installments = st.number_input(
        "Número de Parcelas",
        min_value=1,
        value=36,
        step=1
    )
    
    # Campo 4: Sistema de Amortização
    system_options = {
        "Tabela Price (Parcelas Fixas)": "price",
        "SAC (Parcelas Decrescentes)": "sac"
    }
    selected_system_label = st.selectbox(
        "Sistema de Amortização",
        options=list(system_options.keys())
    )
    system = system_options[selected_system_label]
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_resultados:
    if asset_value <= 0 or installments <= 0:
        st.info("💡 Por favor, configure os valores ao lado para ver a simulação.")
    else:
        # Executa os cálculos utilizando o motor python
        parcelas, total_juros = calcular_simulacao(asset_value, interest_rate, installments, system)
        
        total_financed = asset_value + total_juros
        primeira_parcela = parcelas[0]['pmt']
        ultima_parcela = parcelas[-1]['pmt']
        sistema_nome = "Price" if system == "price" else "SAC"
        
        # 1. Seção de Detalhes e Métricas Principais (Utilizando HTML idêntico ao original)
        st.markdown(f"""
        <div class="card animate-fade-in" style="margin-bottom: 2rem;">
            <div class="simulation-details">
                <div>
                    <span class="summary-label">Valor do Bem</span>
                    <span class="detail-value">{formatar_brl(asset_value)}</span>
                </div>
                <div>
                    <span class="summary-label">Taxa de Juros</span>
                    <span class="detail-value">{interest_rate:.2f}% a.m.</span>
                </div>
                <div>
                    <span class="summary-label">Parcelas</span>
                    <span class="detail-value">{installments}x ({sistema_nome})</span>
                </div>
            </div>
            
            <div class="summary-cards">
                <div class="summary-item">
                    <span class="summary-label">Total Financiado</span>
                    <span class="summary-value" style="color: #00f2fe;">{formatar_brl(total_financed)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Total de Juros</span>
                    <span class="summary-value" style="color: #7f00ff;">{formatar_brl(total_juros)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Primeira Parcela</span>
                    <span class="summary-value" style="color: #10b981;">{formatar_brl(primeira_parcela)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Última Parcela</span>
                    <span class="summary-value" style="color: #f59e0b;">{formatar_brl(ultima_parcela)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Gráfico Avançado de Evolução (Exclusivo da versão Python!)
        st.markdown('<div class="card animate-fade-in" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-bottom: 1rem; font-family: Outfit; font-weight:600;'>Visualização de Evolução Financeira</h3>", unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Barras de Amortização e Juros (Empilhados)
        fig.add_trace(go.Bar(
            x=[p['num'] for p in parcelas],
            y=[p['amortizacao'] for p in parcelas],
            name='Amortização (Principal)',
            marker=dict(color='rgba(0, 242, 254, 0.75)', line=dict(color='#00f2fe', width=1)),
            hovertemplate='Parcela %{x}<br>Amortização: R$ %{y:,.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=[p['num'] for p in parcelas],
            y=[p['juros'] for p in parcelas],
            name='Juros Pagos',
            marker=dict(color='rgba(127, 0, 255, 0.75)', line=dict(color='#7f00ff', width=1)),
            hovertemplate='Parcela %{x}<br>Juros: R$ %{y:,.2f}<extra></extra>'
        ))
        
        # Linha de Saldo Devedor (Eixo Y Secundário)
        fig.add_trace(go.Scatter(
            x=[p['num'] for p in parcelas],
            y=[p['saldo_devedor'] for p in parcelas],
            name='Saldo Devedor',
            yaxis='y2',
            line=dict(color='#f59e0b', width=3, dash='solid'),
            marker=dict(size=6, color='#f59e0b'),
            mode='lines+markers',
            hovertemplate='Parcela %{x}<br>Saldo Devedor: R$ %{y:,.2f}<extra></extra>'
        ))
        
        # Configurando layout do gráfico com tema escuro elegante
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title='Número da Parcela',
                titlefont=dict(color='#94a3b8', family='Outfit'),
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title='Valor da Parcela / Componentes (R$)',
                titlefont=dict(color='#94a3b8', family='Outfit'),
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis2=dict(
                title='Saldo Devedor Restante (R$)',
                titlefont=dict(color='#94a3b8', family='Outfit'),
                tickfont=dict(color='#94a3b8'),
                overlaying='y',
                side='right',
                gridcolor='transparent',
                linecolor='rgba(255,255,255,0.1)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#f8fafc', family='Outfit')
            ),
            margin=dict(l=20, r=20, t=10, b=20),
            hovermode="x unified",
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. Tabela de Detalhes em HTML Premium
        st.markdown('<div class="card animate-fade-in">', unsafe_allow_html=True)
        
        table_rows_html = ""
        for p in parcelas:
            table_rows_html += f"""
            <tr>
                <td>{p['num']}</td>
                <td class="highlight">{formatar_brl(p['pmt'])}</td>
                <td>{formatar_brl(p['amortizacao'])}</td>
                <td>{formatar_brl(p['juros'])}</td>
                <td>{formatar_brl(p['saldo_devedor'])}</td>
                <td><span class="discount-badge">-{formatar_brl(p['desconto'])}</span></td>
            </tr>
            """
        
        table_html = f"""
        <div class="results-table-container">
            <h3 style="font-family: Outfit; font-weight:600; margin-bottom: 0.5rem;">Detalhamento das Parcelas</h3>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Parcela</th>
                        <th>Amortização</th>
                        <th>Juros</th>
                        <th>Saldo Devedor</th>
                        <th>Desc. Antecip.</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>
        """
        st.markdown(table_html, unsafe_allow_html=True)
        
        # 4. Botão de Exportação para CSV (Pandas DataFrame)
        df_parcelas = pd.DataFrame(parcelas)
        df_parcelas.columns = ["Parcela", "Valor da Parcela (R$)", "Amortização (R$)", "Juros (R$)", "Saldo Devedor (R$)", "Desconto Antecipação (R$)"]
        csv_data = df_parcelas.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="📥 Exportar Simulação para Excel / CSV",
            data=csv_data,
            file_name=f"simulacao_{sistema_nome.lower()}_{int(asset_value)}.csv",
            mime="text/csv"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
