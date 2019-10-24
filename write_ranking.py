import write_ranking_for_mode
""""Crash Cove": (1, 100),
        "Roo Tubes": (3, 100),
        "Mystery Caves": (5, 100),
        "ss": (7, 100),
        "sc": (9, 100),
        "tt": (11, 100),
        "Coco Park": (13, 100),
        "Tiger Temple": (15, 100),
        "pap": (17, 120),
        "dc": (19, 100),
        "Blizzard Bluff": (21, 100),
        "dm": (23, 100),
        "pop": (25, 100),
        "ta": (27, 100),
        "ngl": (29, 800),
        "cc": (31, 100),
        "has": (33,100),
        "os": (35, 100),
        "ii": (39, 100),
        "jb": (41, 100),
        "tit": (43, 100),
        "mg": (45, 100),
        "br": (47, 100),
        "dsd": (49, 100),
        "oot": (51, 100),
        "cw": (53, 100),
        "ts": (55, 800),
        "al": (57, 100),
        "nn": (59, 100),
        "ea": (61, 100),
        "hs": (63, 100),
        "twt": (77, 100),
        "prp": (79, 100),
        "spc": (81, 100),
        "aa": (83, 100)"""

def main():
    tracks = {
        "has": (33,100)
              }
    for value in tracks.values():
        write_ranking_for_mode.main(value[1], value[0])

if __name__ == "__main__":
    main()