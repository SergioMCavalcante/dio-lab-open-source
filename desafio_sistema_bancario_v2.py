# Desafio do Sistena Bancário com as operações de Depósito, Saque e Extrato. 

import textwrap, time

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato   
    [4]\tNovo usuário
    [5]\tNova conta
    [6]\tListar contas
    [9]\tSair
    Digite a opção desejada => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito    (+):\tR$ {valor:10.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n>>> Depósito não realizado! Valor do depósito não pode ser negativo. <<<")

    time.sleep(3)
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("\n>>> Saque não realizado! Saldo disponível menor do que o valor do saque. <<<")

    elif excedeu_limite:
        print(f"\n>>> Saque não realizado! O valor do saque excede o limite de R$ {limite:.2f}.  <<<")

    elif excedeu_saques:
        print("\n>>> Saque não realizado! Número máximo de saques excedido.  <<<")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque       (-):\tR$ {valor:10.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n>>> Saque não realizado! O valor informado é inválido.  <<<")

    time.sleep(3)
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    if saldo == 0: 
        print(f"Saldo atual    :\tR$ {saldo:10.2f}")
    elif saldo > 0:
        print(f"Saldo atual (+):\tR$ {saldo:10.2f}")
    else:           
        print(f"Saldo atual (-):\tR$ {saldo:10.2f}")
    print("======================================")
    time.sleep(3)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n>>> Já existe usuário com esse CPF!  <<<")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")
    time.sleep(3)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        time.sleep(3)
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n>>> Usuário não encontrado, fluxo de criação de conta encerrado!  <<<")
    time.sleep(3)

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "9":
            break

        else:
            print("Opção inválida, por favor selecione novamente a opção desejada.")
            time.sleep(3)

main()