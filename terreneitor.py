from itertools import product
import pyfiglet
from tabulate import tabulate

texto = pyfiglet.figlet_format("Terreneitor", font="slant")
print(texto)
# expresion_a_evaluar = input("Ingrese la expresión a evaluar: ")
resultado = []

ultima_columna_resuelta = []

# expresionTokenizada =["(", "A","∧","B",")", "∧","(","¬", "A", "∨", "C" ,")"]
# expresionTokenizada =["¬","¬","A"]
# expresionTokenizada =["[","A","→","(","A","↔","B",")"] 
# ""
def obtenerVariables(expresion):
    '''
    Esta función obtiene todas las variables presentes en una expresión.

    Parámetro:
    - expresion: string que contiene la expresión (ej: "A ∧ B ∨ C")

    Retorna:
    - Una lista con las variables sin repetir (ej: ["A", "B", "C"])
    '''

    variables = []
    '''
    Creamos una lista vacía donde vamos a guardar
    las variables encontradas en la expresión.
    '''

    for caracter in expresion:
        '''
        Recorremos la expresión carácter por carácter.
        '''

        if caracter.isalpha() and caracter not in variables:
            '''
            Verificamos dos cosas:
            - caracter.isalpha(): que el carácter sea una letra (A, B, C, etc.)
            - caracter not in variables: que no esté ya en la lista para evitar repetir variables
            '''

            variables.append(caracter)
            '''
            Si cumple las condiciones, agregamos la variable a la lista.
            '''

    return variables
    '''
    Devolvemos la lista final con todas las variables encontradas
    en la expresión, sin repeticiones.
    '''

def generarCombinaciones(variables):
    return product([False, True], repeat=len(variables))

def solicitar_expresion():
    '''
    Solicita al usuario una expresión lógica válida.

    Una expresión es válida si todos sus caracteres:
    - son letras
    O
    - pertenecen a los operadores permitidos

    Retorna:
    - La expresión ingresada por el usuario
    '''

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

        # Validar que no esté vacía
        if expresion == "":
            print("\nError: la expresión no puede estar vacía.")
            continue

        expresion_valida = True
        '''
        Suponemos que la expresión es válida.
        Si aparece un carácter inválido,
        cambiamos esta variable a False.
        '''

        # Revisar cada carácter de la expresión
        for caracter in expresion:

            '''
            El carácter es válido si:
            - es una letra
            O
            - pertenece a los operadores permitidos
            '''

            if not caracter.isalpha() and caracter not in operadores_validos:

                print(f"\nError: carácter inválido -> {caracter}")

                expresion_valida = False
                break

        # Si la expresión es válida, retornarla
        if expresion_valida:
            return expresion

def crear_contexto(variables, valores):
    '''
    Crea un diccionario que relaciona cada variable
    con su valor booleano correspondiente.

    Parámetros:
    - variables: lista con nombres de variables
      Ejemplo: ["A", "B", "C"]

    - valores: lista con valores booleanos
      Ejemplo: [True, False, True]

    Retorna:
    - Un diccionario con la relación variable → valor

      Ejemplo:
      {
          "A": True,
          "B": False,
          "C": True
      }
    '''

    contexto = {}
    '''
    Creamos un diccionario vacío.

    Aquí iremos guardando cada variable junto
    con su valor correspondiente.
    '''

    # Recorremos todas las posiciones de la lista
    for i in range(len(variables)):
        '''
        Usamos índices porque necesitamos acceder
        simultáneamente a:

        - variables[i]
        - valores[i]

        Ejemplo:
        i = 0
        variables[0] → "A"
        valores[0] → True
        '''

        variable_actual = variables[i]
        '''
        Obtenemos el nombre de la variable actual.
        '''

        valor_actual = valores[i]
        '''
        Obtenemos el valor asociado a esa variable.
        '''

        contexto[variable_actual] = valor_actual
        '''
        Guardamos la relación dentro del diccionario.

        Ejemplo:
        contexto["A"] = True
        '''

    return contexto
    '''
    Devolvemos el diccionario completo.
    '''

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

print(f"Resultados finales (resultado expresión): {ultima_columna_resuelta}")
print(tabulate(resultado, headers=expresionTokenizada, tablefmt="grid"))

# #Todos
# #crear funcion para tomar la expresion del usuario con un input y convertirla en la variable expreison tokenizada
# #Crear funcion para parsear implicacion ( y colocarla en el flujo, llamarla donde se debe llamar)
# #Crear funcion para parsear bicondicional ( y colocarla en el flujo, llamarla donde se debe llamar)
# #analizar el resultado de la variable ultima_columna_resuelta y en base a eso decir si es una tautologia, contradiccion o contingencia. 
