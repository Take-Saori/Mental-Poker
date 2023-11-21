import Crypto
from Crypto.Util.number import *

class Protocol:
    def __init__(self,d = -1,e=-1):
        self.p=233
        self.q=211

        self.n = self.p * self.q
        self.phi =(self.p-1)*(self.q-1)

        while True:
            #Getting random e
            self.encryption_key = Crypto.Util.number.getPrime(8, randfunc=Crypto.Random.get_random_bytes)

            #Getting modular inverse of e mod phi(n)
            self.decryption_key = pow(self.encryption_key, -1, self.phi)

            #Checking for weiner attack vulnerability
            decryption_key_limit =  int((1/3)*(self.n)**(1/4))
            if (self.decryption_key > decryption_key_limit):
                break
            else:
                continue


        if((d != -1) and (e != -1)):
            self.decryption_key = d
            self.encryption_key = e


        # print("Encryption Key is: ", self.encryption_key)
        # print("Decryption Key is: ", self.decryption_key)

    def get_encrypted_card(self,message):

        #Encrypt C = M^e (mod n)
        ciphertext = pow(message, self.encryption_key, self.n)
        return ciphertext
    
    def get_decrypted_card(self, ciphertext):
        
        # Decrypt M = C^d (mod n) using the private key (self.decryption_key, self.n)
        decrypted_int = pow(ciphertext, self.decryption_key, self.n)

        return decrypted_int