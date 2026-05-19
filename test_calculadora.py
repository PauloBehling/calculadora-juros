import unittest
from calculadora import calcular_simulacao

class TestCalculadora(unittest.TestCase):
    def test_price_simulacao(self):
        # Cenário: Valor de R$ 12.000,00, Taxa de 2% a.m., 12 Parcelas no sistema Price
        valor_bem = 12000.00
        taxa_juros = 2.0
        n_parcelas = 12
        
        parcelas, total_juros = calcular_simulacao(valor_bem, taxa_juros, n_parcelas, 'price')
        
        # O número de parcelas deve ser 12
        self.assertEqual(len(parcelas), 12)
        
        # A soma das amortizações deve ser exatamente igual ao valor do bem (R$ 12.000,00)
        soma_amortizacao = sum(p['amortizacao'] for p in parcelas)
        self.assertAlmostEqual(soma_amortizacao, valor_bem, places=1)
        
        # O saldo devedor da última parcela deve ser exatamente 0.0
        self.assertEqual(parcelas[-1]['saldo_devedor'], 0.0)
        
        # No sistema Price, todas as parcelas (pmt) devem ser iguais
        # Nota: Permitimos pequena tolerância para ajuste da última parcela de arredondamento
        pmts = [p['pmt'] for p in parcelas]
        first_pmt = pmts[0]
        for pmt in pmts[:-1]:
            self.assertAlmostEqual(pmt, first_pmt, places=1)
            
        # O desconto de antecipação deve ser positivo e crescente para parcelas futuras
        self.assertTrue(all(p['desconto'] >= 0 for p in parcelas))
        for i in range(len(parcelas) - 1):
            self.assertLess(parcelas[i]['desconto'], parcelas[i+1]['desconto'])

    def test_sac_simulacao(self):
        # Cenário: Valor de R$ 12.000,00, Taxa de 2% a.m., 12 Parcelas no sistema SAC
        valor_bem = 12000.00
        taxa_juros = 2.0
        n_parcelas = 12
        
        parcelas, total_juros = calcular_simulacao(valor_bem, taxa_juros, n_parcelas, 'sac')
        
        # O número de parcelas deve ser 12
        self.assertEqual(len(parcelas), 12)
        
        # No SAC, a amortização mensal deve ser exatamente valor_bem / n_parcelas
        # R$ 12.000,00 / 12 = R$ 1.000,00
        for p in parcelas:
            self.assertEqual(p['amortizacao'], 1000.00)
            
        # O saldo devedor da última parcela deve ser 0.0
        self.assertEqual(parcelas[-1]['saldo_devedor'], 0.0)
        
        # As parcelas (pmt) devem ser decrescentes
        pmts = [p['pmt'] for p in parcelas]
        for i in range(len(pmts) - 1):
            self.assertGreater(pmts[i], pmts[i+1])

    def test_taxa_zero(self):
        # Testando edge-case de taxa de juros a 0%
        valor_bem = 10000.00
        taxa_juros = 0.0
        n_parcelas = 10
        
        parcelas, total_juros = calcular_simulacao(valor_bem, taxa_juros, n_parcelas, 'sac')
        self.assertEqual(total_juros, 0.0)
        self.assertEqual(parcelas[0]['pmt'], 1000.00)
        self.assertEqual(parcelas[0]['juros'], 0.0)
        self.assertEqual(parcelas[0]['desconto'], 0.0)

if __name__ == '__main__':
    unittest.main()
