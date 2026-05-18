# 🎮 Kids Number Match Game

An interactive, educational number matching game built with Python and Tkinter. Perfect for kids to practice number recognition and quick thinking skills!

## 🌟 Features

- **Interactive Gameplay**: Watch numbers float up the screen and select the correct answer before they disappear
- **10 Question Rounds**: Progressive difficulty with varied number options
- **Real-time Scoring**: Track your score as you progress through the game
- **Progress Tracking**: Visual progress dots show your position in the game
- **Colorful UI**: Kid-friendly interface with bright colors, emojis, and decorative elements
- **Animated Elements**: Floating clouds, balloons, and stars create an engaging atmosphere
- **Sound Effects**: Synthesized sound effects for correct/wrong answers and game events
- **Background Music**: Optional looping background music during gameplay
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- numpy (for audio synthesis)
- simpleaudio (for audio playback)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohiddeenshaik-del/Kids_Numbers_Game.git
   cd Kids_Numbers_Game
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Play

1. Run the game:
   ```bash
   python game.py
   ```

2. Click **"Start Game"** to begin

3. Watch as a number floats up the screen from the bottom

4. Select the **correct answer** from the 4 button options before the number reaches the top and disappears

5. Answer all 10 questions to complete the game

6. View your final score and replay as many times as you want!

### Scoring
- ✅ **Correct Answer**: +1 point
- ❌ **Wrong Answer**: No points, number floats away
- ⏱️ **Missed Number**: Move to next question

## 🎯 Game Features Breakdown

### User Interface
- **Header**: Game title and level badge
- **Start Screen**: Instructions and game description
- **Game Screen**: 
  - Canvas with animated floating number
  - Progress dots showing question completion
  - Question counter and score display
  - 4 answer buttons arranged in a 2x2 grid
  - Status messages for feedback

### Animations
- Numbers float up smoothly from bottom to top
- Clouds continuously move across the sky
- Decorative stars and balloons on canvas
- Button hover effects for interactivity

### Audio
- **Background Music**: Synthesized violin arpeggio loop (if numpy/simpleaudio available)
- **Sound Effects**:
  - ✓ Correct answer: Bright chord
  - ✗ Wrong answer: Dissonant tone
  - 🎪 Missed number: Low-pitched tone
  - 🎉 Game finish: Ascending tone sequence
  - ▶️ Game start: Rising tone

## 📊 Game Completion Messages

| Score | Message |
|-------|---------|
| 10/10 | 🎉 Congratulations! Perfect score! 🎉 |
| 6-9/10 | Awesome! You passed with great marks. |
| <6/10 | Keep practicing! You can score higher next time. |

## 🏗️ Project Structure

```
Kids_Numbers_Game/
├── game.py              # Main game application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Technical Details

### Architecture
- **Single-threaded GUI**: Main application uses tkinter's event loop
- **Multi-threaded Audio**: Background music runs in a separate daemon thread to avoid blocking UI
- **Canvas-based Animation**: Uses tkinter Canvas for smooth number and cloud animations
- **Responsive Controls**: Non-blocking button callbacks with proper state management

### Code Optimization
- Configuration dictionary for centralized color/font/sound management
- Helper methods for repetitive widget creation
- Efficient sound synthesis using NumPy arrays
- Smart fallback for missing audio libraries

### Audio Generation
- **Violin Synthesis**: Additive synthesis with multiple harmonics and vibrato
- **Short Tones**: ADSR envelope (Attack, Decay, Sustain, Release) for sound effects
- **Sample Rate**: 44.1 kHz for high-quality audio

## 🐛 Troubleshooting

### Game won't start
- Ensure Python 3.7+ is installed
- Verify tkinter is available: `python -m tkinter`
- Check that all dependencies are installed: `pip install -r requirements.txt`

### No sound
- This is normal if numpy/simpleaudio aren't installed - the game falls back to system beeps
- To enable synthesized sound: `pip install numpy simpleaudio`

### Slow performance
- The game is lightweight and should run on any modern system
- Close other resource-intensive applications if needed

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Shaik Mohiddeen**
- GitHub: [@mohiddeenshaik-del](https://github.com/mohiddeenshaik-del)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork and submit pull requests.

## 🎓 Educational Value

This game helps children develop:
- **Number Recognition**: Identify numbers quickly under time pressure
- **Decision Making**: Make quick choices among multiple options
- **Hand-Eye Coordination**: Click precise buttons rapidly
- **Concentration**: Focus on moving targets
- **Problem Solving**: Match numbers under gameplay constraints

---

**Made with ❤️ for kids to learn and have fun!**
