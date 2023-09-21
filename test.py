
import pytest
from sparse_recommender import SparseMatrix

def test_set_get():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(3, 3)
    # Set a value
    matrix.set(0, 0, 1)
    # Test if the set value is retrieved correctly
    assert matrix.get(0, 0) == 1
    matrix.set(1, 1, 3)
    assert matrix.get(1, 1) == 3
    matrix.set(2, 2, 4)
    assert matrix.get(2, 2) == 4

    # Attempt to set a negative value in the matrix
    with pytest.raises(ValueError) as excinfo:
        matrix.set(0, 0, -1)

    # Check if the ValueError message contains the expected text
    expected_message = "Negative values are not allowed in the matrix"
    assert expected_message in str(excinfo.value)

# //added test cases  on 09/12

    # Test setting and getting values at invalid indices
    # with pytest.raises(ValueError):
    #     matrix.get(2, 1)

    with pytest.raises(ValueError):
        matrix.set(3, 0, 1)

    with pytest.raises(ValueError):
        matrix.set(0, 3, 1)

    with pytest.raises(ValueError):
        matrix.get(3, 0)

    with pytest.raises(ValueError):
        matrix.get(0, 3)


def test_recommend():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(3, 3)

    # Set values in the matrix
    matrix.set(0, 0, 1)
    matrix.set(1, 1, 2)
    matrix.set(2, 2, 3)

    # Initialize a user vector
    user_vector = [1, 0, 0]

    # Test if recommendations are generated correctly
    assert matrix.recommend(user_vector) == [1, 0, 0]

    # Test recommending with an invalid vector (dimension doesn't match)
    with pytest.raises(ValueError):
        matrix.recommend([1, 0])

def test_add_movie():
    # Initialize two SparseMatrices of the same dimensions
    matrix1 = SparseMatrix(3, 3)
    matrix2 = SparseMatrix(3, 3)

    # Set values in both matrices
    matrix1.set(0, 0, 1)
    matrix1.set(1, 1, 2)
    matrix2.set(1, 2, 3)
    matrix2.set(2, 0, 4)

    # Add matrix2 to matrix1
    matrix1.add_movie(matrix2)

    # Test if values are correctly added
    assert matrix1.get(0, 0) == 1
    assert matrix1.get(1, 1) == 2
    assert matrix1.get(1, 2) == 3
    assert matrix1.get(2, 0) == 4

    # Initialize two SparseMatrices with different dimensions
    matrix3 = SparseMatrix(3, 3)
    matrix4 = SparseMatrix(2, 2)

    # Attempt to add matrix2 to matrix1 (dimensions don't match)
    with pytest.raises(ValueError):
        matrix3.add_movie(matrix4)

def test_to_dense():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(2, 2)

    # Set values in the matrix
    matrix.set(0, 0, 1)
    matrix.set(1, 1, 2)

    # Convert to a dense matrix
    dense_matrix = matrix.to_dense()

    # Test if the dense matrix is correctly generated
    assert dense_matrix == [[1, 0], [0, 2]]

def test_invalid_set_get():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(3, 3)

    # Attempt to set values at invalid indices
    with pytest.raises(ValueError):
        matrix.set(3, 0, 1)

    with pytest.raises(ValueError):
        matrix.set(0, 3, 1)

    # Attempt to get values at invalid indices
    with pytest.raises(ValueError):
        matrix.get(3, 0)

    with pytest.raises(ValueError):
        matrix.get(0, 3)

def test_recommend_invalid_vector():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(3, 3)

    # Set values in the matrix
    matrix.set(0, 0, 1)
    matrix.set(1, 1, 2)
    matrix.set(2, 2, 3)

    # Initialize an invalid user vector (dimension doesn't match matrix)
    user_vector = [1, 0]

    # Test if an error is raised when recommending with an invalid vector
    with pytest.raises(ValueError):
        matrix.recommend(user_vector)

def test_add_movie_invalid_dimensions():
    # Initialize two SparseMatrices with different dimensions
    matrix1 = SparseMatrix(3, 3)
    matrix2 = SparseMatrix(2, 2)

    # Attempt to add matrix2 to matrix1 (dimensions don't match)
    with pytest.raises(ValueError):
        matrix1.add_movie(matrix2)


# Add more test cases for other methods

def test_recommend_top_n_movies():
    # Initialize a SparseMatrix
    matrix = SparseMatrix(3, 3)

    # Set values in the matrix
    matrix.set(0, 0, 5)
    matrix.set(1, 1, 4)
    matrix.set(2, 2, 3)
    matrix.set(0, 1, 2)
    matrix.set(1, 2, 1)

    # Recommend the top 2 movies based on ratings
    top_movies = matrix.recommend_top_n_movies(2)

    # Verify that the top movies are recommended correctly
    # assert top_movies == [1, 0]
    assert top_movies == [1, 0]



# if __name__ == "__main__":
#     pytest.main()
