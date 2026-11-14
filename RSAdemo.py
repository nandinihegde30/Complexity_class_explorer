
import math

# Check whether a number is prime
def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True


# Generate RSA keys
def generate_keys(p, q):

    if not is_prime(p) or not is_prime(q) or p == q:
        raise ValueError("Enter two different prime numbers.")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose public exponent
    e = 2

    while e < phi:
        if math.gcd(e, phi) == 1:
            break
        e += 1

    # Calculate private exponent
    d = pow(e, -1, phi)

    return (e, n), (d, n), phi


# Encrypt message
def encrypt(message, public_key):

    e, n = public_key

    if not 0 <= message < n:
        raise ValueError("Message must be between 0 and n-1.")

    return pow(message, e, n)


# Decrypt message
def decrypt(ciphertext, private_key):

    d, n = private_key

    return pow(ciphertext, d, n)


# Main program
print("===== RSA ENCRYPTION AND DECRYPTION =====")

p = int(input("Enter first prime number: "))
q = int(input("Enter second prime number: "))

public_key, private_key, phi = generate_keys(p, q)

print("\n----- KEY GENERATION -----")
print("Prime number p:", p)
print("Prime number q:", q)
print("n = p * q:", p * q)
print("Euler's Totient:", phi)

print("\nPublic Key:", public_key)
print("Private Key:", private_key)

message = int(input("\nEnter a numeric message (0 to n-1): "))

ciphertext = encrypt(message, public_key)

print("\n----- ENCRYPTION -----")
print("Original Message:", message)
print("Encrypted Message:", ciphertext)

decrypted = decrypt(ciphertext, private_key)

print("\n----- DECRYPTION -----")
print("Decrypted Message:", decrypted)

if message == decrypted:
    print("\nSUCCESS: Original message recovered!")
else:
    print("\nERROR: Decryption failed!")
