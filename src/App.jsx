import { useState } from "react";
import './App.css';


function App() {
  const [target] = useState(Math.floor(Math.random() * 10) + 1);
  const [guess, setGuess] = useState('');
  const [message, setMessage] = useState('');
  const [attempts, setAttempts] = useState(0);

  const checkGuess = () => {
    if (attempts < 3) {
      setAttempts(attempts + 1);

      if (parseInt(guess) === target) {
        setMessage('🥳 Congratulations!! Your guess is correct!');
      } else {
        setMessage(guess > target ? "Too high 🤯" : "Too low ☹️");
      }

      setGuess('');
    } else {
      setMessage("😣 Sorry, you've reached the maximum limit!");
    }
  };

  return (
<div>
        <h1 style={{ background: 'blue', color: 'white', padding: '10px' }}>
          Guess the Number Game
        </h1>
        <p>Guess a number between 1 and 10</p>
        <input
          type="number"
          value={guess}
          onChange={(e) => setGuess(e.target.value)}
          disabled={attempts >= 3}
        />
        <p>
          <button onClick={checkGuess} disabled={attempts >= 3}>
            Check
          </button>
        </p>
        <p>{message}</p>
        <p style={{background:'blue'}}>Attempts left: {3 - attempts}</p>
      </div>
   
  );
}

export default App;