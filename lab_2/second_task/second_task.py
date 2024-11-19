import numpy as np
import os

matrix = np.load('second_task.npy')

x = []
y = []
z = []

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] > 582:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])
        else:
            continue


with open('second_task_result.npz', 'wb') as outfile:
    np.savez(outfile, x=x, y=y, z=z)

with open('second_task_result_compressed.npz', 'wb') as outfile:
    np.savez_compressed(outfile, x=x, y=y, z=z)


file_info = os.stat('second_task_result.npz')
file_info_compressed = os.stat('second_task_result_compressed.npz')
file_size = file_info.st_size
file_size_compressed = file_info_compressed.st_size

print(f" Разница между файлом second_task_result.npz и second_task_result_compressed.npz {file_size - file_size_compressed} байт")