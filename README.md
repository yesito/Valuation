# Valuation
Esse é um projeto voltado para a automatização do uso de dados na avaliação de empresas

- O arquivo "calculadora do beta" usa informações da biblioteca Y-finance para pegar o preço de fechamento do período selecionado, tirar uma regressão linear, e calcular o coeficiente beta de risco do investimento.
- O "conversor pdf_para_df" realiza o scraping de balanços patrimoniais, DRE's e fluxos de caixa retornando data frames com as informações nescessárias para o valuation.
- Com a informação dada por este arquivo, a "calculadora do Wacc" se utiliza da informação dada pela "calculadora do beta" e do "conversor_pdf_df" para estimar o custo de capital da empresa.

O projeto está inconcluido sendo nescessária a parte final do programa, em que se calculará o fluxo de caixa descontado e sua projeção para o futuro


Notas:

- Até o momento os testes feitos por mim foram realizados com a WEG, portanto, os períodos e nome da empresa podem ser substítuidos para diferentes análises.
- Em próximas atualizações o código estará mais limpo e sem resquícios dos testes

Qualquer dúvida, mande um email para: lucabesposito@gmail.com
