import numpy as np


def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n = len(seq1)
    m = len(seq2)

    # initialize scoring matrix
    score = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n + 1):
        score[i][0] = i * gap
    for j in range(m + 1):
        score[0][j] = j * gap

    # fill the matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i-1] == seq2[j-1]:
                diag = score[i-1][j-1] + match
            else:
                diag = score[i-1][j-1] + mismatch

            up = score[i-1][j] + gap
            left = score[i][j-1] + gap

            score[i][j] = max(diag, up, left)

    # traceback
    align1 = ""
    align2 = ""
    i, j = n, m

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                s = match
            else:
                s = mismatch

            if score[i][j] == score[i-1][j-1] + s:
                align1 = seq1[i-1] + align1
                align2 = seq2[j-1] + align2
                i -= 1
                j -= 1
                continue

        if i > 0 and score[i][j] == score[i-1][j] + gap:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    return score[n][m], align1, align2


def print_alignment(align1, align2):
    middle = ""
    for a, b in zip(align1, align2):
        if a == b:
            middle += "|"
        elif a == "-" or b == "-":
            middle += " "
        else:
            middle += "."
    print(f"  {align1}")
    print(f"  {middle}")
    print(f"  {align2}")


def print_scoring_matrix(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n = len(seq1)
    m = len(seq2)
    score = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n + 1):
        score[i][0] = i * gap
    for j in range(m + 1):
        score[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i-1] == seq2[j-1]:
                diag = score[i-1][j-1] + match
            else:
                diag = score[i-1][j-1] + mismatch
            score[i][j] = max(diag, score[i-1][j] + gap, score[i][j-1] + gap)

    header = "     -  " + "  ".join(f"{c:>2}" for c in seq2)
    print(header)
    for i in range(n + 1):
        label = seq1[i-1] if i > 0 else "-"
        row_str = "  ".join(f"{score[i][j]:>3}" for j in range(m + 1))
        print(f"  {label} {row_str}")


def main():
    print("=" * 60)
    print("NEEDLEMAN-WUNSCH GLOBAL SEQUENCE ALIGNMENT")
    print("=" * 60)

    print("\nScoring: match = +1, mismatch = -1, gap = -2")

    # example 1 - DNA sequences
    print("\n--- Example 1: DNA sequences ---")
    seq1 = "AGTACGCA"
    seq2 = "TATGC"
    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")

    print("\nScoring matrix:")
    print_scoring_matrix(seq1, seq2)

    score, align1, align2 = needleman_wunsch(seq1, seq2)
    print(f"\nOptimal alignment (score = {score}):")
    print_alignment(align1, align2)

    # example 2
    print("\n--- Example 2: Protein sequences ---")
    seq1 = "HEAGAWGHEE"
    seq2 = "PAWHEAE"
    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")

    score, align1, align2 = needleman_wunsch(seq1, seq2)
    print(f"\nOptimal alignment (score = {score}):")
    print_alignment(align1, align2)

    # example 3 - similar sequences
    print("\n--- Example 3: Similar sequences ---")
    seq1 = "GCATGCG"
    seq2 = "GATTACA"
    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")

    score, align1, align2 = needleman_wunsch(seq1, seq2)
    print(f"\nOptimal alignment (score = {score}):")
    print_alignment(align1, align2)

    print("\n" + "=" * 60)
    print("DYNAMIC PROGRAMMING IN NEEDLEMAN-WUNSCH")
    print("=" * 60)
    print("""
The Needleman-Wunsch algorithm is a classic example of Dynamic Programming.

Recurrence relation:
  M[i][j] = max(
    M[i-1][j-1] + s(i,j),   # match/mismatch (diagonal)
    M[i-1][j] + gap,          # gap in sequence 2 (up)
    M[i][j-1] + gap           # gap in sequence 1 (left)
  )

where s(i,j) = match if seq1[i] == seq2[j], else mismatch

Optimal substructure:
  The optimal alignment of seq1[1..i] and seq2[1..j] can be
  constructed from optimal alignments of shorter prefixes.

Overlapping subproblems:
  The same subproblems (aligning prefixes) are needed multiple
  times, so we store them in the scoring matrix.

Time complexity: O(n * m) where n and m are sequence lengths
Space complexity: O(n * m) for the scoring matrix
""")

    # --- BLOSUM62-style scoring ---
    print("=" * 60)
    print("BLOSUM62 SUBSTITUTION MATRIX")
    print("=" * 60)

    blosum62_scores = blosum62_scoring()

    seq1 = "HEAGAWGHEE"
    seq2 = "PAWHEAE"
    print(f"\nSequences: {seq1} vs {seq2}")

    print("\n  Using simple scoring (match=+1, mismatch=-1, gap=-2):")
    s1, a1, a2 = needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2)
    print(f"  Score = {s1}")
    print_alignment(a1, a2)

    print("\n  Using BLOSUM62 scoring (gap=-4):")
    s2, a1b, a2b = needleman_wunsch_blosum(seq1, seq2, blosum62_scores, gap=-4)
    print(f"  Score = {s2}")
    print_alignment(a1b, a2b)

    print("\n  BLOSUM62 uses empirically derived substitution rates from")
    print("  aligned protein sequences. Similar amino acids (like D and E)")
    print("  get positive scores, dissimilar ones get negative scores.")
    print("  This produces biologically more meaningful alignments.")

    # --- Gap penalty analysis ---
    print("\n" + "=" * 60)
    print("GAP PENALTY ANALYSIS")
    print("=" * 60)

    seq1 = "AGTACGCA"
    seq2 = "TATGC"
    print(f"\nSequences: {seq1} vs {seq2}")
    print(f"\n{'Gap Penalty':>12} {'Score':>8}  Alignment")
    print("-" * 65)

    for gap in [0, -1, -2, -3, -5, -10]:
        score, a1, a2 = needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=gap)
        gaps_count = a1.count('-') + a2.count('-')
        matches = sum(1 for x, y in zip(a1, a2) if x == y and x != '-')
        print(f"{gap:>12} {score:>8}  {a1}  (gaps={gaps_count}, matches={matches})")
        print(f"{'':>22}{a2}")

    print("\nAs gap penalty becomes more severe, the algorithm avoids")
    print("introducing gaps and prefers mismatches. With very low")
    print("gap penalties (0), it may introduce unnecessary gaps.")
    print("Finding the right gap penalty depends on the biological context.")


def blosum62_scoring():
    amino_acids = "ARNDCQEGHILKMFPSTWYV"
    raw = [
        [ 4,-1,-2,-2, 0,-1,-1, 0,-2,-1,-1,-1,-1,-2,-1, 1, 0,-3,-2, 0],
        [-1, 5, 0,-2,-3, 1, 0,-2, 0,-3,-2, 2,-1,-3,-2,-1,-1,-3,-2,-3],
        [-2, 0, 6, 1,-3, 0, 0, 0, 1,-3,-3, 0,-2,-3,-2, 1, 0,-4,-2,-3],
        [-2,-2, 1, 6,-3, 0, 2,-1,-1,-3,-4,-1,-3,-3,-1, 0,-1,-4,-3,-3],
        [ 0,-3,-3,-3, 9,-3,-4,-3,-3,-1,-1,-3,-1,-2,-3,-1,-1,-2,-2,-1],
        [-1, 1, 0, 0,-3, 5, 2,-2, 0,-3,-2, 1, 0,-3,-1, 0,-1,-2,-1,-2],
        [-1, 0, 0, 2,-4, 2, 5,-2, 0,-3,-3, 1,-2,-3,-1, 0,-1,-3,-2,-2],
        [ 0,-2, 0,-1,-3,-2,-2, 6,-2,-4,-4,-2,-3,-3,-2, 0,-2,-2,-3,-3],
        [-2, 0, 1,-1,-3, 0, 0,-2, 8,-3,-3,-1,-2,-1,-2,-1,-2,-2, 2,-3],
        [-1,-3,-3,-3,-1,-3,-3,-4,-3, 4, 2,-3, 1, 0,-3,-2,-1,-3,-1, 3],
        [-1,-2,-3,-4,-1,-2,-3,-4,-3, 2, 4,-2, 2, 0,-3,-2,-1,-2,-1, 1],
        [-1, 2, 0,-1,-3, 1, 1,-2,-1,-3,-2, 5,-1,-3,-1, 0,-1,-3,-2,-2],
        [-1,-1,-2,-3,-1, 0,-2,-3,-2, 1, 2,-1, 5, 0,-2,-1,-1,-1,-1, 1],
        [-2,-3,-3,-3,-2,-3,-3,-3,-1, 0, 0,-3, 0, 6,-4,-2,-2, 1, 3,-1],
        [-1,-2,-2,-1,-3,-1,-1,-2,-2,-3,-3,-1,-2,-4, 7,-1,-1,-4,-3,-2],
        [ 1,-1, 1, 0,-1, 0, 0, 0,-1,-2,-2, 0,-1,-2,-1, 4, 1,-3,-2,-2],
        [ 0,-1, 0,-1,-1,-1,-1,-2,-2,-1,-1,-1,-1,-2,-1, 1, 5,-2,-2, 0],
        [-3,-3,-4,-4,-2,-2,-3,-2,-2,-3,-2,-3,-1, 1,-4,-3,-2,11, 2,-3],
        [-2,-2,-2,-3,-2,-1,-2,-3, 2,-1,-1,-2,-1, 3,-3,-2,-2, 2, 7,-1],
        [ 0,-3,-3,-3,-1,-2,-2,-3,-3, 3, 1,-2, 1,-1,-2,-2, 0,-3,-1, 4],
    ]
    scores = {}
    for i, aa1 in enumerate(amino_acids):
        for j, aa2 in enumerate(amino_acids):
            scores[(aa1, aa2)] = raw[i][j]
    return scores


def needleman_wunsch_blosum(seq1, seq2, blosum_scores, gap=-4):
    n = len(seq1)
    m = len(seq2)

    score = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n + 1):
        score[i][0] = i * gap
    for j in range(m + 1):
        score[0][j] = j * gap

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            pair = (seq1[i-1], seq2[j-1])
            sub_score = blosum_scores.get(pair, -1)

            diag = score[i-1][j-1] + sub_score
            up = score[i-1][j] + gap
            left = score[i][j-1] + gap
            score[i][j] = max(diag, up, left)

    align1 = ""
    align2 = ""
    i, j = n, m

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            pair = (seq1[i-1], seq2[j-1])
            sub_score = blosum_scores.get(pair, -1)

            if score[i][j] == score[i-1][j-1] + sub_score:
                align1 = seq1[i-1] + align1
                align2 = seq2[j-1] + align2
                i -= 1
                j -= 1
                continue

        if i > 0 and score[i][j] == score[i-1][j] + gap:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

    return score[n][m], align1, align2


if __name__ == "__main__":
    main()
