from dataclasses import replace


def extract_numbers_with_na(line: str) -> [str]:
    lines_strip = line.strip()
    lines = lines_strip.split(' ')
    return lines


def transform_numbers_with_replace_na(numbers_str: [str]) -> [float]:
    result_number_list = []
    for i in range(len(numbers_str)):
        if numbers_str[i] == 'N/A':
            prev_number = float(numbers_str[i - 1])
            next_number = float(numbers_str[i + 1])
            mean = (prev_number + next_number) / 2
            result_number_list.append(mean)
        else:
            result_number_list.append(float(numbers_str[i]))
    return result_number_list


def filter_numbers(number: float) -> bool:
    return number % 2 == 0 and number > 500


with open('third_task.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()

numbers_with_na = map(extract_numbers_with_na, lines)
numbers_with_replace_na = map(transform_numbers_with_replace_na, numbers_with_na)
filtered_numbers = map(lambda num: filter(filter_numbers, num), numbers_with_replace_na)
sums = list(map(sum, filtered_numbers))
sum_column_str = '\n'.join(map(str, sums))

result_str = f'{sum_column_str}'
with open('third_task_results.txt', mode='w', encoding='utf-8') as res_f:
    res_f.write(result_str)
