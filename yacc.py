import ply.yacc as yacc
import datetime
import os

# Get the token map from the lexer.  This is required.
from lex import tokens

# ========== REGLAS SINTÁCTICAS BÁSICAS ==========


# Start symbol - programa principal
def p_program(p):
    """program : statement_list
    | empty"""
    p[0] = ("program", p[1] if p[1] else [])


def p_empty(p):
    "empty :"
    pass


def p_expression_plus(p):
    "expression : expression PLUS term"
    # Handle string concatenation or numeric addition
    try:
        p[0] = p[1] + p[3]
    except TypeError:
        p[0] = str(p[1]) + str(p[3])


def p_expression_minus(p):
    "expression : expression MINUS term"
    # Only handle numeric subtraction
    try:
        p[0] = p[1] - p[3]
    except (TypeError, ValueError):
        p[0] = ("minus", p[1], p[3])


def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


def p_expression_identifier(p):
    "expression : IDENTIFIER"
    p[0] = p[1]


def p_expression_function_call(p):
    "expression : function_call"
    p[0] = p[1]


def p_term_times(p):
    "term : term MULTIPLY factor"
    try:
        p[0] = p[1] * p[3]
    except (TypeError, ValueError):
        p[0] = ("multiply", p[1], p[3])


def p_term_div(p):
    "term : term DIVIDE factor"
    try:
        p[0] = p[1] / p[3]
    except (TypeError, ValueError, ZeroDivisionError):
        p[0] = ("divide", p[1], p[3])


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_int(p):
    "factor : INTEGER"
    p[0] = p[1]


def p_factor_float(p):
    "factor : FLOAT"
    p[0] = p[1]


def p_factor_string(p):
    "factor : STRING"
    p[0] = p[1]


def p_factor_identifier(p):
    "factor : IDENTIFIER"
    p[0] = p[1]


def p_factor_expr(p):
    "factor : OPEN_PAREN expression CLOSE_PAREN"
    p[0] = p[2]


# ========== REGLAS COMUNES ==========


# Using statements - Fixed to handle System
def p_using_statement(p):
    """using_statement : USING IDENTIFIER SEMICOLON
    | USING CLASS_NAME SEMICOLON"""
    p[0] = ("using", p[2])


# Function calls
def p_function_call(p):
    """function_call : IDENTIFIER OPEN_PAREN CLOSE_PAREN
    | IDENTIFIER OPEN_PAREN argument_list CLOSE_PAREN
    | CLASS_NAME OPEN_PAREN CLOSE_PAREN
    | CLASS_NAME OPEN_PAREN argument_list CLOSE_PAREN"""
    if len(p) == 4:
        p[0] = ("function_call", p[1], [])
    else:
        p[0] = ("function_call", p[1], p[3])


def p_function_call_statement(p):
    "function_call_statement : function_call SEMICOLON"
    p[0] = ("call_stmt", p[1])


def p_argument_list(p):
    """argument_list : expression
    | argument_list COMMA expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Impresión (Console.WriteLine)
def p_print_statement(p):
    """print_statement : CONSOLE DOT WRITELINE OPEN_PAREN expression CLOSE_PAREN SEMICOLON
    | CONSOLE DOT WRITE OPEN_PAREN expression CLOSE_PAREN SEMICOLON"""
    p[0] = ("print", p[5])


# Ingreso de datos por teclado
def p_input_statement(p):
    "input_statement : CONSOLE DOT READLINE OPEN_PAREN CLOSE_PAREN"
    p[0] = ("input",)


# Convert.ToInt32
def p_convert_statement(p):
    "convert_statement : CONVERT DOT TOINT32 OPEN_PAREN expression CLOSE_PAREN"
    p[0] = ("convert_int", p[5])


# Asignación de variables - Enhanced to support multiple declarations
def p_assignment(p):
    """assignment : IDENTIFIER ASSIGN expression SEMICOLON
    | IDENTIFIER ASSIGN convert_statement SEMICOLON
    | INT_TYPE IDENTIFIER ASSIGN expression SEMICOLON
    | INT_TYPE IDENTIFIER ASSIGN convert_statement SEMICOLON
    | INT_TYPE multiple_var_declaration SEMICOLON
    | FLOAT_TYPE IDENTIFIER ASSIGN expression SEMICOLON
    | STRING_TYPE IDENTIFIER ASSIGN expression SEMICOLON
    | STRING_TYPE IDENTIFIER ASSIGN input_statement SEMICOLON
    | BOOL_TYPE IDENTIFIER ASSIGN expression SEMICOLON"""
    if len(p) == 5:
        p[0] = ("assign", p[1], p[3])
    elif len(p) == 4 and p[2] != "ASSIGN":  # multiple declarations
        p[0] = ("multiple_decl", p[1], p[2])
    else:
        p[0] = ("declare_assign", p[1], p[2], p[4])


def p_multiple_var_declaration(p):
    """multiple_var_declaration : IDENTIFIER ASSIGN expression COMMA IDENTIFIER ASSIGN expression
    | multiple_var_declaration COMMA IDENTIFIER ASSIGN expression"""
    if len(p) == 8:  # first case: a = 0, b = 1
        p[0] = [("var_assign", p[1], p[3]), ("var_assign", p[5], p[7])]
    else:  # continuation: ..., c = 2
        p[0] = p[1] + [("var_assign", p[3], p[5])]


# Condiciones con conectores lógicos
def p_condition(p):
    """condition : expression EQUAL expression
    | expression NOT_EQUAL expression
    | expression LESS_THAN expression
    | expression GREATER_THAN expression
    | expression LESS_THAN_EQUAL expression
    | expression GREATER_THAN_EQUAL expression
    | expression EQUAL STRING
    | STRING EQUAL expression"""
    p[0] = ("condition", p[2], p[1], p[3])


def p_logical_condition(p):
    """logical_condition : condition
    | condition DOUBLE_AMPERSAND condition
    | condition DOUBLE_PIPE condition"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("logical", p[2], p[1], p[3])


# ========== SECCIÓN DavidlunaT ==========
# Responsable de: Arreglos, If-Else, Función básica


# Estructura de datos: Arreglos
def p_array_declaration(p):
    """array_declaration : INT_TYPE OPEN_BRACKET CLOSE_BRACKET IDENTIFIER ASSIGN NEW INT_TYPE OPEN_BRACKET INTEGER CLOSE_BRACKET SEMICOLON
    | STRING_TYPE OPEN_BRACKET CLOSE_BRACKET IDENTIFIER ASSIGN NEW STRING_TYPE OPEN_BRACKET INTEGER CLOSE_BRACKET SEMICOLON
    """
    p[0] = ("array_decl", p[1], p[4], p[9])


def p_array_access(p):
    "array_access : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET"
    p[0] = ("array_access", p[1], p[3])


def p_array_assignment(p):
    "array_assignment : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET ASSIGN expression SEMICOLON"
    p[0] = ("array_assign", p[1], p[3], p[6])


# Estructura de control: If-Else
def p_if_statement(p):
    """if_statement : IF OPEN_PAREN logical_condition CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | IF OPEN_PAREN logical_condition CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE ELSE IF OPEN_PAREN logical_condition CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | IF OPEN_PAREN logical_condition CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE ELSE OPEN_BRACE statement_list CLOSE_BRACE
    """
    if len(p) == 8:
        p[0] = ("if", p[3], p[6])
    elif len(p) == 16:
        p[0] = ("if_elif", p[3], p[6], p[11], p[14])
    else:
        p[0] = ("if_else", p[3], p[6], p[10])


# Función básica
def p_basic_function(p):
    "basic_function : VOID IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE"
    p[0] = ("function", p[2], [], p[6])


# ========== SECCIÓN waldaara ==========
# Responsable de: Listas, While, Función con parámetros


# Estructura de datos: Listas (List<T>) - FIXED
def p_list_declaration(p):
    """list_declaration : LIST LESS_THAN INT_TYPE GREATER_THAN IDENTIFIER ASSIGN NEW LIST LESS_THAN INT_TYPE GREATER_THAN OPEN_PAREN CLOSE_PAREN SEMICOLON
    | LIST LESS_THAN STRING_TYPE GREATER_THAN IDENTIFIER ASSIGN NEW LIST LESS_THAN STRING_TYPE GREATER_THAN OPEN_PAREN CLOSE_PAREN SEMICOLON
    """
    p[0] = ("list_decl", p[3], p[5])


def p_list_add(p):
    "list_add : IDENTIFIER DOT ADD OPEN_PAREN expression CLOSE_PAREN SEMICOLON"
    p[0] = ("list_add", p[1], p[5])


# Estructura de control: While
def p_while_statement(p):
    "while_statement : WHILE OPEN_PAREN logical_condition CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE"
    p[0] = ("while", p[3], p[6])


# Estructura de control: For (AÑADIDO para algoritmo2.cs)
def p_for_statement(p):
    "for_statement : FOR OPEN_PAREN for_init SEMICOLON logical_condition SEMICOLON for_update CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE"
    p[0] = ("for", p[3], p[5], p[7], p[10])


def p_for_init(p):
    """for_init : INT_TYPE IDENTIFIER ASSIGN expression
    | assignment_no_semicolon"""
    if len(p) == 5:
        p[0] = ("for_init", p[1], p[2], p[4])
    else:
        p[0] = p[1]


def p_assignment_no_semicolon(p):
    "assignment_no_semicolon : IDENTIFIER ASSIGN expression"
    p[0] = ("assign", p[1], p[3])


def p_for_update(p):
    """for_update : IDENTIFIER INCREMENT
    | IDENTIFIER DECREMENT
    | INCREMENT IDENTIFIER
    | DECREMENT IDENTIFIER"""
    if p[2] in ("++", "--"):
        p[0] = ("post_op", p[1], p[2])
    else:
        p[0] = ("pre_op", p[2], p[1])


# Función con parámetros
def p_param_function(p):
    """param_function : VOID IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | INT_TYPE IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    """
    p[0] = ("function_params", p[1], p[2], p[4], p[7])


def p_parameter_list(p):
    """parameter_list : parameter
    | parameter_list COMMA parameter"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    """parameter : INT_TYPE IDENTIFIER
    | STRING_TYPE IDENTIFIER
    | FLOAT_TYPE IDENTIFIER"""
    p[0] = ("param", p[1], p[2])


# ========== SECCIÓN gabsjimz ==========
# Responsable de: Diccionarios, Switch, Función con retorno


# Estructura de datos: Diccionarios (Dictionary<TKey, TValue>) - FIXED
def p_dictionary_declaration(p):
    """dictionary_declaration : DICTIONARY LESS_THAN STRING_TYPE COMMA INT_TYPE GREATER_THAN IDENTIFIER ASSIGN NEW DICTIONARY LESS_THAN STRING_TYPE COMMA INT_TYPE GREATER_THAN OPEN_PAREN CLOSE_PAREN SEMICOLON
    | DICTIONARY LESS_THAN INT_TYPE COMMA STRING_TYPE GREATER_THAN IDENTIFIER ASSIGN NEW DICTIONARY LESS_THAN INT_TYPE COMMA STRING_TYPE GREATER_THAN OPEN_PAREN CLOSE_PAREN SEMICOLON
    """
    p[0] = ("dict_decl", p[3], p[5], p[7])


def p_dictionary_access(p):
    "dictionary_access : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET"
    p[0] = ("dict_access", p[1], p[3])


# Switch with different name to avoid conflict
def p_dict_assignment(p):
    "dict_assignment : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET ASSIGN expression SEMICOLON"
    p[0] = ("dict_assign", p[1], p[3], p[6])


# Estructura de control: Switch
def p_switch_statement(p):
    "switch_statement : SWITCH OPEN_PAREN expression CLOSE_PAREN OPEN_BRACE case_list CLOSE_BRACE"
    p[0] = ("switch", p[3], p[6])


def p_case_list(p):
    """case_list : case_statement
    | case_list case_statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_case_statement(p):
    """case_statement : CASE expression COLON statement_list BREAK SEMICOLON
    | DEFAULT COLON statement_list BREAK SEMICOLON"""
    if len(p) == 7:
        p[0] = ("case", p[2], p[4])
    else:
        p[0] = ("default", p[3])


# Función con retorno
def p_return_function(p):
    """return_function : INT_TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list RETURN expression SEMICOLON CLOSE_BRACE
    | STRING_TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list RETURN expression SEMICOLON CLOSE_BRACE
    | FLOAT_TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list RETURN expression SEMICOLON CLOSE_BRACE
    """
    p[0] = ("return_function", p[1], p[2], p[6], p[8])


def p_return_statement(p):
    "return_statement : RETURN SEMICOLON"
    p[0] = ("return_void",)

def p_expression_array_access(p):
    "expression : expression OPEN_BRACKET expression CLOSE_BRACKET"
    p[0] = ("array_access", p[1], p[3])

def p_expression_dot(p):
    "expression : expression DOT IDENTIFIER"
    p[0] = ("dot_access", p[1], p[3])

def p_array_declaration_with_values(p):
    """array_declaration : INT_TYPE OPEN_BRACKET CLOSE_BRACKET IDENTIFIER ASSIGN expression SEMICOLON"""
    p[0] = ("array_decl_values", p[1], p[4], p[6])


def p_value_list(p):
    """value_list : expression
    | value_list COMMA expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression_new_array_with_values(p):
    """expression : NEW INT_TYPE OPEN_BRACKET CLOSE_BRACKET OPEN_BRACE value_list CLOSE_BRACE"""
    p[0] = ("new_array_init", p[2], p[6])


# ========== REGLAS ADICIONALES ==========


# Static methods - AÑADIDO para algoritmo2.cs
def p_static_method(p):
    """static_method : STATIC VOID IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID CLASS_NAME OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID CLASS_NAME OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC INT_TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC INT_TYPE IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC INT_TYPE CLASS_NAME OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC INT_TYPE CLASS_NAME OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    """
    if len(p) == 9:  # no parameters
        p[0] = ("static_method", p[2], p[3], [], p[7])
    else:  # with parameters
        p[0] = ("static_method", p[2], p[3], p[5], p[8])


# Main method
def p_main_method(p):
    """main_method : STATIC VOID IDENTIFIER OPEN_PAREN STRING_TYPE OPEN_BRACKET CLOSE_BRACKET IDENTIFIER CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID CLASS_NAME OPEN_PAREN STRING_TYPE OPEN_BRACKET CLOSE_BRACKET IDENTIFIER CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC VOID CLASS_NAME OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    """
    if len(p) == 13:
        p[0] = ("main_method", p[3], p[8], p[11])
    elif len(p) == 8:
        p[0] = ("main_method", p[3], [], p[7])
    else:
        p[0] = ("main_method", p[3], [], p[6])


# Definición de clases
def p_class_definition(p):
    """class_definition : CLASS CLASS_NAME OPEN_BRACE class_body CLOSE_BRACE
    | CLASS IDENTIFIER OPEN_BRACE class_body CLOSE_BRACE
    | PUBLIC CLASS CLASS_NAME OPEN_BRACE class_body CLOSE_BRACE"""
    if len(p) == 6:
        p[0] = ("class", p[2], p[4])
    else:
        p[0] = ("public_class", p[3], p[5])


def p_class_body(p):
    """class_body : class_member
    | class_body class_member"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_class_member(p):
    """class_member : property_definition
    | method_definition
    | main_method
    | static_method"""
    p[0] = p[1]


# Propiedades
def p_property_definition(p):
    """property_definition : PUBLIC INT_TYPE IDENTIFIER OPEN_BRACE GET SEMICOLON SET SEMICOLON CLOSE_BRACE
    | PUBLIC STRING_TYPE IDENTIFIER OPEN_BRACE GET SEMICOLON SET SEMICOLON CLOSE_BRACE
    """
    p[0] = ("property", p[2], p[3])


# Métodos
def p_method_definition(p):
    """method_definition : PUBLIC VOID IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | PUBLIC INT_TYPE IDENTIFIER OPEN_PAREN CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    """
    p[0] = ("method", p[2], p[3], p[7])


# Lista de statements
def p_statement_list(p):
    """statement_list : statement
    | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : assignment
    | print_statement
    | array_declaration
    | if_statement
    | while_statement
    | for_statement
    | switch_statement
    | array_assignment
    | list_declaration
    | list_add
    | dictionary_declaration
    | dict_assignment
    | class_definition
    | basic_function
    | param_function
    | return_function
    | return_statement
    | using_statement
    | function_call_statement"""
    p[0] = p[1]


# Error rule for syntax errors
error_log = []


def p_error(p):
    if p:
        msg = (
            f"[ERROR] Syntax error at token {p.type} ('{p.value}') at line {p.lineno}\n"
        )
    else:
        msg = "[ERROR] Syntax error at EOF\n"
    error_log.append(msg)
    print(msg.strip())


# Build the parser
parser = yacc.yacc()


def run_syntactic_analysis(file_path, user_git_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/sintactico-{user_git_name}-{timestamp}.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Clear previous errors
    error_log.clear()

    # Parse the code
    result = parser.parse(source_code)

    # Write log
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(
            f"Syntactic Analysis Log\nUser: {user_git_name}\nFile: {file_path}\nDate: {timestamp}\n\n"
        )

        if error_log:
            log_file.write("=== SYNTACTIC ERRORS ===\n")
            for err in error_log:
                log_file.write(err)
        else:
            log_file.write("No syntactic errors detected.\n")
            log_file.write(f"Parse result: {result}\n")

        # Add parser.out content if it exists
        if os.path.exists("parser.out"):
            log_file.write("\n=== PARSER DEBUG INFO ===\n")
            try:
                with open("parser.out", "r", encoding="utf-8") as parser_file:
                    log_file.write(parser_file.read())
            except Exception as e:
                log_file.write(f"Error reading parser.out: {e}\n")

    print(f"\n✔ Syntactic analysis complete. Log saved to {log_filename}\n")
    return result


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
    }

    print("Select algorithm to analyze syntactically:")
    for key, data in algorithms.items():
        print(f"{key}. {data['name']} (Git: {data['user']})")

    choice = input("Enter choice: ").strip()

    if choice in algorithms:
        selected = algorithms[choice]
        run_syntactic_analysis(
            file_path=selected["path"], user_git_name=selected["user"]
        )
    else:
        print("❌ Invalid option.")
