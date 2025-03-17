import { useState, useEffect } from 'react';
import Navigation from './Navigation';
import Keyboard from './Keyboard';

export default function HangmanGame() {
    const [word, setWord] = useState('');
    const [guessedLetters, setGuessedLetters] = useState(new Set());
    const [remainingGuesses, setRemainingGuesses] = useState(6);

    const fetchWord = async () => {
        try {
            const response = await fetch('/hangman/api/hangman/word/');
            const data = await response.json();
            setWord(data.word);
        } catch (error) {
            setWord('HANGMAN'); // fallback word
        }
    };

    // Load word when component mounts
    useEffect(() => {
        fetchWord();
    }, []);

    const guessLetter = (letter) => {
        if (remainingGuesses <= 0) return;
        
        const newGuessedLetters = new Set(guessedLetters);
        newGuessedLetters.add(letter);
        setGuessedLetters(newGuessedLetters);
        
        if (!word.includes(letter)) {
            setRemainingGuesses(remainingGuesses - 1);
        }
    };

    const displayWord = word
        .split('')
        .map(letter => guessedLetters.has(letter) ? letter : '_')
        .join(' ');
        
    const hasWon = !displayWord.includes('_');
    const hasLost = remainingGuesses <= 0;

    return (
        <div>
            <Navigation />
            <div className="max-w-2xl mx-auto p-4">
                <div className="mb-8">
                    <p className="text-2xl font-mono mb-4">{displayWord}</p>
                    <p className="text-lg">Remaining guesses: {remainingGuesses}</p>
                </div>
                
                {!hasWon && !hasLost && (
                    <Keyboard 
                        guessedLetters={guessedLetters}
                        onGuess={guessLetter}
                    />
                )}
                
                {(hasWon || hasLost) && (
                    <div className="text-center">
                        <p className="text-xl mb-4">
                            {hasWon ? 'Congratulations! You won!' : 'Game Over!'}
                        </p>
                        <button
                            onClick={() => {
                                setWord('HANGMAN');
                                setGuessedLetters(new Set());
                                setRemainingGuesses(6);
                            }}
                            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                        >
                            Play Again
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
} 