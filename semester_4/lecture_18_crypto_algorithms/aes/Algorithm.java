import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

/**
 * AES Encryption Algorithm.
 * 
 * Advanced Encryption Standard.
 */
public class Algorithm {
    
    static class AESEncryption {
        private SecretKey key;
        private static final String ALGORITHM = "AES/CBC/PKCS5Padding";
        
        AESEncryption() throws Exception {
            KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
            keyGenerator.init(256);
            this.key = keyGenerator.generateKey();
        }
        
        String encrypt(String plaintext) throws Exception {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            
            byte[] iv = cipher.getIV();
            byte[] ciphertext = cipher.doFinal(plaintext.getBytes("UTF-8"));
            
            byte[] combined = new byte[iv.length + ciphertext.length];
            System.arraycopy(iv, 0, combined, 0, iv.length);
            System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);
            
            return Base64.getEncoder().encodeToString(combined);
        }
        
        String decrypt(String encrypted) throws Exception {
            byte[] combined = Base64.getDecoder().decode(encrypted);
            
            byte[] iv = new byte[16];
            byte[] ciphertext = new byte[combined.length - 16];
            System.arraycopy(combined, 0, iv, 0, 16);
            System.arraycopy(combined, 16, ciphertext, 0, ciphertext.length);
            
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
            
            byte[] plaintext = cipher.doFinal(ciphertext);
            return new String(plaintext, "UTF-8");
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("AES ENCRYPTION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        try {
            AESEncryption aes = new AESEncryption();
            
            String plaintext = "Hello, this is a secret message!";
            System.out.println("Plaintext: " + plaintext);
            
            String encrypted = aes.encrypt(plaintext);
            System.out.println("Encrypted: " + encrypted.substring(0, 
                Math.min(50, encrypted.length())) + "...");
            
            String decrypted = aes.decrypt(encrypted);
            System.out.println("Decrypted: " + decrypted);
            System.out.println("Match: " + plaintext.equals(decrypted));
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nAlgorithm: AES-256 encryption");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
