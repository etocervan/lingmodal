#============================================================
import matplotlib.pyplot as plt
import pandas as pd
import os
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
# e.g. TALLY("eng", "n")
#============================================================
