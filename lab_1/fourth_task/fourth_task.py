import pandas as pd

df = pd.read_csv('fourth_task.txt')

df = df.drop('rating', axis=1)

mean_value_quantity = df.loc[:, 'quantity'].mean()
max_value_price = df.loc[:, 'price'].max()
min_value_price = df.loc[:, 'price'].min()

df = df[df['status'] !='Shipping']

result_str = f'{mean_value_quantity}\n\n{max_value_price}\n\n{min_value_price}'


with open('fourth_task_results.txt', mode='w', encoding='utf-8') as res_f:
    res_f.write(result_str)

df.to_csv('fourth_task_result.csv', header=True, index=False)