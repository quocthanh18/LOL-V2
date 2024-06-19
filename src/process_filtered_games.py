def main():
    with open("data/filtered__matches.txt") as f:
        matches = f.read().splitlines()
    new_matches = set()
    for match in matches:
        tmp_match = eval(match)
        if not (tmp_match[-2] == False and tmp_match[-1] == False) or (tmp_match[-2] == True and tmp_match[-1] == True):
            new_matches.update([tmp_match[0]])
    new_matches = list(new_matches)
    for idx, i in enumerate(range(0, len(new_matches), 30000)):
        with open(f"data/batch_{idx}.txt", "w") as f:
            f.write("\n".join(new_matches[i:i+30000]))

if __name__ == "__main__":
    main()