import pandas as pd

df = pd.read_html('fifth_task.html', encoding='utf-8')

df = df[0]

df.to_csv('fifth_task_result.csv', header=True, index=False)