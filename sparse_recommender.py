class SparseMatrix:
    def __init__(self):
        self.matrix = {}

    def set(self, row, col, value):
        if value < 0:
            raise ValueError("Value must be non-negative.")

        if value != 0:
            self.matrix[(row, col)] = value
        elif (row, col) in self.matrix:
            del self.matrix[(row, col)]
            
    def get(self, row, col):
        if row < 0 or col < 0:
            raise ValueError("Invalid row or column index")
        
        max_row = max(row for row, _ in self.matrix.keys()) + 1 if self.matrix else 0
        max_col = max(col for _, col in self.matrix.keys()) + 1 if self.matrix else 0

        if row >= max_row or col >= max_col:
            raise ValueError("Invalid row or column index")  # Raise a ValueError here
        return self.matrix.get((row, col), 0)
    
    def recommend(self, vector):
        # Multiplies the sparse matrix with a given vector to produce recommendations
        recommendations = []

        cols = len(vector)  # Determine the number of columns from the length of the vector
        cols = max(col for _, col in self.matrix.keys()) + 1 if self.matrix else 0  # Calculate the number of columns

        if len(vector) != cols:
         raise ValueError("The dimension of the user vector does not match the number of columns in the sparse matrix.")

        for row in range(cols):  # Iterate over rows
            recommendation = 0
            for col, value in self.matrix.items():  # Iterate over matrix items
                if col[1] == row:  # Check if the column index matches the row index
                    recommendation += value * vector[col[0]]
            recommendations.append(recommendation)

        return recommendations
    
    def add_movie(self, movie_matrix):
        """
        Adds another sparse matrix to the current matrix.
        
        Args:
            movie_matrix (dict): Sparse matrix representing the new movie's ratings.
        
        Returns:
            dict: The merged sparse matrix.
        """
        for (row, col), value in movie_matrix.items():
            if value < 0:
                raise ValueError("Value must be non-negative.")
            if value != 0:
                self.matrix[(row, col)] = value
            elif (row, col) in self.matrix:
                del self.matrix[(row, col)]
        return self.matrix

    
    def to_dense(self):
        # Determine the number of rows and columns
        num_rows = max(row for row, _ in self.matrix.keys()) + 1 if self.matrix else 0
        num_cols = max(col for _, col in self.matrix.keys()) + 1 if self.matrix else 0

        # Initialize a dense matrix filled with zeros
        dense_matrix = [[0] * num_cols for _ in range(num_rows)]

        # Fill in the dense matrix with non-zero values from the sparse matrix
        for (row, col), value in self.matrix.items():
            dense_matrix[row][col] = value

        return dense_matrix
