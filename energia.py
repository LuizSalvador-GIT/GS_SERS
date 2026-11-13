"""
Módulo de Energia do Citizen Assist AI
Disciplina: Soluções em Energias Renováveis e Sustentáveis

Necessidade: reduzir a conta de luz de uma residência urbana (São Paulo/SP).
Alternativas comparadas (mesma necessidade, mesmo período de 10 anos):
  A) Banho 30% mais curto           (mudança de hábito, custo zero)
  B) Trocar lâmpadas por LED         (eficiência energética)
  C) Sistema solar fotovoltaico      (fonte renovável)

ATENÇÃO: valores são ESTIMATIVAS/PREMISSAS (ver dados.md). Todos podem ser
alterados nas constantes abaixo ou informados pelo usuário ao abrir o programa.
"""

# ---------------- PREMISSAS ----------------
TARIFA = 0.94            # R$/kWh com impostos (TUSD+TE, contas reais Enel SP mar/2026)
FATOR_CO2 = 0.0385       # kg CO2/kWh (média anual 2023 do SIN, MCTI)
ANOS = 10                # período de referência comum
ANO_INICIO = 2027        # 1º ano completo de operação (usado no modelo ano a ano)

TARIFAS = {
    "1": ("Enel SP - contas reais de mar/2026 (dado público)", 0.94),
    "2": ("Enel SP - estimativa após reajuste de jul/2026 (0,941 x 1,0897)", 1.03),  # ESTIMADO
}

# Casa-exemplo (ESTIMADA): nome -> (potência W, horas/dia, dias/mês, quantidade)
EQUIPAMENTOS = {
    "Chuveiro elétrico":        (5500, 0.7, 30, 1),
    "Geladeira":                (120, 8, 30, 1),        # 8 h/dia equivalentes (ciclo do compressor)
    "Lâmpadas incandescentes":  (60, 5, 30, 6),
    "TV":                       (100, 5, 30, 1),
    "Ventilador":               (60, 6, 30, 1),
    "Outros (celular, PC etc.)": (1000, 1, 30, 1),      # ~30 kWh/mês estimados
}
LAMP = "Lâmpadas incandescentes"   # nome da linha de lâmpadas em EQUIPAMENTOS

# Alternativa A: banho mais curto
REDUCAO_BANHO = 0.30     # 30% menos tempo de banho (premissa)

# Alternativa B: LED
POT_LED = 9              # W por lâmpada LED equivalente a 60 W
CUSTO_LED = 12.0         # R$ por lâmpada (estimado)

# Alternativa C: fotovoltaico
KWP = 1.5                # potência do sistema (kWp)
HSP = 4.5                # horas de sol pleno/dia (capital paulista: 4,5-4,8; Atlas Solar INPE)
DESEMPENHO = 0.80        # taxa de desempenho (perdas)
CUSTO_KWP = 2840.0       # R$/kWp instalado (Greener 2025: R$ 2,84/Wp; média 2026 ~R$ 2,45/Wp)
DISPONIBILIDADE = 30     # kWh/mês mínimos cobrados, ligação monofásica (ANEEL, REN 1000/2021)
FIO_B = 0.12             # R$/kWh injetado, com Fio B a 60% (2026, Lei 14.300)
FIO_B_100 = FIO_B / 0.60 # equivalente a 100% do Fio B
FIO_B_PERC = {2026: 0.60, 2027: 0.75, 2028: 0.90}   # a partir de 2029: 100% (simplificação)
SIMULTANEIDADE = 0.30    # fração da geração consumida na hora (estimativa)
DEGRADACAO = 0.005       # perda de geração por ano (0,5%/ano, estimativa típica)


# ---------------- CÁLCULOS ----------------
def kwh_mes(pot_w, h_dia, dias, qtd=1):
    """Energia (kWh/mês) = potência (kW) x tempo (h) x quantidade."""
    return pot_w / 1000 * h_dia * dias * qtd


def consumo_total():
    return {n: kwh_mes(*v) for n, v in EQUIPAMENTOS.items()}


def total_kwh():
    return sum(consumo_total().values())


def dimensionar_kwp(total):
    """Sistema que cobre ~60% do consumo (acima da taxa mínima), arredondado a 0,5 kWp."""
    alvo = 0.6 * max(total - DISPONIBILIDADE, 0)
    kwp = alvo / (HSP * 30 * DESEMPENHO)
    return max(0.5, round(-(-kwp * 2 // 1) / 2, 1))


def _resumo(nome, eco_kwh, custo, geracao=None, desconto_rs=0.0):
    eco_rs = eco_kwh * TARIFA - desconto_rs
    return {
        "nome": nome,
        "kwh_mes": eco_kwh,
        "geracao_kwh_mes": geracao,
        "reais_mes": eco_rs,
        "custo_inicial": custo,
        "retorno_meses": custo / eco_rs if eco_rs > 0 else float("inf"),
        "saldo_10_anos": eco_rs * 12 * ANOS - custo,
        "co2_evitado_10_anos_kg": eco_kwh * 12 * ANOS * FATOR_CO2,
    }


def alternativa_banho():
    p, h, d, q = EQUIPAMENTOS["Chuveiro elétrico"]
    return _resumo("Banho 30% mais curto", kwh_mes(p, h, d, q) * REDUCAO_BANHO, 0.0)


def alternativa_led():
    p, h, d, q = EQUIPAMENTOS[LAMP]
    eco = kwh_mes(p, h, d, q) - kwh_mes(min(POT_LED, p), h, d, q)
    return _resumo("LED", eco, CUSTO_LED * q)


def geracao_mensal(ano_idx=0):
    return KWP * HSP * 30 * DESEMPENHO * ((1 - DEGRADACAO) ** ano_idx)


def alternativa_solar():
    geracao = geracao_mensal()
    compensado = min(geracao, max(total_kwh() - DISPONIBILIDADE, 0))  # a conta não zera
    injetado = compensado * (1 - SIMULTANEIDADE)
    return _resumo("Solar fotovoltaico", compensado, KWP * CUSTO_KWP, geracao, injetado * FIO_B)


def fluxo_solar(tarifa=None, custo_kwp=None):
    """Modelo ano a ano: Fio B subindo (75% em 2027, 90% em 2028, 100% depois) e perda de 0,5%/ano."""
    t = tarifa if tarifa else TARIFA
    custo = KWP * (custo_kwp if custo_kwp else CUSTO_KWP)
    acumulado, payback, linhas = -custo, None, []
    for i in range(ANOS):
        ano = ANO_INICIO + i
        comp = min(geracao_mensal(i), max(total_kwh() - DISPONIBILIDADE, 0))
        inj = comp * (1 - SIMULTANEIDADE)
        eco_ano = 12 * (comp * t - inj * FIO_B_100 * FIO_B_PERC.get(ano, 1.0))
        anterior = acumulado
        acumulado += eco_ano
        if payback is None and acumulado >= 0 and eco_ano > 0:
            payback = i + (-anterior) / eco_ano
        linhas.append((ano, eco_ano, acumulado))
    return {"linhas": linhas, "payback_anos": payback, "saldo": acumulado, "custo": custo}


def configurar_casa(consumo_kwh, chuveiro_w, banho_min, n_lamp, lamp_w, lamp_h):
    """Personaliza a análise com os dados da casa do usuário."""
    global EQUIPAMENTOS, LAMP, KWP
    chuv = (chuveiro_w, banho_min / 60, 30, 1)
    lamp = (lamp_w, lamp_h, 30, n_lamp)
    outros = max(consumo_kwh - kwh_mes(*chuv) - kwh_mes(*lamp), 0)
    LAMP = "Lâmpadas atuais"
    EQUIPAMENTOS = {
        "Chuveiro elétrico": chuv,
        LAMP: lamp,
        "Outros (geladeira, TV etc.)": (1000, outros / 30, 30, 1),
    }
    KWP = dimensionar_kwp(total_kwh())


# ---------------- ASSISTENTE ----------------
def aviso():
    return (f"\n(Estimativas, não garantias: dependem da sua tarifa, hábitos, sol local e preços. "
            f"Casa analisada: ~{total_kwh():.0f} kWh/mês. Digite 'fontes' para as referências.)")


FONTES = (
    "Fontes para conferir os dados:\n"
    "- Contas reais Enel SP (tarifa TUSD+TE): Câmara dos Deputados, camara.leg.br/cota-parlamentar\n"
    "- ANEEL: tarifas e reajustes (aneel.gov.br); custo de disponibilidade, REN 1000/2021\n"
    "- INPE: Atlas Brasileiro de Energia Solar; CRESESB SunData\n"
    "- MCTI: fator de emissão do Sistema Interligado Nacional (2023: 38,5 kg CO2/MWh)\n"
    "- Greener / Solfácil: custo do sistema fotovoltaico residencial\n"
    "- Lei 14.300/2022: marco legal da geração distribuída (Fio B)\n"
    "- Procel/Inmetro: consumo de equipamentos (procelinfo.com.br)")


def _fmt(a):
    custo = "sem custo" if a["custo_inicial"] == 0 else f"investimento ~R$ {a['custo_inicial']:.0f}"
    if a["retorno_meses"] == float("inf"):
        retorno = "sem retorno nesta casa"
    elif a["custo_inicial"] == 0:
        retorno = "economia imediata"
    else:
        retorno = f"retorno em ~{a['retorno_meses']:.0f} meses"
    return (f"{a['nome']}: economia de {a['kwh_mes']:.0f} kWh/mês (R$ {a['reais_mes']:.0f}/mês); "
            f"{custo}; {retorno}; saldo em {ANOS} anos ~R$ {a['saldo_10_anos']:.0f}; "
            f"CO2 evitado ~{a['co2_evitado_10_anos_kg']:.0f} kg em {ANOS} anos.")


def _has(p, palavras):
    return any(k in p for k in palavras)


def responder(pergunta):
    """Função para integrar ao Citizen Assist AI: recebe texto, devolve orientação."""
    p = pergunta.lower()
    banho, led, sol = alternativa_banho(), alternativa_led(), alternativa_solar()

    if _has(p, ["sensib", "e se "]):
        ts, cs = [0.80, TARIFA, 1.03], [2450, CUSTO_KWP, 3500]
        linhas = ["Retorno do solar em anos, variando tarifa (linhas) e custo por kWp (colunas):",
                  "Tarifa \\ Custo/kWp   " + "   ".join(f"R${c:.0f}" for c in cs)]
        for t in ts:
            vals = []
            for c in cs:
                pb = fluxo_solar(t, c)["payback_anos"]
                vals.append(f"{pb:6.1f}" if pb else "  >10 ")
            linhas.append(f"R$ {t:.2f}/kWh          " + "   ".join(vals))
        return "\n".join(linhas) + "\nTarifa e custo mudam muito o retorno; peça orçamentos reais." + aviso()
    if _has(p, ["ano a ano", "fio b", "refin", "detalh", "10 anos"]):
        f = fluxo_solar()
        pb = f"{f['payback_anos']:.1f} anos" if f["payback_anos"] else "mais de 10 anos"
        ini, fim = f["linhas"][0], f["linhas"][-1]
        return (f"Solar ano a ano (Fio B sobe para 75% em 2027, 90% em 2028 e 100% depois; painéis perdem "
                f"{DEGRADACAO:.1%}/ano): economia {ini[0]}: R$ {ini[1]:.0f}; {fim[0]}: R$ {fim[1]:.0f}. "
                f"Retorno em ~{pb}; saldo acumulado em {ANOS} anos ~R$ {f['saldo']:.0f} "
                f"(investimento R$ {f['custo']:.0f}). Considera tarifa constante e não inclui troca do inversor." + aviso())
    if _has(p, ["kwh", "potência", "potencia", "eficiên", "eficien", "conceito"]):
        return (f"Potência (kW ou W) é quanto um aparelho 'puxa' num instante. Energia (kWh) = potência (kW) × tempo (h). "
                f"Ex.: chuveiro de 5,5 kW ligado 1 h gasta 5,5 kWh (≈ R$ {5.5 * TARIFA:.2f} com a tarifa atual). "
                f"Eficiência energética é obter o mesmo serviço com menos energia: um LED de {POT_LED} W dá a luz de uma "
                f"lâmpada de 60 W, com {1 - POT_LED / 60:.0%} menos potência. Fonte renovável é a que se renova naturalmente, "
                f"como o sol usado nos painéis fotovoltaicos." + aviso())
    if _has(p, ["co2", "ambient", "emiss", "carbono", "sustent"]):
        return (f"Impacto ambiental em {ANOS} anos (fator {FATOR_CO2} kg CO2/kWh): banho mais curto evita "
                f"~{banho['co2_evitado_10_anos_kg']:.0f} kg, LED ~{led['co2_evitado_10_anos_kg']:.0f} kg e solar "
                f"~{sol['co2_evitado_10_anos_kg']:.0f} kg. A rede elétrica brasileira já é majoritariamente renovável, "
                "então o ganho em CO2 é pequeno; o principal benefício é financeiro. A fabricação e o descarte dos "
                "painéis não entram nesta conta." + aviso())
    if _has(p, ["viabil", "telhado", "preciso", "posso instalar"]):
        return (f"Viabilidade: banho mais curto, qualquer pessoa, sem custo. LED, qualquer moradia (~R$ {led['custo_inicial']:.0f}). "
                f"Solar: precisa de telhado ou área com sol e pouca sombra, imóvel próprio (ou autorização), projeto, "
                f"aprovação da distribuidora e investimento de ~R$ {sol['custo_inicial']:.0f}." + aviso())
    if _has(p, ["banho", "chuveiro"]) and not _has(p, ["gasta", "consumo", "pesa"]):
        return _fmt(banho) + "\nDica: é a ação de maior economia sem custo, pois o chuveiro é o maior consumo." + aviso()
    if _has(p, ["gasta mais", "maior consumo", "vilão", "consumo", "pesa", "onde gasto"]):
        c = consumo_total()
        total = sum(c.values())
        linhas = "\n".join(f"- {n}: {v:.0f} kWh/mês ({v / total:.0%})"
                           for n, v in sorted(c.items(), key=lambda x: -x[1]))
        return f"Consumo estimado ({total:.0f} kWh/mês, ~R$ {total * TARIFA:.0f}/mês):\n{linhas}" + aviso()
    if _has(p, ["led", "lâmpada", "lampada"]):
        return _fmt(led) + "\nDica: troque primeiro as lâmpadas mais usadas." + aviso()
    if _has(p, ["solar", "painel", "fotovoltaic", "renovável", "renovavel"]):
        return (_fmt(sol) + f"\nGeração estimada: {sol['geracao_kwh_mes']:.0f} kWh/mês (sistema de {KWP} kWp). "
                "Limitações: a conta nunca zera (taxa mínima), o Fio B de 2026 já está considerado e sobe até 2028 "
                "(digite 'ano a ano'), exige telhado com sol e preços/regras podem mudar." + aviso())
    if _has(p, ["comparar", "melhor", "recomend", "vale", "economizar", "economia"]):
        nota = ("\nObs.: nesta casa o LED rende pouco (lâmpadas já eficientes ou poucas)."
                if led["kwh_mes"] < 10 else "")
        return ("Comparação (mesma casa, 10 anos):\n" + _fmt(banho) + "\n" + _fmt(led) + "\n" + _fmt(sol) + nota +
                "\nRecomendação: comece pelo banho mais curto (grátis) e pelo LED (barato, retorno rápido). "
                "Se tiver telhado adequado e puder investir, o solar dá a maior economia a longo prazo e usa fonte "
                "renovável." + aviso())
    if _has(p, ["fonte", "referência", "referencia", "dados", "origem"]):
        return FONTES
    if _has(p, ["limit", "garant", "certeza", "premissa"]):
        return (f"Premissas: tarifa R$ {TARIFA:.2f}/kWh, sol {HSP} h/dia, desempenho {DESEMPENHO:.0%}, "
                f"solar R$ {CUSTO_KWP:.0f}/kWp, Fio B R$ {FIO_B}/kWh injetado, {FATOR_CO2} kg CO2/kWh, "
                f"perda de painéis {DEGRADACAO:.1%}/ano. São estimativas; tarifas, preços e hábitos mudam, "
                "e o solar exige avaliação técnica do local.")
    return ("Posso ajudar com: o que gasta mais energia, banho mais curto, trocar para LED, energia solar, "
            "comparar opções, ano a ano, sensibilidade, viabilidade, impacto ambiental, conceitos (kWh, potência), "
            "fontes e limitações. Ex.: 'o que gasta mais energia?'")


# ---------------- EXECUÇÃO NO TERMINAL ----------------
def _numero(msg, padrao, minimo, maximo):
    r = input(f"{msg} [{padrao}]: ").strip().replace(",", ".")
    try:
        v = float(r) if r else padrao
        return v if minimo <= v <= maximo else padrao
    except ValueError:
        return padrao


def escolher_tarifa():
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


def escolher_casa():
    r = input("\nUsar a casa-exemplo (Enter) ou informar os dados da SUA casa (digite s)? ").strip().lower()
    if r != "s":
        return
    consumo = _numero("Consumo mensal da conta de luz (kWh)", 254, 50, 2000)
    chuv_w = _numero("Potência do chuveiro (W, na etiqueta)", 5500, 2000, 8000)
    banho = _numero("Minutos de banho por dia, somando a casa toda", 42, 5, 300)
    n_lamp = int(_numero("Quantas lâmpadas ficam acesas no dia a dia", 6, 1, 50))
    lamp_w = _numero("Potência de cada lâmpada atual (W)", 60, 3, 150)
    lamp_h = _numero("Horas por dia que ficam acesas", 5, 1, 24)
    configurar_casa(consumo, chuv_w, banho, n_lamp, lamp_w, lamp_h)
    print(f"\nCasa configurada: {total_kwh():.0f} kWh/mês analisados; solar dimensionado em {KWP} kWp.")


if __name__ == "__main__":
    TARIFA = escolher_tarifa()
    print(f"\nUsando tarifa de R$ {TARIFA:.2f}/kWh.")
    escolher_casa()
    print("\nAssistente de Energia (digite 'sair' para encerrar)")
    while True:
        q = input("\nVocê: ")
        if q.strip().lower() in ("sair", "exit"):
            break
        print("\nAssistente:", responder(q))
