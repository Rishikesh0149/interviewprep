CODING_PROBLEMS = [
    {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Arrays & HashMaps",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "output": "[1,2]",
                "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
            }
        ],
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ],
        "starter_code": {
            "python": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Implement your solution here\n    pass\n",
            "javascript": "function twoSum(nums, target) {\n    // Implement your solution here\n    return [];\n}\n"
        },
        "test_cases": [
            {"args": [[2, 7, 11, 15], 9], "expected": [0, 1], "is_hidden": False},
            {"args": [[3, 2, 4], 6], "expected": [1, 2], "is_hidden": False},
            {"args": [[3, 3], 6], "expected": [0, 1], "is_hidden": False},
            {"args": [[1, 5, 7, 11, 19], 20], "expected": [0, 4], "is_hidden": True},
            {"args": [[-1, -2, -3, -4, -5], -8], "expected": [2, 4], "is_hidden": True}
        ],
        "hints": [
            "A brute force approach computes every pair in O(N^2) time. Can we do better with auxiliary space?",
            "Can we use a hash map to check whether the complement (target - current_val) has already been seen?",
            "Iterate through the array once: for each index i and value n, check if (target - n) exists in our hash map. If yes, return [map[target - n], i]."
        ],
        "optimal_complexity": "Time: O(N), Space: O(N)"
    },
    {
        "id": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "category": "Stacks",
        "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "examples": [
            {
                "input": "s = \"()\"",
                "output": "true"
            },
            {
                "input": "s = \"()[]{}\"",
                "output": "true"
            },
            {
                "input": "s = \"(]\"",
                "output": "false"
            }
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'."
        ],
        "starter_code": {
            "python": "def is_valid_parentheses(s: str) -> bool:\n    # Implement your solution here\n    pass\n",
            "javascript": "function isValidParentheses(s) {\n    // Implement your solution here\n    return false;\n}\n"
        },
        "test_cases": [
            {"args": ["()"], "expected": True, "is_hidden": False},
            {"args": ["()[]{}"], "expected": True, "is_hidden": False},
            {"args": ["(]"], "expected": False, "is_hidden": False},
            {"args": ["([)]"], "expected": False, "is_hidden": True},
            {"args": ["{[]}"], "expected": True, "is_hidden": True}
        ],
        "hints": [
            "Use a LIFO (Last-In-First-Out) stack data structure.",
            "Push opening brackets onto the stack. When encountering a closing bracket, verify that the top of the stack matches its corresponding opening type.",
            "At the end of the string traversal, the stack must be empty for the string to be valid."
        ],
        "optimal_complexity": "Time: O(N), Space: O(N)"
    },
    {
        "id": "longest-substring-without-repeats",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "category": "Sliding Window",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "examples": [
            {
                "input": "s = \"abcabcbb\"",
                "output": "3",
                "explanation": "The answer is \"abc\", with the length of 3."
            },
            {
                "input": "s = \"bbbbb\"",
                "output": "1",
                "explanation": "The answer is \"b\", with the length of 1."
            },
            {
                "input": "s = \"pwwkew\"",
                "output": "3",
                "explanation": "The answer is \"wke\", with the length of 3."
            }
        ],
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces."
        ],
        "starter_code": {
            "python": "def length_of_longest_substring(s: str) -> int:\n    # Implement sliding window here\n    pass\n",
            "javascript": "function lengthOfLongestSubstring(s) {\n    // Implement sliding window here\n    return 0;\n}\n"
        },
        "test_cases": [
            {"args": ["abcabcbb"], "expected": 3, "is_hidden": False},
            {"args": ["bbbbb"], "expected": 1, "is_hidden": False},
            {"args": ["pwwkew"], "expected": 3, "is_hidden": False},
            {"args": [""], "expected": 0, "is_hidden": True},
            {"args": ["dvdf"], "expected": 3, "is_hidden": True}
        ],
        "hints": [
            "Maintain a sliding window [left, right] along with a hash map recording the last seen index of each character.",
            "When a duplicate character is encountered at index right, update the left pointer to max(left, last_seen_index + 1).",
            "Continuously update max_len = max(max_len, right - left + 1)."
        ],
        "optimal_complexity": "Time: O(N), Space: O(min(N, M)) where M is alphabet size"
    },
    {
        "id": "coin-change",
        "title": "Coin Change",
        "difficulty": "Medium",
        "category": "Dynamic Programming",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "examples": [
            {
                "input": "coins = [1,2,5], amount = 11",
                "output": "3",
                "explanation": "11 = 5 + 5 + 1 (3 coins)"
            },
            {
                "input": "coins = [2], amount = 3",
                "output": "-1"
            },
            {
                "input": "coins = [1], amount = 0",
                "output": "0"
            }
        ],
        "constraints": [
            "1 <= coins.length <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4"
        ],
        "starter_code": {
            "python": "def coin_change(coins: list[int], amount: int) -> int:\n    # Implement DP here\n    pass\n",
            "javascript": "function coinChange(coins, amount) {\n    // Implement DP here\n    return -1;\n}\n"
        },
        "test_cases": [
            {"args": [[1, 2, 5], 11], "expected": 3, "is_hidden": False},
            {"args": [[2], 3], "expected": -1, "is_hidden": False},
            {"args": [[1], 0], "expected": 0, "is_hidden": False},
            {"args": [[186, 419, 83, 408], 6249], "expected": 20, "is_hidden": True}
        ],
        "hints": [
            "Define dp[i] as the minimum number of coins needed to make amount i.",
            "Initialize dp array of size amount + 1 with infinity, and set dp[0] = 0.",
            "For each amount from 1 to total, and for each coin c: if i - c >= 0, dp[i] = min(dp[i], dp[i - c] + 1)."
        ],
        "optimal_complexity": "Time: O(amount * coins.length), Space: O(amount)"
    },
    {
        "id": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "Medium",
        "category": "Heaps & HashMaps",
        "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "examples": [
            {
                "input": "nums = [1,1,1,2,2,3], k = 2",
                "output": "[1,2]"
            },
            {
                "input": "nums = [1], k = 1",
                "output": "[1]"
            }
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
            "k is in the range [1, the number of unique elements in the array].",
            "It is guaranteed that the answer is unique."
        ],
        "starter_code": {
            "python": "def top_k_frequent(nums: list[int], k: int) -> list[int]:\n    # Implement here\n    pass\n",
            "javascript": "function topKFrequent(nums, k) {\n    // Implement here\n    return [];\n}\n"
        },
        "test_cases": [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2], "is_hidden": False},
            {"args": [[1], 1], "expected": [1], "is_hidden": False},
            {"args": [[4, 1, -1, 2, -1, 2, 3], 2], "expected": [-1, 2], "is_hidden": True}
        ],
        "hints": [
            "First, build a frequency map of each element in O(N) time.",
            "Use either a min-heap of size k in O(N log k), or Bucket Sort where index represents frequency in O(N) time.",
            "With bucket sort, iterate backwards from index N down to 0 collecting numbers until k elements are retrieved."
        ],
        "optimal_complexity": "Time: O(N), Space: O(N)"
    }
]
