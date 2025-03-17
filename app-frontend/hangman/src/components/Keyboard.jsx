export default function Keyboard({ guessedLetters, onGuess }) {
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    
    return (
        <div className="grid grid-cols-7 gap-2">
            {alphabet.map(letter => (
                <button
                    key={letter}
                    onClick={() => onGuess(letter)}
                    disabled={guessedLetters.has(letter)}
                    className={`p-2 text-center rounded ${
                        guessedLetters.has(letter)
                            ? 'bg-gray-300'
                            : 'bg-blue-500 text-white hover:bg-blue-600'
                    }`}
                >
                    {letter}
                </button>
            ))}
        </div>
    );
} 