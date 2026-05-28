import pandas as pd


def parse_xlsx(file_path):

    excel = pd.ExcelFile(file_path)

    text = []

    for sheet in excel.sheet_names:

        df = excel.parse(sheet)

        text.append(
            f"Sheet: {sheet}"
        )

        text.append(
            df.to_string()
        )

    return "\n".join(text)