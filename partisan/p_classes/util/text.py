import hashlib

def hashText(text: str):
  return hashlib.sha3_512(str.encode(text)).hexdigest()