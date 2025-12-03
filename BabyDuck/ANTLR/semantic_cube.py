# ok    → operacion valida
# error → operacion invalida
# diferente de error y de ok → tipo de resultado de la operacion

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