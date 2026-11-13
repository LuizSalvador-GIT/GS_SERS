# Citizen Assist AI — Módulo de Energia
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (Global Solution 2026)

**Integrantes:**

Luiz Cesar Conti Salvador RM: 571305
Victor Do Prado Manzini RM: 572123
Guilherme de Oliveira Santos RM:572195

> Este repositório pode ser compartilhado com outras disciplinas. A contribuição desta disciplina está em `energia.py`, `dados.md`, `analise.md` e `testes_usuarios.md`.

Contribuição da disciplina (Energias Renováveis e Sustentáveis)
Módulo de energia do Citizen Assist AI: energia.py (cálculos + assistente), dados.md, analise.md e testes_usuarios.md.

Funcionalidades de energia
Consumo por equipamento (energia = potência × tempo) e custo mensal
Comparação de 3 alternativas para a mesma necessidade e período (10 anos): banho mais curto (hábito), LED (eficiência) e solar fotovoltaico (renovável)
Custos, viabilidade e impacto ambiental (CO2) de cada alternativa
Modelo ano a ano do solar (Fio B crescente, perda dos painéis) e análise de sensibilidade (tarifa × custo)
Explicação de conceitos (kWh, potência, eficiência) e das limitações; indica as fontes
Opção de informar os dados da própria casa (consumo da conta, chuveiro, lâmpadas) e a tarifa
Como executar
python energia.py   # no Windows, se necessário: py energia.py

Escolha a tarifa, depois a casa-exemplo (Enter) ou a sua casa (s). Perguntas de exemplo: o que gasta mais energia?, banho, led, solar, comparar, ano a ano, sensibilidade, viabilidade, impacto ambiental, o que é kWh?, fontes, limitações.

Integração ao Citizen Assist AI
from energia import responder
resposta = responder("vale a pena energia solar?")

A função responder() usa os mesmos cálculos documentados em analise.md.
