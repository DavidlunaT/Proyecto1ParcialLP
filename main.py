import flet as ft
import os
import datetime
import glob
from collections import Counter
from lex import run_lexical_analysis, error_log as lex_error_log, lexer, reserved
from yacc import (
    run_syntax_analysis,
    run_semantic_analysis,
    syntax_errors,
    semantic_errors,
    symbol_table,
)


class CompilerAnalyzerGUI:
    def __init__(self):
        self.algorithms = {
            "algoritmo1.cs": {
                "path": "algoritmos/algoritmo1.cs",
                "user": "DavidlunaT",
                "description": "Simple Calculator - Basic arithmetic operations",
            },
            "algoritmo2.cs": {
                "path": "algoritmos/algoritmo2.cs",
                "user": "waldaara",
                "description": "Control structures and loops",
            },
            "algoritmo3.cs": {
                "path": "algoritmos/algoritmo3.cs",
                "user": "gabsjimz",
                "description": "Advanced data structures",
            },
            "test_listas.cs": {
                "path": "algoritmos/test_listas.cs",
                "user": "test",
                "description": "List operations demo",
            },
            "test_errors.cs": {
                "path": "algoritmos/test_errors.cs",
                "user": "test",
                "description": "Semantic errors demonstration",
            },
        }

        self.current_code = ""
        self.current_file = None
        self.page = None

        # UI Components
        self.code_editor = None
        self.algorithm_dropdown = None
        self.analysis_tabs = None
        self.lexical_content = None
        self.syntax_content = None
        self.semantic_content = None
        self.logs_content = None
        self.status_bar = None

    def main(self, page: ft.Page):
        self.page = page
        page.title = "C# Compiler Analyzer"
        page.theme_mode = ft.ThemeMode.DARK
        page.window.width = 1400
        page.window.height = 900
        page.padding = 0

        # Create main layout
        self.create_ui()
        page.add(self.create_main_layout())

    def create_ui(self):
        """Create all UI components"""

        # Algorithm selector
        self.algorithm_dropdown = ft.Dropdown(
            width=300,
            options=[
                ft.dropdown.Option(
                    key=filename, text=f"{filename} - {data['description']}"
                )
                for filename, data in self.algorithms.items()
            ],
            hint_text="Select an algorithm to analyze",
            on_change=self.load_algorithm,
            text_style=ft.TextStyle(size=14),
        )

        # Code editor
        self.code_editor = ft.TextField(
            multiline=True,
            min_lines=25,
            max_lines=25,
            expand=True,
            border_color=ft.Colors.GREY_700,
            text_style=ft.TextStyle(font_family="Consolas, Monaco, monospace", size=14),
            hint_text="Select an algorithm or paste your C# code here...",
            on_change=self.on_code_change,
        )

        # Analysis tabs content containers - expand to fill all available space
        self.lexical_content = ft.Column(
            scroll=ft.ScrollMode.AUTO, expand=True, spacing=10
        )
        self.syntax_content = ft.Column(
            scroll=ft.ScrollMode.AUTO, expand=True, spacing=10
        )
        self.semantic_content = ft.Column(
            scroll=ft.ScrollMode.AUTO, expand=True, spacing=10
        )

        # Analysis tabs
        self.analysis_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="📝 Lexical Analysis",
                    content=self.lexical_content,
                ),
                ft.Tab(
                    text="🔍 Syntax Analysis",
                    content=self.syntax_content,
                ),
                ft.Tab(
                    text="🧠 Semantic Analysis",
                    content=self.semantic_content,
                ),
            ],
            expand=True,
        )

        # Logs section
        self.logs_content = ft.Column(
            controls=[
                ft.Text("📋 Analysis Logs", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Run analysis to see logs here...", color=ft.Colors.GREY_400),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,  # Let logs expand within their container
        )

        # Status bar
        self.status_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Ready", color=ft.Colors.GREEN_400),
                    ft.Text("•", color=ft.Colors.GREY_600),
                    ft.Text("Select an algorithm to begin", color=ft.Colors.GREY_400),
                ]
            ),
            bgcolor=ft.Colors.GREY_900,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.GREY_700)),
        )

    def create_main_layout(self):
        """Create the main split layout"""

        # Left panel - Algorithm selection and code editor
        left_panel = ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "🚀 C# Compiler Analyzer",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_400,
                                ),
                                ft.Text(
                                    "Educational tool for lexical, syntax, and semantic analysis",
                                    size=14,
                                    color=ft.Colors.GREY_400,
                                ),
                                ft.Divider(height=1, color=ft.Colors.GREY_700),
                                # Algorithm selector and controls
                                ft.Row(
                                    [
                                        self.algorithm_dropdown,
                                        ft.ElevatedButton(
                                            "🔄 Refresh",
                                            on_click=self.refresh_files,
                                            bgcolor=ft.Colors.BLUE_600,
                                            color=ft.Colors.WHITE,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ]
                        ),
                        padding=20,
                        bgcolor=ft.Colors.GREY_900,
                        border=ft.border.only(
                            bottom=ft.border.BorderSide(1, ft.Colors.GREY_700)
                        ),
                    ),
                    # Code editor
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "📝 Source Code",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Container(expand=True),
                                        ft.Chip(
                                            label=ft.Text("C#"),
                                            bgcolor=ft.Colors.PURPLE_200,
                                            color=ft.Colors.PURPLE_900,
                                        ),
                                    ]
                                ),
                                self.code_editor,
                            ]
                        ),
                        padding=20,
                        expand=True,
                    ),
                ]
            ),
            expand=True,  # Changed from fixed width=700 to expand=True
            bgcolor=ft.Colors.GREY_800,
            border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_700)),
        )

        # Right panel - Analysis results and logs
        right_panel = ft.Container(
            content=ft.Column(
                [
                    # Analysis controls - now responsive
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "🔬 Analysis Results",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "▶️ Run Lexical",
                                            on_click=self.run_lexical_analysis,
                                            bgcolor=ft.Colors.GREEN_600,
                                            color=ft.Colors.WHITE,
                                            expand=True,  # Make buttons expand
                                        ),
                                        ft.ElevatedButton(
                                            "▶️ Run Syntax",
                                            on_click=self.run_syntax_analysis,
                                            bgcolor=ft.Colors.ORANGE_600,
                                            color=ft.Colors.WHITE,
                                            expand=True,
                                        ),
                                        ft.ElevatedButton(
                                            "▶️ Run Semantic",
                                            on_click=self.run_semantic_analysis,
                                            bgcolor=ft.Colors.PURPLE_600,
                                            color=ft.Colors.WHITE,
                                            expand=True,
                                        ),
                                        ft.ElevatedButton(
                                            "⚡ Run All",
                                            on_click=self.run_all_analysis,
                                            bgcolor=ft.Colors.BLUE_600,
                                            color=ft.Colors.WHITE,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=10,
                                    expand=True,  # Make the row expand
                                ),
                            ]
                        ),
                        padding=20,
                        bgcolor=ft.Colors.GREY_900,
                        border=ft.border.only(
                            bottom=ft.border.BorderSide(1, ft.Colors.GREY_700)
                        ),
                    ),
                    # Analysis tabs - give most of the space to this section
                    ft.Container(
                        content=self.analysis_tabs,
                        expand=True,  # Changed from expand=5 to expand=True for better responsiveness
                        padding=ft.padding.only(left=5, right=5, top=5),
                    ),
                    # Logs section - compact but functional
                    ft.Container(
                        content=ft.Column(
                            [self.logs_content],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True,  # Make logs content expand within its container
                        ),
                        padding=15,
                        bgcolor=ft.Colors.GREY_900,
                        border=ft.border.only(
                            top=ft.border.BorderSide(1, ft.Colors.GREY_700)
                        ),
                        height=150,  # Keep fixed height for logs
                    ),
                ]
            ),
            expand=True,  # Changed to expand=True to take remaining horizontal space
            bgcolor=ft.Colors.GREY_800,
        )

        # Main container
        return ft.Column(
            [ft.Row([left_panel, right_panel], expand=True), self.status_bar],
            expand=True,
        )

    def load_algorithm(self, e):
        """Load selected algorithm file"""
        if not e.control.value:
            return

        try:
            filename = e.control.value
            file_path = self.algorithms[filename]["path"]

            with open(file_path, "r", encoding="utf-8") as f:
                self.current_code = f.read()
                self.current_file = filename
                self.code_editor.value = self.current_code

            self.update_status(f"Loaded: {filename}", ft.Colors.GREEN_400)
            self.clear_analysis_results()
            self.page.update()

        except Exception as ex:
            self.update_status(f"Error loading file: {str(ex)}", ft.Colors.RED_400)
            self.page.update()

    def on_code_change(self, e):
        """Handle code editor changes"""
        self.current_code = e.control.value
        self.clear_analysis_results()

    def refresh_files(self, e):
        """Refresh algorithm files list"""
        self.update_status("Files refreshed", ft.Colors.BLUE_400)
        self.page.update()

    def clear_analysis_results(self):
        """Clear all analysis results and add placeholders"""
        # Clear and add expanding placeholders
        self.lexical_content.controls.clear()
        self.lexical_content.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "📝 Lexical Analysis", size=20, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Run lexical analysis to see tokens here...",
                            color=ft.Colors.GREY_400,
                            size=16,
                        ),
                        ft.Container(expand=True),  # Expanding spacer
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        )

        self.syntax_content.controls.clear()
        self.syntax_content.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "🔍 Syntax Analysis", size=20, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Run syntax analysis to see AST here...",
                            color=ft.Colors.GREY_400,
                            size=16,
                        ),
                        ft.Container(expand=True),  # Expanding spacer
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        )

        self.semantic_content.controls.clear()
        self.semantic_content.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "🧠 Semantic Analysis", size=20, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Run semantic analysis to see symbol table here...",
                            color=ft.Colors.GREY_400,
                            size=16,
                        ),
                        ft.Container(expand=True),  # Expanding spacer
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        )

        self.logs_content.controls = [
            ft.Text("📋 Analysis Logs", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Run analysis to see logs here...", color=ft.Colors.GREY_400),
        ]

    def run_lexical_analysis(self, e):
        """Run lexical analysis"""
        if not self.current_code.strip():
            self.update_status("No code to analyze", ft.Colors.RED_400)
            self.page.update()
            return

        try:
            self.update_status("Running lexical analysis...", ft.Colors.YELLOW_400)
            self.page.update()

            # Save code to temporary file
            temp_file = "temp_analysis.cs"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(self.current_code)

            # Clear previous errors
            lex_error_log.clear()

            # Guardar el nombre original del archivo para usarlo en el log
            if self.current_file:
                # Usar un atributo de función para almacenar el nombre original
                run_lexical_analysis.original_file = self.current_file
            
            # Run analysis
            user_name = self.algorithms.get(self.current_file, {}).get("user", "user")
            run_lexical_analysis(temp_file, user_name)

            # Display results
            self.display_lexical_results()

            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)

            self.update_status("Lexical analysis completed", ft.Colors.GREEN_400)

        except Exception as ex:
            self.update_status(f"Lexical analysis error: {str(ex)}", ft.Colors.RED_400)

        self.page.update()

    def run_syntax_analysis(self, e):
        """Run syntax analysis"""
        if not self.current_code.strip():
            self.update_status("No code to analyze", ft.Colors.RED_400)
            self.page.update()
            return

        try:
            self.update_status("Running syntax analysis...", ft.Colors.YELLOW_400)
            self.page.update()

            # Save code to temporary file
            temp_file = "temp_analysis.cs"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(self.current_code)

            # Guardar el nombre original del archivo para usarlo en el log
            if self.current_file:
                # Usar un atributo de función para almacenar el nombre original
                import yacc
                yacc.run_syntax_analysis.original_file = self.current_file

            # Run analysis
            user_name = self.algorithms.get(self.current_file, {}).get("user", "user")
            success, ast = run_syntax_analysis(temp_file, user_name)

            # Display results
            self.display_syntax_results(success, ast)

            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)

            status = (
                "Syntax analysis completed successfully"
                if success
                else "Syntax analysis completed with errors"
            )
            color = ft.Colors.GREEN_400 if success else ft.Colors.ORANGE_400
            self.update_status(status, color)

        except Exception as ex:
            self.update_status(f"Syntax analysis error: {str(ex)}", ft.Colors.RED_400)

        self.page.update()

    def run_semantic_analysis(self, e):
        """Run semantic analysis"""
        if not self.current_code.strip():
            self.update_status("No code to analyze", ft.Colors.RED_400)
            self.page.update()
            return

        try:
            self.update_status("Running semantic analysis...", ft.Colors.YELLOW_400)
            self.page.update()

            # Save code to temporary file
            temp_file = "temp_analysis.cs"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(self.current_code)

            # Guardar el nombre original del archivo para usarlo en el log
            if self.current_file:
                # Usar un atributo de función para almacenar el nombre original
                import yacc
                yacc.run_semantic_analysis.original_file = self.current_file

            # First run syntax to get AST
            user_name = self.algorithms.get(self.current_file, {}).get("user", "user")
            syntax_success, ast = run_syntax_analysis(temp_file, user_name)

            if syntax_success:
                # Run semantic analysis
                semantic_success = run_semantic_analysis(ast, temp_file, user_name)
                self.display_semantic_results(semantic_success)

                status = (
                    "Semantic analysis completed successfully"
                    if semantic_success
                    else "Semantic analysis completed with errors"
                )
                color = ft.Colors.GREEN_400 if semantic_success else ft.Colors.ORANGE_400
                self.update_status(status, color)
            else:
                self.update_status(
                    "Syntax analysis must pass before semantic analysis",
                    ft.Colors.RED_400,
                )

            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)

        except Exception as ex:
            self.update_status(f"Semantic analysis error: {str(ex)}", ft.Colors.RED_400)

        self.page.update()

    def run_all_analysis(self, e):
        """Run all analyses in sequence"""
        if not self.current_code.strip():
            self.update_status("No code to analyze", ft.Colors.RED_400)
            self.page.update()
            return

        self.update_status("Running complete analysis...", ft.Colors.YELLOW_400)
        self.page.update()

        # Run each analysis
        self.run_lexical_analysis(None)
        self.run_syntax_analysis(None)
        self.run_semantic_analysis(None)

        self.update_status("Complete analysis finished", ft.Colors.GREEN_400)
        self.page.update()

    def display_lexical_results(self):
        """Display lexical analysis results"""
        self.lexical_content.controls.clear()

        # Tokenize current code
        lexer.input(self.current_code)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)

        # Statistics
        token_count = len(tokens)
        error_count = len(lex_error_log)

        self.lexical_content.controls.extend(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            "🎯 Tokens Found",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            str(token_count),
                                            size=24,
                                            color=ft.Colors.BLUE_400,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.VerticalDivider(color=ft.Colors.GREY_600),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "❌ Errors",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            str(error_count),
                                            size=24,
                                            color=(
                                                ft.Colors.RED_400
                                                if error_count > 0
                                                else ft.Colors.GREEN_400
                                            ),
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                        padding=20,
                        bgcolor=ft.Colors.GREY_800,
                    )
                ),
                ft.Text("🔤 Tokens", size=18, weight=ft.FontWeight.BOLD),
            ]
        )

        # Display tokens in a scrollable container instead of DataTable
        if tokens:
            self.lexical_content.controls.append(
                ft.Text(f"Total tokens found: {len(tokens)}", color=ft.Colors.GREY_400)
            )

            # Create a scrollable container with the token table
            token_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Type", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Value", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Line", weight=ft.FontWeight.BOLD)),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(tok.type, color=self.get_token_color(tok.type))
                            ),
                            ft.DataCell(ft.Text(repr(tok.value))),
                            ft.DataCell(ft.Text(str(tok.lineno))),
                        ]
                    )
                    for tok in tokens
                ],
                border=ft.border.all(1, ft.Colors.GREY_600),
                bgcolor=ft.Colors.GREY_900,
            )

            # Wrap the table in a scrollable container that expands
            self.lexical_content.controls.append(
                ft.Container(
                    content=ft.Column(
                        [token_table],
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                    ),
                    border=ft.border.all(1, ft.Colors.GREY_600),
                    border_radius=8,
                    expand=True,
                    padding=10,
                    width=None,  # Remove width constraint
                    height=None,  # Remove height constraint
                )
            )

        # Display errors if any
        if lex_error_log:
            self.lexical_content.controls.extend(
                [
                    ft.Text(
                        "❌ Lexical Errors",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_400,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(error, color=ft.Colors.RED_300)
                                for error in lex_error_log
                            ]
                        ),
                        bgcolor=ft.Colors.RED_900,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.RED_600),
                    ),
                ]
            )

    def display_syntax_results(self, success, ast):
        """Display syntax analysis results"""
        self.syntax_content.controls.clear()

        # Status card
        status_color = ft.Colors.GREEN_400 if success else ft.Colors.RED_400
        status_text = "✅ Syntax Valid" if success else "❌ Syntax Errors Found"

        self.syntax_content.controls.extend(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    status_text,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=status_color,
                                ),
                                ft.Text(
                                    f"Errors: {len(syntax_errors)}",
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                        bgcolor=ft.Colors.GREY_800,
                    )
                )
            ]
        )

        # Display errors if any
        if syntax_errors:
            self.syntax_content.controls.extend(
                [
                    ft.Text(
                        "❌ Syntax Errors",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_400,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(error, color=ft.Colors.RED_300)
                                for error in syntax_errors
                            ]
                        ),
                        bgcolor=ft.Colors.RED_900,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.RED_600),
                    ),
                ]
            )

        # Display AST if successful (full tree)
        if success and ast:
            self.syntax_content.controls.extend(
                [
                    ft.Text(
                        "🌳 Abstract Syntax Tree (Complete)",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    self.format_ast_full(ast),
                                    selectable=True,
                                    style=ft.TextStyle(
                                        font_family="Consolas, Monaco, monospace",
                                        size=12,
                                    ),
                                )
                            ],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True,
                        ),
                        bgcolor=ft.Colors.GREY_900,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_600),
                        expand=True,  # Container expands to fill available space
                    ),
                ]
            )

    def display_semantic_results(self, success):
        """Display semantic analysis results"""
        self.semantic_content.controls.clear()

        # Status card
        status_color = ft.Colors.GREEN_400 if success else ft.Colors.RED_400
        status_text = "✅ Semantics Valid" if success else "❌ Semantic Errors Found"

        self.semantic_content.controls.extend(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    status_text,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=status_color,
                                ),
                                ft.Text(
                                    f"Errors: {len(semantic_errors)}",
                                    color=ft.Colors.GREY_400,
                                ),
                                ft.Text(
                                    f"Symbols: {len(symbol_table)}",
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                        bgcolor=ft.Colors.GREY_800,
                    )
                )
            ]
        )

        # Display symbol table with proper expansion
        if symbol_table:
            symbol_table_dt = ft.DataTable(
                columns=[
                    ft.DataColumn(
                        ft.Text("Symbol", weight=ft.FontWeight.BOLD)
                    ),
                    ft.DataColumn(
                        ft.Text("Type", weight=ft.FontWeight.BOLD)
                    ),
                    ft.DataColumn(
                        ft.Text("Initialized", weight=ft.FontWeight.BOLD)
                    ),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(name, color=ft.Colors.BLUE_300)
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(info.get("type", "unknown")),
                                    color=ft.Colors.GREEN_300,
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    (
                                        "✓"
                                        if info.get("initialized", False)
                                        else "✗"
                                    ),
                                    color=(
                                        ft.Colors.GREEN_400
                                        if info.get("initialized", False)
                                        else ft.Colors.RED_400
                                    ),
                                )
                            ),
                        ]
                    )
                    for name, info in symbol_table.items()
                ],
                border=ft.border.all(1, ft.Colors.GREY_600),
                bgcolor=ft.Colors.GREY_900,
            )

            self.semantic_content.controls.extend(
                [
                    ft.Text("📋 Symbol Table", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column(
                            [symbol_table_dt],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True,
                        ),
                        border=ft.border.all(1, ft.Colors.GREY_600),
                        border_radius=8,
                        expand=True,
                        padding=10,
                        width=None,  # Remove width constraint
                        height=None,  # Remove height constraint
                    ),
                ]
            )

        # Display errors if any
        if semantic_errors:
            self.semantic_content.controls.extend(
                [
                    ft.Text(
                        "❌ Semantic Errors",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_400,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(error, color=ft.Colors.RED_300)
                                for error in semantic_errors
                            ]
                        ),
                        bgcolor=ft.Colors.RED_900,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.RED_600),
                    ),
                ]
            )

    def get_token_color(self, token_type):
        """Get color for token type"""
        color_map = {
            "IDENTIFIER": ft.Colors.BLUE_300,
            "INTEGER": ft.Colors.ORANGE_300,
            "FLOAT": ft.Colors.ORANGE_300,
            "STRING": ft.Colors.GREEN_300,
            "IF": ft.Colors.PURPLE_300,
            "WHILE": ft.Colors.PURPLE_300,
            "FOR": ft.Colors.PURPLE_300,
            "CLASS": ft.Colors.YELLOW_300,
            "PUBLIC": ft.Colors.CYAN_300,
            "PRIVATE": ft.Colors.CYAN_300,
            "STATIC": ft.Colors.CYAN_300,
        }
        return color_map.get(token_type, ft.Colors.WHITE)

    def format_ast_full(self, node, level=0):
        """Format AST showing complete tree without any limitations"""
        if isinstance(node, str):
            return f'"{node}"'
        elif isinstance(node, (int, float, bool)):
            return str(node)
        elif isinstance(node, list):
            if not node:
                return "[]"
            indent = "  " * level
            result = "[\n"
            for item in node:
                result += f"{indent}  {self.format_ast_full(item, level + 1)},\n"
            result += f"{indent}]"
            return result
        elif isinstance(node, tuple) and node:
            indent = "  " * level
            if len(node) == 1:
                return f"{indent}{node[0]}"
            result = f"{indent}{node[0]}(\n"
            for i in range(1, len(node)):  # Show ALL children
                result += f"{self.format_ast_full(node[i], level + 1)}\n"
            result += f"{indent})"
            return result
        else:
            return str(node)

    def update_status(self, message, color=ft.Colors.WHITE):
        """Update status bar"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_bar.content.controls[0] = ft.Text(message, color=color)
        self.status_bar.content.controls[2] = ft.Text(
            f"Last update: {timestamp}", color=ft.Colors.GREY_400
        )

        # Update logs and show where logs are saved
        log_files = glob.glob("logs/*.txt")
        if log_files:
            latest_log = max(log_files, key=os.path.getmtime)
            self.logs_content.controls.append(
                ft.Text(
                    f"[{timestamp}] {message} - Log saved: {latest_log}",
                    color=color,
                    size=12,
                    selectable=True,
                )
            )
        else:
            self.logs_content.controls.append(
                ft.Text(
                    f"[{timestamp}] {message}", color=color, size=12, selectable=True
                )
            )

        # Keep only last 20 log entries (increased from 10)
        if len(self.logs_content.controls) > 22:  # 2 header + 20 logs
            self.logs_content.controls = (
                self.logs_content.controls[:2] + self.logs_content.controls[-20:]
            )


def main():
    app = CompilerAnalyzerGUI()
    ft.app(target=app.main)


if __name__ == "__main__":
    main()
