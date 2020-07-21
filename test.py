from cryptography.fernet import Fernet
key = b'mlgHc4CrmeiVLmR82I1dRTL7zrR-Dff-k8mS_x7x1uY='
cipher_suite = Fernet(key)
# pwd = input("Enter a password: ")

cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b"123")   
print(str(ciphered_text, 'utf-8'))
print(type(repr(ciphered_text)))

pwd = '123'
res = bytes(pwd, 'utf-8') 
print(res)
ciphered_text = b'gAAAAABfE1GrYT7POAEKKOgRSZ36wZGnxIdvHX8AiifGTtr-f6gn-HOOVOJ6xo3KHSQhTEMCdgHVCAyJiOiCHyaoLn8NVb3CNw=='
print(type(ciphered_text))
unciphered_text = (cipher_suite.decrypt(ciphered_text))
unciphered_text = str(unciphered_text, 'utf-8')
print(unciphered_text)