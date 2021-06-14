# Valuation
PT-BR:

Esse é um projeto voltado para a automatização do uso de dados na avaliação de empresas

- O arquivo "calculadora do beta" usa informações da biblioteca Y-finance para pegar o preço de fechamento do período selecionado, tirar uma regressão linear, e calcular o coeficiente beta de risco do investimento.
- O "conversor pdf_para_df" realiza o scraping de balanços patrimoniais, DRE's e fluxos de caixa retornando data frames com as informações nescessárias para o valuation.
- Com a informação dada por este arquivo, a "calculadora do Wacc" se utiliza da informação dada pela "calculadora do beta" e do "conversor_pdf_df" para estimar o custo de capital da empresa.
- O arquivo "algoritmo preço de fechamento" é um trecho da "calculadora do beta" mas está, pode, e deve ser usado de forma avulsa do resto do código para calculo do valuation. Eu o uso para outras análises da bolsa de valores junto com o excel.

O projeto está inconcluido sendo nescessária a parte final do programa, em que se calculará o fluxo de caixa descontado e sua projeção para o futuro


Notas:

- Até o momento os testes feitos por mim foram realizados com a WEG, portanto, os períodos e nome da empresa podem ser substítuidos para diferentes análises.
- Em próximas atualizações o código estará mais limpo e sem resquícios dos testes

Qualquer dúvida, mande um email para: lucabesposito@gmail.com

EN-US:

This is a project aimed at automating the use of data in business valuation

- The "beta calculator" file uses information from the Y-finance library to take the closing price of the selected period, take a linear regression, and calculate the beta risk coefficient of the investment.
- The "pdf_to_df converter" performs the scraping of balance sheets, DRE's and cash flows, returning data frames with the necessary information for valuation.
- With the information given by this file, the "Wacc calculator" uses the information given by the "beta calculator" and the "conversor_pdf_df" to estimate the company's cost of capital.
- The "closing price algorithm" file is an excerpt from the "beta calculator" but it is, can, and should be used separately from the rest of the code to calculate the valuation. I use it for other stock market analysis along with excel.

The project is unfinished and the final part of the program is needed, in which the discounted cash flow and its projection for the future will be calculated

Notes:

- So far, the tests performed by me have been carried out with WEG, therefore, the periods and company name can be substituted for different analyses.
- In future updates, the code will be cleaner and without traces of the tests

Any questions, send an email to: lucabesposito@gmail.com
