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


if __name__ == "__main__":
    main()
