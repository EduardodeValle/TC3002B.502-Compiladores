# semantic_cube[tipo_izquierdo][tipo_derecho][operador] → devuelve el tipo de dato de la expresión

# Los strings no existen como un tipo de dato explicito, solo adentro de las regla 
# <ESCRIBE> para imprimir datos, no se incluye en el cubo semantico

# No hay un tipo de dato explicito para booleano, pero se usa en resultados de expresiones lógicas

# De acuerdo al diagrama de sintaxis no existen los operadores AND, OR, NOT

# ok → resultado semantico valido
# error → resultado semantico invalido
semantic_cube = {
    "entero": {
        "entero": {
            "+": "entero", 
            "-": "entero", 
            "*": "entero", 
            "/": "entero", 
            ">": "booleano", 
            "<": "booleano", 
            "==": "booleano", 
            "!=": "booleano",
            "=": "ok"
        },
        "flotante": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        },
        "booleano": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        }
    },
    "flotante": {
        "entero": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        },
        "flotante": {
            "+": "flotante", 
            "-": "flotante", 
            "*": "flotante", 
            "/": "flotante",
            ">": "booleano", 
            "<": "booleano", 
            "==": "booleano", 
            "!=": "booleano",
            "=": "ok"
        },
        "booleano": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        }
    },
    "booleano": {
        "entero": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        },
        "flotante": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "error", 
            "!=": "error",
            "=": "error"
        },
        "booleano": {
            "+": "error", 
            "-": "error", 
            "*": "error", 
            "/": "error",
            ">": "error", 
            "<": "error", 
            "==": "booleano", 
            "!=": "booleano",
            "=": "error"
        }
    }
}