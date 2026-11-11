# Análise e comparação
**Necessidade:** reduzir a conta de luz da casa-exemplo: 254,1 kWh/mês × R$ 0,94 ≈ **R$ 239/mês**.
**Período de referência comum:** 10 anos. Dados e fontes em `dados.md`.

## Onde a energia é gasta
Chuveiro 45% · lâmpadas 21% · outros 12% · geladeira 11% · TV 6% · ventilador 4%.

## Alternativa A — Trocar 6 lâmpadas de 60 W por LED de 9 W (eficiência)
- Antes: 0,060 kW × 5 h × 30 × 6 = 54,0 kWh/mês · Depois: 0,009 × 5 × 30 × 6 = 8,1 kWh/mês
- Economia: **45,9 kWh/mês × R$ 0,94 = R$ 43,15/mês**
- Custo: 6 × R$ 12 = **R$ 72** → retorno em **~1,7 mês**
- Saldo em 10 anos: 43,15 × 120 − 72 = **~R$ 5.105**
- CO2 evitado: 45,9 × 120 × 0,0385 = **~212 kg**

## Alternativa B — Solar fotovoltaico on-grid de 1,5 kWp (fonte renovável)
- Geração: 1,5 kWp × 4,5 h × 30 dias × 0,80 = **162 kWh/mês**
- Valor da energia gerada: 162 × 0,94 = R$ 152,28
- Fio B (2026): energia injetada = 162 × (1 − 0,30) = 113,4 kWh × R$ 0,12 = −R$ 13,61
- Economia: **R$ 138,67/mês** (a conta nunca zera: taxa mínima de 30 kWh + iluminação pública)
- Custo: 1,5 × R$ 2.840 = **R$ 4.260** → retorno em **~31 meses (~2,6 anos)**
- Saldo em 10 anos: 138,67 × 120 − 4.260 = **~R$ 12.380**
- CO2 evitado: 162 × 120 × 0,0385 = **~748 kg**

## Comparação
| | LED | Solar |
|---|---|---|
| Investimento | R$ 72 | R$ 4.260 |
| Economia/mês | R$ 43 | R$ 139 |
| Retorno | ~2 meses | ~2,6 anos |
| Saldo em 10 anos | ~R$ 5.105 | ~R$ 12.380 |
| CO2 evitado (10 anos) | ~212 kg | ~748 kg |
| Viabilidade | Qualquer moradia | Telhado com sol, imóvel próprio, homologação na distribuidora |

## Justificativa da recomendação
1. **LED primeiro:** custo mínimo, retorno quase imediato, sem restrições.
2. **Solar** economiza mais e usa fonte renovável; exige investimento maior, telhado adequado e aprovação da distribuidora.
3. **Impacto ambiental:** a rede elétrica brasileira já é muito limpa (~38 g CO2/kWh), então o ganho em CO2 é pequeno em valores absolutos; o principal benefício é financeiro.
4. O **chuveiro** é o maior consumo; reduzir o tempo de banho ajuda sem custo.

## Limitações (devem aparecer ao usuário)
- Estimativas, não garantias: dependem de tarifa, hábitos, sol local, preços e orçamento real.
- Tarifa subiu ~9% em jul/2026, então os valores de economia tendem a ser um pouco maiores.
- O Fio B sobe para 75% (2027) e 90% (2028), reduzindo a economia do solar nos próximos anos; **não foi modelado ano a ano**.
- Não considera: troca do inversor (10–15 anos), manutenção, degradação dos painéis, financiamento, iluminação pública e variação futura da tarifa.
- O cenário do LED supõe lâmpadas de 60 W; se a casa já usa LED, a economia é bem menor.
