# Cadastro COMPLETO das classes
classes = {
    "cx 6/1 ml 200":  {"tipo": "cx",  "ml": 200,  "limite": 76},
    "pet 6/1 ml 1500": {"tipo": "pet", "ml": 1500, "limite": 22, "perfil": "padrao"},
    "pet 6/1 ml 1000": {"tipo": "pet", "ml": 1000, "limite": 25, "perfil": "padrao"},
    "pet 6/1 ml 1000 BL": {"tipo": "pet", "ml": 1000, "limite": 24, "perfil": "baixo_largo"},  # 👈 NOVO
    "cx 48/1 ml 310": {"tipo": "cx",  "ml": 310,  "limite": 12},
    "pet 8/1 ml 1500": {"tipo": "pet", "ml": 1500, "limite": 20, "perfil": "padrao"},
    "pet 12/1 ml 500": {"tipo": "pet", "ml": 500,  "limite": 24, "perfil": "padrao"},
    "lt 6/1 ml 220":  {"tipo": "lt",  "ml": 220,  "limite": 60},
    "cx 6/1 ml 1500": {"tipo": "cx",  "ml": 1500, "limite": 22},
    "cx 12/1 ml 200": {"tipo": "cx",  "ml": 200,  "limite": 40},
    "cx 6/1 ml 1000": {"tipo": "cx",  "ml": 1000, "limite": 32},
    "lt 12/1 ml 260": {"tipo": "lt",  "ml": 260,  "limite": 28},
    "lt 12/1 ml 350": {"tipo": "lt",  "ml": 350,  "limite": 28},
    "lt 6/1 ml 350": {"tipo": "lt",  "ml": 350,  "limite": 45},    
    "pet 6/1 ml 2000": {"tipo": "pet", "ml": 2000, "limite": 20, "perfil": "padrao"},
    "pet 6/1 ml 2500": {"tipo": "pet", "ml": 2500, "limite": 15, "perfil": "padrao"},
    "pet 6/1 ml 3000": {"tipo": "pet", "ml": 3000, "limite": 15, "perfil": "padrao"},
}

def compativel(base, item):
    # regra só para PET
    if base["tipo"] != "pet":
        return True

    perfil_base = base.get("perfil", "padrao")
    perfil_item = item.get("perfil", "padrao")

    # baixo/largo não mistura com 1L padrão
    if perfil_base == "baixo_largo" and perfil_item == "padrao" and item["ml"] == 1000:
        return False

    if perfil_item == "baixo_largo" and perfil_base == "padrao" and base["ml"] == 1000:
        return False

    # baixo/largo só aceita 500 ou 600 ml
    if perfil_base == "baixo_largo" and item["ml"] not in (500, 600, 1000):
        return False

    return True


produtos = []

total = int(input("Quantos produtos? "))

for i in range(total):
    print(f"\nProduto {i + 1}")
    nome = input("Nome do produto: ")

    print("\nEscolha a classe:")
    for idx, classe in enumerate(classes.keys(), start=1):
        print(f"{idx} - {classe}")

    opcao = int(input("Digite o número da classe: "))
    classe = list(classes.keys())[opcao - 1]

    quantidade = int(input("Quantidade de fardos: "))

    produtos.append({
        "nome": nome,
        "classe": classe,
        "tipo": classes[classe]["tipo"],
        "ml": classes[classe]["ml"],
        "limite": classes[classe]["limite"],
        "perfil": classes[classe].get("perfil", "padrao"),
        "quantidade": quantidade
    })

# Agrupar por tipo
grupos = {}
for p in produtos:
    grupos.setdefault(p["tipo"], []).append(p)

print("\nRESULTADO DA PALETIZAÇÃO")

for tipo, itens in grupos.items():
    print(f"\n=== TIPO {tipo.upper()} ===")

    itens.sort(key=lambda x: x["ml"], reverse=True)

    camada = 1
    fila = [item.copy() for item in itens]

    while fila and camada <= 6:
        base = fila[0]
        limite = base["limite"]
        capacidade = limite

        print(f"\nCamada {camada} (máx {limite})")

        nova_fila = []

        for item in fila:
            if capacidade == 0 or not compativel(base, item):
                nova_fila.append(item)
                continue

            usar = min(item["quantidade"], capacidade)

            print(f'{item["nome"]} ({item["classe"]}) = {usar}')

            item["quantidade"] -= usar
            capacidade -= usar

            if item["quantidade"] > 0:
                nova_fila.append(item)

        fila = nova_fila
        camada += 1