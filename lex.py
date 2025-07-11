import ply.lex as lex
import datetime
import os

# C# reserved keywords -------------------------------------
reserved = {
    # Reserved keywords
    "abstract": "ABSTRACT",
    "as": "AS",
    "base": "BASE",
    "bool": "BOOL_TYPE",
    "break": "BREAK",
    "byte": "BYTE",
    "case": "CASE",
    "catch": "CATCH",
    "char": "CHAR",
    "checked": "CHECKED",
    "class": "CLASS",
    "const": "CONST",
    "continue": "CONTINUE",
    "decimal": "DECIMAL",
    "default": "DEFAULT",
    "delegate": "DELEGATE",
    "do": "DO",
    "double": "DOUBLE",
    "else": "ELSE",
    "enum": "ENUM",
    "event": "EVENT",
    "explicit": "EXPLICIT",
    "extern": "EXTERN",
    "false": "FALSE",
    "finally": "FINALLY",
    "fixed": "FIXED",
    "float": "FLOAT_TYPE",
    "for": "FOR",
    "foreach": "FOREACH",
    "goto": "GOTO",
    "if": "IF",
    "implicit": "IMPLICIT",
    "in": "IN",
    "int": "INT_TYPE",
    "interface": "INTERFACE",
    "internal": "INTERNAL",
    "is": "IS",
    "lock": "LOCK",
    "long": "LONG",
    "namespace": "NAMESPACE",
    "new": "NEW",
    "null": "NULL",
    "object": "OBJECT",
    "operator": "OPERATOR",
    "out": "OUT",
    "override": "OVERRIDE",
    "params": "PARAMS",
    "private": "PRIVATE",
    "protected": "PROTECTED",
    "public": "PUBLIC",
    "readonly": "READONLY",
    "ref": "REF",
    "return": "RETURN",
    "sbyte": "SBYTE",
    "sealed": "SEALED",
    "short": "SHORT",
    "sizeof": "SIZEOF",
    "stackalloc": "STACKALLOC",
    "static": "STATIC",
    "string": "STRING_TYPE",
    "struct": "STRUCT",
    "switch": "SWITCH",
    "this": "THIS",
    "throw": "THROW",
    "true": "TRUE",
    "try": "TRY",
    "typeof": "TYPEOF",
    "uint": "UINT",
    "ulong": "ULONG",
    "unchecked": "UNCHECKED",
    "unsafe": "UNSAFE",
    "ushort": "USHORT",
    "using": "USING",
    "virtual": "VIRTUAL",
    "void": "VOID",
    "volatile": "VOLATILE",
    "while": "WHILE",
    # Contextual keywords
    "add": "ADD",
    "alias": "ALIAS",
    "ascending": "ASCENDING",
    "async": "ASYNC",
    "await": "AWAIT",
    "by": "BY",
    "capacity": "CAPACITY",
    "clear": "CLEAR",
    "contains": "CONTAINS",
    "Count": "COUNT",
    "descending": "DESCENDING",
    "dynamic": "DYNAMIC",
    "equals": "EQUALS",
    "from": "FROM",
    "get": "GET",
    "global": "GLOBAL",
    "group": "GROUP",
    "indexof": "INDEXOF",
    "insert": "INSERT",
    "into": "INTO",
    "join": "JOIN",
    "let": "LET",
    "nameof": "NAMEOF",
    "notnull": "NOTNULL",
    "on": "ON",
    "orderby": "ORDERBY",
    "partial": "PARTIAL",
    "remove": "REMOVE",
    "removeat": "REMOVEAT",
    "select": "SELECT",
    "set": "SET",
    "unmanaged": "UNMANAGED",
    "value": "VALUE",
    "var": "VAR",
    "when": "WHEN",
    "where": "WHERE",
    "yield": "YIELD",
    # Special identifiers
    "Console": "CONSOLE",
    "WriteLine": "WRITELINE",
    "ReadLine": "READLINE",
    "Convert": "CONVERT",
    "ToInt32": "TOINT32",
    "Write": "WRITE",
    # Data structures
    "List": "LIST",
    "Dictionary": "DICTIONARY",
}
#-------------------------------------------------------------
tokens = [
    # Identifiers and literals
    "IDENTIFIER",
    "CLASS_NAME",
    "INTEGER",
    "FLOAT",
    "STRING",
    "CHAR_LITERAL",
    # Operators and punctuators
    "ASSIGN",
    "OPEN_PAREN",
    "CLOSE_PAREN",
    "OPEN_BRACE",
    "CLOSE_BRACE",
    "OPEN_BRACKET",
    "CLOSE_BRACKET",
    "SEMICOLON",
    "DOT",
    "COMMA",
    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "PERCENT",
    "AMPERSAND",
    "PIPE",
    "CARET",
    "BANG",
    "TILDE",
    "QUESTION",
    "COLON",
    "DOUBLE_QUESTION",
    "DOUBLE_COLON",
    "INCREMENT",
    "DECREMENT",
    "DOUBLE_AMPERSAND",
    "DOUBLE_PIPE",
    "ARROW",
    "LAMBDA_ARROW",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "MULTIPLY_ASSIGN",
    "DIVIDE_ASSIGN",
    "PERCENT_ASSIGN",
    "AMPERSAND_ASSIGN",
    "PIPE_ASSIGN",
    "CARET_ASSIGN",
    "LEFT_SHIFT",
    "RIGHT_SHIFT",
    "LEFT_SHIFT_ASSIGN",
    "RIGHT_SHIFT_ASSIGN",
    "EQUAL",
    "NOT_EQUAL",
    "LESS_THAN",
    "GREATER_THAN",
    "LESS_THAN_EQUAL",
    "GREATER_THAN_EQUAL",
    # Special tokens
    "NULLABLE_OPERATOR",
    "VERBATIM_STRING",
] + list(reserved.values())

# Simple tokens
t_ASSIGN = r"="
t_OPEN_PAREN = r"\("
t_CLOSE_PAREN = r"\)"
t_OPEN_BRACE = r"\{"
t_CLOSE_BRACE = r"\}"
t_OPEN_BRACKET = r"\["
t_CLOSE_BRACKET = r"\]"
t_SEMICOLON = r";"
t_DOT = r"\."
t_COMMA = r","
t_PLUS = r"\+"
t_MINUS = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_PERCENT = r"%"
t_AMPERSAND = r"&"
t_PIPE = r"\|"
t_CARET = r"\^"
t_BANG = r"!"
t_TILDE = r"~"
t_QUESTION = r"\?"
t_COLON = r":"

# Complex tokens (longest patterns first)
t_DOUBLE_QUESTION = r"\?\?"
t_DOUBLE_COLON = r"::"
t_INCREMENT = r"\+\+"
t_DECREMENT = r"--"
t_DOUBLE_AMPERSAND = r"&&"
t_DOUBLE_PIPE = r"\|\|"
t_ARROW = r"->"
t_LAMBDA_ARROW = r"=>"
t_PLUS_ASSIGN = r"\+="
t_MINUS_ASSIGN = r"-="
t_MULTIPLY_ASSIGN = r"\*="
t_DIVIDE_ASSIGN = r"/="
t_PERCENT_ASSIGN = r"%="
t_AMPERSAND_ASSIGN = r"&="
t_PIPE_ASSIGN = r"\|="
t_CARET_ASSIGN = r"\^="
t_LEFT_SHIFT_ASSIGN = r"<<="
t_RIGHT_SHIFT_ASSIGN = r">>="
t_LEFT_SHIFT = r"<<"
t_RIGHT_SHIFT = r">>"
t_EQUAL = r"=="
t_NOT_EQUAL = r"!="
t_LESS_THAN_EQUAL = r"<="
t_GREATER_THAN_EQUAL = r">="
t_LESS_THAN = r"<"
t_GREATER_THAN = r">"
t_NULLABLE_OPERATOR = r"\?"  # Already defined as t_QUESTION, but kept for clarity

# Ignore whitespace and tabs
t_ignore = " \t"


# Verbatim string
def t_VERBATIM_STRING(t):
    r'@"([^"]|"")*"'
    t.value = t.value[2:-1].replace('""', '"')  # Remove @"" and handle escaped quotes
    return t


# Regular string
def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\" "
    t.value = bytes(t.value[1:-1], "utf-8").decode(
        "unicode_escape"
    )  # Handle escape sequences
    return t


# Character literal
def t_CHAR_LITERAL(t):
    r"\'([^\\\n]|(\\.))*?\'"
    t.value = t.value[1:-1]
    return t


# Class names (must start with uppercase)
def t_CLASS_NAME(t):
    r"[A-Z][a-zA-Z_0-9]*"
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = "IDENTIFIER"  # <- Lo marcamos como IDENTIFIER si no está reservado
    return t


# Identifiers
def t_IDENTIFIER(t):
    r"[a-z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


# Floating point numbers with exponent support
def t_FLOAT(t):
    r"(\d+\.\d*|\.\d+)([eE][-+]?\d+)?[fFdDmM]?|\d+[eE][-+]?\d+[fFdDmM]?|\d+[fFdDmM]"
    # Remove type suffix for value conversion
    if t.value[-1] in "fFdDmM":
        value_str = t.value[:-1]
    else:
        value_str = t.value

    try:
        t.value = float(value_str)
    except ValueError:
        print(f"Float conversion error: {t.value}")
        t.value = 0.0
    return t


# Integer literals with support for hex/binary
def t_INTEGER(t):
    r"0[xX][0-9a-fA-F_]+|0[bB][01_]+|\d+"
    if t.value.startswith(("0x", "0X")):
        # Hexadecimal
        t.value = int(t.value[2:].replace("_", ""), 16)
    elif t.value.startswith(("0b", "0B")):
        # Binary
        t.value = int(t.value[2:].replace("_", ""), 2)
    else:
        # Decimal
        t.value = int(t.value.replace("_", ""))
    return t


# Comments
def t_COMMENT(t):
    r"//.*|/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")  # Update line count
    pass  # Ignore comments


# Newline handling
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling
error_log = []


def t_error(t):
    msg = f"[ERROR] Illegal character '{t.value[0]}' at line {t.lineno}\n"
    error_log.append(msg)
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def run_lexical_analysis(file_path, user_git_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/lexico-{user_git_name}-{timestamp}.txt"

    # Extraer el nombre real del archivo desde el path proporcionado
    real_file_name = os.path.basename(file_path)

    # Si es un archivo temporal pero sabemos el nombre original
    original_file_name = None
    if real_file_name == "temp_analysis.cs" and hasattr(run_lexical_analysis, "original_file"):
        original_file_name = run_lexical_analysis.original_file

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Reiniciar el número de línea del lexer antes de cada análisis
    lexer.lineno = 1
    lexer.input(source_code)

    # Recolectar todos los tokens para el análisis
    token_list = []
    while True:
        token = lexer.token()
        if not token:
            break
        token_list.append(token)

    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(
            f"Lexical Analysis Log\nUser: {user_git_name}\n"
            f"File: {original_file_name or real_file_name}\n"
            f"Date: {timestamp}\n\n"
        )
        log_file.write("=== TOKENS ===\n")

        for token in token_list:
            log_file.write(
                f"{token.type:<17} {repr(token.value):<30} (line {token.lineno})\n"
            )

        if error_log:
            log_file.write("\n=== ERRORS ===\n")
            for err in error_log:
                log_file.write(err)
        else:
            log_file.write("\nNo lexical errors detected.\n")

    print(f"\n✔ Analysis complete. Log saved to {log_filename}\n")


# ========== Main Menu ==========
if __name__ == "__main__":
    algorithms = {
        "1": {
            "name": "algoritmo1.cs",
            "path": "algoritmos/algoritmo1.cs",
            "user": "DavidlunaT",
        },
        "2": {
            "name": "algoritmo2.cs",
            "path": "algoritmos/algoritmo2.cs",
            "user": "waldaara",
        },
        "3": {
            "name": "algoritmo3.cs",
            "path": "algoritmos/algoritmo3.cs",
            "user": "gabsjimz",
        },
        "4": {
            "name": "test_listas.cs",
            "path": "algoritmos/test_listas.cs",
            "user": "test",
        },
    }

    print("Select algorithm to analyze:")
    for key, data in algorithms.items():
        print(f"{key}. {data['name']} (Git: {data['user']})")

    choice = input("Enter choice: ").strip()

    if choice in algorithms:
        error_log.clear()
        selected = algorithms[choice]
        run_lexical_analysis(file_path=selected["path"], user_git_name=selected["user"])
    else:
        print("❌ Invalid option.")
