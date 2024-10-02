# Desafio do Sistena Bancário com as operações de Depósito, Saque e Extrato. 

import time

menu =  ("""
      *********************************
      **** MENU - Sistema Bancário ****
      *********************************
            1 - Depósito 
            2 - Saque 
            3 - Extrato
            9 - Sair 
      *********************************
      Digite a opção desejada ==>> """)

saldo = 0
saldo_inicial = saldo
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:
      print()
      opcao = input(menu)

      if opcao == "1": 
            print("Deposito de valor ")
            try: 
                  valor_deposito = float(input("Informe o valor do depósito: "))
                  if valor_deposito > 0:
                        saldo += valor_deposito
                        extrato += f"Depósito      (+): R$ {valor_deposito:11.2f}\n"
                        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
                        time.sleep(2) 
                  else: 
                        print("Valor do depósito não pode ser negativo.")   
                        time.sleep(3)  
            except ValueError:
                  print("Valor do depósito tem que ser numérico.")   
                  time.sleep(3)

      elif opcao == "2": 
            print("Saque de valor ")
            try: 
                  if numero_saque >= LIMITE_SAQUE: 
                        print("Saque indisponível. Limite de saque diário excedido.")  
                        time.sleep(3)
                  else:       
                        valor_saque = float(input("Informe o valor do saque: "))
                        if valor_saque > limite:
                              print(f"Valor do saque maior do que o limite de R$ {limite:.2f} por saque.")
                              time.sleep(2)  
                        elif valor_saque > 0 and saldo >= valor_saque:
                              saldo -= valor_saque
                              extrato += f"Saque         (-): R$ {valor_saque:11.2f}\n"
                              numero_saque += 1
                              print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
                              time.sleep(2) 
                        elif saldo < valor_saque:
                              print("Saque não realizado. Saldo disponível inferior ao valor do saque informado.")
                              time.sleep(3) 
                        else: 
                              print("Valor do saque não pode ser negativo.")   
                              time.sleep(3)  
            except ValueError:
                  print("Valor do saque tem que ser numérico.")   
                  time.sleep(3)            

      elif opcao == "3": 
            print("\n*********************************")
            print("***** Extrato das operações *****")
            print("*********************************")
            if len(extrato) != 0:
                  if saldo_inicial == 0: 
                        print(f"Saldo inicial    : R$ {saldo_inicial:11.2f}")
                  elif saldo_inicial > 0:
                        print(f"Saldo inicial (+): R$ {saldo_inicial:11.2f}")
                  else:           
                        print(f"Saldo inicial (-): R$ {saldo_inicial:11.2f}")
                  print(extrato)
            else:
                  print("\nNão foram realizadas movimentações.\n")
         
            print("---------------------------------")
            if saldo == 0: 
                  print(f"Saldo atual      : R$ {saldo:11.2f}")
            elif saldo > 0:
                  print(f"Saldo atual   (+): R$ {saldo:11.2f}")
            else:           
                  print(f"Saldo atual   (-): R$ {saldo:11.2f}")
            print("---------------------------------\n")
            input("Tecle ENTER para retornar ao menu ...")         
      elif opcao == "9":
            print("\n      Obrigado por utilizar o nosso sistema")
            time.sleep(2) 
            print()
            break   
      else: 
            print("\n   Operação Inválida. Favor selecionar uma das opções do menu.")      
            time.sleep(2)