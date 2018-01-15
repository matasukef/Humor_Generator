import pandas as pd

data = pd.read_csv('exp2_result.csv')
count = 6
all_res = ''
for i in range(1, 51):
    res = '\\begin{table}[htb]\n    \\caption{図'
    res += '\\ref{fig:experiment_images' + str(i) + '}に対応する各被験者の各発話文に対する対話継続欲求向上性に関する得点}'
    res += '\n    \\label{table_each_humor_scores_2_' + str(i) + '}\n    \\centering'
    res += '\n    \\begin{tabularx}{100mm}{CCCC}\n        \hline'
    res += '\n        被験者NO & \\(Origin\\) & \\(HL \\ Caption\) & \\(HH \\ Caption\) \\\\'
    res += '\n        \\hline\\hline'

    for j in range(0, 20):
        res += '\n        ' + str(j+1) + ' & ' + str(data.iloc[j, count]) + ' & ' + str(data.iloc[j, count+1]) + ' & ' + str(data.iloc[j, count+2]) + ' \\\\'

    res += '\n        \\hline\n    \\end{tabularx}\n\\end{table}\n\n'

    all_res += res
    res = ''

    count += 3

with open('test.tex', 'w') as f:
    f.write(all_res)
