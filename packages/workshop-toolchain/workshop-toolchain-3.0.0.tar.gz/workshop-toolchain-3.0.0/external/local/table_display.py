from terminaltables import AsciiTable


def draw_table(table_data):
    table = AsciiTable(table_data)
    print(table.table)
