#============================================================
import matplotlib.pyplot as plt
import pandas as pd
import os
#============================================================
def FRAME(lang_code, target, word_or_phone, flank_or_centre):

    print("FRAME: Generating source lists...")
    df = pd.DataFrame(pd.read_csv(lang_code + "_ST.csv"))
    if word_or_phone == "word":
        source_list = df["word"].to_list()
    if word_or_phone == "phone":
        source_list = df["phone"].to_list()
    source_freq = df["freq"].to_list()

    print("FRAME: Generating frame lists...")
    frame_list = []
    from_which = []
    with_freq = []
    for entry in source_list:
        word = "_" + entry + "_"
        index = list(range(len(word)))
        for pos in index:
            if flank_or_centre == "centre":
                if word[pos] == target:
                    frame = word[pos-1] + word[pos] + word[pos+1] # _ X _ 
                    frame_list.append(frame)
                    from_which.append(word)
                    with_freq.append(source_freq[source_list.index(entry)])
            if flank_or_centre == "flank":
                if word[pos] == target and pos > 1 and len(word) > 2:
                    frame = word[pos-2] + word[pos-1] + word[pos] # _ _ X
                    frame_list.append(frame)
                    from_which.append(word)
                    with_freq.append(source_freq[source_list.index(entry)])
                if word[pos] == target and pos < len(word) - 2 and len(word) > 2:
                    frame = word[pos] + word[pos+1] + word[pos+2] # X _ _
                    frame_list.append(frame)
                    from_which.append(word)
                    with_freq.append(source_freq[source_list.index(entry)])

    print("FRAME: Converting to .csv...")
    df = pd.DataFrame(list(zip(frame_list, from_which, with_freq)),
                      columns=["frame", "source", "freq"])
    df.to_csv(lang_code + "_F=" + target + ".csv",
              index = False,
              header = True)
    
    print("FRAME: Done.")
#============================================================
# e.g. FRAME("eng","n","phone","centre")
#============================================================
