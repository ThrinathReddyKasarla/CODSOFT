import java.util.Scanner;
import java.util.Random;

public class Number_Game {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        
        int min = 1;
        int max = 100;
        int Attempts = 10;
        
        boolean playAgain = true;
        int score = 0;
        
        System.out.println("Welcome to the Number Guessing Game!");
        
        while (playAgain) {
            int target = random.nextInt(max - min + 1) + min;
            int attempts = 0;
            boolean guessedCorrectly = false;
            
            System.out.println("Try to guess a number between " + min + " and " + max + ".");
            
            while (attempts < max && !guessedCorrectly) {
                System.out.print("Enter your guess: ");
                int userGuess = scanner.nextInt();
                attempts++;
                
                if (userGuess == target) {
                    System.out.println("You guessed the correct number " + target + " in " + attempts + " attempts.");
                    guessedCorrectly = true;
                } else if (userGuess < target) {
                    System.out.println("Too low! Try again.");
                } else {
                    System.out.println("Too high! Try again.");
                }
            }
            
            if (!guessedCorrectly) {
                System.out.println("Sorry, you've run out of attempts. The correct number was " + target + ".");
            }
            
            score += Attempts - attempts;
            
            System.out.println("Your current score: " + score);
            
            System.out.print("Do you want to play again? (yes/no): ");
            String playAgainInput = scanner.next();
            playAgain = playAgainInput.equalsIgnoreCase("yes");
        }
        
        System.out.println("Thanks for playing!");
        scanner.close();
    }
}
