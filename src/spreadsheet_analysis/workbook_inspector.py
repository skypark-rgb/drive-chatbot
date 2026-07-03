import pandas as pd


class WorkbookInspector:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def inspect(self):
        excel_file = pd.ExcelFile(self.file_path)

        workbook_summary = []

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
            )

            columns = [
                str(column)
                for column in df.columns
            ]

            numeric_columns = [
                str(column)
                for column in df.select_dtypes(include="number").columns
            ]

            workbook_summary.append(
                {
                    "sheet_name": sheet_name,
                    "row_count": len(df),
                    "columns": columns,
                    "numeric_columns": numeric_columns,
                }
            )

        return workbook_summary


if __name__ == "__main__":
    print("Workbook inspector is running")

    inspector = WorkbookInspector(
        input("Excel file path: ")
    )

    summary = inspector.inspect()

    for sheet in summary:
        print()
        print(f"Sheet: {sheet['sheet_name']}")
        print(f"Rows: {sheet['row_count']}")
        print("Columns:")
        for column in sheet["columns"]:
            print(f"  - {column}")

        print("Numeric Columns:")
        for column in sheet["numeric_columns"]:
            print(f"  - {column}")