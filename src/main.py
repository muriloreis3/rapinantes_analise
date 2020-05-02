import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calc_percentage(df, column, decimals=2):
    """ Returns a series with the percentages of a column"""
    return (df[column].value_counts(normalize=True)).round(decimals).rename('Porcentagem')

def clean_file(f):
    df = pd.read_excel(f)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if isinstance(col, str):
            df[col] = df[col].str.strip()
    return df

def load_ordens(df):
    ordens = ['ACCIPITRIFORMES', 'CATHARTIFORMES', 'STRIGIFORMES', 'FALCONIFORMES']
    lst = []
    for ordem in ordens:
        ord = clean_file('src/files/'+ordem+'.xlsx')
        for nome in ord[ordem].unique():
            lst.append((nome, ordem))
        especies = pd.DataFrame(lst).set_index(0)[1].rename('ORDEM')
    df = df.merge(especies, left_on='ESPÉCIE', right_index=True).reset_index(drop=True)
    df.to_excel('output/full_table.xlsx')
    return df

def pieplot(df, path, title=''):
    _, ax = plt.subplots(figsize=(8,6))
    ax.pie(df, autopct='%1.1f%%', pctdistance=1.1)
    plt.title(title)
    plt.legend(labels=df.index, bbox_to_anchor=(0.9, 1.0), loc="best")
    plt.tight_layout()
    plt.savefig(path)

df = clean_file('src/files/rapinantes_anual.xlsx')
df['DATA'].replace({'jan':'Jan'}, inplace=True)

pieplot(df['ESPÉCIE'].value_counts(normalize=True).round(4),'output/numero_especies_anual.png')

meses = df['DATA'].unique()
df = load_ordens(df)
porcentagem_animais = df["ESPÉCIE"].value_counts(normalize=True).round(4)
porcentagem_motivo_entrada = calc_percentage(df.groupby(['ESPÉCIE']), 'MOTIVO DE ENTRADA', 4)
df_plot = porcentagem_motivo_entrada.reset_index()
porcentagem_motivo_entrada = porcentagem_motivo_entrada.unstack(level=-1, fill_value=0)
g = sns.catplot(kind='bar', x='MOTIVO DE ENTRADA', y='Porcentagem', data=df_plot, col='ESPÉCIE', col_wrap=6, legend=True)
g.set_xticklabels(rotation=90)
plt.tight_layout()
plt.savefig('output/porcentagem_motivo_entrada.png')
porcentagem_motivo_entrada['Total'] = porcentagem_animais
porcentagem_motivo_entrada.to_excel('output/porcentagem_motivo_entrada.xlsx')

porcentagem_traumas = df['MOTIVO DE ENTRADA'].value_counts(normalize=True).round(4)
pieplot(porcentagem_traumas, 'output/porcentagem_traumas.png')
porcentagem_traumas.to_excel('output/porcentagem_traumas.xlsx')

porcentagem_ordem_mes = calc_percentage(df.groupby('DATA'), 'ORDEM', 4).reindex(meses, level=0)
df_plot = porcentagem_ordem_mes.reset_index()
porcentagem_ordem_mes = porcentagem_ordem_mes.unstack(level=-1, fill_value=0)
g = sns.catplot(kind='bar', x='ORDEM', y='Porcentagem', data=df_plot, col='DATA', col_wrap=6, legend=False)
g.set_xticklabels(rotation=90)
plt.tight_layout()
plt.savefig('output/porcentagem_ordem_mes.png')
porcentagem_ordem_mes.to_excel('output/porcentagem_ordem_mes.xlsx')

porcentagem_ordem_anual = df['ORDEM'].value_counts(normalize=True)
pieplot(porcentagem_ordem_anual, 'output/porcentagem_ordem_anual.png')
porcentagem_ordem_anual.to_excel('output/porcentagem_ordem_anual.xlsx')

porcentagem_ordem_motivo_entrada = calc_percentage(df.groupby('ORDEM'), 'MOTIVO DE ENTRADA', 4)
porcentagem_ordem_motivo_entrada.unstack(level=-1, fill_value=0).to_excel('output/porcentagem_ordem_motivo_entrada.xlsx')

for ordem in df['ORDEM'].unique():
    pieplot(porcentagem_ordem_motivo_entrada.loc[ordem], 'output/'+ordem+'.png', ordem)