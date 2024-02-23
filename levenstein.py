hardcode_words = ['Venom',
                  'остров собак',
                  'магия лунного света',
                  'Мстители: война бесконечности',
                  'город в котором меня нет',
                  'как витька чеснок вез леху штыря в дом инвалидов',
                  'Рататуй']




def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]




def offer(user_message):

    similar_names = []

    for i in hardcode_words:

        similar_names.append(levenstein(i, user_message))

    min_lev_dist_index = similar_names.index(min(similar_names))


    if 0 in similar_names:
        return hardcode_words[similar_names.index(0)]
    
    else:
        return 'Ой! Ошибка!\nМожет быть, вы хотели написать: ' + str(hardcode_words[min_lev_dist_index]) + '?' + '\n' + \
               'В таком случае: еще раз введите полное и правильное название :)'

