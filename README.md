# Citizen Assist AI — Módulo de Energia
**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (Global Solution 2026)

**Integrantes:**

Luiz Cesar Conti Salvador RM: 571305
Victor Do Prado Manzini RM: 572123
Guilherme de Oliveira Santos RM:572195

> Este repositório pode ser compartilhado com outras disciplinas. A contribuição desta disciplina está em `energia.py`, `dados.md`, `analise.md` e `testes_usuarios.md`.

## 1. Público e problema
- **Público:** moradores de residências urbanas em São Paulo/SP preocupados com a conta de luz.
- **Necessidade:** reduzir o consumo e o gasto com eletricidade, entendendo se vale mais a pena economizar (eficiência) ou gerar energia renovável.
- **Como ajuda:** o assistente responde, em linguagem simples, o que mais consome, quanto se economiza e qual opção compensa, sempre avisando que são estimativas.

## 2. Funcionalidades de energia
O assistente (`responder()` em `energia.py`) responde perguntas sobre:
consumo por equipamento · troca por LED · energia solar · comparação e recomendação · fontes · premissas e limitações.

## 3. Como executar
```bash
python energia.py   # (no Windows, se necessário: py energia.py)
```
Exemplos de perguntas: `o que gasta mais energia?`, `vale a pena trocar por LED?`, `e energia solar?`, `qual a melhor opção?`, `quais as fontes?`, `quais as limitações?`

Para integrar ao Citizen Assist AI: `from energia import responder` e chame `responder(texto_do_usuario)`.
Requisitos: Python 3.8+ (sem bibliotecas externas).

## 4. Arquivos
| Arquivo | Conteúdo |
|---|---|
| `energia.py` | Cálculos + assistente |
| `dados.md` | Dados, origem e premissas |
| `analise.md` | Cálculos, comparação e justificativas |
| `testes_usuarios.md` | Registro dos testes com usuários |
