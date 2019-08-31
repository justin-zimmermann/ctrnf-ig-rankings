import write_ranking_for_mode


def main():
    tracks = {
        "Crash Cove":(1,30),
              "Roo Tubes": (3,50),
        "Mystery Caves": (5, 30),
        "ss": (7, 30),
        "sc": (9, 30),
        "tt": (11, 30),
              "Coco Park": (13, 30),
        "Tiger Temple": (15, 80),
        "pap": (17, 100),
        "dc": (19, 80),
              "Blizzard Bluff": (21, 30),
        "dm": (23, 30),
        "pop": (25, 30),
        "ta": (27, 30),
        "ngl": (29, 800),
        "cc": (31, 30),
        "has": (23, 30),
        "os": (35, 30),
        "ii": (39, 30),
        "jb": (41, 30),
        "tit": (43, 30),
        "mg": (45, 30),
        "br": (47, 30),
        "dsd": (49, 30),
        "oot": (51, 30),
        "cw": (53, 30),
        "ts": (55, 800),
        "al": (57, 30),
        "aa": (59, 30),
        "ea": (61, 50),
        "hs": (63, 30),
        "twt": (77, 30),
        "prp": (79, 30),
        "spc": (81, 30),
              }
    for value in tracks.values():
        write_ranking_for_mode.main(value[1], value[0])

if __name__ == "__main__":
    main()