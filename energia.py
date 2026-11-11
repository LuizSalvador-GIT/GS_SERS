"""
Módulo de Energia do Citizen Assist AI
Disciplina: Soluções em Energias Renováveis e Sustentáveis

Necessidade: reduzir a conta de luz de uma residência urbana (São Paulo/SP).
Alternativas comparadas (mesma necessidade, mesmo período de 10 anos):
  A) Trocar lâmpadas incandescentes por LED  (eficiência energética)
  B) Instalar sistema solar fotovoltaico on-grid (fonte renovável)

ATENÇÃO: todos os valores abaixo são ESTIMATIVAS/PREMISSAS (ver README.md).
Altere as constantes para refletir a conta de luz real do usuário.
"""

# ---------------- PREMISSAS (ESTIMADAS) ----------------
TARIFA = 0.94            # R$/kWh com impostos (TUSD+TE, contas reais Enel SP mar/2026; ver dados.md).
                         # Obs.: houve reajuste médio de ~9% em jul/2026; troque pelo valor da SUA conta.
FATOR_CO2 = 0.0385       # kg CO2/kWh (média anual 2023 do SIN, MCTI)
ANOS = 10                # período de referência comum

# Opções de tarifa (R$/kWh, com impostos) oferecidas ao abrir o programa
TARIFAS = {
    "1": ("Enel SP - contas reais de mar/2026 (dado público)", 0.94),
    "2": ("Enel SP - estimativa após reajuste de jul/2026 (0,941 x 1,0897)", 1.03),  # ESTIMADO
}

# Equipamentos da residência-exemplo: nome -> (potência W, horas/dia, dias/mês, quantidade)
EQUIPAMENTOS = {
    "Chuveiro elétrico":        (5500, 0.7, 30, 1),
    "Geladeira":                (120, 8, 30, 1),        # 8 h/dia equivalentes (ciclo do compressor)
    "Lâmpadas incandescentes":  (60, 5, 30, 6),
    "TV":                       (100, 5, 30, 1),
    "Ventilador":               (60, 6, 30, 1),
    "Outros (celular, PC etc.)": (1000, 1, 30, 1),      # ~30 kWh/mês estimados
}

# Alternativa A: LED
POT_LED = 9              # W por lâmpada LED equivalente
CUSTO_LED = 12.0         # R$ por lâmpada (estimado)

# Alternativa B: fotovoltaico
KWP = 1.5                # potência do sistema (kWp)
HSP = 4.5                # horas de sol pleno/dia na capital paulista (faixa 4,5-4,8; Atlas Solar INPE/SunData)
DESEMPENHO = 0.80        # taxa de desempenho (perdas)
CUSTO_KWP = 2840.0       # R$/kWp instalado (Greener: R$ 2,84/Wp p/ sistema residencial pequeno, 2025;
                         # média nacional 2026 ~R$ 2,45/Wp, Solfácil). Valor conservador.
DISPONIBILIDADE = 30     # kWh/mês mínimos cobrados em ligação monofásica (ANEEL, REN 1000/2021)
FIO_B = 0.12             # R$/kWh injetado e não compensado (60% do Fio B em 2026, Lei 14.300; varia por distribuidora)
SIMULTANEIDADE = 0.30    # fração da geração consumida na hora (estimativa; o resto é injetado na rede)


# ---------------- CÁLCULOS ----------------
def kwh_mes(pot_w, h_dia, dias, qtd=1):
    """Energia (kWh/mês) = potência(kW) x tempo(h) x quantidade."""
    return pot_w / 1000 * h_dia * dias * qtd


def consumo_total():
    return {n: kwh_mes(*v) for n, v in EQUIPAMENTOS.items()}


def alternativa_led():
    p, h, d, q = EQUIPAMENTOS["Lâmpadas incandescentes"]
    antes = kwh_mes(p, h, d, q)
    depois = kwh_mes(POT_LED, h, d, q)
    eco_kwh = antes - depois
    custo = CUSTO_LED * q
    return _resumo("LED", eco_kwh, custo)


def alternativa_solar():
    total = sum(consumo_total().values())
    geracao = KWP * HSP * 30 * DESEMPENHO
    compensado = min(geracao, total - DISPONIBILIDADE)  # não zera a conta: há taxa mínima
    injetado = compensado * (1 - SIMULTANEIDADE)
    custo_fio_b = injetado * FIO_B                       # parte do Fio B que não é compensada
    custo = KWP * CUSTO_KWP
    return _resumo("Solar fotovoltaico", compensado, custo, geracao, custo_fio_b)


def _resumo(nome, eco_kwh, custo, geracao=None, desconto_rs=0.0):
    eco_rs = eco_kwh * TARIFA - desconto_rs
    return {
        "nome": nome,
        "kwh_mes": eco_kwh,
        "geracao_kwh_mes": geracao,
        "reais_mes": eco_rs,
        "custo_inicial": custo,
        "retorno_meses": custo / eco_rs,
        "saldo_10_anos": eco_rs * 12 * ANOS - custo,
        "co2_evitado_10_anos_kg": eco_kwh * 12 * ANOS * FATOR_CO2,
    }


# ---------------- ASSISTENTE ----------------
AVISO = ("\n(Estimativas, não garantias: dependem da sua tarifa, hábitos, sol local e preços. "
         "Valores de exemplo para uma casa de ~254 kWh/mês.)")

FONTES = (
    "Fontes para conferir os dados:\n"
    "- ANEEL: tarifas e regras de geração distribuída (aneel.gov.br)\n"
    "- INPE: Atlas Brasileiro de Energia Solar\n"
    "- Procel/Inmetro (Selo Procel): consumo de equipamentos (procelinfo.com.br)\n"
    "- MCTI: fator de emissão do Sistema Interligado Nacional\n"
    "- Lei 14.300/2022: marco legal da geração distribuída")


def _fmt(a):
    return (f"{a['nome']}: economia de {a['kwh_mes']:.0f} kWh/mês (R$ {a['reais_mes']:.0f}/mês); "
            f"investimento ~R$ {a['custo_inicial']:.0f}; retorno em ~{a['retorno_meses']:.0f} meses; "
            f"saldo em {ANOS} anos ~R$ {a['saldo_10_anos']:.0f}; "
            f"CO2 evitado ~{a['co2_evitado_10_anos_kg']:.0f} kg em {ANOS} anos.")


def responder(pergunta):
    """Função para integrar ao Citizen Assist AI: recebe texto, devolve orientação."""
    p = pergunta.lower()
    led, sol = alternativa_led(), alternativa_solar()
    if any(k in p for k in ["chuveiro", "gasta mais", "maior consumo", "vilão", "consumo"]):
        c = consumo_total()
        total = sum(c.values())
        linhas = "\n".join(f"- {n}: {v:.0f} kWh/mês ({v/total:.0%})"
                           for n, v in sorted(c.items(), key=lambda x: -x[1]))
        return f"Consumo estimado da casa-exemplo ({total:.0f} kWh/mês):\n{linhas}" + AVISO
    if any(k in p for k in ["led", "lâmpada", "lampada"]):
        return _fmt(led) + "\nDica: troque primeiro as lâmpadas mais usadas." + AVISO
    if any(k in p for k in ["solar", "painel", "fotovoltaic", "renovável", "renovavel"]):
        return (_fmt(sol) + f"\nGeração estimada: {sol['geracao_kwh_mes']:.0f} kWh/mês. "
                "Limitações: a conta nunca zera (taxa mínima), já considera o Fio B de 2026 (60%, "
                "que aumenta até 2028), exige telhado com sol e preços/regras podem mudar." + AVISO)
    if any(k in p for k in ["comparar", "melhor", "recomend", "vale", "economizar", "economia"]):
        return ("Comparação (mesma casa, 10 anos):\n" + _fmt(led) + "\n" + _fmt(sol) +
                "\nRecomendação: comece pelo LED (baixo custo, retorno rápido). Se tiver telhado "
                "adequado e puder investir, o solar dá a maior economia a longo prazo e usa fonte "
                "renovável." + AVISO)
    if any(k in p for k in ["fonte", "referência", "referencia", "dados", "origem"]):
        return FONTES
    if any(k in p for k in ["limit", "garant", "certeza", "premissa"]):
        return (f"Premissas: tarifa R$ {TARIFA}/kWh, sol {HSP} h/dia, desempenho {DESEMPENHO:.0%}, "
                f"solar R$ {CUSTO_KWP:.0f}/kWp, Fio B R$ {FIO_B}/kWh injetado, {FATOR_CO2} kg CO2/kWh. "
                "São estimativas; tarifas, preços e hábitos mudam." )
    return ("Posso ajudar com: consumo da casa, trocar para LED, energia solar, comparar opções, "
            "fontes e limitações. Ex.: 'o que gasta mais energia?'")


def escolher_tarifa():
    """Pergunta a tarifa ao usuário. Enter = valor padrão."""
    print("Escolha a tarifa de energia (R$/kWh):")
    for k, (nome, v) in TARIFAS.items():
        print(f"  {k}) R$ {v:.2f} - {nome}")
    print("  ou digite o valor da SUA conta de luz (ex.: 0,98). Enter = opção 1")
    r = input("Tarifa: ").strip().replace(",", ".")
    if r in TARIFAS:
        return TARIFAS[r][1]
    try:
        v = float(r)
        if 0.3 <= v <= 2.0:
            return v
    except ValueError:
        pass
    return TARIFAS["1"][1]


if __name__ == "__main__":
    TARIFA = escolher_tarifa()
    print(f"\nUsando tarifa de R$ {TARIFA:.2f}/kWh.")
    print("Assistente de Energia (digite 'sair' para encerrar)")
    while True:
        q = input("\nVocê: ")
        if q.strip().lower() in ("sair", "exit"):
            break
        print("\nAssistente:", responder(q))
