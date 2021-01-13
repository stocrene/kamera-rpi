# -*- coding: utf-8 -*-
"""
Diese Datei dient zum Ver- und Entschlüsseln von Daten

https://www.novixys.com/blog/using-aes-encryption-decryption-python-pycrypto/

Dafür muss das Pyton-Package pycrypto installiert werden: 
pip install pycrypto


Der Initalisierungsvektor ist hier Fest gewählt, dieser muss 16 bytes lang sein. 
In der praxis wird dieser anhand der vorherigen Nachricht gewonnen.
In diesem Fall ist zwar der Text verschlüsselt, aber bei bekannten Zeichen der Übertragung
kann der Text theoretisch rekonstruiert werden. -> evtl. IV auch generieren lassen
"""

from Crypto.Cipher import AES

def verschluessel(message, key):
    obj = AES.new(key, AES.MODE_CBC, 'This is an IV457')
    ciphertext = obj.encrypt(message)
    return ciphertext

def entschluessel(ciphertext, key):
    obj = AES.new(key, AES.MODE_CBC, 'This is an IV457')
    text = obj.decrypt(ciphertext)
    return text
