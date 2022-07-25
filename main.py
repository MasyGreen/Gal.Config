import json

import dearpygui.dearpygui as dpg


# Load Table from JSON
def loadJSON():
    with open(jsonFileName) as json_file:
        data = json.load(json_file)
    rind: int = 0
    for item in data:
        rind = rind + 1
        cind: int = 0
        with dpg.table_row(parent='MTable'):
            for j in range(0, len(arrayColName)):
                cind = cind + 1
                with dpg.table_cell():
                    dpg.add_input_text(default_value=item.get(arrayColName[cind]))


# Save List.Table to JSON
def saveJSON(data):
    with open(jsonFileName, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# replace Null to String.Empty
def convertNull(value):
    if value is None:
        return ""
    return value


# Clear Table and Load from JSON
def reload_callback():
    rows = dpg.get_item_children('MTable', 1)
    for row in rows:
        dpg.delete_item(row)
    loadJSON()


# Save all value from List.Table and save to JSON
def save_callback():
    tabledata = []  # Table to List
    tabledata.clear()

    rows = dpg.get_item_children('MTable', 1)
    rind: int = 0
    for row in rows:  # row collection
        rind = rind + 1
        print(f"Row = {row}")
        cols = dpg.get_item_children(row, 1)  # column in row collection

        cind: int = 0
        tablerow = {}  # Row to Dic
        for col in cols:  # Col collection
            cind = cind + 1
            cell = dpg.get_item_children(col, 1)[0]  # cell contain 'input text' item
            tablerow[arrayColName.get(cind)] = convertNull(dpg.get_value(cell))

        tabledata.append(tablerow)

    saveJSON(tabledata)


def generate_callback():
    selections = dpg.sele('MainTableT')
    values = dpg.get_value('MainTableT')
    print(values)

    for i in range(0, 4):
        for j in range(0, 3):
            print(dpg.get_value(f"cell{i}{j}"))


# Add new Row in Table
def add_callback():
    with dpg.table_row(parent='MTable'):
        for j in range(0, len(arrayColName)):
            with dpg.table_cell():
                dpg.add_input_text()


def main():
    dpg.create_context()
    dpg.set_global_font_scale(1.2)

    with dpg.font_registry():
        with dpg.font("c:\Windows\Fonts\ARIALN.TTF", 20) as font1:
            # add the default font range
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)

            # helper to add range of characters
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

            # add specific range of glyphs
            dpg.add_font_range(0x3100, 0x3ff0)

            # add specific glyphs
            dpg.add_font_chars([0x3105, 0x3107, 0x3108])

            # remap や to %
            dpg.add_char_remap(0x3084, 0x0025)

    with dpg.window(id='MWindow', label="Window", width=790, height=590):
        dpg.add_text("Генератор каталогов запуска Галактика ERP 9.1")
        # Buttons
        with dpg.group(horizontal=True):
            dpg.add_button(tag='bt1', label="Reload", callback=reload_callback)
            dpg.add_button(tag='bt2', label="Save", callback=save_callback)
            dpg.add_button(tag='bt3', label="Generate", callback=generate_callback)
            dpg.add_button(tag='bt4', label="Add", callback=add_callback)

        # Table
        global curtable
        curtable = dpg.table(tag='MTable', header_row=True, resizable=True,
                             borders_outerH=True, borders_innerH=True,
                             borders_innerV=True,
                             borders_outerV=True, policy=dpg.mvTable_SizingStretchProp)
        with curtable:
            for key, value in arrayColName.items():
                dpg.add_table_column(tag=f'MColumn{key}', parent='MTable', label=value)

        loadJSON()
        # once it reaches the end of the columns
        # for i in range(0, 4):
        #     with dpg.table_row():
        #         for j in range(0, len(arrayColName)):
        #             with dpg.table_cell():
        #                 dpg.add_input_text(default_value=f"value{i}{j}")

    dpg.bind_font(font1)
    dpg.create_viewport(title='Window', width=800, height=600)
    dpg.set_primary_window('MWindow', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    global jsonFileName

    jsonFileName = 'save.json'

    global arrayColName
    arrayColName = {1: "DatabaseName",
                    2: "HWKey",
                    3: "LicGalaktika",
                    4: "LicSupport",
                    5: "SQLServer",
                    6: "GalaktikaPath",
                    7: "Description"}
    main()
