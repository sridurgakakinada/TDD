import pytest

from sparse_recommender import SparseMatrix

def test_set_method():
    matrix = SparseMatrix()

    # Set a non-zero value at (1, 2)
    matrix.set(1, 2, 5)
    assert matrix.matrix == {(1, 2): 5}
    
    # Set a non-zero value at (0, 0)
    matrix.set(0, 0, 2)
    assert matrix.matrix == {(1, 2): 5, (0, 0): 2}

    # Set a zero value at (1, 2)
    matrix.set(1, 2, 0)
    assert matrix.matrix == {(0, 0): 2}

    # Set a zero value at (2, 3)
    matrix.set(2, 3, 0)
    assert matrix.matrix == {(0, 0): 2}

    # Set a non-zero value at (2, 3)
    matrix.set(2, 3, 7)
    assert matrix.matrix == {(0, 0): 2, (2, 3): 7}
    
    # Attempting to set a negative number
    with pytest.raises(ValueError) as excinfo:
        matrix.set(1, 0, -3)
        
    # Check if the ValueError message contains the expected text
    expected_message = "Value must be non-negative."
    assert expected_message in str(excinfo.value)

def test_get_method():
    # Create a matrix and set some values
    matrix = SparseMatrix()
    matrix.set(0, 0, 2)
    matrix.set(1, 1, 5)
    matrix.set(2, 2, 7)

    # Test getting values that are present in the matrix
    assert matrix.get(0, 0) == 2
    assert matrix.get(1, 1) == 5
    assert matrix.get(2, 2) == 7

    # Test getting values that are not present in the matrix
    assert matrix.get(0, 1) == 0
    assert matrix.get(1, 0) == 0
    assert matrix.get(1, 2) == 0
    assert matrix.get(2, 1) == 0

    # Test getting values at negative indices using pytest.raises
    with pytest.raises(ValueError) as excinfo1:
        matrix.get(-1, -1)
    assert "Invalid row or column index" in str(excinfo1.value)

    with pytest.raises(ValueError) as excinfo2:
        matrix.get(-1, 0)
    assert "Invalid row or column index" in str(excinfo2.value)

    with pytest.raises(ValueError) as excinfo3:
        matrix.get(0, -1)
    assert "Invalid row or column index" in str(excinfo3.value)

    # Test getting values beyond the matrix size using pytest.raises
    with pytest.raises(ValueError) as excinfo4:
        matrix.get(3, 3)
    assert "Invalid row or column index" in str(excinfo4.value)

    with pytest.raises(ValueError) as excinfo5:
        matrix.get(100, 100)
    assert "Invalid row or column index" in str(excinfo5.value)

def test_recommend_method():
    matrix = SparseMatrix()  # Example: 3 rows and 4 columns
    user_vector = [2, 0, 0]  # Example user vector

    # Set some values in the matrix
    matrix.set(0, 0, 2)
    matrix.set(1, 1, 5)
    matrix.set(2, 2, 7)
    
    assert matrix.recommend(user_vector) == [4, 0, 0]
    
    # Test recommending with an invalid vector (dimension doesn't match)
    with pytest.raises(ValueError) as excinfo2:
        matrix.recommend([1, 0])
        
    # Check if the ValueError message contains the expected text
    expected_message = "The dimension of the user vector does not match the number of columns in the sparse matrix."
    assert expected_message in str(excinfo2.value)
    
def test_add_movie_method():
    matrix = SparseMatrix()

    # Set some values in the matrix
    matrix.set(0, 0, 2)
    matrix.set(1, 1, 5)

    # Create a new movie matrix
    movie_matrix = {(0, 1): 3, (2, 2): 4, (1, 1): 1}

    # Add the new movie
    result_matrix = matrix.add_movie(movie_matrix)

    # Check if the result_matrix contains both old and new movie ratings
    expected_result = {(0, 0): 2, (0, 1): 3, (1, 1): 1, (2, 2): 4}
    assert result_matrix == expected_result

    # Attempting to add a movie with a negative value
    movie_matrix_negative = {(1, 0): -2}
    with pytest.raises(ValueError) as excinfo:
        matrix.add_movie(movie_matrix_negative)

    # Check if the ValueError message contains the expected text
    expected_message = "Value must be non-negative."
    assert expected_message in str(excinfo.value)

def test_to_dense_method():
    # Create a matrix and set some values
    matrix = SparseMatrix()
    matrix.set(0, 0, 2)
    matrix.set(1, 1, 5)
    matrix.set(2, 2, 7)

    # Convert the matrix to dense
    dense_matrix = matrix.to_dense()

    # Define the expected dense matrix
    expected_dense_matrix = [
        [2, 0, 0],
        [0, 5, 0],
        [0, 0, 7]
    ]

    # Check if the dense matrix matches the expected result
    assert dense_matrix == expected_dense_matrix

    # Test converting an empty matrix to dense
    empty_matrix = SparseMatrix()
    empty_dense_matrix = empty_matrix.to_dense()
    print("empty_dense_matrix:", empty_dense_matrix)  # Add this line to print the empty_dense_matrix
    assert empty_dense_matrix == []

    # Test converting a matrix with missing rows and columns to dense
    missing_rows_matrix = SparseMatrix()
    missing_rows_matrix.set(0, 1, 3)
    missing_rows_matrix.set(2, 2, 4)
    missing_dense_matrix = missing_rows_matrix.to_dense()
    expected_missing_dense_matrix = [
        [0, 3, 0],
        [0, 0, 0],
        [0, 0, 4]
    ]
    print("missing_dense_matrix:", missing_dense_matrix)  # Add this line to print the missing_dense_matrix
    assert missing_dense_matrix == expected_missing_dense_matrix

    # Test converting a matrix with missing columns to dense
    missing_columns_matrix = SparseMatrix()
    missing_columns_matrix.set(1, 0, 3)
    missing_columns_matrix.set(2, 2, 4)
    missing_columns_dense_matrix = missing_columns_matrix.to_dense()
    print("missing_columns_dense_matrix:", missing_columns_dense_matrix)  # Add this line to print the missing_dense_matrix
    expected_missing_columns_dense_matrix = [
        [0, 0, 0],  # Adjust this line
        [3, 0, 0],
        [0, 0, 4]
    ]
    assert missing_columns_dense_matrix == expected_missing_columns_dense_matrix