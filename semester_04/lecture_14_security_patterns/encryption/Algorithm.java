// package semester_04.lecture_14_security_patterns.encryption;

import java.security.SecureRandom;
import java.util.Arrays;
import java.util.logging.Logger;

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Encryption");
        System.out.println("=".repeat(70));

        EncryptionService service = new EncryptionService(new XorEncryption());
        byte[] plaintext = "Sensitive user data".getBytes();
        EncryptionResult result = service.encryptData(plaintext);
        byte[] decrypted = service.decryptData(result.ciphertext(), result.iv());

        System.out.printf("Plaintext : %s%n", new String(plaintext));
        System.out.printf("Decrypted : %s%n", new String(decrypted));
        System.out.printf("Match     : %s%n", Arrays.equals(plaintext, decrypted));

        System.out.println("=".repeat(70));
    }
}

record EncryptionResult(byte[] ciphertext, byte[] iv) {}

interface EncryptionAlgorithm {
    EncryptionResult encrypt(byte[] plaintext, byte[] key);
    byte[] decrypt(byte[] ciphertext, byte[] key, byte[] iv);
}

class EncryptionService {
    private final EncryptionAlgorithm algorithm;
    private final SecureRandom random = new SecureRandom();
    private final byte[] key = new byte[32];

    EncryptionService(EncryptionAlgorithm algorithm) {
        this.algorithm = algorithm;
        random.nextBytes(key);
    }

    EncryptionResult encryptData(byte[] data) {
        return algorithm.encrypt(data, key);
    }

    byte[] decryptData(byte[] ciphertext, byte[] iv) {
        return algorithm.decrypt(ciphertext, key, iv);
    }
}

class XorEncryption implements EncryptionAlgorithm {
    private static final int IV_SIZE = 16;
    private final SecureRandom random = new SecureRandom();

    @Override
    public EncryptionResult encrypt(byte[] plaintext, byte[] key) {
        byte[] iv = new byte[IV_SIZE];
        random.nextBytes(iv);

        byte[] ciphertext = new byte[plaintext.length];
        for (int i = 0; i < plaintext.length; i++) {
            ciphertext[i] = (byte) (plaintext[i] ^ key[i % key.length] ^ iv[i % iv.length]);
        }
        return new EncryptionResult(ciphertext, iv);
    }

    @Override
    public byte[] decrypt(byte[] ciphertext, byte[] key, byte[] iv) {
        byte[] plaintext = new byte[ciphertext.length];
        for (int i = 0; i < ciphertext.length; i++) {
            plaintext[i] = (byte) (ciphertext[i] ^ key[i % key.length] ^ iv[i % iv.length]);
        }
        return plaintext;
    }
}

