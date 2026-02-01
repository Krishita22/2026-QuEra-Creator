# Team Cook Solution for Quantum Visualizer Project

## Solution Overview

Our team, **Team Cook**, has developed a **Quantum Visualizer** using **Surface Codes** to demonstrate **quantum error correction** techniques. The visualizer demonstrates how **stabilizers detect bit-flip and phase-flip errors** in quantum computing, and how quantum error correction methods are applied to fix these errors. It uses **Manim** for rendering the interactive quantum visualizations.

## Solution Breakdown

The solution is based on the concept of **surface codes** in quantum computing. Here's how we tackled the problem:
- **Manim** was used to create animations and visualize quantum states.
- **Data qubits** are used to represent quantum information, and **stabilizers (Z and X)** detect bit-flip and phase-flip errors respectively.
- The system detects errors by checking the states of the neighbors and corrects them using quantum gates like **X** and **Z**.
- The visualizer animates the entire process, including error detection, correction, and final results.

## File Structure

The file structure of the project is as follows:

- **`media/`**: Contains animations, images, and other media files for the visualizer.
- **`quantum_visualizers/`**: Python scripts and necessary configurations for visualizations using **Manim**.
- **`team_solutions.md`**: Documentation detailing the solution and steps for running the project.
- **`main.py`**: The main script containing the quantum visualizer logic.
- **`documentation.pdf`**: The presentation for the project.

## How to Run the Project

To run the project, follow these steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo-name/team-cook.git

2. **Install the required dependencies**:
    Manim (for quantum visualizations)
    NumPy (for mathematical computations)
    Python 3.8+ for compatibility

3. **Run the program**:
    ```bash
    manim -pql surface_code_animation.py SurfaceCodeAnimation

## Presentation and Assets

Our project also includes a presentation to explain how the quantum visualizer works and showcases its features. The presentation slides in documentation.pdf provide a detailed walkthrough of the surface code, error detection, and how the visualizer functions.

## Animation Video
https://drive.google.com/file/d/1dsfywm6VoCp8yZpP8P8lwQRNcT1muC6G/view

## Presentation Slide 
https://www.canva.com/design/DAHADN8g4NY/XYzDtfHPalMyD4U5YqFbOA/edit?utm_content=DAHADN8g4NY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

