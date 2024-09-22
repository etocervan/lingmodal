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
def TALLY(lang_code, target):

    print("TALLY: Generating lists...")
    df = pd.DataFrame(pd.read_csv(lang_code + "_F=" + target + ".csv"))
    frame_list = df["frame"].to_list()
    freq_list = df["freq"].to_list()

    print("TALLY: Tallying...") # PENDING EFFICIENCY
    final_frame = []
    final_tally = []
    final_weight = []
    for frame in frame_list:
        final_frame.append(frame)
        final_tally.append(frame_list.count(frame))
        weights = [] # WEIGHTS TO BE SUMMED
        index = list(range(len(frame_list)))
        for pos in index:
            if frame_list[pos] == frame:
                weights.append(freq_list[pos])
        final_weight.append(round(sum(weights),10))

    print("TALLY: Converting to .csv...")
    df = pd.DataFrame(list(zip(final_frame, final_tally, final_weight)),
                      columns = ["frame", "tally", "weight"])
    sorted = df.sort_values("tally", ascending = False)
    duplicateless = sorted.drop_duplicates(subset = ["frame"])
    duplicateless.to_csv(lang_code + "_T=" + target + ".csv",
                  index = False,
                  header = True)

    print("TALLY: Done.")
#============================================================
def VERSUS(lang_code, query, versus):

    print("VERSUS: Generating source lists...")
    df_query = pd.DataFrame(pd.read_csv(lang_code + "_T=" + query + ".csv"))
    df_versus = pd.DataFrame(pd.read_csv(lang_code + "_T=" + versus + ".csv"))
    Q_frame_in = df_query["frame"].to_list()
    Q_tally_in = df_query["tally"].to_list()
    Q_weight_in = df_query["weight"].to_list()
    V_frame_in = df_versus["frame"].to_list()
    V_tally_in = df_versus["tally"].to_list()
    V_weight_in = df_versus["weight"].to_list()

    print("VERSUS: Calculating query exclusive + overlap...")
    Q_frame_out = []
    Q_tally_out = []
    Q_weight_out = []
    V_frame_out = []
    V_tally_out = []
    V_weight_out = []
    prob_noweigh = []
    per_million = []
    index = list(range(len(Q_frame_in)))
    for pos in index:
        word = str(Q_frame_in[pos])
        if word[0] == query:
            compare = versus + word[1] + word [2] # X _ _ FLANK
        if word[1] == query:
            compare = word[0] + versus + word[2] # _ X _ CENTRE
        if word[2] == query:
            compare = word[0] + word[1] + versus # _ _ X FLANK
        Q_frame_out.append(Q_frame_in[pos])
        Q_tally_out.append(Q_tally_in[pos])
        Q_weight_out.append(Q_weight_in[pos])
        V_frame_out.append(compare)
        if compare in V_frame_in:
            V_tally_out.append(V_tally_in[V_frame_in.index(compare)])
            V_weight_out.append(V_weight_in[V_frame_in.index(compare)])
            prob_noweigh.append(round(Q_tally_in[pos] / (Q_tally_in[pos] + V_tally_in[V_frame_in.index(compare)]), 2)) # NO-WEIGHT PROBABILITY
        if compare not in V_frame_in:
            V_tally_out.append(0)
            V_weight_out.append(0)
            prob_noweigh.append(1)

    print("VERSUS: i dunk on bash :v")

    print("VERSUS: Calculating versus exclusive...")
    index = list(range(len(V_frame_in)))
    for pos in index:
        word = str(V_frame_in[pos])
        if word[0] == versus:
            compare = query + word[1] + word [2] # X _ _ FLANK
        if word[1] == versus:
            compare = word[0] + query + word[2] # _ X _ CENTRE
        if word[2] == versus:
            compare = word[0] + word[1] + query # _ _ X FLANK
        if compare not in Q_frame_in:
            V_frame_out.append(V_frame_in[pos])
            V_tally_out.append(V_tally_in[pos])
            V_weight_out.append(V_weight_in[pos])
            Q_frame_out.append(compare)
            Q_tally_out.append(0)
            Q_weight_out.append(0)
            prob_noweigh.append(0)

    print("VERSUS: Calculating weighted probabilities...")
    prob_weigh = []
    index = list(range(len(Q_frame_out)))
    for pos in index:
        up = Q_weight_out[pos] * Q_tally_out[pos]
        down = Q_weight_out[pos] * Q_tally_out[pos] + V_weight_out[pos] * V_tally_out[pos]
        if down != 0:
            prob_weigh.append(round(up/down,2))
        else:
            prob_weigh.append(1)

    print("VERSUS: Calculating per million probabilities...")
    per_million = []
    index = list(range(len(Q_frame_out)))
    for pos in index:
        up = Q_weight_out[pos]
        down = Q_weight_out[pos] + V_weight_out[pos]
        if down != 0:
            per_million.append(round(up/down,2))
        else:
            per_million.append(1)

    print("VERSUS: Calculating bimodality...") # DEFAULTS TO USING PER_MILLION 
    if len(per_million) != 0:
        bimodality = round(((per_million.count(1) + per_million.count(0)) / len(per_million)) * 100, 2) # BIMODALITY CALC
    else:
        bimodality = "DATALACK"

    print("VERSUS: Generating plot...") # DEFAULTS TO USING PER MILLION
    plt.hist(per_million, bins=10, color='black', edgecolor='white')
    plt.xlabel("P(" + query + " | Frame) vs " + versus)
    plt.ylabel("Unique Frames")
    plt.title(lang_code + " " + query + "X" + versus + " Distribution | " + str(bimodality) + "% Bimodality (per_million)")
    plt.savefig(lang_code + "=" + query + "X" + versus + ".png")
    plt.close()

    print("VERSUS: Converting to .csv...")
    df = pd.DataFrame(list(zip(Q_frame_out, Q_weight_out, Q_tally_out, V_tally_out, V_weight_out, V_frame_out, prob_noweigh, prob_weigh, per_million)),
                      columns = ["query_frame", "query_weight", "query_tally", "versus_tally", "versus_weight", "versus_frame", "prob_noweigh", "prob_weigh","per_million"])
    df.to_csv(lang_code + "=" + query + "X" + versus + ".csv",
              index = False,
              header = True)

    #print("VERSUS: Purging undesirables...") # Off by default, remove # if deletion is desired
    #os.remove(lang_code + "_F=" + query + ".csv")
    #os.remove (lang_code + "_F=" + versus + ".csv")
    #os.remove(lang_code + "_T=" + query + ".csv")
    #os.remove(lang_code + "_T=" + versus + ".csv")

    print("Done.")
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
#============================================================
#============================================================
def bimodal(lang_code, query, versus, word_or_phone, flank_or_centre):
    
    FRAME(lang_code, query, word_or_phone, flank_or_centre)
    FRAME(lang_code, versus, word_or_phone, flank_or_centre)

    TALLY(lang_code, query)
    TALLY(lang_code, versus)

    VERSUS(lang_code, query, versus)
#============================================================
#============================================================
#============================================================
lang_list = ["eng"]

for lang_code in lang_list:
    SORTTRIM(lang_code, lang_code) # Deactivate if SORTTRIM files have already been generated.
    #pairs = MATRIX(lang_code, "phone") # Default function: generates query/versus pairs from the 10 most common phonemes.

    pairs = ["mn"]
    for pair in pairs:
        bimodal(lang_code, pair[0], pair[1], "phone", "centre") # Only touch "word_or_phone" and "flank_or_centre."
                                                                # Everything else runs automatically.
#============================================================
#============================================================
#============================================================