import unittest

from hestale import Hestale, Passphrase

class TestHestale(unittest.TestCase):
    #setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.hestale = Hestale()
        
    #Each test method starts with the keyword test_
    def test_generate_key_from_phrase(self):
        self.assertEqual(self.hestale.generate_key_from_phrase('just do it'), '8d0877d0e097d391f5bb')
        self.assertEqual(self.hestale.generate_key_from_phrase('my default phrase'), '17aa1b7e961e9f7c1cce')
        self.assertEqual(self.hestale.generate_key_from_phrase('never say never'), '951ae4412a820a248a96')

    def test_mix_words(self):
        self.assertEqual(self.hestale.mix_words('static', '12345678', '8d0877d0e097d391f5bb'), 'z"bxkb |5vc`"qo}>d""')
        self.assertEqual(self.hestale.mix_words('example', 'qwerty', '17aa1b7e961e9f7c1cce'), '%8e~5w#w$%(l$t7i$wb~')
        self.assertEqual(self.hestale.mix_words('any', 'litepass', '951ae4412a820a248a96'), '42<e{,&,\'i".!n8&:q,=')
        
        
class TestPassphrase(unittest.TestCase):
    #setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.passpharse = Passphrase(path_to_passphrase='tests/passphrase.txt')
        
    def test_getset_passphrase(self):
        self.passpharse.passphrase = "   My Passphrase   "
        self.assertEqual(self.passpharse.passphrase, 'my passphrase')
        
    def test_save_passphrase(self):
        self.passpharse.passphrase = "   My Passphrase   "
        self.passpharse.save()
        self.passpharse.passphrase = ""
        self.assertEqual(self.passpharse.passphrase, 'my passphrase')

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
    
      
      