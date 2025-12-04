#!/usr/bin/env python3
"""Script para limpiar comentarios excesivos en archivos Python"""

import re
from pathlib import Path

def clean_python_file(filepath):
    """Limpia comentarios innecesarios de un archivo Python"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Reemplazar docstrings largos con versiones cortas
    content = re.sub(
        r'"""[\s\n]*Punto Neurálgico \d+:([^\n]+)[\s\S]*?"""',
        r'"""PN:\1"""',
        content
    )

    content = re.sub(
        r'"""[\s\n]*Puntos Neurálgicos \d+-\d+:([^\n]+)[\s\S]*?"""',
        r'"""PN:\1"""',
        content
    )

    # Acortar docstrings descriptivos largos
    lines = content.split('\n')
    cleaned_lines = []
    in_docstring = False
    docstring_lines = []

    for line in lines:
        stripped = line.strip()

        # Detectar inicio de docstring
        if '"""' in stripped and not in_docstring:
            if stripped.count('"""') == 2:
                # Docstring de una línea
                cleaned_lines.append(line)
            else:
                in_docstring = True
                docstring_lines = [line]
        elif in_docstring:
            docstring_lines.append(line)
            if '"""' in stripped:
                # Fin del docstring
                in_docstring = False
                # Solo mantener primera línea significativa
                first_line = docstring_lines[0]
                if len(docstring_lines) <= 3:
                    # Docstring corto, mantener
                    cleaned_lines.extend(docstring_lines)
                else:
                    # Docstring largo, acortar
                    cleaned_lines.append(first_line)
                    cleaned_lines.append(docstring_lines[-1])
                docstring_lines = []
        else:
            # Eliminar comentarios inline demasiado descriptivos
            if '#' in line:
                code_part = line.split('#')[0]
                comment_part = line.split('#', 1)[1]

                # Solo mantener comentarios cortos (< 40 chars) o importantes
                if (len(comment_part.strip()) < 40 or
                    any(keyword in comment_part.lower() for keyword in ['importante', 'nota', 'fixme', 'todo', 'hack', 'bug'])):
                    cleaned_lines.append(line)
                else:
                    cleaned_lines.append(code_part.rstrip())
            else:
                cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)

    # Solo escribir si hubo cambios
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Limpia comentarios en todos los archivos Python relevantes"""
    files_to_clean = [
        'SemanticVisitor.py',
        'MemoryManager.py',
        'VM.py',
        'compiler.py',
        'main.py',
        'semantic_cube.py',
        'BabyDuckError.py'
    ]

    cleaned_count = 0
    for filename in files_to_clean:
        filepath = Path(filename)
        if filepath.exists():
            if clean_python_file(filepath):
                print(f"✓ Limpiado: {filename}")
                cleaned_count += 1
            else:
                print(f"○ Sin cambios: {filename}")
        else:
            print(f"✗ No encontrado: {filename}")

    print(f"\nTotal de archivos limpiados: {cleaned_count}")

if __name__ == "__main__":
    main()
