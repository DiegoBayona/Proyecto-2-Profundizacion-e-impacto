import pandas as pd

icfes = pd.read_csv('data/icfes_limpio_2020_2023.csv', dtype={'codigo_divipola': str})
print(icfes.groupby('anio')['codigo_divipola'].count())