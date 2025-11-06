# 🖐️ Hand Gesture Detection with OpenCV and MediaPipe

This project is based on computer vision studies using **MediaPipe**.  
It has a humorous tone and was developed from an idea inspired by the project created by **Gabriela Marculino**, whose [repository](https://github.com/GabrielaMarculino/Nu-Metal-Pose-Random-Image-Detector) served as inspiration for this work.

This project uses **OpenCV**, **MediaPipe**, and **NumPy** to detect hand gestures in real time via webcam.  
Each recognized gesture displays a corresponding image for each detected hand, with a smooth transition effect (fade in/out).

---

## 🎯 Objective

Demonstrate the use of computer vision to:
- Track hands in real time;
- Identify specific gestures (e.g., “Rock”, “Thumbs Up”, “Middle Finger”, etc.);
- Display personalized images according to the recognized gesture.

---

## 🧠 Technologies Used

- [OpenCV](https://opencv.org/) → Image and video capture/processing.  
- [MediaPipe](https://developers.google.com/mediapipe) → Hand detection and tracking.  
- [NumPy](https://numpy.org/) → Numerical array manipulation.  
- [Python 3.x](https://www.python.org/)  

---

## 📁 Project Structure

> Inside the **img/** folder are the images corresponding to each gesture.  
> The subfolder names must exactly match the ones specified in the code:  
> `"Nu_metal"`, `"Joinha"`, `"Rock"`, `"Dedo_do_meio"`.

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/PedroBarbosa239/Hands-image-detector-randon.git
   cd Hands-image-detector-randon
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate      # Linux / macOS
   ```

3. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe numpy
   ```

---

## 👨‍💻 Author

**Pedro Barbosa de Souza**  
- 📘 Project developed for studying and practicing computer vision with Python.  
- 🔗 GitHub: [Pedro Barbosa](https://github.com/PedroBarbosa239)

---

## 📜 License

This project is distributed under the **MIT License**.  
You are free to use, copy, modify, and distribute this project for **educational and experimental** purposes.

---

## 💡 Suggestions and Contributions

Contributions, ideas, and constructive feedback are always welcome!  
Feel free to open pull requests or share improvement suggestions.
