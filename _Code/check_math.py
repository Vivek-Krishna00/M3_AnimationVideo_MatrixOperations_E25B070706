"""Verifies every numerical claim made in the video."""
import numpy as np
A, B, v = np.array([[0, -1], [1, 0]]), np.array([[1, 1], [0, 1]]), np.array([1, 2])
eq = lambda x, y: np.array_equal(x, np.array(y))
assert eq(A @ v, [-2, 1]) and eq(B @ v, [3, 2])
assert eq(A + B, [[1, 0], [1, 1]]) and eq((A + B) @ v, [1, 3])
assert eq(2 * B, [[2, 2], [0, 2]]) and eq(2 * B @ v, [6, 4])
assert eq(A @ B[:, 0], [0, 1]) and eq(A @ B[:, 1], [-1, 1])
assert eq(A @ B, [[0, -1], [1, 1]]) and eq(B @ A, [[1, -1], [1, 0]])
assert eq(A @ B @ v, [-2, 3]) and eq(B @ A @ v, [-1, 1])
print("All numbers in the video check out.")
