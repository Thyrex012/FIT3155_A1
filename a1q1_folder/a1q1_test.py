import unittest
import random
from a1q1 import pattern_matching

def brute_force_match(txt, pat):
    """
    Reference implementation: returns all positions where pat matches txt,
    in descending order to match pattern_matching's output convention.
    """
    return [i for i in range(len(txt) - len(pat) + 1) if txt[i:i + len(pat)] == pat][::-1]


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
            ("aaaaa", "aaaaaaaaaa", [5, 4, 3, 2, 1, 0]),
            ("aaaab", "aaaaaaaaaaaaaaaaab", [13]),
            ("ababaca", "ababababacababaca", [10, 4]),
            ("abacab", "abacaabaccabacabaabb", [10]),
            ("abcab", "abcabcabcab", [6, 3, 0]),
            ("abcd", "abcabcabcabcabc", []),
            ("abcdeabc", "abcdeababcdeabcabcdeabc", [15, 7]),
            ("ababab", "abababababab", [6, 4, 2, 0]),
            ("xyz", "aaaaaaaaaaaaaaaaaaaaaaaaxyz", [24]),
            ("zabc", "aaaaaaaaaaaaaaaaaaaaaaaazabc", [24]),
            ("aabaaac", "aabaaabaaabaaac", [8]),
            ("abcab", "abcxxabcababcab", [10, 5]),
            ("abaaba", "abaabaabaaba", [6, 3, 0]),
            ("aaaaab", "aaaaaaaaaaaaaaaaaaaa", []),
            ("abcde", "zabcdeabcdeabcdez", [11, 6, 1]),
            ("abacabab", "abacabababacabab", [8, 0]),
            ("babab", "ababababababab", [9, 7, 5, 3, 1]),
            ("abcdefg", "abcdefabcdefabcdefg", [12]),
            ("abcabc", "abcabcabcabc", [6, 3, 0]),
            ("aaaaabaaaaa", "aaaaabaaaaaaaaaabaaaaa", [11, 0]),
        ]

        for pattern, text, expected in tests:
            with self.subTest(pattern=pattern, text=text):
                self.assertEqual(pattern_matching(text, pattern), expected)

    def test_long_string(self):
        text = "abcde" * 10000 + "xyzabcde" + "abcde" * 10000
        pattern = "xyzabcde"
        expected = [10000 * 5]  # 50,000

        matches = pattern_matching(text, pattern)
        self.assertEqual(matches, expected)

    def test_random_fuzz_small_alphabet(self):
        """
        Property-based test: generate random patterns and texts over a small
        alphabet, and verify pattern_matching agrees with brute force.

        Small alphabet (3 chars) maximizes the chance of triggering the
        bad-character branch, since mismatched characters will frequently
        reappear elsewhere in the pattern.
        """
        random.seed(42)  # Deterministic for reproducibility.
        alphabet = "abc"
        num_iterations = 5000

        for trial in range(num_iterations):
            m = random.randint(2, 8)
            n = random.randint(m, 25)
            pat = ''.join(random.choices(alphabet, k=m))
            txt = ''.join(random.choices(alphabet, k=n))
            expected = brute_force_match(txt, pat)
            with self.subTest(trial=trial, pattern=pat, text=txt):
                actual = pattern_matching(txt, pat)
                self.assertEqual(
                    actual, expected,
                    msg=f"Mismatch on trial {trial}: pat={pat!r}, txt={txt!r}, "
                        f"expected={expected}, got={actual}"
                )

    def test_random_fuzz_medium_alphabet(self):
        """
        Property-based test with a larger alphabet and longer strings.
        Covers a different region of the input space than the small-alphabet test.
        """
        random.seed(123)
        alphabet = "abcdef"
        num_iterations = 3000

        for trial in range(num_iterations):
            m = random.randint(2, 12)
            n = random.randint(m, 40)
            pat = ''.join(random.choices(alphabet, k=m))
            txt = ''.join(random.choices(alphabet, k=n))
            expected = brute_force_match(txt, pat)
            with self.subTest(trial=trial, pattern=pat, text=txt):
                actual = pattern_matching(txt, pat)
                self.assertEqual(
                    actual, expected,
                    msg=f"Mismatch on trial {trial}: pat={pat!r}, txt={txt!r}, "
                        f"expected={expected}, got={actual}"
                )

    def test_random_fuzz_long_text(self):
        """
        Property-based test with longer texts to stress shift logic across
        many alignments. Patterns are short to maximize the number of shifts.
        """
        random.seed(7)
        alphabet = "abcd"
        num_iterations = 500

        for trial in range(num_iterations):
            m = random.randint(3, 6)
            n = random.randint(50, 150)
            pat = ''.join(random.choices(alphabet, k=m))
            txt = ''.join(random.choices(alphabet, k=n))
            expected = brute_force_match(txt, pat)
            with self.subTest(trial=trial, pattern=pat, text=txt):
                actual = pattern_matching(txt, pat)
                self.assertEqual(
                    actual, expected,
                    msg=f"Mismatch on trial {trial}: pat={pat!r}, txt={txt!r}, "
                        f"expected={expected}, got={actual}"
                )


if __name__ == "__main__":
    unittest.main()

# # Keep in case I wanna do checks to see
# print((z_algorithm_for_boyer_moore(pat1[::-1]))[::-1])
# print(preprocess_p_table("aaaaaa", 2, ord('a')))
# print(pattern_matching("aaaaabaaaaaaaaaabaaaaa","aaaaabaaaaa"))
# print(pattern_matching("babbaababaababaababab","aababaabab"))
# print(pattern_matching("zabcdeabcdeabcdez", "abcde"))
# print(modified_preprocess_rx_table("aadabcd", 4, ord('a')))