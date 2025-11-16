/**
 * Adapter Design Pattern.
 * 
 * Makes incompatible interfaces work together.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Target interface
    interface MediaPlayer {
        void play(String audioType, String fileName);
    }
    
    // Adaptee interface
    interface AdvancedMediaPlayer {
        void playVlc(String fileName);
        void playMp4(String fileName);
    }
    
    // Concrete adaptees
    static class VlcPlayer implements AdvancedMediaPlayer {
        public void playVlc(String fileName) {
            logger.info("Playing VLC file: " + fileName);
        }
        
        public void playMp4(String fileName) {
            // Not supported
        }
    }
    
    static class Mp4Player implements AdvancedMediaPlayer {
        public void playVlc(String fileName) {
            // Not supported
        }
        
        public void playMp4(String fileName) {
            logger.info("Playing MP4 file: " + fileName);
        }
    }
    
    // Adapter
    static class MediaAdapter implements MediaPlayer {
        AdvancedMediaPlayer advancedPlayer;
        
        MediaAdapter(String audioType) {
            if (audioType.equalsIgnoreCase("vlc")) {
                advancedPlayer = new VlcPlayer();
            } else if (audioType.equalsIgnoreCase("mp4")) {
                advancedPlayer = new Mp4Player();
            }
        }
        
        public void play(String audioType, String fileName) {
            if (audioType.equalsIgnoreCase("vlc")) {
                advancedPlayer.playVlc(fileName);
            } else if (audioType.equalsIgnoreCase("mp4")) {
                advancedPlayer.playMp4(fileName);
            }
        }
    }
    
    // Client
    static class AudioPlayer implements MediaPlayer {
        public void play(String audioType, String fileName) {
            if (audioType.equalsIgnoreCase("mp3")) {
                logger.info("Playing MP3 file: " + fileName);
            } else if (audioType.equalsIgnoreCase("vlc") || 
                      audioType.equalsIgnoreCase("mp4")) {
                MediaAdapter adapter = new MediaAdapter(audioType);
                adapter.play(audioType, fileName);
            } else {
                logger.info("Invalid media type: " + audioType);
            }
        }
    }
    
    // Object Adapter Example
    static class Square {
        private double side;
        
        Square(double side) {
            this.side = side;
        }
        
        double getSide() {
            return side;
        }
    }
    
    interface Rectangle {
        double getWidth();
        double getHeight();
        default double getArea() {
            return getWidth() * getHeight();
        }
    }
    
    static class SquareToRectangleAdapter implements Rectangle {
        private Square square;
        
        SquareToRectangleAdapter(Square square) {
            this.square = square;
        }
        
        public double getWidth() {
            return square.getSide();
        }
        
        public double getHeight() {
            return square.getSide();
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("ADAPTER DESIGN PATTERN DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Media Player
        logger.info("Example 1: Media Player Adapter");
        logger.info("-".repeat(70));
        
        AudioPlayer player = new AudioPlayer();
        player.play("mp3", "song.mp3");
        player.play("mp4", "video.mp4");
        player.play("vlc", "movie.vlc");
        logger.info();
        
        // Example 2: Square to Rectangle
        logger.info("Example 2: Square to Rectangle Adapter");
        logger.info("-".repeat(70));
        
        Square square = new Square(5.0);
        SquareToRectangleAdapter adapter = 
            new SquareToRectangleAdapter(square);
        
        logger.info("Square side: " + square.getSide());
        logger.info("Rectangle width: " + adapter.getWidth());
        logger.info("Rectangle height: " + adapter.getHeight());
        logger.info("Rectangle area: " + adapter.getArea());
        logger.info();
        
        long endTime = System.nanoTime();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Makes incompatible interfaces work together");
        logger.info("  - Reuses existing classes");
        logger.info("\nWhen to Use:");
        logger.info("  - Integrating third-party libraries");
        logger.info("  - Legacy code integration");
        logger.info("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}