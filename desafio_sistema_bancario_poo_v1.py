import textwrap, time
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            
        else:
            print("\n>>> Depósito não realizado! Valor informado é inválido. <<<")
            time.sleep(2)
            return False
        
        time.sleep(2)
        return True

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
    
        if excedeu_saldo:
            print("\n>>> Saque não realizado! Saldo disponível menor do que o valor do saque. <<<")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            time.sleep(2)
            return True

        else:
            print("\n>>> Saque não realizado! O valor informado é inválido.  <<<")
        
        time.sleep(2)
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n>>> Saque não realizado! O valor do saque excede o limite. <<<")
        
        elif excedeu_saques:
            print("\n>>> Saque não realizado! Número máximo de saques excedido. <<<")

        else:
            return super().sacar(valor)

        time.sleep(2)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato   
    [4]\tNovo cliente
    [5]\tNova conta
    [6]\tListar contas
    [9]\tSair
    Digite a opção desejada => """
    return input(textwrap.dedent(menu))

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n>>> Cliente não encontrado! <<<")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n======= EXTRATO DAS MOVIMENTAÇÕES =======")
    if len(cliente.nome) > 0: 
        print(f"Cliente: {cliente.nome}")
        
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\nNão foram realizadas movimentações."
    else:
        for transacao in transacoes:

            if transacao["tipo"] == Saque.__name__:
                extrato += f"\n{transacao['tipo']}       (-):\tR$ {transacao['valor']:10.2f}"
            elif transacao["tipo"] == Deposito.__name__:  
                extrato += f"\n{transacao['tipo']}    (+):\tR$ {transacao['valor']:10.2f}"  
            else: 
                extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:10.2f}"      

    print(extrato)
    if conta.saldo == 0: 
        print(f"\nSaldo atual    :\tR$ {conta.saldo:10.2f}")
    elif conta.saldo > 0:
        print(f"\nSaldo atual (+):\tR$ {conta.saldo:10.2f}")
    else:           
        print(f"\nSaldo atual (-):\tR$ {conta.saldo:10.2f}")

    print("=========================================")
    time.sleep(3)

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n>>> Já existe cliente com esse CPF!  <<<")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)

    print("=== Cliente criado com sucesso! ===")
    time.sleep(3)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n>>> Cliente não possui conta! <<<")
        time.sleep(2)
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n>>> Cliente não encontrado, fluxo de criação de conta encerrado! <<<")
        time.sleep(2)
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")
    time.sleep(2)

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n>>> Cliente não encontrado! <<<")
        time.sleep(2)
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n>>> Cliente não encontrado! <<<")
        time.sleep(2)
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)        

def main():
    
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "9":
            break

        else:
            print("Opção inválida, por favor selecione novamente a opção desejada.")
            time.sleep(3)

main()