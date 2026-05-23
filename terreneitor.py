from itertools import product
import pyfiglet
from tabulate import tabulate

textoBienvenida = pyfiglet.figlet_format("Terreneitor", font="slant")
print(textoBienvenida)

resultado = []
ultima_columna_resuelta = []


def obtenerVariables(expresion):
   
    variables = []
    for caracter in expresion:
    
        if caracter.isalpha() and caracter not in variables:
           
            variables.append(caracter)
            
    return variables
   

def generarCombinaciones(variables):
    return product([False, True], repeat=len(variables))

def solicitar_expresion():
   
    operadores_validos = [
        "∧", "∨", "¬",
        "→", "↔️", "⊕",
        "(", ")", "[", "]"
    ]

    while True:

        print("Ingrese una expresión lógica válida.")
        print("Ejemplo:")
        print("(A∧B)∨¬C")

        expresion = input("\nIngrese la expresión: ")

        if expresion == "":
            print("\nError: la expresión no puede estar vacía.")
            continue

        expresion_valida = True
      
        for caracter in expresion:

            if not caracter.isalpha() and caracter not in operadores_validos:

                print(f"\nError: carácter inválido -> {caracter}")

                expresion_valida = False
                break

        if expresion_valida:
            return expresion

def clasificar_expresion(ultima_columna_resuelta):
    if all(ultima_columna_resuelta):
        return "Tautología"
    elif not any(ultima_columna_resuelta):
        return "Contradicción"
    else:
        return "Contingencia"


def crear_contexto(variables, valores):
   
    contexto = {}

    for i in range(len(variables)):
        
        variable_actual = variables[i]
       
        valor_actual = valores[i]
      
        contexto[variable_actual] = valor_actual
     
    return contexto
   

def inyectar_valores_en_expresion(expresion, contexto):
    expresion_a_resolver = []
    for token in expresion:
        if token in contexto:
            expresion_a_resolver.append(contexto[token])
        else:
            expresion_a_resolver.append(token)
    return expresion_a_resolver


def resolver_combinacion(expresion, contexto):
    expresion_a_resolver = inyectar_valores_en_expresion(expresion, contexto)

    estado = {"pos": 0}

    def token_actual():
        if estado["pos"] < len(expresion_a_resolver):
            return expresion_a_resolver[estado["pos"]]
        return None

    def avanzar():
        estado["pos"] += 1

    def parse_imp():
        operando_izquierdo = parse_or() 

        while token_actual() == "→":
            indice_operador = estado["pos"] 
            avanzar()                        
            
            operando_derecho = parse_or()  
            operando_izquierdo = not operando_izquierdo or operando_derecho                # ¡Hace la matemática!
            expresion_a_resolver[indice_operador] = operando_izquierdo  
          

        return operando_izquierdo

   
    def parse_bicondicional():
        operando_izquierdo = parse_imp()
        while token_actual() == "↔":
            indice_operador = estado["pos"]
            avanzar() # Consumimos el "↔"
        
            operando_derecho = parse_imp()
        
            if operando_izquierdo == operando_derecho:
               resultado_logico = True
            else:
               resultado_logico = False
            expresion_a_resolver[indice_operador] = resultado_logico
        
            operando_izquierdo = resultado_logico

        return operando_izquierdo



    def parse_and():
        operando_izquierdo = parse_not() 

        while token_actual() == "∧":
            indice_operador = estado["pos"] 
            avanzar()                        
            
            operando_derecho = parse_not()               
            operando_izquierdo = operando_izquierdo and operando_derecho                # ¡Hace la matemática!
            
            expresion_a_resolver[indice_operador] = operando_izquierdo  
          

       
        return operando_izquierdo

    def parse_or_exlusivo():
        operando_izquierdo = parse_and()
        
        while token_actual() == "⊕":
            indice_operador = estado["pos"] 
            avanzar()                        
            
            operando_derecho = parse_and()               
            operando_izquierdo = (operando_izquierdo and not operando_derecho) or (not operando_izquierdo and operando_derecho)  # XOR
            
            expresion_a_resolver[indice_operador] = operando_izquierdo  
           
        return operando_izquierdo

    def parse_or():
        operando_izquierdo = parse_or_exlusivo()

        while token_actual() == "∨":
            indice_operador = estado["pos"] 
            avanzar()                        
            
            operando_derecho = parse_and()               
            operando_izquierdo = operando_izquierdo or operando_derecho                 # ¡Hace la matemática!
            
            expresion_a_resolver[indice_operador] = operando_izquierdo     
           
        return operando_izquierdo

    def parse_base():
        token = token_actual()

        if token in ["(", "["]:
            avanzar()               
            resultado = parse_bicondicional() 
            while token_actual() in [")", "]"]:
             avanzar() 
            return resultado

        
        avanzar()              
        return token
    
   
    def parse_not():
        
        while token_actual() == "¬":
            indice_operador = estado["pos"]  
            avanzar()                        
            
            operando_derecho = parse_not()
            
            resultado = not operando_derecho
            
            expresion_a_resolver[indice_operador] = resultado
            
            
            return resultado
            
        return parse_base()

    resultado_expresion = parse_bicondicional()
    
    return expresion_a_resolver, resultado_expresion



expresionTokenizada = solicitar_expresion()
variables = obtenerVariables(expresionTokenizada);
combinaciones = generarCombinaciones(variables)

for comb in combinaciones:
    contexto_actual = crear_contexto(variables, comb)
    lista_final, resultado_expresion = resolver_combinacion(
        expresionTokenizada,
        contexto_actual
    )

    ultima_columna_resuelta.append(resultado_expresion)
    resultado.append(lista_final) 


resultado_transformado = []

for fila in resultado:
    fila_transformada = []
    for valor in fila:
        if valor is True:
            fila_transformada.append("V")
        elif valor is False:
            fila_transformada.append("F")
        else:
            fila_transformada.append(valor)
    resultado_transformado.append(fila_transformada)
    
clasificacion = clasificar_expresion(ultima_columna_resuelta)
print(tabulate(resultado_transformado, headers=expresionTokenizada, tablefmt="grid"))
print(f"La expresión es: {clasificacion}")
