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
    
    # Limpa seletores globais do CSS original que conflitam com as colunas e widgets nativos do Streamlit
    import re
    css = re.sub(r'body\s*\{[^}]*\}', '', css)
    css = re.sub(r'body::before\s*\{[^}]*\}', '', css)
    css = re.sub(r'\*\s*\{[^}]*\}', '', css)
    css = re.sub(r'input,\s*select\s*\{[^}]*\}', '', css)
    css = re.sub(r'input\[data-prefix\]\s*\{[^}]*\}', '', css)
    css = re.sub(r'input:focus,\s*select:focus\s*\{[^}]*\}', '', css)
    
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
    
    /* Estilo do formulário Streamlit como Card Glassmorphic */
    form[data-testid="stForm"] {{
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 2rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
        animation: fadeIn 0.6s ease-out forwards;
    }}
    
    /* Estilo do Card para o Gráfico Plotly */
    div.stPlotlyChart {{
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 1.5rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 2rem !important;
        animation: fadeIn 0.6s ease-out forwards;
    }}
    
    /* Estilo do botão de submissão do formulário para o gradiente premium */
    div[data-testid="stFormSubmitButton"] button {{
        background: linear-gradient(135deg, #4facfe, #7f00ff) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(79, 172, 254, 0.2) !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }}
    
    div[data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(79, 172, 254, 0.3) !important;
    }}
    
    div[data-testid="stFormSubmitButton"] button:active {{
        transform: translateY(0) !important;
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

# Inicializa o estado de sessão (Session State) para gerenciar o cálculo
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
    st.session_state.asset_value = 150000.00
    st.session_state.interest_rate = 1.25
    st.session_state.installments = 36
    st.session_state.system = 'price'

# Grid Layout Principal: 1 Coluna Lateral para Inputs, 1 Coluna Grande para Resultados
col_inputs, col_resultados = st.columns([1.1, 2.9])

# Sistema de Opções
system_options = {
    "Tabela Price (Parcelas Fixas)": "price",
    "SAC (Parcelas Decrescentes)": "sac"
}

with col_inputs:
    with st.form("simulador_form"):
        st.markdown("<h3 style='margin-top: 0; margin-bottom: 1.5rem; font-family: Outfit; font-weight:600; color: #f8fafc;'>Configurações</h3>", unsafe_allow_html=True)
        
        asset_value = st.number_input(
            "Valor do Bem (R$)",
            min_value=0.0,
            value=st.session_state.asset_value,
            step=1000.00,
            format="%.2f"
        )
        
        interest_rate = st.number_input(
            "Taxa de Juros (% a.m.)",
            min_value=0.0,
            value=st.session_state.interest_rate,
            step=0.01,
            format="%.2f"
        )
        
        installments = st.number_input(
            "Número de Parcelas",
            min_value=1,
            value=st.session_state.installments,
            step=1
        )
        
        default_index = 0 if st.session_state.system == 'price' else 1
        selected_system_label = st.selectbox(
            "Sistema de Amortização",
            options=list(system_options.keys()),
            index=default_index
        )
        system = system_options[selected_system_label]
        
        submitted = st.form_submit_button("Calcular Simulação")
        
        if submitted:
            st.session_state.calculated = True
            st.session_state.asset_value = asset_value
            st.session_state.interest_rate = interest_rate
            st.session_state.installments = installments
            st.session_state.system = system

with col_resultados:
    if not st.session_state.calculated:
        st.info("💡 Configure os parâmetros ao lado e clique em 'Calcular Simulação' para gerar os resultados.")
    else:
        # Executa os cálculos utilizando os valores salvos na sessão
        val_bem = st.session_state.asset_value
        taxa_j = st.session_state.interest_rate
        parc = st.session_state.installments
        sis = st.session_state.system
        
        parcelas, total_juros = calcular_simulacao(val_bem, taxa_j, parc, sis)
        
        total_financed = val_bem + total_juros
        primeira_parcela = parcelas[0]['pmt']
        ultima_parcela = parcelas[-1]['pmt']
        sistema_nome = "Price" if sis == "price" else "SAC"
        
        # 1. Seção de Detalhes e Métricas Principais (Utilizando HTML idêntico ao original, dedentado e sem linhas em branco para evitar interpretação de código no Markdown)
        st.markdown(f"""
<div class="card animate-fade-in" style="margin-bottom: 2rem;">
<div class="simulation-details">
<div>
<span class="summary-label">Valor do Bem</span>
<span class="detail-value">{formatar_brl(val_bem)}</span>
</div>
<div>
<span class="summary-label">Taxa de Juros</span>
<span class="detail-value">{taxa_j:.2f}% a.m.</span>
</div>
<div>
<span class="summary-label">Parcelas</span>
<span class="detail-value">{parc}x ({sistema_nome})</span>
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
            title=dict(
                text="Visualização de Evolução Financeira",
                font=dict(color='#f8fafc', size=20, family='Outfit'),
                y=0.95,
                x=0.02,
                xanchor='left',
                yanchor='top'
            ),
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title=dict(
                    text='Número da Parcela',
                    font=dict(color='#94a3b8', family='Outfit')
                ),
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title=dict(
                    text='Valor da Parcela / Componentes (R$)',
                    font=dict(color='#94a3b8', family='Outfit')
                ),
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis2=dict(
                title=dict(
                    text='Saldo Devedor Restante (R$)',
                    font=dict(color='#94a3b8', family='Outfit')
                ),
                tickfont=dict(color='#94a3b8'),
                overlaying='y',
                side='right',
                gridcolor='rgba(0,0,0,0)',
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
            margin=dict(l=20, r=20, t=80, b=20),
            hovermode="x unified",
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Tabela de Detalhes em HTML Premium
        table_rows_html = ""
        for p in parcelas:
            table_rows_html += f"<tr><td>{p['num']}</td><td class='highlight'>{formatar_brl(p['pmt'])}</td><td>{formatar_brl(p['amortizacao'])}</td><td>{formatar_brl(p['juros'])}</td><td>{formatar_brl(p['saldo_devedor'])}</td><td><span class='discount-badge'>-{formatar_brl(p['desconto'])}</span></td></tr>"
        
        table_html = f"""
<div class="card animate-fade-in" style="margin-bottom: 2rem;">
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
            file_name=f"simulacao_{sistema_nome.lower()}_{int(val_bem)}.csv",
            mime="text/csv"
        )
