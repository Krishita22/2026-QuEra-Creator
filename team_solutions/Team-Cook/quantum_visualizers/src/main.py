from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8.0 
config.frame_width = 14.2
DEFAULT_FONT = "sans-serif"

YELLOW_DATA = "#F5C518"
DARK_BLUE_Z = "#1E3A5F"
LIGHT_BLUE_X = "#5DADE2"
BLUE_STROKE = "#2980B9"
RED_ERROR = "#E74C3C"
GREEN_OK = "#2ECC71"
ORANGE_ALERT = "#F39C12"
BG_COLOR = "#1A1A2E"
WHITE = "#FFFFFF"
GRAY_TEXT = "#95A5A6"
PURPLE = "#9B59B6"
PURPLE_PHASE = "#9B59B6"

class DataQubit(VGroup):
    def __init__(self, position=ORIGIN, initial_state=0):
        super().__init__()
        self.state = initial_state
        self.phase = 0
        
     
        self.glow = Circle(
            radius=0.35,
            color=YELLOW_DATA,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(position)
        
        self.core = Circle(
            radius=0.28,
            color=YELLOW_DATA, 
            fill_opacity=1.0, 
            stroke_width=4,
            stroke_color=BLUE_STROKE
        ).move_to(position)
        
        self.label = Text(
            "|0⟩" if self.state == 0 else "|1⟩", 
            font_size=24,
            font=DEFAULT_FONT,
            color="#000000", 
            weight=BOLD
        ).move_to(position)
        
        self.highlight_ring = Circle(
            radius=0.38,
            color=WHITE, 
            stroke_width=5,
            stroke_opacity=0, 
            fill_opacity=0
        ).move_to(position)
        
        self.add(self.glow, self.highlight_ring, self.core, self.label)
    
    def get_center(self):
        return self.core.get_center()

    def update_label(self):
        return Text(
            "|1⟩" if self.state == 1 else "|0⟩", 
            font_size=24,
            font=DEFAULT_FONT,
            color="#000000", 
            weight=BOLD
        ).move_to(self.core.get_center())


class StabilizerQubit(VGroup):
    def __init__(self, position=ORIGIN, qubit_type="Z"):
        super().__init__()
        fill_color = DARK_BLUE_Z if qubit_type == "Z" else LIGHT_BLUE_X
        self.qubit_type = qubit_type
        self.base_color = fill_color
        self.home_position = np.array(position) if not isinstance(position, np.ndarray) else position.copy()
        

        self.glow = Circle(
            radius=0.23,
            color=fill_color,
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(position)
        
        self.core = Circle(
            radius=0.18,
            color=fill_color, 
            fill_opacity=1.0, 
            stroke_width=3,
            stroke_color=BLUE_STROKE
        ).move_to(position)
        
        self.label = Text(qubit_type, font_size=20, font=DEFAULT_FONT, color=WHITE, weight=BOLD).move_to(position)
        self.add(self.glow, self.core, self.label)
    
    def get_center(self):
        return self.core.get_center()

class SurfaceCodeCombined(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        self.caption_box = Rectangle(width=14, height=1.0, fill_color="#000000", fill_opacity=0.9, stroke_width=0).to_edge(DOWN, buff=0.1)
        self.add(self.caption_box)
        self.caption_text = Text("", font_size=18, color=WHITE).move_to(self.caption_box)
        self.add(self.caption_text)
        
        self.intro()
        self.show_legend()
        self.build_lattice()
        self.show_syndrome_extraction()
        self.explain_bit_flip()
        self.bit_flip_demo()
        self.explain_phase_flip()
        self.phase_flip_demo()
        self.summary()
    
    
    def update_caption(self, text, color=WHITE):
        new_caption = Text(text, font_size=24, font=DEFAULT_FONT, color=color).move_to(self.caption_box)
        self.play(Transform(self.caption_text, new_caption), run_time=0.3)
    
    def create_circuit(self, center, circuit_type):
        color = DARK_BLUE_Z if circuit_type == "Z" else LIGHT_BLUE_X
        circuit = VGroup()
        line_spacing = 0.25
        line_length = 1.8
        
        for i in range(4):
            y = center[1] + 0.4 - i * line_spacing
            line = Line(
                [center[0] - line_length/2, y, 0], 
                [center[0] + line_length/2, y, 0], 
                stroke_color=YELLOW_DATA, stroke_width=3
            )
            label = Text(f"D{i+1}", font_size=14, font=DEFAULT_FONT, color=GRAY_TEXT).move_to([center[0] - line_length/2 - 0.25, y, 0])
            circuit.add(line, label)
        
        anc_y = center[1] + 0.4 - 4 * line_spacing
        anc_line = Line(
            [center[0] - line_length/2, anc_y, 0], 
            [center[0] + line_length/2, anc_y, 0], 
            stroke_color=color, stroke_width=3
        )
        anc_label = Text(circuit_type, font_size=14, font=DEFAULT_FONT, color=color if circuit_type == "X" else WHITE, weight=BOLD)
        anc_label.move_to([center[0] - line_length/2 - 0.2, anc_y, 0])
        circuit.add(anc_line, anc_label)
        
        return circuit
    
    def create_cnot(self, center, idx):
        circuit = VGroup()
        line_spacing = 0.25
        anc_y = center[1] + 0.4 - 4 * line_spacing
        cnot_x = center[0] - 0.5 + idx * 0.4
        data_y = center[1] + 0.4 - idx * line_spacing
        
        control = Dot([cnot_x, data_y, 0], radius=0.04, color=WHITE)
        vline = Line([cnot_x, data_y, 0], [cnot_x, anc_y, 0], stroke_color=WHITE, stroke_width=2)
        target = Circle(radius=0.05, stroke_color=WHITE, stroke_width=2).move_to([cnot_x, anc_y, 0])
        plus_h = Line([cnot_x - 0.03, anc_y, 0], [cnot_x + 0.03, anc_y, 0], stroke_color=WHITE, stroke_width=2)
        plus_v = Line([cnot_x, anc_y - 0.03, 0], [cnot_x, anc_y + 0.03, 0], stroke_color=WHITE, stroke_width=2)
        
        circuit.add(control, vline, target, plus_h, plus_v)
        return circuit
    
    def create_m_box(self, center, circuit_type):
        color = DARK_BLUE_Z if circuit_type == "Z" else LIGHT_BLUE_X
        line_spacing = 0.25
        line_length = 1.8
        anc_y = center[1] + 0.4 - 4 * line_spacing
        
        m_box = Rectangle(
            width=0.2, height=0.2, 
            stroke_color=WHITE, stroke_width=2, 
            fill_color=color, fill_opacity=0.8
        ).move_to([center[0] + line_length/2 - 0.15, anc_y, 0])
        m_text = Text("M", font_size=10, color=WHITE, weight=BOLD).move_to(m_box)
        
        return VGroup(m_box, m_text)
        
    def create_corner_legend(self):
        legend_bg = Rectangle(
            width=3.8, height=2.6,
            fill_color="#000000", fill_opacity=0.95, 
            stroke_color=WHITE, stroke_width=3
        ).to_corner(UR, buff=0.15)
        
        legend_title = Text("LEGEND", font_size=22, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        legend_title.next_to(legend_bg.get_top(), DOWN, buff=0.15)
        
        d_dot = Circle(radius=0.16, color=YELLOW_DATA, fill_opacity=1, stroke_width=3, stroke_color=BLUE_STROKE)
        d_label = Text("D = Data |0⟩ |1⟩", font_size=16, font=DEFAULT_FONT, color=YELLOW_DATA, weight=BOLD) 
        d_row = VGroup(d_dot, d_label).arrange(RIGHT, buff=0.15)
        
        z_dot = Circle(radius=0.13, color=DARK_BLUE_Z, fill_opacity=1, stroke_width=3, stroke_color=BLUE_STROKE)
        z_label = Text("Z = Bit Flip Detect", font_size=16, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        z_row = VGroup(z_dot, z_label).arrange(RIGHT, buff=0.15)
        
        x_dot = Circle(radius=0.13, color=LIGHT_BLUE_X, fill_opacity=1, stroke_width=3, stroke_color=BLUE_STROKE)
        x_label = Text("X = Phase Flip Detect", font_size=16, font=DEFAULT_FONT, color=LIGHT_BLUE_X, weight=BOLD)
        x_row = VGroup(x_dot, x_label).arrange(RIGHT, buff=0.15)
        
        legend_items = VGroup(d_row, z_row, x_row).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend_items.next_to(legend_title, DOWN, buff=0.2)
        
        self.corner_legend = VGroup(legend_bg, legend_title, legend_items)
        self.play(FadeIn(self.corner_legend), run_time=0.5)


    def intro(self):
        title = Text("Surface Code", font_size=80, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        subtitle = Text("Quantum Error Correction", font_size=40, font=DEFAULT_FONT, color=GRAY_TEXT).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=UP*0.3), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.5)

    def show_legend(self):
        self.update_caption("Understanding Qubits and Error Types", WHITE)
        
        title = Text("Qubit Types & Stabilizers", font_size=38, color=WHITE, weight=BOLD).to_edge(UP, buff=0.6)
        self.play(FadeIn(title), run_time=0.5)
        
        data_circle = Circle(radius=0.6, color=YELLOW_DATA, fill_opacity=1, stroke_color=BLUE_STROKE, stroke_width=5)
        data_label = Text("|0⟩", font_size=42, font=DEFAULT_FONT, color="#000000", weight=BOLD)
        data_vis = VGroup(data_circle, data_label)
        data_title = Text("D = Data Qubit (Yellow)", font_size=32, font=DEFAULT_FONT, color=YELLOW_DATA, weight=BOLD)
        data_desc = Text("Stores info in |0⟩ or |1⟩", font_size=24, font=DEFAULT_FONT, color=GRAY_TEXT)
        data_text = VGroup(data_title, data_desc).arrange(DOWN, buff=0.1)
        data_row = VGroup(data_vis, data_text).arrange(RIGHT, buff=0.6).move_to(UP * 2)
        
        z_circle = Circle(radius=0.45, color=DARK_BLUE_Z, fill_opacity=1, stroke_color=BLUE_STROKE, stroke_width=5)
        z_label = Text("Z", font_size=32, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        z_vis = VGroup(z_circle, z_label)
        z_title = Text("Z-Stabilizer (Dark Blue)", font_size=30, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        z_desc = Text("Detects BIT-FLIP (|0⟩ ↔ |1⟩)", font_size=22, font=DEFAULT_FONT, color=RED_ERROR)
        z_text = VGroup(z_title, z_desc).arrange(DOWN, buff=0.1)
        z_row = VGroup(z_vis, z_text).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
        
        x_circle = Circle(radius=0.45, color=LIGHT_BLUE_X, fill_opacity=1, stroke_color=BLUE_STROKE, stroke_width=5)
        x_label = Text("X", font_size=32, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        x_vis = VGroup(x_circle, x_label)
        x_title = Text("X-Stabilizer (Light Blue)", font_size=30, font=DEFAULT_FONT, color=LIGHT_BLUE_X, weight=BOLD)
        x_desc = Text("Detects PHASE-FLIP (|+⟩ ↔ |−⟩)", font_size=22, font=DEFAULT_FONT, color=PURPLE)
        x_text = VGroup(x_title, x_desc).arrange(DOWN, buff=0.1)
        x_row = VGroup(x_vis, x_text).arrange(RIGHT, buff=0.6).move_to(DOWN * 1.9)
        
        self.play(FadeIn(data_row), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(z_row), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(x_row), run_time=0.8)
        self.wait(1.5)
        
        self.play(FadeOut(title), FadeOut(data_row), FadeOut(z_row), FadeOut(x_row), run_time=0.8)

    def build_lattice(self):
        self.update_caption("Building the Surface Code lattice (3x4 data qubits)", YELLOW_DATA)
        
        self.y_spacing = 0.75
        self.y_rows = 3
        self.y_cols = 4
        self.lattice_center = UP * 1.2  
        self.half = self.y_spacing / 2
        
        self.data_qubits = VGroup()
        self.data_grid = {}
        
        for row in range(self.y_rows):
            for col in range(self.y_cols):
                x = (col - (self.y_cols-1)/2) * self.y_spacing
                y = (row - (self.y_rows-1)/2) * self.y_spacing
                pos = np.array([x, y, 0]) + self.lattice_center
                qubit = DataQubit(position=pos, initial_state=0)
                self.data_qubits.add(qubit)
                self.data_grid[(row, col)] = qubit
        
        self.z_stabilizers = VGroup()
        self.x_stabilizers = VGroup()
        self.z_info = []
        self.x_info = []
        
        for row in range(self.y_rows + 1):
            for col in range(self.y_cols + 1):
                x = (col - self.y_cols/2) * self.y_spacing
                y = (row - self.y_rows/2) * self.y_spacing
                pos = np.array([x, y, 0]) + self.lattice_center
                
                neighbors = []
                if row > 0 and col > 0:
                    neighbors.append(self.data_grid[(row-1, col-1)])
                if row > 0 and col < self.y_cols:
                    neighbors.append(self.data_grid[(row-1, col)])
                if row < self.y_rows and col > 0:
                    neighbors.append(self.data_grid[(row, col-1)])
                if row < self.y_rows and col < self.y_cols:
                    neighbors.append(self.data_grid[(row, col)])
                
                if len(neighbors) == 0:
                    continue
                
                if (row + col) % 2 == 0:
                    qubit = StabilizerQubit(position=pos, qubit_type="Z")
                    self.z_stabilizers.add(qubit)
                    self.z_info.append({"qubit": qubit, "home": pos.copy(), "neighbors": neighbors})
                else:
                    qubit = StabilizerQubit(position=pos, qubit_type="X")
                    self.x_stabilizers.add(qubit)
                    self.x_info.append({"qubit": qubit, "home": pos.copy(), "neighbors": neighbors})
        
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in self.data_qubits], lag_ratio=0.04), run_time=1.5)
        
        self.update_caption("Adding stabilizer qubits", LIGHT_BLUE_X)
        
        self.play(
            LaggedStart(*[FadeIn(q, scale=0.5) for q in self.z_stabilizers], lag_ratio=0.03),
            LaggedStart(*[FadeIn(q, scale=0.5) for q in self.x_stabilizers], lag_ratio=0.03),
            run_time=1.2
        )
        
        self.create_corner_legend()
        self.update_caption("Each data qubit surrounded by Z and X stabilizers", WHITE)
        self.wait(1.5)

    def show_syndrome_extraction(self):
        self.update_caption("Syndrome extraction: Stabilizers check neighboring data qubits", WHITE)
        
        self.x_circuit_pos = LEFT * 5.0 + DOWN * 2.0
        self.z_circuit_pos = RIGHT * 5.0 + DOWN * 2.0
        
        self.x_circuit = self.create_circuit(self.x_circuit_pos, "X")
        self.z_circuit = self.create_circuit(self.z_circuit_pos, "Z")
        
        self.x_circuit_label = Text("X-Syndrome", font_size=20, font=DEFAULT_FONT, color=LIGHT_BLUE_X, weight=BOLD)
        self.x_circuit_label.next_to(self.x_circuit, UP, buff=0.15)
        
        self.z_circuit_label = Text("Z-Syndrome", font_size=20, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        self.z_circuit_label.next_to(self.z_circuit, UP, buff=0.15)
        
        self.play(
            Create(self.x_circuit), FadeIn(self.x_circuit_label),
            Create(self.z_circuit), FadeIn(self.z_circuit_label),
            run_time=1
        )

        self.x_measure_zone = LEFT * 6.0 + UP * 0.5
        self.z_measure_zone = RIGHT * 6.0 + UP * 0.5
        
        diagonals = [
            np.array([1, 1, 0]), 
            np.array([-1, 1, 0]), 
            np.array([-1, -1, 0]), 
            np.array([1, -1, 0])
        ]

        self.update_caption("X-stabilizers move to neighbors and ENTANGLE", LIGHT_BLUE_X)
        
        for idx, diag in enumerate(diagonals):
            move_dist = self.half * 0.5
            normalized_diag = diag / np.linalg.norm(diag)
            
            move_x = [info["qubit"].animate.shift(normalized_diag * move_dist) for info in self.x_info]
            self.play(*move_x, run_time=0.3)
            
            entangle_lines = VGroup()
            for info in self.x_info:
                pos = info["qubit"].get_center()
                for neighbor in info["neighbors"]:
                    y_pos = neighbor.get_center()
                    if np.linalg.norm(pos - y_pos) < self.half * 0.85:
                        neighbor.highlight_ring.set_stroke(color=LIGHT_BLUE_X, opacity=0.9)
                        ent_line = Line(pos, y_pos, color=LIGHT_BLUE_X, stroke_width=2, stroke_opacity=0.8)
                        entangle_lines.add(ent_line)
            
            self.play(Create(entangle_lines), run_time=0.15)
            self.wait(0.08)
            
            self.play(FadeOut(entangle_lines), run_time=0.1)
            for dq in self.data_qubits:
                dq.highlight_ring.set_stroke(opacity=0)
            
            return_x = [info["qubit"].animate.move_to(info["home"]) for info in self.x_info]
            self.play(*return_x, run_time=0.2)
            
            x_cnot = self.create_cnot(self.x_circuit_pos, idx)
            self.play(Create(x_cnot), run_time=0.1)
            self.x_circuit.add(x_cnot)

        self.update_caption("Shuttling to measurement zone", LIGHT_BLUE_X)
        
        num_x = len(self.x_stabilizers)
        cols = 4
        x_positions = [
            self.x_measure_zone + RIGHT * (i % cols) * 0.4 + DOWN * (i // cols) * 0.4 
            for i in range(num_x)
        ]
        move_anims = [self.x_stabilizers[i].animate.move_to(x_positions[i]) for i in range(num_x)]
        self.play(*move_anims, run_time=0.7)

        self.x_wait = Text("waiting", font_size=18, font=DEFAULT_FONT, color=GRAY_TEXT)
        self.x_wait.next_to(self.x_measure_zone, UP, buff=0.3)
        self.play(FadeIn(self.x_wait), run_time=0.2)

        self.update_caption("Z-stabilizers move to neighbors and ENTANGLE", WHITE)
        
        for idx, diag in enumerate(diagonals):
            move_dist = self.half * 0.5
            normalized_diag = diag / np.linalg.norm(diag)
            
            move_z = [info["qubit"].animate.shift(normalized_diag * move_dist) for info in self.z_info]
            self.play(*move_z, run_time=0.3)
            
            entangle_lines = VGroup()
            for info in self.z_info:
                pos = info["qubit"].get_center()
                for neighbor in info["neighbors"]:
                    y_pos = neighbor.get_center()
                    if np.linalg.norm(pos - y_pos) < self.half * 0.85:
                        neighbor.highlight_ring.set_stroke(color=DARK_BLUE_Z, opacity=0.9)
                        ent_line = Line(pos, y_pos, color=DARK_BLUE_Z, stroke_width=2, stroke_opacity=0.8)
                        entangle_lines.add(ent_line)
            
            self.play(Create(entangle_lines), run_time=0.15)
            self.wait(0.08)
            
            self.play(FadeOut(entangle_lines), run_time=0.1)
            for dq in self.data_qubits:
                dq.highlight_ring.set_stroke(opacity=0)
            
            return_z = [info["qubit"].animate.move_to(info["home"]) for info in self.z_info]
            self.play(*return_z, run_time=0.2)
            
            z_cnot = self.create_cnot(self.z_circuit_pos, idx)
            self.play(Create(z_cnot), run_time=0.1)
            self.z_circuit.add(z_cnot)

        self.update_caption("Z-stabilizers shuttle to measurement zone", WHITE)
        
        num_z = len(self.z_stabilizers)
        z_positions = [
            self.z_measure_zone + LEFT * (i % cols) * 0.4 + DOWN * (i // cols) * 0.4
            for i in range(num_z)
        ]
        move_anims = [self.z_stabilizers[i].animate.move_to(z_positions[i]) for i in range(num_z)]
        self.play(*move_anims, run_time=0.7)

        self.z_wait = Text("waiting", font_size=18, font=DEFAULT_FONT, color=GRAY_TEXT)
        self.z_wait.next_to(self.z_measure_zone, UP, buff=0.3)
        self.play(FadeIn(self.z_wait), run_time=0.2)

        self.update_caption("FLASH and MEASURE all stabilizers!", ORANGE_ALERT)
        
        x_m = self.create_m_box(self.x_circuit_pos, "X")
        z_m = self.create_m_box(self.z_circuit_pos, "Z")
        self.play(FadeIn(x_m), FadeIn(z_m), run_time=0.3)
        self.x_m_box = x_m
        self.z_m_box = z_m
        
        flash_anims = [x.core.animate.set_stroke(color=WHITE, width=5) for x in self.x_stabilizers]
        flash_anims += [z.core.animate.set_stroke(color=WHITE, width=5) for z in self.z_stabilizers]
        self.play(*flash_anims, run_time=0.25)
        self.wait(0.2)
        
        x_ready = Text("done!", font_size=18, font=DEFAULT_FONT, color=GREEN_OK).move_to(self.x_wait)
        z_ready = Text("done!", font_size=18, font=DEFAULT_FONT, color=GREEN_OK).move_to(self.z_wait)
        
        reset_anims = [x.core.animate.set_color(GREEN_OK).set_stroke(color=BLUE_STROKE, width=3) for x in self.x_stabilizers]
        reset_anims += [z.core.animate.set_color(GREEN_OK).set_stroke(color=BLUE_STROKE, width=3) for z in self.z_stabilizers]
        
        self.play(*reset_anims, Transform(self.x_wait, x_ready), Transform(self.z_wait, z_ready), run_time=0.3)

        self.x_result = Text("+1", font_size=24, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD)
        self.x_result.next_to(self.x_circuit_label, DOWN, buff=0.1)
        
        self.z_result = Text("+1", font_size=24, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD)
        self.z_result.next_to(self.z_circuit_label, DOWN, buff=0.1)
        
        self.play(FadeIn(self.x_result), FadeIn(self.z_result), run_time=0.3)
        
        self.update_caption("Results: +1 and +1 = NO ERRORS DETECTED!", GREEN_OK)
        self.wait(1.5)

        self.update_caption("Stabilizers return to lattice positions", WHITE)
        
        return_x = [self.x_stabilizers[i].animate.move_to(self.x_info[i]["home"]) for i in range(len(self.x_info))]
        reset_x = [x.core.animate.set_color(LIGHT_BLUE_X) for x in self.x_stabilizers]
        self.play(*return_x, *reset_x, FadeOut(self.x_wait), run_time=0.7)
        
        return_z = [self.z_stabilizers[i].animate.move_to(self.z_info[i]["home"]) for i in range(len(self.z_info))]
        reset_z = [z.core.animate.set_color(DARK_BLUE_Z) for z in self.z_stabilizers]
        self.play(*return_z, *reset_z, FadeOut(self.z_wait), run_time=0.7)
        
        self.wait(1)

    def explain_bit_flip(self):
        self.update_caption("", WHITE)
        
        all_elements = VGroup(
            self.data_qubits, self.z_stabilizers, self.x_stabilizers, self.corner_legend,
            self.x_circuit, self.z_circuit, self.x_circuit_label, self.z_circuit_label,
            self.x_m_box, self.z_m_box, self.x_result, self.z_result
        )
        self.play(FadeOut(all_elements), run_time=0.5)
        
        title = Text("What is a Bit-Flip Error?", font_size=56, font=DEFAULT_FONT, color=RED_ERROR, weight=BOLD).to_edge(UP, buff=0.7)
        self.play(FadeIn(title), run_time=0.5)

        before_state = VGroup(
            Text("|0⟩", font_size=60, font=DEFAULT_FONT, color=GREEN_OK),
            Text("or", font_size=26, font=DEFAULT_FONT, color=GRAY_TEXT),
            Text("|1⟩", font_size=60, font=DEFAULT_FONT, color=LIGHT_BLUE_X)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.0 + LEFT * 4.0)
        
        arrow = Arrow(LEFT * 1.5 + UP * 1.0, RIGHT * 1.5 + UP * 1.0, color=RED_ERROR, stroke_width=6)
        error_text = Text("BIT-FLIP (X)", font_size=24, font=DEFAULT_FONT, color=RED_ERROR, weight=BOLD).next_to(arrow, UP, buff=0.15)
        
        after_state = VGroup(
            Text("|1⟩", font_size=60, font=DEFAULT_FONT, color=RED_ERROR),
            Text("or", font_size=26, font=DEFAULT_FONT, color=GRAY_TEXT),
            Text("|0⟩", font_size=60, font=DEFAULT_FONT, color=RED_ERROR)
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.0 + RIGHT * 4.0)
        
        self.play(FadeIn(before_state), run_time=0.5)
        self.wait(0.4)
        self.play(GrowArrow(arrow), FadeIn(error_text), run_time=0.5)
        self.play(FadeIn(after_state), run_time=0.5)
        
        self.update_caption("How Z-stabilizers detect bit-flips", DARK_BLUE_Z)

        detection = Text(
            "Z-Stabilizer checks 4 neighbors:\n" +
            "Counts how many are in |1⟩ state\n" +
            "If ODD number → Result = -1 (ERROR!)\n" +
            "If EVEN number → Result = +1 (OK)",
            font_size=26, font=DEFAULT_FONT, color=WHITE, weight=BOLD,
            line_spacing=1.3
        ).move_to(DOWN * 1.8)
        
        self.play(FadeIn(detection), run_time=0.8)
        self.wait(2.5)
        
        self.play(
            FadeOut(title), FadeOut(before_state), FadeOut(arrow), 
            FadeOut(error_text), FadeOut(after_state), FadeOut(detection),
            run_time=0.5
        )
        
        lattice_elements = VGroup(self.data_qubits, self.z_stabilizers, self.x_stabilizers)
        circuit_elements = VGroup(
            self.x_circuit, self.z_circuit, self.x_circuit_label, self.z_circuit_label,
            self.x_m_box, self.z_m_box, self.x_result, self.z_result
        )
        self.play(FadeIn(lattice_elements), FadeIn(circuit_elements), run_time=0.5)
        self.create_corner_legend()

    def bit_flip_demo(self):
        self.update_caption("BIT-FLIP ERROR DEMONSTRATION", RED_ERROR)
        self.wait(0.5)
        
        error_q = self.data_grid[(1, 1)]
        
        self.update_caption("STEP 1: Bit-flip error hits this data qubit!", RED_ERROR)
        pointing_arrow = Arrow(
            error_q.get_center() + UP * 1.5,
            error_q.get_center() + UP * 0.6,
            color=RED_ERROR,
            stroke_width=8,
            tip_length=0.4
        )
        arrow_label = Text(
            "ERROR HERE!",
            font_size=22,
            font=DEFAULT_FONT,
            color=RED_ERROR,
            weight=BOLD
        ).next_to(pointing_arrow, UP, buff=0.15)

        self.play(
            GrowArrow(pointing_arrow),
            FadeIn(arrow_label),
            run_time=0.5
        )
        
        error_circle = Circle(radius=0.4, color=RED_ERROR, stroke_width=5, fill_opacity=0).move_to(error_q.get_center())
        self.play(FadeIn(error_circle), error_q.core.animate.set_color(RED_ERROR), run_time=0.5)
        
        error_q.state = 1
        new_label = error_q.update_label()
        self.play(Transform(error_q.label, new_label), run_time=0.3)
     
        error_text = Text("BIT-FLIP!", font_size=18, font=DEFAULT_FONT, color=RED_ERROR, weight=BOLD)
        error_text.next_to(error_q, DOWN, buff=1)
        self.play(FadeIn(error_text), run_time=0.3)
        self.wait(0.8)
        
        self.play(
            FadeOut(error_circle),
            FadeOut(pointing_arrow),
            FadeOut(arrow_label),
            run_time=0.3
        )
        
        affected_z = [i for i, info in enumerate(self.z_info) if error_q in info["neighbors"]]
        
        self.update_caption("STEP 2: Z-stabilizers measure parity of neighbors", WHITE)
        self.wait(0.5)
        
        result_labels = []
        
        for idx in affected_z:
            z_stab = self.z_info[idx]["qubit"]
            
            connections = VGroup()
            for neighbor in self.z_info[idx]["neighbors"]:
                line_color = RED_ERROR if neighbor == error_q else GRAY_TEXT
                line = Line(z_stab.get_center(), neighbor.get_center(), color=line_color, stroke_width=2)
                connections.add(line)
            
            self.play(Create(connections), run_time=0.2)
            
            z_stab.core.set_color(ORANGE_ALERT)
            
            r_text = Text("-1", font_size=20, font=DEFAULT_FONT, color=ORANGE_ALERT, weight=BOLD)
            odd_text = Text("(ODD)", font_size=14, font=DEFAULT_FONT, color=ORANGE_ALERT)
            result_grp = VGroup(r_text, odd_text).arrange(RIGHT, buff=0.08)
         
            stab_pos = z_stab.get_center()
            if stab_pos[0] < 0: 
                result_grp.next_to(z_stab, LEFT, buff=0.15)
            else:  
                result_grp.next_to(z_stab, RIGHT, buff=0.15)
            
            result_labels.append(result_grp)
            self.play(FadeIn(result_grp), run_time=0.2)
            
            self.play(FadeOut(connections), run_time=0.12)
        
        new_z_result = Text("-1", font_size=24, font=DEFAULT_FONT, color=ORANGE_ALERT, weight=BOLD)
        new_z_result.next_to(self.z_circuit_label, DOWN, buff=0.1)
        self.play(Transform(self.z_result, new_z_result), run_time=0.3)
        
        self.update_caption("STEP 3: Error at intersection of -1 stabilizers", ORANGE_ALERT)
        
        lines = VGroup()
        for idx in affected_z:
            z_stab = self.z_info[idx]["qubit"]
            line = Line(z_stab.get_center(), error_q.get_center(), color=RED_ERROR, stroke_width=3)
            lines.add(line)
        
        self.play(Create(lines), run_time=0.5)
        self.wait(1.2)
        
        self.play(FadeOut(lines), *[FadeOut(r) for r in result_labels], FadeOut(error_text), run_time=0.3)
        
        self.update_caption("STEP 4: Apply X gate to fix the error", GREEN_OK)
        
        fix_circle = Circle(radius=0.4, color=GREEN_OK, stroke_width=5, fill_opacity=0).move_to(error_q.get_center())
        x_gate = Text("X", font_size=28, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD).move_to(error_q.get_center())
        
        self.play(FadeIn(fix_circle), FadeIn(x_gate), run_time=0.3)
        
        error_q.state = 0
        fixed_label = error_q.update_label()
        
        self.play(
            error_q.core.animate.set_color(YELLOW_DATA),
            Transform(error_q.label, fixed_label),
            FadeOut(fix_circle), FadeOut(x_gate), 
            run_time=0.5
        )
        
        self.update_caption("STEP 5: All stabilizers now show +1 - ERROR CORRECTED!", GREEN_OK)
        
        for z in self.z_stabilizers:
            z.core.set_color(GREEN_OK)
        for x in self.x_stabilizers:
            x.core.set_color(GREEN_OK)
        
        ok_z_result = Text("+1", font_size=24, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD)
        ok_z_result.next_to(self.z_circuit_label, DOWN, buff=0.1)
        self.play(Transform(self.z_result, ok_z_result), run_time=0.3)
        
        self.wait(1.5)
        
        for z in self.z_stabilizers:
            z.core.set_color(DARK_BLUE_Z)
        for x in self.x_stabilizers:
            x.core.set_color(LIGHT_BLUE_X)

    def explain_phase_flip(self):
        self.update_caption("", WHITE)
        
        all_elements = VGroup(
            self.data_qubits, self.z_stabilizers, self.x_stabilizers, self.corner_legend,
            self.x_circuit, self.z_circuit, self.x_circuit_label, self.z_circuit_label,
            self.x_m_box, self.z_m_box, self.x_result, self.z_result
        )
        self.play(FadeOut(all_elements), run_time=0.5)
        
        title = Text("What is a Phase-Flip Error?", font_size=56, font=DEFAULT_FONT, color=PURPLE, weight=BOLD).to_edge(UP, buff=0.7)
        self.play(FadeIn(title), run_time=0.5)
      
        before_state = VGroup(
            Text("|+⟩", font_size=56, font=DEFAULT_FONT, color=GREEN_OK),
            Text("=", font_size=32, font=DEFAULT_FONT, color=GRAY_TEXT),
            Text("(|0⟩+|1⟩)/√2", font_size=26, font=DEFAULT_FONT, color=GRAY_TEXT)
        ).arrange(RIGHT, buff=0.15).move_to(UP * 1.0 + LEFT * 4.0)
        
        arrow = Arrow(LEFT * 1.0 + UP * 1.0, RIGHT * 1.0 + UP * 1.0, color=PURPLE, stroke_width=6)
        error_text = Text("PHASE-FLIP (Z)", font_size=24, font=DEFAULT_FONT, color=PURPLE, weight=BOLD).next_to(arrow, UP, buff=0.15)
        
        after_state = VGroup(
            Text("|−⟩", font_size=56, font=DEFAULT_FONT, color=RED_ERROR),
            Text("=", font_size=32, font=DEFAULT_FONT, color=GRAY_TEXT),
            Text("(|0⟩−|1⟩)/√2", font_size=26, font=DEFAULT_FONT, color=GRAY_TEXT)
        ).arrange(RIGHT, buff=0.15).move_to(UP * 1.0 + RIGHT * 4.0)
        
        self.play(FadeIn(before_state), run_time=0.5)
        self.wait(0.4)
        self.play(GrowArrow(arrow), FadeIn(error_text), run_time=0.5)
        self.play(FadeIn(after_state), run_time=0.5)
        
        insight = Text(
            "The + sign becomes − (phase flips by π)",
            font_size=26, font=DEFAULT_FONT, color=ORANGE_ALERT, weight=BOLD
        ).move_to(DOWN * 0.2)
        self.play(FadeIn(insight), run_time=0.5)
        
        detection = Text(
            "X-Stabilizer checks 4 neighbors:\n" +
            "Counts how many have flipped phase\n" +
            "If ODD number → Result = -1 (ERROR!)\n" +
            "If EVEN number → Result = +1 (OK)",
            font_size=26, font=DEFAULT_FONT, color=WHITE, weight=BOLD,
            line_spacing=1.3
        ).move_to(DOWN * 2.2)
        
        self.play(FadeIn(detection), run_time=0.8)
        self.wait(2.5)
        
        self.play(
            FadeOut(title), FadeOut(before_state), FadeOut(arrow), 
            FadeOut(error_text), FadeOut(after_state), FadeOut(insight), 
            FadeOut(detection), 
            run_time=0.5
        )
        
        lattice_elements = VGroup(self.data_qubits, self.z_stabilizers, self.x_stabilizers)
        circuit_elements = VGroup(
            self.x_circuit, self.z_circuit, self.x_circuit_label, self.z_circuit_label,
            self.x_m_box, self.z_m_box, self.x_result, self.z_result
        )
        self.play(FadeIn(lattice_elements), FadeIn(circuit_elements), run_time=0.5)
        self.create_corner_legend()

    def phase_flip_demo(self):
        self.update_caption("PHASE-FLIP ERROR DEMONSTRATION", PURPLE)
        self.wait(0.5)
        
        error_q = self.data_grid[(1, 2)]
        
        self.update_caption("STEP 1: Phase-flip error hits this data qubit!", PURPLE)
     
        pointing_arrow = Arrow(
            error_q.get_center() + UP * 1.5,
            error_q.get_center() + UP * 0.6,
            color=PURPLE,
            stroke_width=8,
            tip_length=0.4
        )
        arrow_label = Text(
            "PHASE ERROR!",
            font_size=22,
            font=DEFAULT_FONT,
            color=PURPLE,
            weight=BOLD
        ).next_to(pointing_arrow, UP, buff=0.15)
  
        self.play(
            GrowArrow(pointing_arrow),
            FadeIn(arrow_label),
            run_time=0.5
        )
        
        error_circle = Circle(radius=0.4, color=PURPLE, stroke_width=5, fill_opacity=0).move_to(error_q.get_center())
        self.play(
            FadeIn(error_circle), 
            error_q.core.animate.set_color(PURPLE), 
            run_time=0.5
        )
        
        error_text = Text("PHASE-FLIP!", font_size=18, font=DEFAULT_FONT, color=PURPLE, weight=BOLD)
        error_text.next_to(error_q, DOWN, buff=1)
        phase_label = Text("|+⟩ → |−⟩", font_size=20, font=DEFAULT_FONT, color=PURPLE)
        phase_label.next_to(error_q, DOWN, buff=1.6)
        
        self.play(FadeIn(error_text), FadeIn(phase_label), run_time=0.3)
        self.wait(0.8)
        
        self.play(
            FadeOut(error_circle),
            FadeOut(pointing_arrow),
            FadeOut(arrow_label),
            run_time=0.3
        )
        
        affected_x = [i for i, info in enumerate(self.x_info) if error_q in info["neighbors"]]
        
        self.update_caption("STEP 2: X-stabilizers measure phase parity", LIGHT_BLUE_X)
        
        result_labels = []
        for idx in affected_x:
            x_stab = self.x_info[idx]["qubit"]
            
            connections = VGroup()
            for neighbor in self.x_info[idx]["neighbors"]:
                line_color = PURPLE if neighbor == error_q else GRAY_TEXT
                line = Line(x_stab.get_center(), neighbor.get_center(), color=line_color, stroke_width=2)
                connections.add(line)
            
            self.play(Create(connections), run_time=0.2)
            
            x_stab.core.set_color(ORANGE_ALERT)
            
            r_text = Text("-1", font_size=20, font=DEFAULT_FONT, color=ORANGE_ALERT, weight=BOLD)
            odd_text = Text("(ODD)", font_size=14, font=DEFAULT_FONT, color=ORANGE_ALERT)
            result_grp = VGroup(r_text, odd_text).arrange(DOWN, buff=0.05)
            
            stab_pos = x_stab.get_center()
            if stab_pos[0] < 0:
                result_grp.next_to(x_stab, LEFT, buff=0.15)
            else:
                result_grp.next_to(x_stab, RIGHT, buff=0.15)
            
            result_labels.append(result_grp)
            self.play(FadeIn(result_grp), run_time=0.2)
            
            self.play(FadeOut(connections), run_time=0.12)
        
        new_x_result = Text("-1", font_size=24, font=DEFAULT_FONT, color=ORANGE_ALERT, weight=BOLD)
        new_x_result.next_to(self.x_circuit_label, DOWN, buff=0.1)
        self.play(Transform(self.x_result, new_x_result), run_time=0.3)
        
        self.update_caption("STEP 3: Error at intersection of -1 X-syndromes", ORANGE_ALERT)
        
        lines = VGroup()
        for idx in affected_x:
            x_stab = self.x_info[idx]["qubit"]
            line = Line(x_stab.get_center(), error_q.get_center(), color=PURPLE, stroke_width=3)
            lines.add(line)
        
        self.play(Create(lines), run_time=0.5)
        self.wait(1.2)
        
        self.play(FadeOut(lines), *[FadeOut(r) for r in result_labels], FadeOut(error_text), FadeOut(phase_label), run_time=0.3)
        
        self.update_caption("STEP 4: Apply Z gate to fix the phase error", GREEN_OK)
        
        fix_circle = Circle(radius=0.4, color=GREEN_OK, stroke_width=5, fill_opacity=0).move_to(error_q.get_center())
        z_gate = Text("Z", font_size=28, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD).move_to(error_q.get_center())
        
        self.play(FadeIn(fix_circle), FadeIn(z_gate), run_time=0.3)
        self.play(
            error_q.core.animate.set_color(YELLOW_DATA), 
            FadeOut(fix_circle), FadeOut(z_gate), 
            run_time=0.5
        )
        
        self.update_caption("STEP 5: ERROR CORRECTED!", GREEN_OK)
        
        for z in self.z_stabilizers:
            z.core.set_color(GREEN_OK)
        for x in self.x_stabilizers:
            x.core.set_color(GREEN_OK)
        
        ok_x_result = Text("+1", font_size=24, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD)
        ok_x_result.next_to(self.x_circuit_label, DOWN, buff=0.1)
        self.play(Transform(self.x_result, ok_x_result), run_time=0.3)
        
        self.wait(1.5)
        
        for z in self.z_stabilizers:
            z.core.set_color(DARK_BLUE_Z)
        for x in self.x_stabilizers:
            x.core.set_color(LIGHT_BLUE_X)

    def summary(self):
        all_elements = VGroup(
            self.data_qubits, self.z_stabilizers, self.x_stabilizers, self.corner_legend,
            self.x_circuit, self.z_circuit, self.x_circuit_label, self.z_circuit_label,
            self.x_m_box, self.z_m_box, self.x_result, self.z_result
        )
        self.play(FadeOut(all_elements), run_time=0.5)
        self.update_caption("", WHITE)
        
        title = Text("Surface Code Summary", font_size=56, font=DEFAULT_FONT, color=WHITE, weight=BOLD)
        title.move_to(UP * 3.0)
        self.play(FadeIn(title), run_time=0.5)
        
        bf_box = Rectangle(width=5.0, height=2.5, fill_color="#1a1a2e", fill_opacity=0.9, stroke_color=RED_ERROR, stroke_width=3).move_to(LEFT * 3.5 + DOWN * 0.2)
        bf_title = Text("BIT-FLIP ERROR", font_size=28, font=DEFAULT_FONT, color=RED_ERROR, weight=BOLD).move_to(LEFT * 3.5 + UP * 1.6)
        bf_text = Text(
            "Changes: |0⟩ ↔ |1⟩\n" +
            "Detected by: Z-stabilizers\n" +
            "Fixed with: X gate",
            font_size=22, font=DEFAULT_FONT, color=WHITE, line_spacing=1.3
        ).move_to(LEFT * 3.5 + DOWN * 0.2)
        
        pf_box = Rectangle(width=5.0, height=2.5, fill_color="#1a1a2e", fill_opacity=0.9, stroke_color=PURPLE, stroke_width=3).move_to(RIGHT * 3.5 + DOWN * 0.2)
        pf_title = Text("PHASE-FLIP ERROR", font_size=28, font=DEFAULT_FONT, color=PURPLE, weight=BOLD).move_to(RIGHT * 3.5 + UP * 1.6)
        pf_text = Text(
            "Changes: |+⟩ ↔ |−⟩\n" +
            "Detected by: X-stabilizers\n" +
            "Fixed with: Z gate",
            font_size=22, font=DEFAULT_FONT, color=WHITE, line_spacing=1.3
        ).move_to(RIGHT * 3.5 + DOWN * 0.2)
        
        self.play(FadeIn(bf_box), FadeIn(bf_title), FadeIn(bf_text), run_time=0.6)
        self.play(FadeIn(pf_box), FadeIn(pf_title), FadeIn(pf_text), run_time=0.6)
        
        self.wait(1)
        
        insight_box = Rectangle(width=11, height=1.0, fill_color="#000000", fill_opacity=0.9, stroke_color=GREEN_OK, stroke_width=2).move_to(DOWN * 2.5)
        insight = Text(
            "KEY: Error location = intersection of stabilizers showing -1",
            font_size=28, font=DEFAULT_FONT, color=GREEN_OK, weight=BOLD
        ).move_to(DOWN * 2.5)
        
        self.play(FadeIn(insight_box), FadeIn(insight), run_time=0.6)
        self.wait(5)