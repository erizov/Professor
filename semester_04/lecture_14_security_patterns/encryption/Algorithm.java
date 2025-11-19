/**
 * Encryption Pattern.
 * 
 * General encryption pattern demonstrating symmetric and asymmetric encryption
 * concepts, key management, and encryption best practices.
 */
import java.security.SecureRandom;
import java.util.*;

interface EncryptionAlgorithm {
    EncryptionResult encrypt(byte[] plaintext, byte[] key);
    byte[] decrypt(byte[] ciphertext, byte[] key, byte[] iv);
}

import java.util.logging.Logger;
class EncryptionResult {
    byte[] ciphertext;
    byte[] iv;
    
    EncryptionResult(byte[] ciphertext, byte[] iv) {
        this.ciphertext = ciphertext;
        this.iv = iv;
    }
}

class SimpleXOREncryption implements EncryptionAlgorithm {
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

class EncryptionService {
    private final EncryptionAlgorithm algorithm;
    private final byte[] key;
    private final SecureRandom random = new SecureRandom();
    
    EncryptionService(EncryptionAlgorithm algorithm) {
        this.algorithm = algorithm;
        this.key = new byte[32];
        random.nextBytes(this.key);
    }
    
    EncryptionResult encryptData(byte[] data) {
        return algorithm.encrypt(data, key);
    }
    
    byte[] decryptData(byte[] ciphertext, byte[] iv) {
        return algorithm.decrypt(ciphertext, key, iv);
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("ENCRYPTION PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        EncryptionAlgorithm algorithm = new SimpleXOREncryption();
        EncryptionService service = new EncryptionService(algorithm);
        
        byte[] plaintext = "Sensitive user data".getBytes();
        EncryptionResult result = service.encryptData(plaintext);
        byte[] decrypted = service.decryptData(result.ciphertext, result.iv);
        
        System.out.printf("Plaintext: %s%n", new String(plaintext));
        System.out.printf("Decrypted: %s%n", new String(decrypted));
        System.out.printf("Match: %s%n", Arrays.equals(plaintext, decrypted));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Secure data encryption");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}