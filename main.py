import ply.lex as lex
import datetime
import os


reserved = {
    #incio DavidlunaT{
    'using': 'USING',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'int': 'INT_TYPE',
    'string': 'STRING_TYPE',
    'bool': 'BOOL_TYPE',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN',
    'Console': 'CONSOLE',
    'WriteLine': 'WRITELINE',
    'ReadLine': 'READLINE',
    'Convert': 'CONVERT',
    'ToInt32': 'TOINT32',
    #}fin DavidlunaT
    #inicio waldaara {
    'Write': "WRITE",
    "for": "FOR",
    #}fin waldaara
}

tokens = [
    #incio DavidlunaT {
    'IDENTIFIER',
    'INTEGER',
    'OPERATOR',
    'ASSIGN',
    'OPEN_PAREN',
    'CLOSE_PAREN',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'SEMICOLON',
    'STRING',
    'DOT',
    # }fin DavidlunaT
    #inicio waldaara {
    'COMMA',
    #}fin waldaara
] + list(reserved.values())

#inicio waldaara{
# preguntar si esto es necesario en lugar de t_OPERATOR
# literals = ['+', '-', '*', '/', '=', '<', '>', '!', ';', ',', '.', '(', ')', '{', '}', '[', ']']
#}fin waldaara

#incio DavidlunaT{
t_OPERATOR = r'[\+\-\*/=<>!]=?|==|!='
t_ASSIGN = r'='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_ignore = ' \t'
#}fin DavidlunaT
#inicio waldaara{
t_COMMA = r','
#}fin waldaara

#incio DavidlunaT{
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

error_log = []

def t_error(t):
    msg = f"[ERROR] Illegal character '{t.value[0]}' at line {t.lineno}\n"
    error_log.append(msg)
    t.lexer.skip(1)

#} fin DavidlunaT

#inicio waldaara{
def t_COMMENT(t):
    r'//.*\n'
    pass  # Ignore single-line comments
#} fin waldaara

lexer = lex.lex()

#funcion que ejecuta el analizador lexico y guarda el log con el nombre respectivogit 
def run_lexical_analysis(file_path, user_git_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/lexico-{user_git_name}-{timestamp}.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    lexer.input(source_code)

    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"Lexical Analysis Log\nUser: {user_git_name}\nFile: {file_path}\nDate: {timestamp}\n\n")
        log_file.write("=== TOKENS ===\n")

        for token in lexer:
            log_file.write(f"{token.type:<17} {repr(token.value):<30} (line {token.lineno})\n")

        if error_log:
            log_file.write("\n=== ERRORS ===\n")
            for err in error_log:
                log_file.write(err)
        else:
            log_file.write("\nNo lexical errors detected.\n")

    print(f"\n✔ Analysis complete. Log saved to {log_filename}\n")

# ========== Main Menu ==========
if __name__ == "__main__":
    #incio DavidlunaT{
    algorithms = {
        "1": {
            "name": "algoritmo1.cs",
            "path": "algoritmos/algoritmo1.cs",
            "user": "DavidlunaT"
        }
        #}fin DavidlunaT
        #inicio waldaara{
        , "2": {
            "name": "algoritmo2.cs",
            "path": "algoritmos/algoritmo2.cs",
            "user": "waldaara"
        }
        #}fin waldaara
        #inicio gabsjimz{
        , "3": {
            "name": "algoritmo3.cs",
            "path": "algoritmos/algoritmo3.cs",
            "user": "gabsjimz"
        }
        #}fin gabsjimz
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
    
