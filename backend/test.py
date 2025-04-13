from src import etoro_data

file = open("./etoro-account-statement-1-12-2015-4-12-2025.xlsx", "rb").read()
df = etoro_data.extract_closed_position(file)
print(df)
