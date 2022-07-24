import json

import dearpygui.dearpygui as dpg


def loadJSON():
    with open(jsonFileName) as json_file:
        data = json.load(json_file)
    i = 0
    for item in data:
        i = i + 1
        newRow = dpg.add_table_row(parent=110)
        for a in range(0, 5):
            with dpg.table_cell(parent=newRow):
                dpg.add_input_text()

        # cell = dpg.add_table_cell(tag=f"{i}", parent=newRow)
        # dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue1))

        # for j in range(0, 4):
        #     cell = dpg.table_cell(parent=newRow)
        #     if j == 0:
        #         dpg.add_input_text(tag=f"cell{i}{j}", parent=cell, default_value=item.get(nameValue1))
            # if j == 1:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue2))
            # if j == 2:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue3))
            # if j == 3:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue4))
            # if j == 4:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue5))
            # if j == 5:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue6))
            # if j == 6:
            #     dpg.add_input_text(tag=f"cell{i}{j}", default_value=item.get(nameValue7))

        # cell = dpg.table_cell(parent=newRow)
        # dpg.add_input_text(parent=cell,default_value= item.get(nameValue1))
        #
        # for j in range(0, 3):
        #     with dpg.table_cell(parent=newRow):
        #         dpg.add_input_text()

        print(item.get(nameValue1))


def saveJSON(data):
    with open(jsonFileName, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convertNull(value):
    if value is None:
        return ""
    return value


def reload_callback():
    rows = dpg.get_item_children(110, 1)
    for row in rows:
        dpg.delete_item(row)
    loadJSON()


# Get all value from Table
def save_callback():
    tableData = []
    tableData.clear()

    rows = dpg.get_item_children(110, 1)
    rInd = 0
    for row in rows:  # row collection
        rInd = rInd + 1
        print(f"Row = {row}")
        cols = dpg.get_item_children(row, 1)  # column in row collection
        value1 = ""
        value2 = ""
        value3 = ""
        value4 = ""
        value5 = ""
        value6 = ""
        value7 = ""
        cInd = 0
        for col in cols:
            cInd = cInd + 1
            cell = dpg.get_item_children(col, 1)[0]  # cell contain 'input text' item
            print(f"Cell {rInd}/{cInd} = {dpg.get_value(cell)}/{dpg.get_item_label(cell)}")  # get item value

            if cInd == 1:
                value1 = dpg.get_value(cell)

            if cInd == 2:
                value2 = dpg.get_value(cell)

            if cInd == 3:
                value3 = dpg.get_value(cell)

            if cInd == 4:
                value4 = dpg.get_value(cell)

            if cInd == 5:
                value5 = dpg.get_value(cell)

            if cInd == 6:
                value6 = dpg.get_value(cell)

            if cInd == 7:
                value7 = dpg.get_value(cell)

        tableRow = {nameValue1: convertNull(value1),
                    nameValue2: convertNull(value2),
                    nameValue3: convertNull(value3),
                    nameValue4: convertNull(value4),
                    nameValue5: convertNull(value5),
                    nameValue6: convertNull(value6),
                    nameValue7: convertNull(value7)}
        tableData.append(tableRow)

    saveJSON(tableData)


def generate_callback():
    selections = dpg.sele('MainTableT')
    values = dpg.get_value('MainTableT')
    print(values)

    for i in range(0, 4):
        for j in range(0, 3):
            print(dpg.get_value(f"cell{i}{j}"))


# Add new Row
def add_callback():
    newRow = dpg.add_table_row(parent=110)
    for j in range(0, 3):
        with dpg.table_cell(parent=newRow):
            dpg.add_input_text()


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

with dpg.window(id=100, label="Window", width=790, height=590):
    dpg.add_text("Генератор каталогов запуска Галактика ERP 9.1")
    # Buttons
    with dpg.group(horizontal=True):
        b1 = dpg.add_button(tag='bt1', label="Reload", callback=reload_callback)
        b2 = dpg.add_button(tag='bt2', label="Save", callback=save_callback)
        b3 = dpg.add_button(tag='bt3', label="Generate", callback=generate_callback)
        b4 = dpg.add_button(tag='bt4', label="Add", callback=add_callback)

    # Table
    global curTable
    curTable = dpg.table(id=110, tag='MainTableT', label='MainTableL', header_row=True, resizable=True,
                         borders_outerH=True, borders_innerH=True,
                         borders_innerV=True,
                         borders_outerV=True, policy=dpg.mvTable_SizingStretchProp)
    with curTable:
        dpg.add_table_column(label="Database Name")
        dpg.add_table_column(label="HWKey")
        dpg.add_table_column(label="Lic Galaktika")
        dpg.add_table_column(label="Lic Support")
        dpg.add_table_column(label="SQL Server")
        dpg.add_table_column(label="Galaktika Path")
        dpg.add_table_column(label="Description")

        # once it reaches the end of the columns
        for i in range(0, 4):
            with dpg.table_row():
                for j in range(0, 7):
                    with dpg.table_cell():
                        dpg.add_input_text(tag=f"cell{i}{j}", default_value=f"value{i}{j}")

global jsonFileName
jsonFileName = 'save.json'

nameValue1 = "DatabaseName"
nameValue2 = "HWKey"
nameValue3 = "LicGalaktika"
nameValue4 = "LicSupport"
nameValue5 = "SQLServer"
nameValue6 = "GalaktikaPath"
nameValue7 = "Description"

dpg.bind_font(font1)
dpg.create_viewport(title='Window', width=800, height=600)
dpg.set_primary_window(100, True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
