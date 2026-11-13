# Dados, origem e premissas
Período: 1 mês (consumo) e 10 anos (comparação). Energia em kWh. Valores em R$ (preços de 2026).
**Legenda:** 🟢 dado de fonte pública · 🟡 estimativa/premissa do grupo (identificada como tal).
O usuário também pode informar os dados da própria casa ao abrir o programa (consumo da conta, chuveiro, lâmpadas, tarifa).

## 1. Casa-exemplo (🟡 estimada: família pequena, ligação monofásica, São Paulo/SP)
Energia (kWh/mês) = potência (kW) × horas/dia × dias × quantidade

| Equipamento | Potência | Uso | Qtd | kWh/mês |
|---|---|---|---|---|
| Chuveiro elétrico | 5500 W | 0,7 h/dia | 1 | 115,5 |
| Geladeira | 120 W | 8 h/dia equiv. | 1 | 28,8 |
| Lâmpadas incandescentes | 60 W | 5 h/dia | 6 | 54,0 |
| TV | 100 W | 5 h/dia | 1 | 15,0 |
| Ventilador | 60 W | 6 h/dia | 1 | 10,8 |
| Outros (celular, PC etc.) | 1000 W | 1 h/dia equiv. | 1 | 30,0 |
| **Total** | | | | **254,1** |

> Potências e usos são premissas, conferíveis na Tabela de consumo do Procel/Inmetro.

## 2. Premissas e fontes
| Item | Valor usado | Tipo | Origem |
|---|---|---|---|
| Tarifa | R$ 0,94/kWh | 🟢 | Contas reais da Enel SP (mar–abr/2026) publicadas pela Câmara dos Deputados: TUSD + TE com tributos = 0,5613 + 0,3799 = R$ 0,941/kWh (275 kWh) e 0,5544 + 0,3753 = R$ 0,930/kWh (593 kWh). **Conservador:** a ANEEL aprovou reajuste médio de 8,97% para baixa tensão a partir de 04/07/2026. Opção 2 do programa (R$ 1,03) é **estimativa** (0,941 × 1,0897). |
| Sol (capital paulista) | 4,5 h/dia de sol pleno | 🟢 | Faixa de 4,5–4,8 kWh/m²/dia (Surge PV, baseado no Atlas Brasileiro de Energia Solar). Conferir em CRESESB SunData / Atlas INPE. Usamos o limite inferior. |
| Fator de emissão | 0,0385 kg CO2/kWh | 🟢 | MCTI: média anual 2023 do SIN = 38,5 kg CO2/MWh. Valores mensais de 2025 ficaram entre ~21 e 29 kg/MWh. |
| Custo do solar | R$ 2,84/Wp (1,5 kWp = R$ 4.260) | 🟢/🟡 | Greener (jun/2025): 4 kWp = R$ 11.360. Média nacional 2026 ≈ R$ 2,45/Wp (Solfácil). Usamos o valor mais alto por ser sistema pequeno. Fazer orçamentos reais. |
| Fio B | R$ 0,12/kWh injetado (2026) | 🟢/🟡 | Lei 14.300/2022: 60% do Fio B em 2026 (exemplo Canal Solar: R$ 0,1239/kWh); varia por distribuidora. |
| Evolução do Fio B | 75% (2027), 90% (2028), 100% (2029+) | 🟢/🟡 | Cronograma da Lei 14.300; 100% a partir de 2029 é **simplificação**. |
| Simultaneidade | 30% | 🟡 | Parte da geração consumida na hora (sem passar pela rede). |
| Taxa mínima | 30 kWh/mês | 🟢 | Custo de disponibilidade, ligação monofásica (ANEEL, REN 1000/2021). |
| Desempenho do sistema | 80% | 🟡 | Perdas típicas (inversor, temperatura, sujeira). |
| Perda anual dos painéis | 0,5%/ano | 🟡 | Estimativa típica de degradação. |
| Sistema solar | 1,5 kWp | 🟡 | Dimensionado para cobrir ~60% do consumo acima da taxa mínima. |
| LED | 9 W, R$ 12/lâmpada | 🟡 | Estimativa; 9 W equivale a ~60 W incandescente. |
| Banho mais curto | −30% no tempo | 🟡 | Premissa de mudança de hábito. |

## 3. Referências
- Contas reais Enel SP (Câmara dos Deputados): https://www.camara.leg.br/cota-parlamentar/documentos/publ/993/2026/8067830.pdf e https://www.camara.leg.br/cota-parlamentar/documentos/publ/3283/2026/8096594.pdf
- Reajuste Enel SP 2026 (baixa tensão 8,97%): https://www.bnewssaopaulo.com.br/amp/noticias/politica/conta-de-luz-deve-ficar-mais-cara-em-sp-no-final-de-semana-veja-o-reajuste.html
- Irradiação solar em SP: https://www.surgepv.com/pt/solar-compliance/brazil/estado/sao-paulo · Atlas Brasileiro de Energia Solar (INPE) · CRESESB SunData: http://www.cresesb.cepel.br/sundata/
- Fator de emissão (MCTI): https://eixos.com.br/brasil-tem-menor-taxa-de-emissao-de-carbono-na-geracao-eletrica-em-onze-anos/ · https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
- Custo do solar: https://olhardigital.com.br/curiosidades/?p=10663 · https://cenarioenergia.com.br/2026/06/09/preco-do-watt-pico-residencial-recua-7-em-um-ano-e-abre-janela-de-oportunidade-na-mmgd/
- Fio B (Lei 14.300/2022): https://canalsolar.com.br/consumidores-60-do-fio-b-2026/
