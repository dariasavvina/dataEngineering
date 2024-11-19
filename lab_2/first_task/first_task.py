import numpy as np
import json

from lab_2.fifth_task.fifth_task import new_df

matrix = np.load('first_task.npy')


sum_matrix = int(np.sum(matrix))

mean_matrix = float(np.mean(matrix))

main_diagonal = np.diag(matrix)
side_diagonal = np.diag(np.rot90(matrix))

sum_main_diagonal = int(np.sum(main_diagonal))
sum_side_diagonal = int(np.sum(side_diagonal))

mean_main_diagonal = float(np.mean(main_diagonal))
mean_side_diagonal = float(np.mean(side_diagonal))

min_matrix = int(np.min(matrix))
max_matrix = int(np.max(matrix))

dict = {
    "sum": sum_matrix,
    "avr": mean_matrix,
    "sumMD": sum_main_diagonal,
    "avrMD": mean_main_diagonal,
    "sumSD": sum_side_diagonal,
    "avrSD": mean_side_diagonal,
    "max": max_matrix,
    "min": min_matrix
}


normalize_matrix = matrix / mean_matrix



json_object = json.dumps(dict, indent=4)

with open('first_task_result.json', 'w') as outfile:
        outfile.write(json_object)

with open('first_task_answer.npy', 'wb') as f:
    np.save(f, normalize_matrix)




