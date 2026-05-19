"""
Módulo de cálculo de simulação de financiamento (SAC e Price) com desconto por antecipação.
Possui um motor de arredondamento financeiro de alta precisão (livre de discrepâncias de centavos).
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
    # Tipagem defensiva robusta
    valor_bem = float(valor_bem)
    taxa_juros = float(taxa_juros)
    n_parcelas = int(n_parcelas)
    
    taxa = taxa_juros / 100.0
    balance = round(valor_bem, 2)
    total_juros = 0.0
    parcelas = []
    
    if sistema == 'price':
        if taxa == 0:
            pmt_calc = valor_bem / n_parcelas
        else:
            # Tabela Price Formula: PMT = PV * [i * (1+i)^n] / [(1+i)^n - 1]
            pmt_calc = valor_bem * (taxa * (1 + taxa)**n_parcelas) / ((1 + taxa)**n_parcelas - 1)
        
        pmt_standard = round(pmt_calc, 2)
        
        for i in range(1, n_parcelas + 1):
            juros = round(balance * taxa, 2)
            
            if i == n_parcelas:
                # Na última parcela, a amortização liquida exatamente o saldo restante
                amortizacao = round(balance, 2)
                pmt = round(amortizacao + juros, 2)
            else:
                amortizacao = round(pmt_standard - juros, 2)
                pmt = pmt_standard
                
            if taxa == 0:
                desconto = 0.0
            else:
                desconto = round(pmt - (pmt / ((1 + taxa)**i)), 2)
                
            balance_restante = round(max(0.0, balance - amortizacao), 2)
            
            parcelas.append({
                "num": i,
                "pmt": pmt,
                "amortizacao": amortizacao,
                "juros": juros,
                "saldo_devedor": balance_restante,
                "desconto": desconto
            })
            
            balance = balance_restante
            total_juros += juros
            
    else: # SAC
        # Amortização padrão SAC (arredondada para 2 casas)
        amortizacao_standard = round(valor_bem / n_parcelas, 2)
        
        for i in range(1, n_parcelas + 1):
            juros = round(balance * taxa, 2)
            
            if i == n_parcelas:
                # Na última parcela, amortiza exatamente o saldo devedor restante
                amortizacao = round(balance, 2)
            else:
                amortizacao = amortizacao_standard
                
            pmt = round(amortizacao + juros, 2)
            
            if taxa == 0:
                desconto = 0.0
            else:
                desconto = round(pmt - (pmt / ((1 + taxa)**i)), 2)
                
            balance_restante = round(max(0.0, balance - amortizacao), 2)
            
            parcelas.append({
                "num": i,
                "pmt": pmt,
                "amortizacao": amortizacao,
                "juros": juros,
                "saldo_devedor": balance_restante,
                "desconto": desconto
            })
            
            balance = balance_restante
            total_juros += juros
            
    return parcelas, round(total_juros, 2)
