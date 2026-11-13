# Citizen Assist AI — Módulo de Energia

**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (Global Solution 2026)

## Integrantes
- Luiz Cesar Conti Salvador — RM 571305
- Victor Do Prado Manzini — RM 572123
- Guilherme de Oliveira Santos — RM 572195

> Este repositório pode ser compartilhado com outras disciplinas. A contribuição de Soluções em Energias Renováveis e Sustentáveis está em `energia.py`, `dados.md`, `analise.md` e `testes_usuarios.md`.

## Público e problema
- **Público:** moradores de residências urbanas em São Paulo/SP que querem reduzir a conta de luz.
- **Necessidade:** entender onde a energia é gasta e se compensa mais economizar (hábito e eficiência) ou gerar energia renovável (solar).
- **Como o assistente ajuda:** responde em linguagem simples quanto cada opção custa, quanto economiza, em quanto tempo se paga e quais são as limitações, sempre indicando que os valores são estimativas.

## Funcionalidades de energia
- Consumo por equipamento (energia = potência × tempo) e custo mensal
- Comparação de 3 alternativas para a mesma necessidade e período (10 anos): banho mais curto (hábito), LED (eficiência) e solar fotovoltaico (renovável)
- Custos, viabilidade e impacto ambiental (CO2) de cada alternativa
- Modelo ano a ano do solar (Fio B crescente, perda dos painéis) e análise de sensibilidade (tarifa × custo)
- Explicação de conceitos (kWh, potência, eficiência) e das limitações, com indicação das fontes
- Opção de informar os dados da própria casa (consumo da conta, chuveiro, lâmpadas) e a tarifa

## Como executar
Requisitos: Python 3.8 ou mais novo, sem bibliotecas externas.

```bash
python energia.py   # no Windows, se necessário: py energia.py
```

Escolha a tarifa e depois a casa-exemplo (Enter) ou a sua casa (`s`). Perguntas de exemplo:
`o que gasta mais energia?`, `banho`, `led`, `solar`, `comparar`, `ano a ano`, `sensibilidade`, `viabilidade`, `impacto ambiental`, `o que é kWh?`, `fontes`, `limitações`.

## Integração ao Citizen Assist AI
```python
from energia import responder
resposta = responder("vale a pena energia solar?")
```
A função `responder()` usa os mesmos cálculos documentados em `analise.md`.

## Arquivos do repositório
| Arquivo | Conteúdo |
|---|---|
| `energia.py` | Cálculos e assistente de energia |
| `dados.md` | Dados utilizados, origem e premissas |
| `analise.md` | Cálculos, comparação das alternativas e justificativas |
| `testes_usuarios.md` | Testes com usuários e ajustes realizados |
