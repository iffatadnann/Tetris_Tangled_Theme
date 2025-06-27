# Tetris Game with Linear Algebra & Geometry Concepts 🎮📐

A visually appealing version of the classic Tetris game built using **Python** and **Pygame**, enhanced with real applications of **Linear Algebra** and **Geometry**. This game demonstrates fundamental transformations and logic concepts behind the scenes, making it more than just a game — it's also an educational tool.

## 🔍 Key Features

- 🎨 **Custom Background & Classic Tetromino Colors**
- 📐 **Real-Time Collision Detection**
- 🔄 **Block Rotation Using 2D Matrix Transformation**
- 🧠 **Applies Linear Algebra & Geometry Concepts**

---

## 📚 Math Concepts Implemented

### 1. **2D Rotation Using Linear Algebra**
- Each Tetromino shape rotates using a transformation based on **90° counter-clockwise rotation**.
- This is achieved using the formula:
[x'] = [-y]
[y'] = [x]


### 2. **Collision Detection (Matrix Intersections)**
- Before placing or moving a block, the program checks for intersections with existing blocks using **matrix-boundary checks**.
- Helps ensure blocks don't overlap or go out of bounds.

### 3. **Coordinate System for Block Mapping**
- The playfield is represented as a **2D grid** (matrix), and each block's position is calculated relative to its top-left origin.
- This helps in rendering, positioning, and line-breaking logic.

---

## 🚀 How to Run

1. Install Python:
https://www.python.org/downloads/


2. Install Pygame:

pip install pygame

3. Clone the repository:

git clone https://github.com/iffatadnann/Tetris_Tangled_Theme.git

4. Run the game:
   
python tetris.py

## 🎮 Controls
Arrow Keys – Move the block left/right/down

Up Arrow – Rotate block

Spacebar – Hard drop

ESC – Restart after Game Over

## 📸 Preview

![screenshot](https://github.com/user-attachments/assets/26c91425-bd5a-45eb-aac1-c630c7afee1c)

## 🤝 Contributions
Feel free to fork this repo, suggest improvements, or build on this idea!

## 📫 Connect with Me
💼 Iffat Adnan
💼 Rafia Gull

   
