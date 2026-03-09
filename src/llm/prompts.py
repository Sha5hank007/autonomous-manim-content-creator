# llm/prompts.py

def build_script_prompt(topic: str, num_sections: int) -> str:
    return f"""
You are an expert technical director designing a dynamic Manim animation script.

Topic: {topic}
Number of sections: {num_sections}

You MUST return ONLY valid JSON. No markdown. No explanations.

Return EXACTLY this structure:
{{
  "topic": "{topic}",
  "sections": [
    {{
      "title": "short title",
      "narration": "short narration paragraph",
      "visual_plan": [
        "Phase 1: Initial state description",
        "Phase 2: Dynamic motion or transformation"
      ]
    }}
  ]
}}

FIRST SECTION INTRODUCTION

The first section must visually introduce the topic at a conceptual level.
It should establish the core idea before demonstrating internal mechanisms.
Do not immediately jump into deep system behavior.

CRITICAL VISUAL CONSTRAINTS (FLAT 2D ONLY)

All visuals must remain strictly 2D.
strictly ensure that there is no overlap in animation and objects remain clearly spaced. be creative

Allowed primitives include but are not limited to: Circles, Squares, Rectangles, RoundedRectangles, Polygons, Lines, Arrows, Dots, greenticks

Symbols must act as indicators inside the visual system rather than decorative elements. Be explicit about animation

TEXT REQUIREMENT

Each scene must contain words or relavant information that label or explain components in the animation.
These words should appear as titles, labels, annotations, or explanations attached to objects.
Do not generate scenes made entirely of symbols or shapes without text.

VISUAL COMPLEXITY

Scenes should depict meaningful systems rather than isolated shapes.
Visual structures may include complex arrangements such as:
• clustered components  
• branching structures  
• layered architectures  
• distributed nodes  
• pipelines or flows  
• circular systems  
• modular assemblies  
• network graphs  
• hierarchical structures  
• expanding or contracting groups  

Objects should interact through movement, transformation, or reorganization be creative according to topic

VISUAL CLARITY
- Objects must be placed so they remain clearly visible.
- There must be no overlap between objects.
- Elements should be distributed across the frame so each structure is readable and distinct.
- Avoid stacking objects on top of each other unless the overlap represents a meaningful relationship.

VISUAL PLAN STRUCTURE
- Each section must contain 4–5 phases.

Phase 1  
Establish the layout of the system and introduce the main concept visually.

Phase 2  
Introduce interactions or triggers between components.

Phase 3  
Show transformations, propagation, or internal system behavior.

Phase 4  
Reveal the final system state and highlight the conceptual result.

Each scene should contain multiple interacting elements and should not consist of a single object or minimal diagram.

REQUIREMENTS:
- ONLY valid JSON parseable by json.loads()
- NO 3D objects. Make it dynamic and creative, but strictly 2D.
"""



#============================================================================================================================



def build_manim_prompt(section: dict, duration: float) -> str:
    return f"""
You are an expert technical animator writing highly creative Manim Community v0.19 code.

Section Title: {section['title']}
Narration: {section['narration']}
Visual Plan:
{section['visual_plan']}

Target Duration: {duration:.2f} seconds.


===============================
CRITICAL CODE STRUCTURE REQUIREMENTS
===============================
You are a code generator. You MUST output EXACTLY and ONLY valid Python code. 

RULE 1: The very first line of your output MUST BE:
from manim import *
RULE 2: The class name MUST BE EXACTLY:
class GeneratedScene(Scene):
RULE 3: Do NOT name the class after the section title. Do NOT use `class {{tempting_class_name}}(Scene):`.
RULE 4: Do not include ANY markdown formatting. Do NOT wrap the code in ```python ``` blocks. No backticks. No explanations.

START YOUR RESPONSE EXACTLY LIKE THIS:
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Your code...
        
===============================
STRICT MANIM CODING RULES
===============================
1. SHAPES & COLORS (NO HALLUCINATIONS):
- Use only these classes: Rectangle,RoundedRectangle,Circle,Square,Dot,Line,Arrow,Text,VGroup,DashedLine.
- Use only these Manim colors:
   Base colors: WHITE,BLACK,BLUE,GREEN,RED,YELLOW,ORANGE,PURPLE,PINK,TEAL,GOLD,GRAY

   Variant colors allowed ONLY for: BLUE_A,BLUE_B,BLUE_C,BLUE_D,BLUE_E, GREEN_A,GREEN_B,GREEN_C,GREEN_D,GREEN_E, RED_A,RED_B,RED_C,RED_D,RED_E, YELLOW_A,YELLOW_B,YELLOW_C,YELLOW_D,YELLOW_E, GRAY_A,GRAY_B,GRAY_C,GRAY_D,GRAY_E
- And never use BLACK text

2. MACRO LAYOUT (CRITICAL FIX):
- Group objects (`VGroup`), arrange them (`.arrange()` or `.next_to()`), combine into a single `full_diagram`, and center it (`.move_to(ORIGIN)`).
The animation may also include symbolic indicators rendered through text or shapes such as:
✓ ✗ → ↑ ↓ ⚡ ⚙ 📦 🔒 and any other symbol supported by Manim.

3. ARROWS:
- Arrows MUST ONLY connect to VGroups. 
- Draw arrows ONLY AFTER scaling the `full_diagram`.

===============================
CREATIVE ARSENAL (USE THESE!)
===============================
- ENTRY: Use `DrawBorderThenFill`, `GrowFromCenter`, or `SpinInFromNothing`.
- GROUP ENTRY: Use `LaggedStart(*[Create(obj) for obj in group], lag_ratio=0.1)`.
- HIGHLIGHTING: Use `Indicate(object)` or `Circumscribe(object, color=YELLOW)`.
- FLOW: Use `MoveAlongPath(dot, arrow)` for data transfer. 
- MORPHING: Use `ReplacementTransform(old_group, new_group)` to show state changes.
===============================
COMPLEX SCENE TEMPLATE :
take this code structure as a reference. Pay close attention to the CREATIVE RECIPES used for data flow and chunking.
but dont replicate exactly be free and creative to add elements

from manim import *

class DataModelVariety(Scene):
    def construct(self):
        # Define common properties for containers
        container_width = 2.5
        container_height = 2.0
        padding = 1.0 # Spacing between conceptual sections

        # Phase 1: Four distinct, empty container shapes appear across the screen

        # Key-Value Container
        kv_container = Rectangle(width=container_width, height=container_height, color=BLUE, stroke_width=2)
        kv_label = Text("Key-Value", font_size=28, color=WHITE).next_to(kv_container, UP, buff=0.3)
        kv_group = VGroup(kv_container, kv_label)

        # Document Container
        doc_outer = RoundedRectangle(width=container_width, height=container_height, corner_radius=0.2, color=BLUE, stroke_width=2)
        doc_inner = RoundedRectangle(width=container_width * 0.8, height=container_height * 0.8, corner_radius=0.15, color=BLUE, stroke_width=1).move_to(doc_outer)
        doc_container = VGroup(doc_outer, doc_inner)
        doc_label = Text("Document", font_size=28, color=WHITE).next_to(doc_container, UP, buff=0.3)
        doc_group = VGroup(doc_container, doc_label)

        # Column-Family Container
        col_width_single = container_width / 3.0
        col_spacing = 0.05 # Small gap between columns
        col1_rect = Rectangle(width=col_width_single - col_spacing, height=container_height, color=BLUE, stroke_width=2)
        col2_rect = Rectangle(width=col_width_single - col_spacing, height=container_height, color=BLUE, stroke_width=2).next_to(col1_rect, RIGHT, buff=col_spacing)
        col3_rect = Rectangle(width=col_width_single - col_spacing, height=container_height, color=BLUE, stroke_width=2).next_to(col2_rect, RIGHT, buff=col_spacing)
        col_container = VGroup(col1_rect, col2_rect, col3_rect)
        col_label = Text("Column-Family", font_size=28, color=WHITE).next_to(col_container, UP, buff=0.3)
        col_group = VGroup(col_container, col_label)

        # Graph Container (initial nodes and edges)
        graph_node1 = Circle(radius=0.3, color=BLUE, stroke_width=2, fill_opacity=0.5)
        graph_node2 = Circle(radius=0.3, color=BLUE, stroke_width=2, fill_opacity=0.5).shift(RIGHT * 1.0)
        graph_node3 = Circle(radius=0.3, color=BLUE, stroke_width=2, fill_opacity=0.5).shift(UP * 1.0)
        graph_edge1 = Line(graph_node1.get_center(), graph_node2.get_center(), color=BLUE, stroke_width=2)
        graph_edge2 = Line(graph_node2.get_center(), graph_node3.get_center(), color=BLUE, stroke_width=2)
        graph_edge3 = Line(graph_node3.get_center(), graph_node1.get_center(), color=BLUE, stroke_width=2)
        graph_container = VGroup(graph_node1, graph_node2, graph_node3, graph_edge1, graph_edge2, graph_edge3)
        graph_label = Text("Graph", font_size=28, color=WHITE).next_to(graph_container, UP, buff=0.3)
        graph_group = VGroup(graph_container, graph_label)

        # Arrange all groups horizontally and center them
        all_groups = VGroup(kv_group, doc_group, col_group, graph_group).arrange(RIGHT, buff=padding * 0.75).center()
        
        # Re-assign individual components to their new positions after arrangement
        kv_container = all_groups[0][0]
        kv_label = all_groups[0][1]
        doc_container = all_groups[1][0]
        doc_label = all_groups[1][1]
        col_container = all_groups[2][0]
        col_label = all_groups[2][1]
        graph_container = all_groups[3][0]
        graph_label = all_groups[3][1]

        # Animation for Phase 1
        self.play(
            LaggedStart(
                Create(kv_container), Create(kv_label),
                Create(doc_container), Create(doc_label),
                Create(col_container), Create(col_label),
                Create(graph_container), Create(graph_label),
                lag_ratio=0.05,
                run_time=3.0
            )
        )

        # Phase 2: Key-Value data demonstration
        key_shape = Polygon(
            [-0.3, 0.2, 0], [0.3, 0.2, 0], [0.3, -0.2, 0],
            [0.1, -0.2, 0], [0.1, -0.4, 0], [-0.1, -0.4, 0],
            [-0.1, -0.2, 0], [-0.3, -0.2, 0]
        ).scale(0.8).set_color(GOLD).set_stroke(WHITE, width=1.5).shift(LEFT * 0.5)
        value_shape = Rectangle(width=1.0, height=0.6, color=TEAL, fill_opacity=0.8).set_stroke(WHITE, width=1.5).shift(RIGHT * 0.5)
        kv_data = VGroup(key_shape, value_shape).next_to(kv_container, DOWN, buff=0.5)

        self.play(Create(kv_data), run_time=0.8)
        self.play(
            kv_data.animate.move_to(kv_container.get_center()).scale(0.6).fade(0.2),
            kv_container.animate.set_stroke(color=YELLOW, width=5),
            run_time=0.6
        )
        self.play(
            kv_container.animate.set_stroke(color=BLUE, width=2),
            run_time=0.6
        )

        # Phase 3: Document data demonstration (JSON-like structure)
        json_dot_key1 = Dot(color=PINK, radius=0.08) # Key dot
        json_line1 = Line(ORIGIN, RIGHT * 0.3, color=WHITE, stroke_width=1.5).next_to(json_dot_key1, RIGHT, buff=0.05)
        json_dot_val1 = Dot(color=PURPLE, radius=0.08).next_to(json_line1, RIGHT, buff=0.05) # Value dot

        json_dot_key2 = Dot(color=PINK, radius=0.08).next_to(json_dot_key1, DOWN, buff=0.2).align_to(json_dot_key1, LEFT)
        json_line2 = Line(ORIGIN, RIGHT * 0.3, color=WHITE, stroke_width=1.5).next_to(json_dot_key2, RIGHT, buff=0.05)
        json_dot_val2 = Dot(color=PURPLE, radius=0.08).next_to(json_line2, RIGHT, buff=0.05)

        json_dot_key3 = Dot(color=PINK, radius=0.08).next_to(json_dot_key2, DOWN, buff=0.2).align_to(json_dot_key2, LEFT) # Nested object key
        json_line3 = Line(ORIGIN, RIGHT * 0.3, color=WHITE, stroke_width=1.5).next_to(json_dot_key3, RIGHT, buff=0.05)

        nested_offset = 0.2
        nested_dot_key1 = Dot(color=PINK, radius=0.06).next_to(json_line3, RIGHT, buff=0.1).shift(UP * nested_offset)
        nested_line1 = Line(ORIGIN, RIGHT * 0.2, color=WHITE, stroke_width=1).next_to(nested_dot_key1, RIGHT, buff=0.03)
        nested_dot_val1 = Dot(color=PURPLE, radius=0.06).next_to(nested_line1, RIGHT, buff=0.03)

        nested_dot_key2 = Dot(color=PINK, radius=0.06).next_to(nested_dot_key1, DOWN, buff=0.15).align_to(nested_dot_key1, LEFT)
        nested_line2 = Line(ORIGIN, RIGHT * 0.2, color=WHITE, stroke_width=1).next_to(nested_dot_key2, RIGHT, buff=0.03)
        nested_dot_val2 = Dot(color=PURPLE, radius=0.06).next_to(nested_line2, RIGHT, buff=0.03)

        doc_data = VGroup(
            json_dot_key1, json_line1, json_dot_val1,
            json_dot_key2, json_line2, json_dot_val2,
            json_dot_key3, json_line3,
            nested_dot_key1, nested_line1, nested_dot_val1,
            nested_dot_key2, nested_line2, nested_dot_val2
        ).scale(1.2).next_to(doc_container, DOWN, buff=0.5)

        self.play(LaggedStart(*[Create(m) for m in doc_data], lag_ratio=0.05), run_time=1.5)
        self.play(
            doc_data.animate.move_to(doc_container.get_center()).scale(0.7).fade(0.3),
            doc_container.animate.set_stroke(color=YELLOW, width=5),
            run_time=0.8
        )
        self.play(
            doc_container.animate.set_stroke(color=BLUE, width=2),
            run_time=0.7
        )

        # Phase 4: Column-Family data demonstration
        col1_obj, col2_obj, col3_obj = col_container # Unpack the individual column rectangles
        data_cells_start = VGroup()
        data_cells_end = VGroup()
        cell_side = 0.4
        num_rows = 3
        cell_y_spacing = (col1_obj.height - cell_side) / (num_rows - 1) if num_rows > 1 else 0

        for i in range(num_rows):
            y_pos_in_column = col1_obj.get_top()[1] - cell_side/2 - i * cell_y_spacing

            cell_col1_end = Square(side_length=cell_side, color=ORANGE, fill_opacity=1.0).set_stroke(WHITE, width=1).move_to([col1_obj.get_center()[0], y_pos_in_column, 0])
            cell_col2_end = Square(side_length=cell_side, color=ORANGE, fill_opacity=1.0).set_stroke(WHITE, width=1).move_to([col2_obj.get_center()[0], y_pos_in_column, 0])
            cell_col3_end = Square(side_length=cell_side, color=ORANGE, fill_opacity=1.0).set_stroke(WHITE, width=1).move_to([col3_obj.get_center()[0], y_pos_in_column, 0])

            cell_col1_start = cell_col1_end.copy().shift(UP * 1.5)
            cell_col2_start = cell_col2_end.copy().shift(UP * 1.5)
            cell_col3_start = cell_col3_end.copy().shift(UP * 1.5)

            data_cells_start.add(cell_col1_start, cell_col2_start, cell_col3_start)
            data_cells_end.add(cell_col1_end, cell_col2_end, cell_col3_end)

        self.play(
            LaggedStart(
                *[Transform(s, e) for s, e in zip(data_cells_start, data_cells_end)],
                lag_ratio=0.1
            ),
            col_container.animate.set_stroke(color=YELLOW, width=5),
            run_time=1.5
        )
        self.play(
            col_container.animate.set_stroke(color=BLUE, width=2),
            run_time=1.0
        )

        # Phase 5: Graph data demonstration
        # Existing nodes/edges are within graph_container
        new_node4 = Circle(radius=0.25, color=GREEN, fill_opacity=1.0).set_stroke(WHITE, width=1.5)
        new_node5 = Circle(radius=0.25, color=GREEN, fill_opacity=1.0).set_stroke(WHITE, width=1.5)

        # Calculate final positions relative to existing graph_container
        node1_center = graph_container[0].get_center()
        node2_center = graph_container[1].get_center()
        node3_center = graph_container[2].get_center()

        new_node4.move_to(node1_center + DOWN * 1.0 + RIGHT * 0.3)
        new_node5.move_to(node1_center + LEFT * 1.0 + DOWN * 0.3)

        new_edge4 = Line(graph_container[0].get_edge_center(DOWN), new_node4.get_edge_center(UP), color=GREEN, stroke_width=2)
        new_edge5 = Line(new_node4.get_edge_center(RIGHT), graph_container[1].get_edge_center(DOWN), color=GREEN, stroke_width=2)
        new_edge6 = Line(new_node5.get_edge_center(RIGHT), graph_container[0].get_edge_center(LEFT), color=GREEN, stroke_width=2)
        new_edge7 = Line(new_node5.get_edge_center(UP), graph_container[2].get_edge_center(LEFT), color=GREEN, stroke_width=2)
        new_edge8 = Line(new_node4.get_center(), new_node5.get_center(), color=GREEN, stroke_width=2)

        # Initial positions for incoming nodes/edges (off-screen or displaced)
        new_node4_start = new_node4.copy().shift(DOWN * 1.5)
        new_node5_start = new_node5.copy().shift(LEFT * 1.5)
        new_edge4_start = Line(graph_container[0].get_edge_center(DOWN), new_node4_start.get_edge_center(UP), color=GREEN, stroke_width=2)
        new_edge5_start = Line(new_node4_start.get_edge_center(RIGHT), graph_container[1].get_edge_center(DOWN), color=GREEN, stroke_width=2)
        new_edge6_start = Line(new_node5_start.get_edge_center(RIGHT), graph_container[0].get_edge_center(LEFT), color=GREEN, stroke_width=2)
        new_edge7_start = Line(new_node5_start.get_edge_center(UP), graph_container[2].get_edge_center(LEFT), color=GREEN, stroke_width=2)
        new_edge8_start = Line(new_node4_start.get_center(), new_node5_start.get_center(), color=GREEN, stroke_width=2)

        self.play(
            AnimationGroup(
                GrowFromCenter(new_node4_start),
                GrowFromCenter(new_node5_start),
                Create(new_edge4_start),
                Create(new_edge5_start),
                Create(new_edge6_start),
                Create(new_edge7_start),
                Create(new_edge8_start),
                lag_ratio=0.1
            ),
            run_time=1.0
        )

        self.play(
            Transform(new_node4_start, new_node4),
            Transform(new_node5_start, new_node5),
            Transform(new_edge4_start, new_edge4),
            Transform(new_edge5_start, new_edge5),
            Transform(new_edge6_start, new_edge6),
            Transform(new_edge7_start, new_edge7),
            Transform(new_edge8_start, new_edge8),
            graph_container.animate.set_stroke(color=YELLOW, width=5),
            run_time=0.8
        )
        self.play(
            graph_container.animate.set_stroke(color=BLUE, width=2),
            run_time=0.61
        )

        self.wait(0.5)
        
MACRO LAYOUT & POSITIONING (CRITICAL):
- Manim's camera frame is roughly 14.2 units wide and 8.0 units high.
- If you stack elements vertically (using UP/DOWN), you MUST ensure the total height does not exceed 7.0 units. 
- Use ONLY standard positioning methods: `.move_to()`, `.next_to()`, `.shift()`, `.arrange()`, and `.arrange_in_grid()`.
- NEVER invent layout methods (NO `.arrange_in_triangle()`, NO `.arrange_circular()`).
- Group ALL elements (`VGroup`), arrange them, and scale the `full_diagram` to fit `config.frame_height * 0.8` or `config.frame_width * 0.8` BEFORE animating.
- Arrows MUST ONLY connect to the edges of VGroups or Shapes, not overlap them.        


CAMERA FRAME RULES (STRICT)
All objects must stay inside the Manim camera frame. 
strictly ensure that there is no overlap and objects remain clearly spaced.

MANIM API RULES (STRICT)
Do NOT invent classes or parameters.
Allowed constructor args: width,height,radius,color,fill_opacity,stroke_width.
Allowed methods: move_to,next_to,shift,scale,arrange,arrange_in_grid,set_color,set_fill,set_stroke,rotate.
set_stroke may only use: color,opacity,width.
If dashed lines are needed use DashedLine.
If unsure about a parameter name, do NOT include it. Use only parameters listed in the allowed parameter list.



LAYOUT & CONTRAST RULES (STRICT)
Objects must not overlap unless representing containment or stacking.
Text must never exceed its container width. If needed, shorten labels.
Ensure clear spacing using arrange(), next_to(), and buff so elements remain readable.
Boxes must be large enough to comfortably contain their labels.
Vertical stacking must stay within the camera frame. When placing objects below a main diagram, use small spacing (buff ≤ 1.0) and ensure total layout height stays under ~80% of the frame height.

Finally center the diagram with move_to(ORIGIN).
Never shift or reposition the full diagram after this final scaling step.

===============================
YOUR TASK
===============================
- Write the full Scene class starting with `from manim import *`.
- Use `ReplacementTransform` if the script mentions splitting, chunking, or dividing.
- Use `Dot` and `.animate.move_to` if the script mentions data flow.
- Animations should roughly match the target duration. If animation time is shorter than the target duration, keep the last frame visible using self.wait().
- Never use self.wait(0) or negative values.
- The final frame must not be empty.

OUTPUT ONLY RAW PYTHON CODE. NO MARKDOWN FORMATTING. NO BACKTICKS.
"""