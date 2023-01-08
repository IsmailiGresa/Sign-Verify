# Sign-Verify

Commands on cmd:

1.Create two users so the communication is set up:

	python Sign-Verify.py create-user grese

	python Sign-Verify.py create-user someone

Users will be saved in the main directory and the private and public key get placed in keys

2.Write the message from a user to another:

	python Sign-Verify.py write-message 423857 grese someone

The message is sent from grese to someone and is saved on the main directory as someone.json file.
With the message, the signature is also saved in the same file.

3.Read the message (integer only) the sender sent to the receiver:

	python Sign-Verify.py read-message 423857 someone grese

Displays the decrypted message and verifies the signature in the file.




