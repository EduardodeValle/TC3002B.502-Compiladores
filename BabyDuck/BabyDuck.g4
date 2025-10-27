grammar BabyDuck;

programa: PROGRAM ID SEMI_COLON optional_variables optional_functions MAIN body END;

optional_variables
    : vars
    | // epsilon
    ;

optional_functions
    : funcs
    | // epsilon
    ;

var: VAR declare_vars;

declare_vars: declare_ids COLON type SEMI_COLON declare_vars_prime;

declare_vars_prime
    : declare_vars
    | // epsilon
    ;

declare_ids: ID declare_ids_prime;

declare_ids_prime
    : COMMA declare_ids
    | // epsilon
    ;

// Palabras reservadas
PROGRAM: 'program';
MAIN: 'main';
END: 'end';
VAR: 'var';
INT: 'int';
FLOAT: 'float';
IF: 'if';
ELSE: 'else';
PRINT: 'print';
WHILE: 'while';
DO: 'do';
VOID: 'void';

// Operadores y puntuaciones
LEFT_PARENTHESIS: '(';
RIGHT_PARENTHESIS: ')';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
LEFT_BRACE: '{';
RIGHT_BRACE: '}';
SEMI_COLON: ';';
COLON: ':';
COMMA: ',';
PLUS: '+';
MINUS: '-';
MULTIPLICATION: '*';
DIVISION: '/';
GREATER_THAN: '>';
LESS_THAN: '<';
NOT_EQUAL: '!=';
EQUAL: '=';

// IDs y constantes
ID: [a-zA-Z_] [a-zA-Z_0-9]*;
CTE_I: [0-9]+;
CTE_F: [0-9]+ '.' [0-9]+;
CTE_STRING: '"' .*? '"';

// Ignorar espacios en blanco y saltos de línea
SPACES: [ \t\r\n]+ -> skip;