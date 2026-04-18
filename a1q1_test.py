import unittest
from a1q1 import pattern_matching

class TestBoyerMoore(unittest.TestCase):

    def test_cases(self):
        tests = [
            # --- Original tests ---
            ("abc", "abc", [0]),
            ("abc", "abcabcabc", [6, 3, 0]),
            ("abc", "aaaaaa", []),
            ("aba", "ababa", [2, 0]),
            ("aaa", "aaaaaa", [3, 2, 1, 0]),
            ("hello", "hello world", [0]),
            ("world", "hello world", [6]),
            ("algorithm", "algorithm", [0]),
            ("abcdef", "abc", []),
            ("a", "banana", [5, 3, 1]),
            ("aaaa", "aaaaaaaa", [4, 3, 2, 1, 0]),
            ("abab", "abababab", [4, 2, 0]),
            ("abcd", "abcxabcxabcd", [8]),
            ("ababa", "abababababa", [6, 4, 2, 0]),
            ("xyz", "aaaaaaaaaaaaaaaaaaaa", []),
            ("abba", "abbabbaabba", [7, 3, 0]),
            ("aaaab", "aaaaaaaaaab", [6]),

            # --- Harder / adversarial tests ---
            ("aaaaa", "aaaaaaaaaa", [5,4,3,2,1,0]),
            ("aaaab", "aaaaaaaaaaaaaaaaab", [13]),
            ("ababaca", "ababababacababaca", [10,4]),
            ("abacab", "abacaabaccabacabaabb", [10]),
            ("abcab", "abcabcabcab", [6,3,0]),
            ("abcd", "abcabcabcabcabc", []),
            ("abcdeabc", "abcdeababcdeabcabcdeabc", [15,7]),
            ("ababab", "abababababab", [6,4,2,0]),
            ("xyz", "aaaaaaaaaaaaaaaaaaaaaaaaxyz", [24]),
            ("zabc", "aaaaaaaaaaaaaaaaaaaaaaaaazabc", [25]),
            ("aabaaac", "aabaaabaaabaaac", [8]),
            ("abcab", "abcxxabcababcab", [10,5]),
            ("abaaba", "abaabaabaaba", [6,3,0]),
            ("aaaaab", "aaaaaaaaaaaaaaaaaaaa", []),
            ("abcde", "zabcdeabcdeabcdez", [11,6,1]),
            ("abacabab", "abacabababacabab", [8,0]),
            ("babab", "ababababababab", [9,7,5,3,1]),
            ("abcdefg", "abcdefabcdefabcdefg", [12]),
            ("abcabc", "abcabcabcabc", [6,3,0]),
            ("aaaaabaaaaa", "aaaaabaaaaaaaaaabaaaaa", [11,0]),
        ]

        for pattern, text, expected in tests:
            with self.subTest(pattern=pattern, text=text):
                self.assertEqual(pattern_matching(text, pattern), expected)

    # def test_long_string(self):
    #     text = "abcde" * 10000 + "xyzabcde" + "abcde" * 10000
    #     pattern = "xyzabcde"
    #     expected = [10000 * 5]  # 50,000

    #     matches = pattern_matching(text, pattern)
    #     self.assertEqual(matches, expected)


if __name__ == "__main__":
    unittest.main()