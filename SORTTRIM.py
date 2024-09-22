#============================================================
import matplotlib.pyplot as plt
import pandas as pd
import os
#============================================================
def DICER(lang_code, merge, word_or_phone):

    print("DICER: Dicing...")
    plate = merge[word_or_phone].to_list()
    diced = []
    for chunk in plate:
        for crumb in str(chunk):
            diced.append(crumb)

    print("DICER: Counting...")
    symbol_list = []
    symbol_count = []
    for crumb in diced:
        if crumb not in symbol_list: # PENDING EFFICIENCY: REMOVE ALL FROM DICED
            symbol_list.append(crumb)
            symbol_count.append(diced.count(crumb))

    print("DICER: Converting to .csv...")
    df = pd.DataFrame(list(zip(symbol_list, symbol_count)),
                      columns = ["symbol", "count"])
    df_sorted = df.sort_values("count", ascending = False)
    df_sorted.to_csv(lang_code + "_ST_DC=" + word_or_phone + ".csv",
              index = False,
              header = True)

    print("DICER: Done.")
#============================================================
def SORTTRIM(word_input, phone_input):

    print("SORTTRIM: Converting inputs to dataframes...")
    words = pd.DataFrame(pd.read_excel(word_input + ".ods", engine = "odf"))
    phones = pd.DataFrame(pd.read_table(phone_input + ".tsv", sep = "\t"))

    print("SORTTRIM: Sort-trimming word_input...")
    sorted = words.sort_values("freq", ascending = False)
    trimmed = sorted[0:20000] # TRIM_COUNT = 20,000
    word_output = trimmed["word"].str.lower().to_list()
    freq_output = trimmed["freq"].to_list()
    words = pd.DataFrame(list(zip(word_output, freq_output)),
                         columns = ["word", "freq"])

    print("SORTTRIM: Sort-trimming phone_input...")
    word_output = phones["word"].str.lower().to_list() # MERGE ON WORDS
    space_phones = phones["phone"].to_list()
    phone_output = []
    for space_phone in space_phones:
        phone_output.append(str(space_phone.replace(" ","")))
    phones = pd.DataFrame(list(zip(word_output, phone_output)),
                          columns = ["word", "phone"])

    print ("SORTTRIM: Merging word_input with phone_input...")
    merge = pd.merge(words, phones, on = "word")

    print("SORTTRIM: Saving as .csv...")
    merge.to_csv(word_input + "_ST.csv",
                  index = False,
                  header = True)

    DICER(word_input, merge, "word")
    DICER(phone_input, merge, "phone")

    print("SORTTRIM: Done.")
#============================================================
# e.g. SORTTRIM("eng", "eng")
#============================================================