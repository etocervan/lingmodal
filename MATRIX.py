#============================================================
import matplotlib.pyplot as plt
import pandas as pd
import os
#============================================================
def MATRIX(lang_code, word_or_phone):
    
    print("MATRIX: Generating input list...")
    if word_or_phone == "phone":
        df = pd.DataFrame(pd.read_csv(lang_code + "_ST_DC=phone.csv"))
    elif word_or_phone == "word":
        df = pd.DataFrame(pd.read_csv(lang_code) + "ST_DC=word.csv")
    symbol_list = df["symbol"].to_list()

    print("MATRIX: Generating query-versus list...")
    matrix = []
    for query in symbol_list[0:10]: # TOP_WHAT = 10
        for versus in symbol_list[0:10]: # TOP_WHAT = 10
            if query != versus:
                matrix.append(query + versus)

    return matrix
#============================================================
#e.g. print(MATRIX("eng","phone"))
#============================================================