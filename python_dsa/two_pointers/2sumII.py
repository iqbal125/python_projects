"""
LeetCode 167: Two Sum II - Input Array Is Sorted

Given a 1-indexed array of integers 'numbers' that is already sorted in non-decreasing order,
find two numbers such that they add up to a specific target number.

Return the indices of the two numbers (1-indexed) as an integer array [index1, index2].

You may not use the same element twice.
There is exactly one solution.

Example 1:
    Input: numbers = [2,7,11,15], target = 9
    Output: [1,2]
    Explanation: 2 + 7 = 9, so index1 = 1, index2 = 2

Example 2:
    Input: numbers = [2,3,4], target = 6
    Output: [1,3]

Example 3:
    Input: numbers = [-1,0], target = -1
    Output: [1,2]

Constraints:
    - 2 <= numbers.length <= 3 * 10^4
    - -1000 <= numbers[i] <= 1000
    - numbers is sorted in non-decreasing order
    - -1000 <= target <= 1000
    - Only one valid answer exists
"""

from typing import List


def two_sum(numbers: List[int], target: int) -> List[int]:
    """
    Two-pointer approach (optimal for sorted array)
    Time: O(n), Space: O(1)
    """
    # TODO: Implement solution
    pass


# Test cases
if __name__ == "__main__":
    # Test case 1
    numbers1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Input: {numbers1}, target: {target1}")
    print(f"Output: {two_sum(numbers1, target1)}")  # Expected: [1, 2]

    # Test case 2
    numbers2 = [2, 3, 4]
    target2 = 6
    print(f"Input: {numbers2}, target: {target2}")
    print(f"Output: {two_sum(numbers2, target2)}")  # Expected: [1, 3]

    # Test case 3
    numbers3 = [-1, 0]
    target3 = -1
    print(f"Input: {numbers3}, target: {target3}")
    print(f"Output: {two_sum(numbers3, target3)}")  # Expected: [1, 2]
