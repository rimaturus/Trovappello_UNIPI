import pandas as pd

days_before_month = {
    "gennaio": 0,
    "febbraio": 31,
    "marzo": 59,
    "aprile": 90,
    "maggio": 120,
    "giugno": 151,
    "luglio": 181,
    "agosto": 212,
    "settembre": 243,
    "ottobre": 273,
    "novembre": 304,
    "dicembre": 334
}


def chronological_reordering(csv_path):
    df = pd.read_csv(csv_path, sep='\t', index_col=0)

    reordering_idx = []
    for date_str in df[df.columns[4]]:
        day, month = date_str.split(" ")[1:3]
        
        weight = int(day) + days_before_month[month]
        reordering_idx.append(weight)
    
    sorted_idx = sorted(range(len(reordering_idx)), key=lambda k: reordering_idx[k])
    df = df.iloc[sorted_idx]
    df.to_csv(csv_path, sep='\t', index=True)

    

if __name__ == "__main__":
    csv_path = "/home/edo/Desktop/Appello2_Inverno2024_STUDENTI3_filtered.csv"
    chronological_reordering(csv_path)