def load_sparse_matrix(filename):
    """Reads a sparse matrix from a file in the specified format."""
    with open(filename, 'r') as file:
        rows, cols = [int(file.readline().strip().split('=')[1]) for _ in range(2)]
        sparse_matrix = {}
        for line in file:
            if line.strip():
                try:
                    r, c, v = [int(x) for x in line.strip()[1:-1].split(',')]
                    if r not in sparse_matrix:
                        sparse_matrix[r] = {}
                    sparse_matrix[r][c] = v
                except ValueError:
                    raise ValueError("Incorrect format in input file.")
    return sparse_matrix


def perform_matrix_operation(matrix1, matrix2, operation):
    """Performs addition, subtraction, or multiplication of two matrices."""
    rows1, cols1 = max(matrix1.keys()) + 1, max(max(row.keys()) for row in matrix1.values()) + 1
    rows2, cols2 = max(matrix2.keys()) + 1, max(max(row.keys()) for row in matrix2.values()) + 1

    if operation in ['add', 'subtract']:
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError("Matrices must have compatible dimensions.")
    elif operation == 'multiply':
        if cols1 != rows2:
            raise ValueError("Matrices must have compatible dimensions.")

    result = {}
    
    if operation == 'add':
        for i in range(rows1):
            for j in range(cols1):
                result[i] = result.get(i, {})
                result[i][j] = matrix1.get(i, {}).get(j, 0) + matrix2.get(i, {}).get(j, 0)
                
    elif operation == 'subtract':
        for i in range(rows1):
            for j in range(cols1):
                result[i] = result.get(i, {})
                result[i][j] = matrix1.get(i, {}).get(j, 0) - matrix2.get(i, {}).get(j, 0)
                
    elif operation == 'multiply':
        for i in range(rows1):
            for j in range(cols2):
                result[i] = result.get(i, {})
                result[i][j] = sum(matrix1.get(i, {}).get(k, 0) * matrix2.get(k, {}).get(j, 0) for k in range(cols1))

    return result


def save_matrix_to_file(matrix, output_file):
    """Writes the matrix to a file in the specified format."""
    with open(output_file, 'w') as file:
        rows, cols = max(matrix.keys()) + 1, max(max(row.keys()) for row in matrix.values())
        file.write(f"rows={rows}\n")
        file.write(f"cols={cols}\n")
        for i, row in matrix.items():
            for j, val in row.items():
                if val != 0:  # Only write non-zero values
                    file.write(f"({i}, {j}, {val})\n")


def main():
    """Main function to handle user input and matrix operations."""
    try:
        file1 = input("Input the path of the first file: ")
        file2 = input("Input the path of the second file: ")
        operation = input("What operation do you want to perform [add, subtract, multiply]: ")
        output_file = input("What's the name of the output file: ") or f"matrix_{operation}.txt"

        matrix1 = load_sparse_matrix(file1)
        matrix2 = load_sparse_matrix(file2)

        if operation in ['add', 'subtract', 'multiply']:
            result = perform_matrix_operation(matrix1, matrix2, operation)
            print(f"Matrix {operation}:")
            save_matrix_to_file(result, output_file)

        else:
            raise ValueError("Invalid operation")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
