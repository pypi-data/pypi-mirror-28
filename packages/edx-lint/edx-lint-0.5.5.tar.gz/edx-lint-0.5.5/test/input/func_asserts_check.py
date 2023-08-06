"""
Test for the right_assert pylint plugin.
"""
import unittest


class TestStringMethods(unittest.TestCase):
    """
    Test class for the right_assert pylint plugin.
    """
    def test_right_usage(self):
        """
        This is the right usage of various assert functions.
        """
        self.assertEqual('foo'.upper(), 'FOO')

        true = True
        self.assertTrue(true)
        self.assertFalse(not true)

        self.assertIn("a", "lala")
        self.assertNotIn("b", "lala")

        self.assertGreater(1, 0)
        self.assertLess(1, 2)

    def test_wrong_usage(self):
        """
        This is the wrong usage of assertTrue and False, but test should still pass.
        right_assert should throw an error for each line here.
        """
        self.assertTrue('foo'.upper() == 'FOO')
        self.assertFalse(500 == 501)

        self.assertTrue("a" in "lala")
        self.assertFalse("b" not in "lala")

        self.assertTrue(1 > 0)
        self.assertFalse(1 < 2)

        my_zero = 0

        self.assertTrue(my_zero is 0)
        self.assertFalse(my_zero is 1)
        self.assertTrue(my_zero is not 1)
        self.assertFalse(my_zero is not 0)

        my_none = None

        self.assertTrue(my_none is None)
        self.assertFalse(my_zero is None)
        self.assertTrue(my_zero != None)

    def test_wrong_but_with_pragma(self):
        """
        This uses the wrong assert, but has a pragma to quiet the message.
        """
        self.assertTrue("a" in "lala")      # pylint: disable=wrong-assert-type

    def test_chained_comparisons(self):
        """
        These uses of assertTrue and assertFalse are fine, because we can't
        pick apart the chained comparisons.
        """
        my_value = my_other_value = 10
        self.assertTrue(0 < my_value < 1000)
        self.assertFalse(0 < my_value < 5)
        self.assertTrue(my_value == my_other_value == 10)
