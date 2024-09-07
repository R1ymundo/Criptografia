import sys
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Set mode
mode = AES.MODE_ECB
if mode != AES.MODE_ECB:
    print('Only ECB mode supported...')
    sys.exit()

# Set sizes
keySize = 16  # Tamaño de clave de 128 bits
ivSize = 0  # IV size is 0 for ECB

#
# Start Encryption ----------------------------------------------------------------------------------------------
#

# Load original image
imageOrig = cv2.imread("linux.bmp")
rowOrig, columnOrig, depthOrig = imageOrig.shape

# Check for minimum width
minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
if columnOrig < minWidth:
    print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
    sys.exit()

# Display original image
cv2.imshow("Original image", imageOrig)
cv2.waitKey()

# Convert original image data to bytes
imageOrigBytes = imageOrig.tobytes()

# Encrypt
key = get_random_bytes(keySize)
cipher = AES.new(key, AES.MODE_ECB)

# Add padding to original image data
block_size = AES.block_size
imageOrigBytesPadded = pad(imageOrigBytes, block_size)
ciphertext = cipher.encrypt(imageOrigBytesPadded)

# Convert ciphertext bytes to encrypted image data
paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
void = columnOrig * depthOrig - ivSize - paddedSize
ivCiphertextVoid = ciphertext + bytes(void)
imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype=imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

# Display encrypted image
cv2.imshow("Encrypted image", imageEncrypted)
cv2.waitKey()

# Convert encrypted image data to ciphertext bytes
rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
rowOrig = rowEncrypted - 1
encryptedBytes = imageEncrypted.tobytes()
imageOrigBytesSize = rowOrig * columnOrig * depthOrig
paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
encrypted = encryptedBytes[imageOrigBytesSize + paddedSize:]

# Decrypt
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt the data and remove padding
decryptedImageBytesPadded = cipher.decrypt(encrypted)
decryptedImageBytes = unpad(decryptedImageBytesPadded, block_size)

# Convert bytes to decrypted image data
decryptedImage = np.frombuffer(decryptedImageBytes, imageOrig.dtype).reshape(rowOrig, columnOrig, depthOrig)

# Display decrypted image
cv2.imshow("Decrypted Image", decryptedImage)
cv2.waitKey()

# Close all windows
cv2.destroyAllWindows()
