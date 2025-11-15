/**
 * Adapter Design Pattern.
 * 
 * Makes incompatible interfaces work together.
 */
public class Algorithm {
    
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
            System.out.println("Playing VLC file: " + fileName);
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
            System.out.println("Playing MP4 file: " + fileName);
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
                System.out.println("Playing MP3 file: " + fileName);
            } else if (audioType.equalsIgnoreCase("vlc") || 
                      audioType.equalsIgnoreCase("mp4")) {
                MediaAdapter adapter = new MediaAdapter(audioType);
                adapter.play(audioType, fileName);
            } else {
                System.out.println("Invalid media type: " + audioType);
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
        
        System.out.println("=".repeat(70));
        System.out.println("ADAPTER DESIGN PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Media Player
        System.out.println("Example 1: Media Player Adapter");
        System.out.println("-".repeat(70));
        
        AudioPlayer player = new AudioPlayer();
        player.play("mp3", "song.mp3");
        player.play("mp4", "video.mp4");
        player.play("vlc", "movie.vlc");
        System.out.println();
        
        // Example 2: Square to Rectangle
        System.out.println("Example 2: Square to Rectangle Adapter");
        System.out.println("-".repeat(70));
        
        Square square = new Square(5.0);
        SquareToRectangleAdapter adapter = 
            new SquareToRectangleAdapter(square);
        
        System.out.println("Square side: " + square.getSide());
        System.out.println("Rectangle width: " + adapter.getWidth());
        System.out.println("Rectangle height: " + adapter.getHeight());
        System.out.println("Rectangle area: " + adapter.getArea());
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Makes incompatible interfaces work together");
        System.out.println("  - Reuses existing classes");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Integrating third-party libraries");
        System.out.println("  - Legacy code integration");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
