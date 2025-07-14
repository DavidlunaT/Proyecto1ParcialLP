import ply.yacc as yacc
import datetime
import os
from lex import tokens, lexer

# ========== ANÁLISIS SINTÁCTICO ==========

# Variables globales para control de errores
syntax_errors = []
semantic_errors = []
symbol_table = {}
current_scope = "global"
undeclared_vars_reported = set()

# ========== REGLAS GRAMATICALES: PROGRAMA PRINCIPAL ==========


def p_program(p):
    """program : using_statements class_declarations"""
    p[0] = ("program", p[1], p[2])


def p_using_statements(p):
    """using_statements : using_statements using_statement
    | using_statement
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]]


def p_using_statement(p):
    """using_statement : USING IDENTIFIER SEMICOLON
    | USING IDENTIFIER DOT IDENTIFIER SEMICOLON"""
    if len(p) == 4:
        p[0] = ("using", p[2])
    else:
        p[0] = ("using", f"{p[2]}.{p[4]}")


# ========== REGLAS GRAMATICALES: DEFINICIÓN DE CLASES ==========


def p_class_declarations(p):
    """class_declarations : class_declarations class_declaration
    | class_declaration"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_class_declaration(p):
    """class_declaration : access_modifier CLASS IDENTIFIER OPEN_BRACE class_body CLOSE_BRACE
    | CLASS IDENTIFIER OPEN_BRACE class_body CLOSE_BRACE"""
    if len(p) == 7:
        p[0] = ("class", p[1], p[3], p[5])
    else:
        p[0] = ("class", "internal", p[2], p[4])


def p_access_modifier(p):
    """access_modifier : PUBLIC
    | PRIVATE
    | PROTECTED
    | INTERNAL"""
    p[0] = p[1]


def p_class_body(p):
    """class_body : class_body class_member
    | class_member
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]]


def p_class_member(p):
    """class_member : field_declaration
    | method_declaration
    | property_declaration"""
    p[0] = p[1]


# ========== REGLAS GRAMATICALES: PROPIEDADES ==========


def p_property_declaration(p):
    """property_declaration : access_modifier type_specifier IDENTIFIER OPEN_BRACE property_accessors CLOSE_BRACE"""
    p[0] = ("property", p[1], p[2], p[3], p[5])


def p_property_accessors(p):
    """property_accessors : GET SEMICOLON SET SEMICOLON
    | GET SEMICOLON
    | SET SEMICOLON"""
    if len(p) == 5:
        p[0] = ("get_set",)
    elif p[1] == "get":
        p[0] = ("get_only",)
    else:
        p[0] = ("set_only",)


# ========== REGLAS GRAMATICALES: CAMPOS ==========


def p_field_declaration(p):
    """field_declaration : access_modifier type_specifier IDENTIFIER SEMICOLON
    | access_modifier type_specifier IDENTIFIER ASSIGN expression SEMICOLON
    | type_specifier IDENTIFIER SEMICOLON
    | type_specifier IDENTIFIER ASSIGN expression SEMICOLON"""
    if len(p) == 5:
        if p[1] in ["public", "private", "protected", "internal"]:
            p[0] = ("field", p[1], p[2], p[3], None)
        else:
            p[0] = ("field", "private", p[1], p[2], None)
    elif len(p) == 7:
        if p[1] in ["public", "private", "protected", "internal"]:
            p[0] = ("field", p[1], p[2], p[3], p[5])
        else:
            p[0] = ("field", "private", p[1], p[2], p[4])


# ========== REGLAS GRAMATICALES: MÉTODOS Y FUNCIONES ==========


def p_method_declaration(p):
    """method_declaration : access_modifier STATIC type_specifier IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | access_modifier type_specifier IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    | STATIC type_specifier IDENTIFIER OPEN_PAREN parameter_list CLOSE_PAREN OPEN_BRACE statement_list CLOSE_BRACE
    """
    if len(p) == 11:
        p[0] = ("method", p[1], True, p[3], p[4], p[6], p[9])
    elif len(p) == 10 and p[1] == "static":
        p[0] = ("method", "internal", True, p[2], p[3], p[5], p[8])
    else:
        p[0] = ("method", p[1], False, p[2], p[3], p[5], p[8])


def p_parameter_list(p):
    """parameter_list : parameter_list COMMA parameter
    | parameter
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    """parameter : type_specifier IDENTIFIER"""
    p[0] = ("parameter", p[1], p[2])


# ========== REGLAS GRAMATICALES: TIPOS DE DATOS ==========


def p_type_specifier(p):
    """type_specifier : INT_TYPE
    | FLOAT_TYPE
    | DOUBLE
    | STRING_TYPE
    | BOOL_TYPE
    | CHAR
    | VOID
    | IDENTIFIER
    | array_type
    | generic_type"""
    p[0] = p[1]


def p_array_type(p):
    """array_type : type_specifier OPEN_BRACKET CLOSE_BRACKET"""
    p[0] = ("array_type", p[1])


def p_generic_type(p):
    """generic_type : LIST LESS_THAN type_specifier GREATER_THAN
    | DICTIONARY LESS_THAN type_specifier COMMA type_specifier GREATER_THAN"""
    if len(p) == 5:
        p[0] = ("list_type", p[3])
    else:
        p[0] = ("dictionary_type", p[3], p[5])


# ========== REGLAS GRAMATICALES: DECLARACIONES Y SENTENCIAS ==========


def p_statement_list(p):
    """statement_list : statement_list statement
    | statement
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : expression_statement
    | declaration_statement
    | assignment_statement
    | if_statement
    | while_statement
    | for_statement
    | foreach_statement
    | return_statement
    | block_statement
    | print_statement
    | input_statement"""
    p[0] = p[1]


def p_block_statement(p):
    """block_statement : OPEN_BRACE statement_list CLOSE_BRACE"""
    p[0] = ("block", p[2])


def p_expression_statement(p):
    """expression_statement : expression SEMICOLON"""
    p[0] = ("expression_stmt", p[1])


# ========== REGLAS GRAMATICALES: ASIGNACIÓN DE VARIABLES ==========



def p_declaration_statement(p):
    """declaration_statement : type_specifier variable_declarator_list SEMICOLON
    | VAR IDENTIFIER ASSIGN expression SEMICOLON"""
    if len(p) == 6 and p[1] == "var":
        p[0] = ("var_declaration", p[2], p[4])
    else:
        p[0] = ("multi_declaration", p[1], p[2])


def p_variable_declarator_list(p):
    """variable_declarator_list : variable_declarator_list COMMA variable_declarator
    | variable_declarator"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_variable_declarator(p):
    """variable_declarator : IDENTIFIER
    | IDENTIFIER ASSIGN expression"""
    if len(p) == 2:
        p[0] = ("declarator", p[1], None)
    else:
        p[0] = ("declarator", p[1], p[3])


def p_assignment_statement(p):
    """assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON
    | IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET ASSIGN expression SEMICOLON
    | IDENTIFIER DOT IDENTIFIER ASSIGN expression SEMICOLON"""
    if len(p) == 5:
        p[0] = ("assignment", p[1], p[3])
    elif len(p) == 8:
        p[0] = ("array_assignment", p[1], p[3], p[6])
    else:
        p[0] = ("member_assignment", p[1], p[3], p[5])


# ========== REGLAS GRAMATICALES: ESTRUCTURAS DE CONTROL ==========


def p_if_statement(p):
    """if_statement : IF OPEN_PAREN expression CLOSE_PAREN statement
    | IF OPEN_PAREN expression CLOSE_PAREN statement ELSE statement"""
    if len(p) == 6:
        p[0] = ("if", p[3], p[5], None)
    else:
        p[0] = ("if", p[3], p[5], p[7])


def p_while_statement(p):
    """while_statement : WHILE OPEN_PAREN boolean_expression CLOSE_PAREN statement"""
    p[0] = ("while", p[3], p[5])


def p_for_statement(p):
    """for_statement : FOR OPEN_PAREN for_init SEMICOLON boolean_expression SEMICOLON for_update CLOSE_PAREN statement"""
    p[0] = ("for", p[3], p[5], p[7], p[9])


def p_for_init(p):
    """for_init : type_specifier IDENTIFIER ASSIGN expression
    | assignment_statement
    | empty"""
    if len(p) == 5:
        p[0] = ("for_declaration", p[1], p[2], p[4])
    else:
        p[0] = p[1]


def p_for_update(p):
    """for_update : assignment_statement
    | IDENTIFIER INCREMENT
    | IDENTIFIER DECREMENT
    | empty"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("update", p[1], p[2])


def p_foreach_statement(p):
    """foreach_statement : FOREACH OPEN_PAREN type_specifier IDENTIFIER IN expression CLOSE_PAREN statement"""
    p[0] = ("foreach", p[3], p[4], p[6], p[8])


def p_return_statement(p):
    """return_statement : RETURN expression SEMICOLON
    | RETURN SEMICOLON"""
    if len(p) == 4:
        p[0] = ("return", p[2])
    else:
        p[0] = ("return", None)


# ========== REGLAS GRAMATICALES: IMPRESIÓN E INGRESO DE DATOS ==========

#--------------------------------------------------------------------------------------------------------------------
def p_print_statement(p):
    """print_statement : CONSOLE DOT WRITELINE OPEN_PAREN expression CLOSE_PAREN SEMICOLON
    | CONSOLE DOT WRITE OPEN_PAREN expression CLOSE_PAREN SEMICOLON
    | CONSOLE DOT WRITELINE OPEN_PAREN CLOSE_PAREN SEMICOLON"""
    if len(p) == 8:
        p[0] = ("print", p[3], p[5])
    else:
        p[0] = ("print", p[3], None)


def p_input_statement(p):
    """input_statement : CONSOLE DOT READLINE OPEN_PAREN CLOSE_PAREN
    | CONVERT DOT TOINT32 OPEN_PAREN CONSOLE DOT READLINE OPEN_PAREN CLOSE_PAREN CLOSE_PAREN
    """
    if len(p) == 6:
        p[0] = ("input", "string")
    else:
        p[0] = ("input", "int")
#--------------------------------------------------------------------------------------------------------------------

# ========== REGLAS GRAMATICALES: EXPRESIONES ARITMÉTICAS ==========


def p_expression(p):
    """expression : primary_expression
    | arithmetic_expression
    | boolean_expression"""
    p[0] = p[1]


def p_primary_expression(p):
    """primary_expression : literal
    | IDENTIFIER
    | function_call
    | array_access
    | member_access
    | array_initialization
    | input_statement
    | TRUE
    | FALSE
    | OPEN_PAREN expression CLOSE_PAREN"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_arithmetic_expression(p):
    """arithmetic_expression : expression PLUS expression
    | expression MINUS expression
    | expression MULTIPLY expression
    | expression DIVIDE expression
    | expression PERCENT expression
    | MINUS expression %prec UMINUS"""
    if len(p) == 3:
        p[0] = ("unary_minus", p[2])
    else:
        p[0] = ("binary_op", p[2], p[1], p[3])


# ========== REGLAS GRAMATICALES: CONDICIONES Y CONECTORES LÓGICOS ==========

#--------------------------------------------------------------------------------------------------------------------
def p_boolean_expression(p):
    """boolean_expression : expression EQUAL expression
    | expression NOT_EQUAL expression
    | expression LESS_THAN expression
    | expression GREATER_THAN expression
    | expression LESS_THAN_EQUAL expression
    | expression GREATER_THAN_EQUAL expression
    | boolean_expression DOUBLE_AMPERSAND boolean_expression
    | boolean_expression DOUBLE_PIPE boolean_expression
    | BANG boolean_expression"""
    if len(p) == 3:
        p[0] = ("not", p[2])
    else:
        p[0] = ("comparison", p[2], p[1], p[3])
#--------------------------------------------------------------------------------------------------------------------

# ========== REGLAS GRAMATICALES: ESTRUCTURAS DE DATOS ==========


def p_array_initialization(p):
    """array_initialization : OPEN_BRACE expression_list CLOSE_BRACE
    | NEW type_specifier OPEN_BRACKET expression CLOSE_BRACKET
    | NEW LIST LESS_THAN type_specifier GREATER_THAN OPEN_PAREN CLOSE_PAREN
    | NEW LIST LESS_THAN type_specifier GREATER_THAN OPEN_BRACE expression_list CLOSE_BRACE"""
    if len(p) == 4:
        p[0] = ("array_init", p[2])
    elif len(p) == 6:
        p[0] = ("array_new", p[2], p[4])
    elif len(p) == 8:
        # new List<int>()
        p[0] = ("list_new", p[4], [])
    elif len(p) == 9:
        # new List<int>{ 1, 2, 3 }
        p[0] = ("list_init", p[4], p[7])


def p_array_access(p):
    """array_access : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET"""
    # El tipo de acceso (array o diccionario) se determina en el análisis semántico
    p[0] = ("array_access", p[1], p[3])


def p_member_access(p):
    """member_access : IDENTIFIER DOT IDENTIFIER"""
    p[0] = ("member_access", p[1], p[3])


def p_function_call(p):
    """function_call : IDENTIFIER OPEN_PAREN argument_list CLOSE_PAREN"""
    p[0] = ("function_call", p[1], p[3])


def p_argument_list(p):
    """argument_list : argument_list COMMA expression
    | expression
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[3]]


def p_expression_list(p):
    """expression_list : expression_list COMMA expression
    | expression
    | empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []


def p_dictionary_initializer_list(p):
    """dictionary_initializer_list : dictionary_initializer_list COMMA dictionary_initializer
    | dictionary_initializer
    | empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []


def p_dictionary_initializer(p):
    """dictionary_initializer : OPEN_BRACE expression COMMA expression CLOSE_BRACE"""
    p[0] = ("key_value", p[2], p[4])

def p_expression_new_generic(p):
    """expression : NEW generic_type OPEN_PAREN CLOSE_PAREN"""
    p[0] = p[2] 


# ========== REGLAS GRAMATICALES: LITERALES ==========


def p_literal(p):
    """literal : INTEGER
    | FLOAT
    | STRING
    | CHAR_LITERAL
    | NULL"""
    p[0] = ("literal", type(p[1]).__name__, p[1])


# ========== REGLAS GRAMATICALES: PRODUCCIONES VACÍAS ==========


def p_empty(p):
    """empty :"""
    pass


# ========== PRECEDENCIA DE OPERADORES ==========

precedence = (
    ("left", "DOUBLE_PIPE"),
    ("left", "DOUBLE_AMPERSAND"),
    ("left", "EQUAL", "NOT_EQUAL"),
    ("left", "LESS_THAN", "GREATER_THAN", "LESS_THAN_EQUAL", "GREATER_THAN_EQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "MULTIPLY", "DIVIDE", "PERCENT"),
    ("right", "UMINUS"),
    ("right", "BANG"),
)

# ========== MANEJO DE ERRORES SINTÁCTICOS ==========


def p_error(p):
    if p:
        msg = f"[SYNTAX ERROR] Unexpected token '{p.value}' at line {p.lineno}"
        syntax_errors.append(msg)
    else:
        msg = "[SYNTAX ERROR] Unexpected end of input"
        syntax_errors.append(msg)


# ========== ANÁLISIS SEMÁNTICO ==========


def semantic_analysis(ast):
    """Realiza el análisis semántico del AST"""
    semantic_errors.clear()
    symbol_table.clear()
    global undeclared_vars_reported
    undeclared_vars_reported = set()

    if ast:
        check_node(ast)

    return len(semantic_errors) == 0


def check_method(node):
    """Registra una función en la tabla de símbolos"""
    method_name = node[4]
    parameters = node[5]

    symbol_table[method_name] = {
        "type": "function",
        "initialized": True,
        "parameters": parameters,
    }

    # Registrar parámetros en el scope local
    for param in parameters:
        if isinstance(param, tuple) and param[0] == "parameter":
            param_type = param[1]
            param_name = param[2]
            symbol_table[param_name] = {"type": param_type, "initialized": True}


def check_parameter(node):
    """Procesa un parámetro de función"""
    param_type = node[1]
    param_name = node[2]

    symbol_table[param_name] = {"type": param_type, "initialized": True}


def check_for_declaration(node):
    """Procesa una declaración en un for loop"""
    var_type = node[1]
    var_name = node[2]
    init_expr = node[3]

    symbol_table[var_name] = {"type": var_type, "initialized": True}


def check_node(node):
    """Verifica un nodo del AST recursivamente"""
    if not isinstance(node, tuple):
        return

    node_type = node[0]

    # ========== PROCESAMIENTO DE DECLARACIONES ==========
    if node_type == "method":
        check_method(node)
    elif node_type == "parameter":
        check_parameter(node)
    elif node_type == "for_declaration":
        check_for_declaration(node)

    # ========== VALIDACIÓN: COMPATIBILIDAD DE TIPOS ==========
    elif node_type == "assignment":
        check_assignment_compatibility(node)
    elif node_type == "declaration":
        check_declaration(node)
    elif node_type == "multi_declaration":
        check_multi_declaration(node)
    elif node_type == "binary_op":
        check_arithmetic_compatibility(node)
    elif node_type == "comparison":
        check_comparison_compatibility(node)

    # ========== VALIDACIÓN: ESTRUCTURAS DE CONTROL ==========
    elif node_type == "if":
        check_control_structure(node)
    elif node_type == "while":
        check_control_structure(node)
    elif node_type == "for":
        check_for_structure(node)
    elif node_type == "foreach":
        check_foreach_structure(node)

    # ========== VALIDACIÓN: OPERACIONES ==========
    elif node_type == "function_call":
        check_function_call(node)
    elif node_type == "array_access":
        check_array_access(node)
    elif node_type in ["dict_access", "dict_init"]:
        check_dictionary_operation(node)

    # Recursión para nodos hijos
    for i in range(1, len(node)):
        if isinstance(node[i], (list, tuple)):
            if isinstance(node[i], list):
                for item in node[i]:
                    check_node(item)
            else:
                check_node(node[i])


def check_assignment_compatibility(node):
    """Verifica compatibilidad en asignaciones"""
    var_name = node[1]
    expr = node[2]

    if var_name not in symbol_table:
        semantic_errors.append(f"[SEMANTIC ERROR] Variable '{var_name}' not declared")
        return

    var_type = symbol_table[var_name]["type"]
    expr_type = get_expression_type(expr)

    # Solo verificar compatibilidad si el tipo de expresión es válido
    if expr_type != "unknown" and not are_types_compatible(var_type, expr_type):
        semantic_errors.append(
            f"[SEMANTIC ERROR] Type mismatch: Cannot assign {expr_type} to {var_type} variable '{var_name}'"
        )


def check_declaration(node):
    """Registra una declaración en la tabla de símbolos"""
    var_type = node[1]
    var_name = node[2]
    init_expr = node[3] if len(node) > 3 else None

    if var_name in symbol_table:
        semantic_errors.append(
            f"[SEMANTIC ERROR] Variable '{var_name}' already declared"
        )
    else:
        symbol_table[var_name] = {
            "type": var_type,
            "initialized": init_expr is not None,
        }

        if init_expr:
            expr_type = get_expression_type(init_expr)
            # Solo verificar compatibilidad si el tipo de expresión es válido
            if expr_type != "unknown" and not are_types_compatible(var_type, expr_type):
                semantic_errors.append(
                    f"[SEMANTIC ERROR] Type mismatch in declaration: Cannot initialize {var_type} with {expr_type}"
                )


def check_multi_declaration(node):
    """Registra múltiples declaraciones en la tabla de símbolos"""
    var_type = node[1]
    declarators = node[2]

    for declarator in declarators:
        if isinstance(declarator, tuple) and declarator[0] == "declarator":
            var_name = declarator[1]
            init_expr = declarator[2] if len(declarator) > 2 else None

            if var_name in symbol_table:
                semantic_errors.append(
                    f"[SEMANTIC ERROR] Variable '{var_name}' already declared"
                )
            else:
                symbol_table[var_name] = {
                    "type": var_type,
                    "initialized": init_expr is not None,
                }

                if init_expr:
                    expr_type = get_expression_type(init_expr)
                    # Solo verificar compatibilidad si el tipo de expresión es válido
                    if expr_type != "unknown" and not are_types_compatible(
                        var_type, expr_type
                    ):
                        semantic_errors.append(
                            f"[SEMANTIC ERROR] Type mismatch in declaration: Cannot initialize {var_type} with {expr_type}"
                        )
    # En check_multi_declaration o donde sea que verifiques tipos, asegúrate de incluir:
    if isinstance(var_type, tuple) and var_type[0] == "list_type" and isinstance(expr_type, tuple) and expr_type[0] == "list_type":
        # Verificar que los tipos de elementos sean compatibles
        if not are_types_compatible(var_type[1], expr_type[1]):
            semantic_errors.append(
                f"[SEMANTIC ERROR] Cannot initialize List<{var_type[1]}> with List<{expr_type[1]}>"
            )


def check_arithmetic_compatibility(node):
    """Verifica compatibilidad en operaciones aritméticas"""
    op = node[1]
    left = node[2]
    right = node[3]

    left_type = get_expression_type(left)
    right_type = get_expression_type(right)

    # Solo verificar compatibilidad si ambos tipos son válidos
    if (
        left_type != "unknown"
        and right_type != "unknown"
        and not are_arithmetic_compatible(left_type, right_type)
    ):
        semantic_errors.append(
            f"[SEMANTIC ERROR] Arithmetic operation '{op}' not supported between {left_type} and {right_type}"
        )


def check_comparison_compatibility(node):
    """Verifica compatibilidad en comparaciones"""
    op = node[1]
    left = node[2]
    right = node[3]

    left_type = get_expression_type(left)
    right_type = get_expression_type(right)

    # Solo verificar compatibilidad si ambos tipos son válidos
    if (
        left_type != "unknown"
        and right_type != "unknown"
        and not are_comparable(left_type, right_type)
    ):
        semantic_errors.append(
            f"[SEMANTIC ERROR] Comparison '{op}' not supported between {left_type} and {right_type}"
        )


def check_control_structure(node):
    """Verifica estructuras de control"""
    node_type = node[0]
    condition = node[1]

    cond_type = get_expression_type(condition, is_condition=True)
    if cond_type != "bool":
        semantic_errors.append(
            f"[SEMANTIC ERROR] {node_type.capitalize()} condition must be boolean, got {cond_type}"
        )


def check_for_structure(node):
    """Verifica estructura for"""
    init_stmt = node[1]
    condition = node[2]
    update_stmt = node[3]

    if condition:
        cond_type = get_expression_type(condition)
        if cond_type != "bool":
            semantic_errors.append(
                "[SEMANTIC ERROR] For loop condition must be boolean"
            )


def check_foreach_structure(node):
    """Verifica estructura foreach y registra la variable del loop"""
    var_type = node[1]  # tipo de la variable (ej: int)
    var_name = node[2]  # nombre de la variable (ej: num)
    collection = node[3]  # expresión de la colección (ej: numbers)
    body = node[4]  # cuerpo del loop

    # Registrar la variable del foreach en la tabla de símbolos
    symbol_table[var_name] = {"type": var_type, "initialized": True}


def check_function_call(node):
    """Verifica llamadas a función"""
    func_name = node[1]
    args = node[2]

    # Validar funciones conocidas del sistema
    if (
        func_name not in ["WriteLine", "Write", "ReadLine", "ToInt32"]
        and func_name not in symbol_table
    ):
        semantic_errors.append(f"[SEMANTIC ERROR] Function '{func_name}' not declared")


def check_array_access(node):
    """Verifica acceso a arrays"""
    array_name = node[1]
    index_expr = node[2]

    if array_name not in symbol_table:
        semantic_errors.append(f"[SEMANTIC ERROR] Array '{array_name}' not declared")

    index_type = get_expression_type(index_expr)
    # Solo verificar tipo de índice si es válido
    if index_type != "unknown" and index_type != "int":
        semantic_errors.append(
            f"[SEMANTIC ERROR] Array index must be integer, got {index_type}"
        )


def check_dictionary_operation(node):
    """Verifica operaciones con diccionarios"""
    if node[0] == "dict_access":
        dict_name = node[1]
        key_expr = node[2]

        if dict_name not in symbol_table:
            semantic_errors.append(f"[SEMANTIC ERROR] Dictionary '{dict_name}' not declared")
            return

        dict_type = symbol_table[dict_name]["type"]
        if not isinstance(dict_type, tuple) or dict_type[0] != "dictionary":
            semantic_errors.append(f"[SEMANTIC ERROR] Variable '{dict_name}' is not a dictionary")
            return

        key_type = get_expression_type(key_expr)
        expected_key_type = dict_type[1]

        if key_type != "unknown" and key_type != expected_key_type:
            semantic_errors.append(
                f"[SEMANTIC ERROR] Dictionary key must be of type {expected_key_type}, got {key_type}"
            )

    elif node[0] == "dict_init":
        key_value_pairs = node[3]  # Lista de tuplas (key_value, key, value)
        key_type = node[1]
        value_type = node[2]

        for pair in key_value_pairs:
            if pair[0] == "key_value":
                actual_key_type = get_expression_type(pair[1])
                actual_value_type = get_expression_type(pair[2])

                if actual_key_type != "unknown" and actual_key_type != key_type:
                    semantic_errors.append(
                        f"[SEMANTIC ERROR] Dictionary key must be of type {key_type}, got {actual_key_type}"
                    )

                if actual_value_type != "unknown" and actual_value_type != value_type:
                    semantic_errors.append(
                        f"[SEMANTIC ERROR] Dictionary value must be of type {value_type}, got {actual_value_type}"
                    )


def get_expression_type(expr, is_condition=False):
    """Obtiene el tipo de una expresión"""
    if isinstance(expr, str):
        if expr in symbol_table:
            expr_type = symbol_table[expr]["type"]
            if is_condition and expr_type != "bool":
                semantic_errors.append(
                    f"[SEMANTIC ERROR] Cannot use type {expr_type} as a condition"
                )
                return "unknown"
            return expr_type
        # Valores booleanos
        if expr in ["true", "false", "True", "False"]:
            return "bool"
        # Variable no declarada
        if expr.isidentifier() and expr not in undeclared_vars_reported:
            semantic_errors.append(f"[SEMANTIC ERROR] Variable '{expr}' not declared")
            undeclared_vars_reported.add(expr)
        return "unknown"

    if isinstance(expr, tuple):
        expr_type = expr[0]

        if expr_type == "literal":
            type_name = expr[1]
            if type_name == "int":
                if is_condition:
                    semantic_errors.append(
                        "[SEMANTIC ERROR] Cannot use integer literal as a condition"
                    )
                    return "unknown"
                return "int"
            elif type_name == "float":
                if is_condition:
                    semantic_errors.append(
                        "[SEMANTIC ERROR] Cannot use float literal as a condition"
                    )
                    return "unknown"
                return "float"
            elif type_name == "str":
                if is_condition:
                    semantic_errors.append(
                        "[SEMANTIC ERROR] Cannot use string literal as a condition"
                    )
                    return "unknown"
                return "string"
            elif type_name == "bool":
                return "bool"

        elif expr_type == "binary_op":
            op = expr[1]
            left_type = get_expression_type(expr[2])
            right_type = get_expression_type(expr[3])

            # Para concatenación de strings
            if op == "+" and (left_type == "string" or right_type == "string"):
                return "string"

            # Para operaciones de comparación
            if op in ["<", ">", "<=", ">=", "==", "!="]:
                return "bool"

            return resolve_arithmetic_type(left_type, right_type)

        elif expr_type == "comparison":
            return "bool"

        elif expr_type == "array_access":
            array_name = expr[1]
            if array_name in symbol_table:
                array_type = symbol_table[array_name]["type"]
                if isinstance(array_type, tuple) and array_type[0] == "array_type":
                    element_type = array_type[1]
                    if is_condition:
                        semantic_errors.append(
                            f"[SEMANTIC ERROR] Cannot use array element of type {element_type} directly as a condition"
                        )
                        return "unknown"
                    return element_type
            return "unknown"

        elif expr_type == "dict_access":
            dict_name = expr[1]
            if dict_name in symbol_table:
                dict_type = symbol_table[dict_name]["type"]
                if isinstance(dict_type, tuple) and dict_type[0] == "dictionary":
                    value_type = dict_type[2]  # El tipo del valor es el tercer elemento
                    if is_condition:
                        semantic_errors.append(
                            f"[SEMANTIC ERROR] Cannot use dictionary value of type {value_type} directly as a condition"
                        )
                        return "unknown"
                    return value_type
                else:
                    semantic_errors.append(
                        f"[SEMANTIC ERROR] Variable '{dict_name}' is not a dictionary"
                    )
            else:
                semantic_errors.append(
                    f"[SEMANTIC ERROR] Dictionary '{dict_name}' not declared"
                )
            return "unknown"

        elif expr_type == "dict_new":
            return ("dictionary", expr[1], expr[2])  # (tipo_clave, tipo_valor)

        elif expr_type == "dict_init":
            return ("dictionary", expr[1], expr[2])  # (tipo_clave, tipo_valor)

        elif expr_type == "member_access":
            obj_name = expr[1]
            member_name = expr[2]
            if member_name == "Length" and obj_name in symbol_table:
                if is_condition:
                    semantic_errors.append(
                        "[SEMANTIC ERROR] Cannot use array length directly as a condition"
                    )
                    return "unknown"
                return "int"
            return "unknown"

        elif expr_type == "input":
            input_type = expr[1]  # "string" o "int"
            if is_condition:
                semantic_errors.append(
                    f"[SEMANTIC ERROR] Cannot use input of type {input_type} directly as a condition"
                )
                return "unknown"
            return input_type

        elif expr_type == "array_literal":
            # Si es un array literal, retornar array_type del primer elemento
            elements = expr[1]
            if elements and len(elements) > 0:
                elem_type = get_expression_type(elements[0])
                return ("array_type", elem_type)
            return "unknown"

        elif expr_type == "list_new":
            element_type = expr[1]
            return ("list_type", element_type)

        elif expr_type == "list_init":
            element_type = expr[1]
            return ("list_type", element_type)

    return "unknown"


def are_types_compatible(target_type, source_type):
    """Verifica si los tipos son compatibles para asignación"""
    if target_type == source_type:
        return True

    # Conversiones implícitas permitidas
    if target_type == "float" and source_type == "int":
        return True
    if target_type == "double" and source_type in ["int", "float"]:
        return True

    # Compatibilidad de arrays
    if isinstance(target_type, tuple) and isinstance(source_type, tuple):
        if target_type[0] == "array_type" and source_type[0] == "array_type":
            return are_types_compatible(target_type[1], source_type[1])

    # String concatenation
    if target_type == "string" and source_type in ["int", "float", "string"]:
        return True

    return False


def are_arithmetic_compatible(left_type, right_type):
    """Verifica compatibilidad para operaciones aritméticas"""
    numeric_types = ["int", "float", "double"]

    # Operaciones numéricas
    if left_type in numeric_types and right_type in numeric_types:
        return True

    # Concatenación de strings (operador +)
    if left_type == "string" or right_type == "string":
        return True

    return False


def are_comparable(left_type, right_type):
    """Verifica si los tipos se pueden comparar"""
    if left_type == right_type:
        return True

    numeric_types = ["int", "float", "double"]
    return left_type in numeric_types and right_type in numeric_types


def resolve_arithmetic_type(left_type, right_type):
    """Resuelve el tipo resultado de una operación aritmética"""
    if "double" in [left_type, right_type]:
        return "double"
    elif "float" in [left_type, right_type]:
        return "float"
    else:
        return "int"


# ========== FUNCIONES DE FORMATEO ==========


def format_ast(node, indent=0):
    """Formatea el AST de manera legible con indentación"""
    if node is None:
        return "None"

    indent_str = "  " * indent

    if isinstance(node, str):
        return f'"{node}"'

    if isinstance(node, (int, float, bool)):
        return str(node)

    if isinstance(node, list):
        if not node:
            return "[]"

        result = "[\n"
        for i, item in enumerate(node):
            result += f"{indent_str}  {format_ast(item, indent + 1)}"
            if i < len(node) - 1:
                result += ","
            result += "\n"
        result += f"{indent_str}]"
        return result

    if isinstance(node, tuple):
        if not node:
            return "()"

        node_type = node[0]
        result = f"({node_type}"

        if len(node) > 1:
            result += ",\n"
            for i in range(1, len(node)):
                result += f"{indent_str}  {format_ast(node[i], indent + 1)}"
                if i < len(node) - 1:
                    result += ","
                result += "\n"
            result += f"{indent_str}"

        result += ")"
        return result

    return str(node)


# ========== FUNCIONES DE ANÁLISIS ==========


def run_syntax_analysis(file_path, user_git_name):
    """Ejecuta el análisis sintáctico"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/sintactico-{user_git_name}-{timestamp}.txt"

    # Extraer el nombre real del archivo desde el path proporcionado
    real_file_name = os.path.basename(file_path)
    
    # Si es un archivo temporal pero sabemos el nombre original
    original_file_name = None
    if real_file_name == "temp_analysis.cs" and hasattr(run_syntax_analysis, "original_file"):
        original_file_name = run_syntax_analysis.original_file

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Limpiar errores previos
    syntax_errors.clear()
    
    # Reiniciar el lexer para asegurar que las líneas comiencen desde 1
    lexer.lineno = 1

    # Construir el parser
    parser = yacc.yacc()

    try:
        # Parsear el código
        ast = parser.parse(source_code, lexer=lexer)

        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(
                f"Syntax Analysis Log\nUser: {user_git_name}\nFile: {original_file_name or real_file_name}\nDate: {timestamp}\n\n"
            )

            if syntax_errors:
                log_file.write("=== SYNTAX ERRORS ===\n")
                for err in syntax_errors:
                    log_file.write(err + "\n")
                success = False
            else:
                log_file.write("✔ Syntax analysis completed successfully.\n")
                log_file.write("\n=== ABSTRACT SYNTAX TREE ===\n")
                log_file.write(format_ast(ast))
                success = True

        print(f"\n✔ Syntax analysis complete. Log saved to {log_filename}")
        return success, ast

    except Exception as e:
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(
                f"Syntax Analysis Log\nUser: {user_git_name}\nFile: {original_file_name or real_file_name}\nDate: {timestamp}\n\n"
            )
            log_file.write("=== CRITICAL ERROR ===\n")
            log_file.write(f"Parser failed: {str(e)}\n")

            if syntax_errors:
                log_file.write("\n=== SYNTAX ERRORS ===\n")
                for err in syntax_errors:
                    log_file.write(err + "\n")

        print(f"\n❌ Syntax analysis failed. Log saved to {log_filename}")
        return False, None


def run_semantic_analysis(ast, file_path, user_git_name):
    """Ejecuta el análisis semántico"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y-%Hh%M")

    log_filename = f"logs/semantico-{user_git_name}-{timestamp}.txt"

    # Extraer el nombre real del archivo desde el path proporcionado
    real_file_name = os.path.basename(file_path)
    
    # Si es un archivo temporal pero sabemos el nombre original
    original_file_name = None
    if real_file_name == "temp_analysis.cs" and hasattr(run_semantic_analysis, "original_file"):
        original_file_name = run_semantic_analysis.original_file

    success = semantic_analysis(ast)

    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(
            f"Semantic Analysis Log\nUser: {user_git_name}\nFile: {original_file_name or real_file_name}\nDate: {timestamp}\n\n"
        )

        log_file.write("=== SYMBOL TABLE ===\n")
        for name, info in symbol_table.items():
            log_file.write(f"{name}: {info}\n")

        if semantic_errors:
            log_file.write("\n=== SEMANTIC ERRORS ===\n")
            for err in semantic_errors:
                log_file.write(err + "\n")
        else:
            log_file.write("\n✔ Semantic analysis completed successfully.\n")

    print(f"\n✔ Semantic analysis complete. Log saved to {log_filename}")
    return success


# ========== MENÚ PRINCIPAL ==========

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
            "name": "test_errors.cs (Semantic Errors Demo)",
            "path": "algoritmos/test_errors.cs",
            "user": "test",
        },
    }

    print("Select algorithm to analyze:")
    for key, data in algorithms.items():
        print(f"{key}. {data['name']} (Git: {data['user']})")

    choice = input("Enter choice: ").strip()

    if choice in algorithms:
        selected = algorithms[choice]

        # Ejecutar análisis sintáctico
        syntax_success, ast = run_syntax_analysis(
            file_path=selected["path"], user_git_name=selected["user"]
        )

        # Solo continuar con semántico si sintáctico fue exitoso
        if syntax_success:
            semantic_success = run_semantic_analysis(
                ast=ast, file_path=selected["path"], user_git_name=selected["user"]
            )

            if semantic_success:
                print("\n🎉 Both syntax and semantic analysis completed successfully!")
            else:
                print("\n⚠️ Syntax analysis passed, but semantic analysis found errors.")
        else:
            print("\n❌ Syntax analysis failed. Semantic analysis skipped.")
    else:
        print("❌ Invalid option.")
