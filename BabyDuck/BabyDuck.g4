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
WS: [ \t\r\n]+ -> skip;
