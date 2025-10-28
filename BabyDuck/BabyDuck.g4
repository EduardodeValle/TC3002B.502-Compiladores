grammar BabyDuck;

programa: PROGRAM ID SEMI_COLON vars? funcs? MAIN cuerpo END;

// Palabras reservadas
PROGRAMA: 'programa';
INICIO: 'inicio';
FIN: 'fin';
VARS: 'vars';
ENTERO: 'entero';
FLOTANTE: 'flotante';
SI: 'si';
SINO: 'sino';
ESCRIBE: 'escribe';
MIENTRAS: 'mientras';
HAZ: 'haz';
NULA: 'nula';

// Operadores y puntuaciones
PARENTESIS_IZQUIERDO: '(';
PARENTESIS_DERECHO: ')';
BRACKET_IZQUIERDO: '[';
BRACKET_DERECHO: ']';
LLAVE_IZQUIERDA: '{';
LLAVE_DERECHA: '}';
PUNTO_Y_COMA: ';';
DOS_PUNTOS: ':';
COMA: ',';
ASIGNACION: '=';
MAS: '+';
MENOS: '-';
MULTIPLICACION: '*';
DIVISION: '/';
MAYOR_QUE: '>';
MENOR_QUE: '<';
DIFERENTE_DE: '!=';
IGUAL_QUE: '==';

// IDs y constantes
ID: [a-zA-Z_] [a-zA-Z_0-9]*;
CTE_ENT: [0-9]+;
CTE_FLOT: [0-9]+ '.' [0-9]+;
LETRERO: '"' .*? '"';

// Ignorar espacios en blanco y saltos de línea
ESPACIOS: [ \t\r\n]+ -> skip;