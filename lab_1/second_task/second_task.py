import re


def extract_negative_number(number_str: str) -> [int]:
    pattern = r'-[0-9]+'
    negative_numbers = re.findall(pattern, number_str)
    numbers = map(lambda num: int(num), negative_numbers)
    return numbers


def sum_negative_numbers(negative_numbers: [int]) -> int:
    numbers = map(lambda num: abs(num), negative_numbers)
    sums = sum(numbers)
    return sums


def mean_numbers(sums: [int]) -> int:
    mean = sum(sums) / len(sums)
    return mean


with open('second_task.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()

negative_numbers = map(extract_negative_number, lines)
sums_negative_numbers = list(map(sum_negative_numbers, negative_numbers))
mean_numbers = mean_numbers(sums_negative_numbers)
sum_column_str = '\n'.join(map(str, sums_negative_numbers))

result_str = f'{sum_column_str}\n\n{mean_numbers}'
with open('second_task_results.txt', mode='w', encoding='utf-8') as res_f:
    res_f.write(result_str)
