def analyzeRow(row):
    prevI = ""
    for i in row:
        if i == 0 or prevI == i:
            return "CanMove"
        prevI = i
    return "CantMove"

print(analyzeRow([4,16]))