import itertools
import operator
import re


with open('first_task.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()

pattern = r'[\.\?! \n]+'
split_words = itertools.chain.from_iterable(map(lambda line: re.split(pattern, line), lines))
filtered_words = filter(lambda word: word != '', split_words)
lower_words = map(lambda word: word.lower(), filtered_words)
words = list(lower_words)

dictionary = {}
for word in words:
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1


sorted_dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)

freq_words = map(lambda item: item[0] + ':' + str(item[1]), sorted_dictionary)
with open('first_task_results.txt', mode='w', encoding='utf-8') as res_f:
    res_f.write('\n'.join(freq_words))

def find_consolant_letter(word):
    pattern = r'^[qwrtpsdfghjklzxcvbnm].*$'
    return len(re.findall(pattern, word)) != 0

filtered_words_cons_letter = list(filter(find_consolant_letter, words))
count_filtered_words = len(filtered_words_cons_letter)
freq_filtered_words = (count_filtered_words / len(words)) * 100
result_str = f'Количество слов: {count_filtered_words} \nДоля: {freq_filtered_words} %'
with open('first_task_2var_results.txt', mode='w', encoding='utf-8') as res2_f:
    res2_f.write(result_str)
