from tinyec import registry
import secrets

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

curve = registry.get_curve('brainpoolP256r1')

alicePrivKey = secrets.randbelow(curve.field.n)
alicePubKey = alicePrivKey * curve.g
print("Alice public key:", compress(alicePubKey))

bobPrivKey = secrets.randbelow(curve.field.n)
bobPubKey = bobPrivKey * curve.g
print("Bob public key:", compress(bobPubKey))

charlyPrivKey = secrets.randbelow(curve.field.n)
charlyPubKey = charlyPrivKey * curve.g
print("Charly  public key:", compress(charlyPubKey))
print("Now exchange the public keys (e.g. through Internet)")

aliceSharedKey = alicePrivKey * bobPubKey
print("Alice shared key:", compress(aliceSharedKey))

bobSharedKey = bobPrivKey * charlyPubKey
print("Bob shared key:", compress(bobSharedKey))

charlySharedKey = charlyPrivKey * alicePubKey
print("Charly shared key:", compress(charlySharedKey))

print("\n\n")

aliceSharedKey_1 =  bobSharedKey* alicePrivKey
print("Alice shared key:", compress(aliceSharedKey_1))

bobSharedKey_1 =  charlySharedKey * bobPrivKey
print("Bob shared key:", compress(bobSharedKey_1))

charlySharedKey_1 =  aliceSharedKey * charlyPrivKey
print("Charly shared key:", compress(charlySharedKey_1))


#print("Equal shared keys:", aliceSharedKey == bobSharedKey)