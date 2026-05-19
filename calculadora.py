"""
Módulo de cálculo de simulação de financiamento (SAC e Price) com desconto por antecipação.
"""

def calcular_simulacao(valor_bem: float, taxa_juros: float, n_parcelas: int, sistema: str):
    """
    Realiza o cálculo detalhado das parcelas de um financiamento.
    
    Parâmetros:
    -----------
    valor_bem : float
        O valor total do bem a ser financiado.
    taxa_juros : float
        A taxa de juros mensal em porcentagem (ex: 2.0 para 2% a.m.).
    n_parcelas : int
        O número total de parcelas do financiamento.
    sistema : str
        O sistema de amortização: 'price' ou 'sac'.
        
    Retorna:
    --------
    tuple: (list of dict, float)
        - Uma lista contendo os dicionários com o detalhamento de cada parcela.
        - O valor total dos juros acumulados no período.
    """
    taxa = taxa_juros / 100.0
    balance = valor_bem
    total_juros = 0.0
    parcelas = []
    
    if sistema == 'price':
        # Se a taxa for zero, a parcela é apenas a divisão simples do valor
        if taxa == 0:
            pmt = valor_bem / n_parcelas
        else:
            # Fórmula Tabela Price: PMT = PV * [i * (1+i)^n] / [(1+i)^n - 1]
            pmt = valor_bem * (taxa * (1 + taxa)**n_parcelas) / ((1 + taxa)**n_parcelas - 1)
            
        for i in range(1, n_parcelas + 1):
            juros = balance * taxa
            amortizacao = pmt - juros
            
            # Evita problemas de arredondamento de ponto flutuante na última parcela
            if i == n_parcelas:
                amortizacao = balance
                pmt = amortizacao + juros
                
            # Fórmula do desconto por antecipação: pmt - (pmt / (1 + i)^n_parcela)
            if taxa == 0:
                desconto = 0.0
            else:
                desconto = pmt - (pmt / ((1 + taxa)**i))
                
            balance_restante = max(0.0, balance - amortizacao)
            
            parcelas.append({
                "num": i,
                "pmt": round(pmt, 2),
                "amortizacao": round(amortizacao, 2),
                "juros": round(juros, 2),
                "saldo_devedor": round(balance_restante, 2),
                "desconto": round(desconto, 2)
            })
            
            balance = balance_restante
            total_juros += juros
            
    else: # SAC
        # Fórmula SAC: Amortização constante = PV / n
        amortizacao = valor_bem / n_parcelas
        
        for i in range(1, n_parcelas + 1):
            juros = balance * taxa
            pmt = amortizacao + juros
            
            # Evita problemas de arredondamento de ponto flutuante na última parcela
            if i == n_parcelas:
                amortizacao = balance
                pmt = amortizacao + juros
                
            if taxa == 0:
                desconto = 0.0
            else:
                desconto = pmt - (pmt / ((1 + taxa)**i))
                
            balance_restante = max(0.0, balance - amortizacao)
            
            parcelas.append({
                "num": i,
                "pmt": round(pmt, 2),
                "amortizacao": round(amortizacao, 2),
                "juros": round(juros, 2),
                "saldo_devedor": round(balance_restante, 2),
                "desconto": round(desconto, 2)
            })
            
            balance = balance_restante
            total_juros += juros
            
    return parcelas, round(total_juros, 2)
