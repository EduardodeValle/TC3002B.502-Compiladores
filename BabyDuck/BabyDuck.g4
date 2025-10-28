grammar BabyDuck;

programa: PROGRAMA ID PUNTO_Y_COMA vars? funcs* INICIO cuerpo FIN ;

vars: VARS declarar_variables+ ;
declarar_variables: declarar_ids+ DOS_PUNTOS tipo PUNTO_Y_COMA ;
declarar_ids: ID (COMA ID)* ;

funcs: (NULA | tipo) ID PARENTESIS_IZQUIERDO parametros? PARENTESIS_DERECHO LLAVE_IZQUIERDA vars? cuerpo LLAVE_DERECHA PUNTO_Y_COMA ;
parametros: ID DOS_PUNTOS tipo (COMA ID DOS_PUNTOS tipo)* ;

cuerpo: LLAVE_IZQUIERDA estatuto* LLAVE_DERECHA ;

tipo: ENTERO | FLOTANTE

estatuto: ID continuacion_de_estatuto_id | condicion | ciclo | imprime | CORCHETE_IZQUIERDO estatuto* CORCHETE_DERECHO ;
continuacion_de_estatuto_id: ASIGNACION expresion PUNTO_Y_COMA | PARENTESIS_IZQUIERDO (expresion (COMA expresion)*)? PARENTESIS_DERECHO PUNTO_Y_COMA ;

asigna: ID ASIGNACION expresion PUNTO_Y_COMA ;

condicion: SI PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO cuerpo (SINO cuerpo)? PUNTO_Y_COMA ;

ciclo: MIENTRAS PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO HAZ cuerpo PUNTO_Y_COMA ;

llamada: ID PARENTESIS_IZQUIERDO (expresion (COMA expresion)*)? PARENTESIS_DERECHO

imprime: ESCRIBE PARENTESIS_IZQUIERDO imprimir_elementos PARENTESIS_DERECHO PUNTO_Y_COMA ;
imprimir_elementos: ((expresion | LETRERO) (COMA (expresion | LETRERO))*) ;

expresion: exp ((MAYOR_QUE | MENOR_QUE | DIFERENTE_DE | IGUAL_QUE) exp)?

exp: termino ((MAS | MENOS) termino)*

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
CORCHETE_IZQUIERDO: '[';
CORCHETE_DERECHO: ']';
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