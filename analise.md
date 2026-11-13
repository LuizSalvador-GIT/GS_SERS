# Análise e comparação
**Necessidade:** reduzir a conta de luz da casa-exemplo: 254,1 kWh/mês × R$ 0,94 ≈ **R$ 239/mês**.
**Período de referência comum:** 10 anos. Dados e fontes em `dados.md`.

## Conceitos aplicados
- **Potência** (W ou kW): quanto um aparelho consome num instante. **Energia** (kWh) = potência (kW) × tempo (h). Ex.: chuveiro de 5,5 kW por 1 h = 5,5 kWh.
- **Eficiência energética:** mesmo serviço com menos energia. LED de 9 W = luz de 60 W incandescente (85% menos potência).
- **Fonte renovável:** energia solar fotovoltaica. A geração = kWp × horas de sol × dias × desempenho.

## Onde a energia é gasta
Chuveiro 45% · lâmpadas 21% · outros 12% · geladeira 11% · TV 6% · ventilador 4%.

## Alternativa A — Banho 30% mais curto (hábito, custo zero)
- 5,5 kW × 0,7 h × 30 dias = 115,5 kWh/mês → reduzir 30% = **34,65 kWh/mês = R$ 32,57/mês**
- Custo: R$ 0 · Saldo em 10 anos: **~R$ 3.909** · CO2 evitado: **~160 kg**

## Alternativa B — Trocar 6 lâmpadas de 60 W por LED de 9 W (eficiência)
- Antes: 0,060 kW × 5 h × 30 × 6 = 54,0 kWh/mês · Depois: 0,009 × 5 × 30 × 6 = 8,1 kWh/mês
- Economia: **45,9 kWh/mês × R$ 0,94 = R$ 43,15/mês**
- Custo: 6 × R$ 12 = **R$ 72** → retorno em **~1,7 mês**
- Saldo em 10 anos: 43,15 × 120 − 72 = **~R$ 5.105** · CO2 evitado: **~212 kg**

## Alternativa C — Solar fotovoltaico on-grid de 1,5 kWp (fonte renovável)
- Geração: 1,5 kWp × 4,5 h × 30 dias × 0,80 = **162 kWh/mês**
- Valor da energia gerada: 162 × 0,94 = R$ 152,28
- Fio B (2026): injetado = 162 × (1 − 0,30) = 113,4 kWh × R$ 0,12 = −R$ 13,61
- Economia: **R$ 138,67/mês** (a conta nunca zera: taxa mínima de 30 kWh + iluminação pública)
- Custo: 1,5 × R$ 2.840 = **R$ 4.260** → retorno em **~31 meses (~2,6 anos)**
- Saldo em 10 anos (modelo simples): 138,67 × 120 − 4.260 = **~R$ 12.380** · CO2 evitado: **~748 kg**

### Modelo refinado, ano a ano (comando `ano a ano`)
Considera Fio B subindo (75% em 2027, 90% em 2028, 100% depois) e perda de 0,5%/ano nos painéis, com tarifa constante:
- Economia: R$ 1.623 em 2027 → R$ 1.487 em 2036
- **Retorno em ~2,7 anos · saldo acumulado em 10 anos ≈ R$ 11.042**
- Mostra que o modelo simples é um pouco otimista (~R$ 1.340 a mais em 10 anos).

### Sensibilidade (comando `sensibilidade`): retorno do solar, em anos
| Tarifa \ Custo/kWp | R$ 2.450 | R$ 2.840 | R$ 3.500 |
|---|---|---|---|
| R$ 0,80/kWh | 2,8 | 3,3 | 4,0 |
| R$ 0,94/kWh | 2,3 | 2,7 | 3,3 |
| R$ 1,03/kWh | 2,1 | 2,4 | 3,0 |

## Comparação (mesma casa, 10 anos)
| | Banho curto | LED | Solar |
|---|---|---|---|
| Investimento | R$ 0 | R$ 72 | R$ 4.260 |
| Economia/mês | R$ 33 | R$ 43 | R$ 139 |
| Retorno | imediato | ~2 meses | ~2,6 anos (2,7 ref.) |
| Saldo em 10 anos | ~R$ 3.909 | ~R$ 5.105 | ~R$ 12.380 (R$ 11.042 ref.) |
| CO2 evitado (10 anos) | ~160 kg | ~212 kg | ~748 kg |
| Viabilidade | Qualquer pessoa | Qualquer moradia | Telhado com sol, imóvel próprio, homologação na distribuidora |

## Justificativa da recomendação
1. **Banho curto e LED primeiro:** custo zero ou mínimo, retorno imediato e sem restrições. As ações combinadas somam ~R$ 76/mês.
2. **Solar** economiza mais e usa fonte renovável, mas exige investimento, telhado adequado e aprovação da distribuidora; o retorno é sensível à tarifa e ao preço.
3. **Impacto ambiental:** a rede brasileira já é muito limpa (~38 g CO2/kWh), então o ganho em CO2 é pequeno em valores absolutos; o benefício principal é financeiro. Fabricação e descarte dos painéis não estão no cálculo.
4. O **chuveiro** é o maior consumo (45%), por isso o hábito do banho tem grande efeito.

## Coerência com o assistente
Cada resposta do assistente (`o que gasta mais energia?`, `banho`, `led`, `solar`, `comparar`, `ano a ano`, `sensibilidade`, `viabilidade`, `impacto ambiental`, `fontes`, `limitações`) é calculada pelas mesmas funções e constantes de `energia.py`, e os valores desta análise são os mesmos que o assistente retorna.

## Limitações (devem aparecer ao usuário)
- Estimativas, não garantias: dependem de tarifa, hábitos, sol local, preços e orçamento real.
- A tarifa subiu ~9% em jul/2026; os valores de economia tendem a ser um pouco maiores.
- O modelo ano a ano mantém a tarifa constante e não inclui troca do inversor (10–15 anos), manutenção, financiamento e iluminação pública.
- O cenário do LED supõe lâmpadas de 60 W; se a casa já usa LED, a economia é bem menor.
