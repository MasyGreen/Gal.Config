import json
import os.path
import shutil

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


def table_to_list():
    tabledata = []  # Table to List
    tabledata.clear()

    rows = dpg.get_item_children('MTable', 1)
    rind: int = 0
    for row in rows:  # row collection
        rind = rind + 1
        cols = dpg.get_item_children(row, 1)  # column in row collection

        cind: int = 0
        tablerow = {}  # Row to Dic
        for col in cols:  # Col collection
            cind = cind + 1
            cell = dpg.get_item_children(col, 1)[0]  # cell contain 'input text' item
            tablerow[arrayColName.get(cind)] = convertNull(dpg.get_value(cell))

        tabledata.append(tablerow)
    return tabledata


# Save all value from List.Table and save to JSON
def save_callback():
    saveJSON(table_to_list())


# Generate File
def generate_callback():
    resultpath = dpg.get_value('prpath')

    newDir = os.path.join(os.getcwd(), "Generate")
    newDir910 = os.path.join(newDir, "910")
    newDirLic = os.path.join(newDir, "Lic")
    newDirODBC = os.path.join(newDir, "ODBC")
    shutil.rmtree(newDir, ignore_errors=True, onerror=None)
    if not os.path.exists(newDir):
        os.makedirs(newDir)
        os.makedirs(newDir910)
        os.makedirs(newDirLic)
        os.makedirs(newDirODBC)

        tabledata = table_to_list()  # Table to List

        for db in tabledata:
            curDir = os.path.join(newDir910, db[arrayColName[1]])
            os.makedirs(curDir)
            # ------------------------------------------------
            with open(os.path.join(curDir, 'SETS.BAT'), 'w', encoding='utf-8') as f:
                f.write(f'rem ключ Галактика\n')
                f.write(f'set LICGAL={db[arrayColName[3]]}\n')
                f.write(f'rem ключ Support\n')
                f.write(f'set LICSUP={db[arrayColName[4]]}\n')
                f.write(f'rem путь сборки Галактика\n')
                f.write(f'set GALPATH={db[arrayColName[6]]}\n')

            with open(os.path.join(curDir, 'DATABASE.INC'), 'w', encoding='utf-8') as f:
                f.write(f'!{db[arrayColName[7]]}\n')
                f.write(f'[SQLDriver]\n')
                f.write(f'  SQLServer=ncacn_ip_tcp:{db[arrayColName[5]]}[1997] \n')
                f.write(f'  FullLoginName=On\n')
                f.write(f'  ForceRights=On\n')
                f.write(f'  UseSQLRole=On\n\n')
                f.write(f'[DataBase]\n')
                f.write(f'  DatabaseName={db[arrayColName[1]]}\n')
                f.write(f'  FiltersResource=%USER%\\filters.res\n')
                f.write(f'  DataBaseDriver=MS70DRV.DLL\n')
                f.write(f'  CheckRepository=off\n')
                f.write(f'  UserTablesLocalCache=On\n')
                f.write(f'  SolidJournalClear=0\n')

            # ------------------------------------------------
            curDirGalaktika = os.path.join(curDir, "Galaktika")
            os.makedirs(curDirGalaktika)
            with open(os.path.join(curDirGalaktika, 'wingal.bat'), 'w', encoding='utf-8') as f:
                f.write('rem if exist dsk rd /S /Q dsk\n')
                f.write('if exist out rd /S /Q out\n')
                f.write('if exist data rd /S /Q data\n')
                f.write('if exist tmp  rd tmp\n')
                f.write('if exist *.tmp del *.tmp\n')
                f.write('if exist *.log del *.log\n')
                f.write('if exist Atlantis*.res del Atlantis*.res\n\n')
                f.write('@ECHO OFF\n')
                f.write('rem настройка пути к БД\n')
                f.write(f'set BUILD={resultpath}\910\{db[arrayColName[1]]}\\\n')
                f.write('rem копируем файл локально\n')
                f.write('COPY %BUILD%\SETS.BAT ..\SETS.BAT /y\n')
                f.write('rem переменные БД\n')
                f.write('@call ..\SETS.BAT\n')
                f.write('rem запуск\n')
                f.write(r'@start %GALPATH%\galaktika\exe\atlexec.exe /c:wingal.cfg')

            with open(os.path.join(curDirGalaktika, 'wingal.cfg'), 'w', encoding='utf-8') as f:
                f.write(f'#include {resultpath}\hwkey9.inc\n')
                f.write(f'#include {resultpath}\910\StartUp.inc\n')
                f.write(f'#include {resultpath}\910\AllParams.inc\n')
                f.write(f'#include {resultpath}\910\%USERNAME%.inc\n')
                f.write(f'#include %BUILD%\DATABASE.INC\n')
                f.write(f'[licparam]\n')
                f.write(f'licfilename=%LICGAL%\n')

            # ------------------------------------------------
            curDirPatchManager = os.path.join(curDir, "PatchManager")
            os.makedirs(curDirPatchManager)

            # ------------------------------------------------
            curDirSupport = os.path.join(curDir, "Support")
            os.makedirs(curDirSupport)

            # ------------------------------------------------
            curDirViper = os.path.join(curDir, "Viper")
            os.makedirs(curDirViper)
            print(db)


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
        with dpg.font(r"C:\Windows\Fonts\arial.ttf", 14) as font1:
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

    dpg.bind_font(font1)

    with dpg.window(id='MWindow', label="Window", width=790, height=590):
        dpg.add_text("Генератор каталогов запуска Галактика ERP 9.1")
        # Buttons
        with dpg.group(horizontal=True):
            dpg.add_button(tag='bt1', label="Reload", callback=reload_callback)
            dpg.add_button(tag='bt2', label="Save", callback=save_callback)
            dpg.add_button(tag='bt3', label="Generate", callback=generate_callback)
            dpg.add_button(tag='bt4', label="Add", callback=add_callback)

        with dpg.group(horizontal=True):
            dpg.add_text("Каталог назначения: ")
            dpg.add_input_text(tag='prpath', default_value=r't:\configSrv')

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

    #dpg.add_additional_font(file=r"C:\Windows\Fonts\arial.ttf", size=14, glyph_ranges='cyrillic')
    dpg.create_viewport(title='Window', width=800, height=600)
    dpg.set_primary_window('MWindow', True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    global jsonFileName

    jsonFileName = os.path.join(os.getcwd(), 'save.json')

    global arrayColName
    arrayColName = {1: "DatabaseName",
                    2: "HWKey",
                    3: "LicGalaktika",
                    4: "LicSupport",
                    5: "SQLServer",
                    6: "GalaktikaPath",
                    7: "Description"}

    main()
