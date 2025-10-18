from unittest import TestCase

from brutils.ie import (
    remove_symbols,
    format_ie,
    is_valid,
)

class TestIE(TestCase):

    def test_remove_symbols(self):
        self.assertEqual(remove_symbols("110.042.490.114"), "110042490114")
        self.assertEqual(remove_symbols("11-00.42490/114"), "110042490114")
        self.assertEqual(remove_symbols("11@0042490#114"), "110042490114")

    def test_format_ie(self):
        self.assertEqual(format_ie("110042490114"), "110.042.490.114")
        self.assertEqual(format_ie("P011004249011"), "P011004249011")  # Formato especial SP (produtor rural)
        self.assertEqual(format_ie("INVALID!"), None)

    def test_is_valid_sp(self):
        self.assertTrue(is_valid("110042490114", "SP"))
        self.assertFalse(is_valid("110042490115", "SP"))  # Dígito inválido
        self.assertTrue(is_valid("P011004249011", "SP"))  # Produtor Rural

    def test_is_valid_mg(self):
        self.assertTrue(is_valid("0623079040081", "MG"))
        self.assertFalse(is_valid("0623079040080", "MG"))

    def test_is_valid_rj(self):
        self.assertTrue(is_valid("78508383", "RJ"))
        self.assertFalse(is_valid("78508384", "RJ"))

    def test_is_valid_rs(self):
        self.assertTrue(is_valid("2243658792", "RS"))
        self.assertFalse(is_valid("2243658791", "RS"))

    def test_invalid_uf(self):
        self.assertFalse(is_valid("123456789", "ZZ"))

if __name__ == "__main__":
    from unittest import main
    main()