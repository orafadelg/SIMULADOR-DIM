import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Título principal do aplicativo
st.title("Simulador de Marketing Mix Modeling")

# Sidebar com título e seleção de aba
st.sidebar.title("DIM")
aba_selecionada = st.sidebar.selectbox("Selecione a aba", ["Dash IMM", "Media Behavior", "TRACKfluencers", "BRAINfluencers", "Governança"])

import streamlit as st
import numpy as np

# Título principal do aplicativo
st.title("Simulador de Marketing de Influência")

# Sidebar com título e seleção de aba
st.sidebar.title("Influência")
aba_selecionada = st.sidebar.selectbox("Selecione a aba", ["Influência"])

# Definindo os tipos de influenciadores e investimentos iniciais
investimentos_iniciais = {
    "Megainfluenciadores": 150,
    "Macroinfluenciadores": 120,
    "Mid-Influenciadores": 80,
    "Microinfluenciadores": 60,
    "Nanoinfluenciadores": 40
}

# Função para calcular métricas com base nos investimentos
def calcular_metricas(investimentos):
    acessos = sum(investimentos.values()) * 0.4
    leads = acessos * 0.25
    vendas = leads * 0.15
    return acessos, leads, vendas

# Valores de referência para os cálculos dos percentuais
valor_base_acessos = 1000
valor_base_leads = 250
valor_base_vendas = 75

# Parte 1: Influência
if aba_selecionada == "Influência":
    st.header("Dashboard de Marketing de Influência")

    # Bloco Inicial: KPIs Principais
    st.subheader("Principais KPIs de Influência")
    col1, col2, col3, col4 = st.columns(4)

    investimento_total = sum(investimentos_iniciais.values())
    roi_geral = 115.7  # ROI Geral fictício inicial em %
    roi_mega_macro = 125.4  # ROI combinado de mega e macro influenciadores
    roi_micro_nano = 108.2  # ROI combinado de micro e nano influenciadores

    with col1:
        st.metric(label="Investimento Total (mil R$)", value=f"{investimento_total:.0f}", delta="")
    with col2:
        st.metric(label="ROI Geral de Influência", value=f"{roi_geral:.1f}%", delta="")
    with col3:
        st.metric(label="ROI Mega e Macro", value=f"{roi_mega_macro:.1f}%", delta="")
    with col4:
        st.metric(label="ROI Micro e Nano", value=f"{roi_micro_nano:.1f}%", delta="")

    # Bloco 1: Alocação de Investimento por Tipo de Influenciador
    st.subheader("Alocação de Investimento por Tipo de Influenciador")
    col1, col2, col3 = st.columns(3)

    investimentos = {}
    with col1:
        investimentos["Megainfluenciadores"] = st.slider("Megainfluenciadores (mil R$)", 0, 500, investimentos_iniciais["Megainfluenciadores"])
        investimentos["Macroinfluenciadores"] = st.slider("Macroinfluenciadores (mil R$)", 0, 500, investimentos_iniciais["Macroinfluenciadores"])
    with col2:
        investimentos["Mid-Influenciadores"] = st.slider("Mid-Influenciadores (mil R$)", 0, 500, investimentos_iniciais["Mid-Influenciadores"])
    with col3:
        investimentos["Microinfluenciadores"] = st.slider("Microinfluenciadores (mil R$)", 0, 500, investimentos_iniciais["Microinfluenciadores"])
        investimentos["Nanoinfluenciadores"] = st.slider("Nanoinfluenciadores (mil R$)", 0, 500, investimentos_iniciais["Nanoinfluenciadores"])

    # Bloco 2: Simulação de Resultados
    st.subheader("Simulação de Resultados")
    acessos, leads, vendas = calcular_metricas(investimentos)

    col1, col2, col3 = st.columns(3)
    col1.metric("Acessos", f"{acessos:.0f}", f"{(acessos / valor_base_acessos - 1) * 100:.0f}%", delta_color="normal")
    col2.metric("Leads", f"{leads:.0f}", f"{(leads / valor_base_leads - 1) * 100:.0f}%", delta_color="normal")
    col3.metric("Vendas", f"{vendas:.0f}", f"{(vendas / valor_base_vendas - 1) * 100:.0f}%", delta_color="normal")

# Parte 2: Media Behavior
elif aba_selecionada == "Media Behavior":
    st.header("Comportamento de Mídia")

    # Inicialização da variável investimentos com valores padrão
    investimentos = {
        "Google Ads": 100,
        "Meta Ads": 100,
        "Out of Home": 50,
        "Rádio": 75,
        "TV Paga": 150,
        "TV Aberta": 200,
        "Influenciadores": 120
    }

    # Curva de resposta de mídia com ponto de investimento
    st.subheader("Curva de Resposta de Mídia")
    canal_selecionado = st.selectbox("Selecione o Canal de Mídia", options=list(investimentos.keys()))

    # Definindo a curva de resposta (modelo em três fases)
    x = np.linspace(0, 500, 500)
    y = np.piecewise(x, [x < 100, (x >= 100) & (x < 300), x >= 300],
                     [lambda x: 0.5 * x / 100, lambda x: x * 0.01 + 0.5, lambda x: 3])

    # Gráfico da curva de resposta com ponto de investimento destacado
    fig_resposta = go.Figure()
    fig_resposta.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Curva de Resposta"))
    fig_resposta.add_trace(go.Scatter(
        x=[investimentos[canal_selecionado]],
        y=[y[int(investimentos[canal_selecionado])]],  # Convertendo índice para acessar a curva
        mode="markers", marker=dict(color="red", size=10), name="Investimento Atual"
    ))
    fig_resposta.update_layout(
        title=f"Curva de Resposta para {canal_selecionado}",
        xaxis_title="Investimento",
        yaxis_title="Efeito"
    )
    st.plotly_chart(fig_resposta)

    # Gráfico de Vendas Previstas vs. Realizadas
    st.subheader("Previsto vs. Realizado")
    datas = pd.date_range(start="2023-01-01", periods=12, freq="M")
    vendas_previstas = np.sin(np.linspace(0, 3 * np.pi, 12)) * 200 + 1000
    vendas_reais = vendas_previstas + np.random.normal(0, 50, 12)

    fig_previsto_realizado = go.Figure()
    fig_previsto_realizado.add_trace(go.Scatter(x=datas, y=vendas_previstas, mode='lines', name='Vendas Previstas'))
    fig_previsto_realizado.add_trace(go.Scatter(x=datas, y=vendas_reais, mode='lines+markers', name='Vendas Reais'))
    fig_previsto_realizado.update_layout(
        title="Vendas Previstas vs. Realizadas",
        xaxis_title="Mês",
        yaxis_title="Vendas"
    )
    st.plotly_chart(fig_previsto_realizado)


# Aba 3: TRACKfluencers
elif aba_selecionada == "TRACKfluencers":
    st.header("MARCA, CAMPANHAS & INFLUÊNCIA")

    # Matriz de performance por importância
    st.subheader("O que a marca é e precisa ser")
    atributos = ["Qualidade", "Inovação", "Confiabilidade", "Disponibilidade", "Atendimento", "Preço", "Sustentabilidade", "Design"]
    importancia = [8, 7, 9, 5, 6, 4, 7, 8]
    performance = [6, 8, 7, 4, 5, 3, 8, 7]

    fig_matriz = go.Figure()
    fig_matriz.add_trace(go.Scatter(
        x=importancia, y=performance, mode='markers+text', text=atributos, textposition="top center",
        marker=dict(size=12, color="red")
    ))
    fig_matriz.update_layout(title="Matriz de Importância vs. Performance", xaxis_title="Importância", yaxis_title="Performance")
    st.plotly_chart(fig_matriz)

    # Gráfico de radar para impacto de influenciadores
    st.subheader("Importância de Influência nos Atributos de Marca")
    atributos_radar = ["Qualidade", "Inovação", "Confiabilidade", "Disponibilidade", "Atendimento", "Preço", "Sustentabilidade", "Design"]
    influencia = [6, 7, 8, 6, 5, 6, 7, 8]
    geral = [5, 6, 6, 4, 4, 5, 6, 6]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=influencia, theta=atributos_radar, fill='toself', name='Influência'))
    fig_radar.add_trace(go.Scatterpolar(r=geral, theta=atributos_radar, fill='toself', name='Geral'))
    fig_radar.update_layout(title="Impacto de Influência vs. Geral")
    st.plotly_chart(fig_radar)

    # Gráfico de avaliação de eficiência de influenciadores
    st.subheader("Eficiência de Influência")
    eficiencia = {"Autenticidade": 7, "Adequação": 8, "Relevância": 6, "Endossamento": 7}
    fig_eficiencia = go.Figure(go.Bar(
        x=list(eficiencia.keys()), y=list(eficiencia.values()), marker=dict(color="red")
    ))
    fig_eficiencia.update_layout(title="Avaliação de Influência por Métrica")
    st.plotly_chart(fig_eficiencia)

# Aba 4: BRAINfluencers
elif aba_selecionada == "BRAINfluencers":
    st.header("OS TALENTOS QUE SUA MARCA PRECISA")

    # Gráfico de barra de influence power por influenciador
    st.subheader("Influence Power por Influenciador")
    influenciadores = ["Influencer A", "Influencer B", "Influencer C", "Influencer D", "Influencer E", "Influencer F", "Influencer G", "Influencer H"]
    influence_power = [80, 75, 70, 65, 60, 55, 50, 45]
    fig_influencer = go.Figure(go.Bar(
        x=influenciadores, y=influence_power, marker=dict(color="red")
    ))
    fig_influencer.update_layout(title="Influence Power dos Influenciadores", xaxis_title="Influenciador", yaxis_title="Influence Power")
    st.plotly_chart(fig_influencer)

    # Matriz de bolhas de influência por risco
    st.subheader("Influência vs. Risco")
    riscos = [30, 25, 20, 15, 35, 40, 45, 50]
    alcance = [500, 400, 300, 200, 600, 550, 650, 700]

    fig_risco = go.Figure()
    fig_risco.add_trace(go.Scatter(
        x=influence_power, y=riscos, mode='markers', marker=dict(
            size=[a * 0.1 for a in alcance], color="red", sizemode='area', opacity=0.6
        ),
        text=influenciadores
    ))
    fig_risco.update_layout(title="Influence Power vs. Risco", xaxis_title="Influence Power", yaxis_title="Risco")
    st.plotly_chart(fig_risco)

# Aba 5: Governança
elif aba_selecionada == "Governança":
    st.header("Governança de Dados")
    st.subheader("Origem dos Dados")
    st.write("Dados de investimentos semanais em mídia de cada canal coletados de relatórios internos e parceiros.")
    st.subheader("Accountability")
    st.write("Ferramentas usadas: Google Analytics, Meta Business Suite, TV Tracking.")
    st.write("Data de última atualização do modelo: 03/03/2025")
    st.write("Data da próxima rodada do modelo: 05/08/2025")
