
{ pkgs ? import <nixpkgs> {} }:

let
  # copiar Python y paquetes instalados globalmente
  customPython = (pkgs.python312.withPackages (ps: with ps; [
    antlr4-python3-runtime
    pytest
  ]));
in
pkgs.mkShell {
  # lista de paquetes disponibles en shell
  buildInputs = [
    customPython
    pkgs.antlr4
    pkgs.jdk
  ];

  # hook para confirmar que todo cargó
  shellHook = ''
    echo "Entorno de Compilador activado"
    echo "   Variable: \$ANTLR_JAR"
    echo "   Python: $(which python)"
  '';
}
