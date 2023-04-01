import os
import win32com.client as wincl


def run_macro(path):

    if os.path.exists(path):
        macro = wincl.Dispatch("Excel.Application")
        workbook = macro.Workbooks.Open(Filename=path)
        try:
            macro.Application.Run("Module_Name.Macro_Name")
            workbook.Save()
        except Exception as e:
            print(e)
        finally:
            macro.Application.Quit()
            del macro


if __name__ == "__main__":
    file_path = "Excel-File.xlsm"
    run_macro(file_path)
