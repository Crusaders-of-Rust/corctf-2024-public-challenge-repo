"""solution.py"""
import re
import socket


def create_vector_representations(n: int) -> list[list[int]]:
    """
    Create vector representations for each position on the n x n board.

    Args:
        n (int): The size of the board (n x n).

    Returns:
        list[list[int]]: A list of vectors representing the effect of
                           toggling each light.
    """
    vectors = []
    for i in range(n * n):
        vector = [0] * (n * n)
        vector[i] = 1
        if i % n != 0:
            vector[i - 1] = 1  # left
        if i % n != n - 1:
            vector[i + 1] = 1  # right
        if i >= n:
            vector[i - n] = 1  # up
        if i < n * (n - 1):
            vector[i + n] = 1  # down
        vectors.append(vector)
    return vectors


def create_augmented_matrix(vectors: list[list[int]],
                            board: list[int]) -> list[list[int]]:
    """
    Create an augmented matrix from the vectors and board state.

    Args:
        vectors (list[list[int]]): The vector representations.
        board (list[int]): The current state of the board.

    Returns:
        list[list[int]]: The augmented matrix.
    """
    matrix = [vec + [board[i]] for i, vec in enumerate(vectors)]
    return matrix


def gauss_jordan_elimination(matrix: list[list[int]]) -> list[list[int]]:
    """
    Perform Gauss-Jordan elimination on the given matrix to produce its
    Reduced Row Echelon Form (RREF).

    Args:
        matrix (list[list[int]]): The matrix to be reduced.

    Returns:
        list[list[int]]: The matrix in RREF.
    """
    rows, cols = len(matrix), len(matrix[0])
    r = 0
    for c in range(cols - 1):
        if r >= rows:
            break
        pivot = None
        for i in range(r, rows):
            if matrix[i][c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        if r != pivot:
            matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        for i in range(rows):
            if i != r and matrix[i][c] == 1:
                for j in range(cols):
                    matrix[i][j] ^= matrix[r][j]
        r += 1
    return matrix


def is_solvable(matrix: list[list[int]]) -> bool:
    """
    Check if the given augmented matrix represents a solvable system.

    Args:
        matrix (list[list[int]]): The augmented matrix.

    Returns:
        bool: True if the system is solvable, False otherwise.
    """
    rref = gauss_jordan_elimination(matrix)
    for row in rref:
        if row[-1] == 1 and all(val == 0 for val in row[:-1]):
            return False
    return True


def get_solution(board: list[int], n: int) -> list[int] | None:
    """
    Get a solution for the Lights Out board if it exists.

    Args:
        board (list[int]): The current state of the board.
        n (int): The size of the board (n x n).

    Returns:
        list[int] | None: A list representing the solution, or None
                            if no solution exists.
    """
    vectors = create_vector_representations(n)
    matrix = create_augmented_matrix(vectors, board)
    if not is_solvable(matrix):
        return None
    rref_matrix = gauss_jordan_elimination(matrix)
    return [row[-1] for row in rref_matrix[:n * n]]


def connect_to_server(host: str, port: int) -> None:
    """
    Connects to a server, reads the Lights Out board,
    solves it, sends the solution back, then retrieves
    and prints the flag.

    Args:
        host (str): The server's hostname or IP address.
        port (int): The server's port number.

    Returns:
        None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        try:
            buffer = ""
            while True:
                data = s.recv(1024).decode(
                    "utf-8")  # Read data from the server
                if not data:
                    break
                buffer += data

                # Extract the board from the received data
                matches = re.findall(
                    r"Lights Out Board:\n\n([\s\S]*?)\n\nYour Solution: ",
                    buffer)
                if matches:
                    board_str = matches[-1]
                    n = len(board_str.strip().split("\n"))
                    board = [
                        1 if char == "#" else 0 for char in board_str
                        if char in "#."
                    ]

                    # Solve the Lights Out board
                    solution = get_solution(board, n)

                    # Convert solution back to # and .
                    if solution:
                        solution_str = "".join("#" if val == 1 else "."
                                               for val in solution)

                        # Send the solution back to the server
                        s.sendall((solution_str + "\n").encode("utf-8"))

                        # Get and print flag
                        flag = s.recv(1024).decode("utf-8")
                        print(flag)

                    # Exit the loop after retrieving the flag
                    break

        except KeyboardInterrupt:
            print("Connection closed by user.")
        finally:
            s.close()


if __name__ == "__main__":
    SERVER_HOST = "be.ax"  # Replace with the server's IP address
    SERVER_PORT = 32421  # Replace with the server's port number
    connect_to_server(SERVER_HOST, SERVER_PORT)
