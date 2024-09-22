#============================================================
import matplotlib.pyplot as plt
import pandas as pd
import os
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

    print("VERSUS: Purging undesirables...") # Off by default, remove # if deletion is desired
    #os.remove(lang_code + "_F=" + query + ".csv")
    #os.remove (lang_code + "_F=" + versus + ".csv")
    #os.remove(lang_code + "_T=" + query + ".csv")
    #os.remove(lang_code + "_T=" + versus + ".csv")

    print("Done.")
#============================================================
# e.g. VERSUS("eng","m","n")
#============================================================