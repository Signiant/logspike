from Crypto.Cipher import XOR
import base64

#Please note that this is not secure at all!!!
#This cipher is easily breakable.
#DO NOT allow unpriviledged users access to anything output from this cipher

def encode(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decode(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))
