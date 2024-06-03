def findMin(A, K):
    min_chocolate = 1
    n = len(A)

    # Simulate each day
    for day in range(K):
        # Find the next smallest chocolate not removed by this day's process
        current = min_chocolate
        for i in range(n):
            if A[i] >= current:
                if A[i] == current:
                    current += 1  # Skip this chocolate since it's taken
                else:
                    break  # Found the smallest missing chocolate for this day
        # Update the minimum chocolate for the next day's calculation
        min_chocolate = current

    return min_chocolate

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = [int(data[i + 1]) for i in range(N)]
K = int(data[N + 1])

# Call the function and print result
print(findMin(A, K))
