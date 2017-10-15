from Client_Script import encrypt_response
from Server_Script import decrypt_response


def test_encrypt_decrypt_response():
    encrypted_text = encrypt_response("Hello World!")
    decrypted_text = decrypt_response(encrypted_text)
    assert(decrypted_text == 'Hello World')
