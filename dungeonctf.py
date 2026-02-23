import heapq

def load_grid(filename="dungeon.txt"):
    grid = []
    with open(filename, "r") as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            grid.append(row)
    return grid

def dijkstra(grid):
    n = len(grid)

    dist = [[float('inf')] * n for _ in range(n)]
    dist[0][0] = grid[0][0]

    heap = [(grid[0][0], 0, 0)]

    while heap:
        cost, r, c = heapq.heappop(heap)

        if cost > dist[r][c]:
            continue

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n:
                new_cost = cost + grid[nr][nc]

                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return dist[n-1][n-1]

if __name__ == "__main__":
    grid = load_grid("dungeon.txt")
    min_cost = dijkstra(grid)
    print(f"Minimum path cost: {min_cost}")
    print(f"Flag: FantasyCTF{{{min_cost}}}")