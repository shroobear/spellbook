from simple_term_menu import TerminalMenu

class Prompt:
    def ask(question):
        value = input(question)
        return value

    def yes_or_no(question):
        value = input(question + " y/n: ")

    def menu(options):
        terminal_menu = TerminalMenu(options, skip_empty_entries=True)
        menu_entry_index = terminal_menu.show()
        selection = options[menu_entry_index]
        return selection