from manim import *
import numpy as np

# We define the Apple-inspired colors for consistency
COLOR_BG = "#1C1C1E"
COLOR_GROUND = "#8E8E93"
COLOR_GREY_BALL = "#E5E5EA"
COLOR_BLUE_BALL = "#007AFF"
COLOR_VEC_G = "#FF3B30"     # Apple Red for gravity
COLOR_VEC_V_X = "#32ADE6"   # Apple Cyan for initial velocity

class Scene1_Act1_Drop(Scene):
    def construct(self):

        self.camera.background_color = COLOR_BG
        # ==================================================
        # --- 0. THE FADING BACKGROUND GRID ---
        # ==================================================
        grid = VGroup()
        max_x = 12
        max_y = 8
        grid_spacing = 0.5
        
        # Helper function to create a line that fades out at its ends
        def get_fading_line(start, end, peak_opacity):
            line_segments = VGroup()
            segs = 30
            vec = end - start
            for i in range(segs):
                p1 = start + vec * (i / segs)
                p2 = start + vec * ((i + 1) / segs)
                # Parabolic fade along the line length
                t = (i + 0.5) / segs
                op = peak_opacity *0.25* (1 - (2*t - 1)**2)
                line_segments.add(Line(p1, p2, stroke_opacity=op, stroke_width=1, color="#E5E5EA"))
            return line_segments
            
        # Vertical grid lines (fade based on X distance from center)
        for x in np.arange(-max_x, max_x + 0.1, grid_spacing):
            peak = 0.2 * (1 - (abs(x)/max_x)**1.5) # The 0.2 controls maximum grid opacity
            if peak > 0:
                grid.add(get_fading_line(UP*max_y + RIGHT*x, DOWN*max_y + RIGHT*x, peak))
                
        # Horizontal grid lines (fade based on Y distance from center)
        for y in np.arange(-max_y, max_y + 0.1, grid_spacing):
            peak = 0.2 * (1 - (abs(y)/max_y)**1.5)
            if peak > 0:
                grid.add(get_fading_line(LEFT*max_x + UP*y, RIGHT*max_x + UP*y, peak))

        self.play(
            LaggedStart(
                *[Create(line) for line in grid],
                lag_ratio=0.02
            ),
            run_time=3
        )

        ground = Line(start=LEFT*7, end=RIGHT*7, color=COLOR_GROUND, stroke_width=2)
        ground.to_edge(DOWN, buff=1)

        ball_core = Circle(radius=0.3, color=COLOR_GREY_BALL, fill_opacity=1)
        ball_glow = Circle(radius=0.4, color=COLOR_GREY_BALL, fill_opacity=0.15, stroke_width=0)
        ball = VGroup(ball_glow, ball_core)
        
        # Ensure the ball is drawn on top of the vectors
        ball.set_z_index(1) 
        
        start_pos = np.array([-5.0, 2.5, 0.0])
        ball.move_to(start_pos)

        # Fade in sequence
        self.play(FadeIn(ground, shift=UP*0.5), run_time=1.5, rate_func=smooth)
        self.wait()
        self.play(FadeIn(ball, scale=0.5), run_time=1.5)
        self.wait(2) 

        # --- NEW: Gravity Vector for Drop ---
        grav_vec_drop = Arrow(
            start=ball.get_center(),
            end=ball.get_center() + DOWN * 1.5,
            color=COLOR_VEC_G,
            buff=0,
            stroke_width=6
        ).set_z_index(0) # Ensure vector is drawn behind the ball
        
        grav_lbl_drop = MathTex("g", color=COLOR_VEC_G).next_to(grav_vec_drop, RIGHT, buff=0.2).set_z_index(0)

        # Introduce the vector static (allows VO explanation before movement)
        self.play(GrowArrow(grav_vec_drop), Write(grav_lbl_drop), run_time=1)
        self.wait(2) 

        drop_distance = ball.get_y() - ground.get_y() - ball_core.radius

        # TRUE PHYSICS: Alpha acts as pure time. Squaring it mimics perfect gravity.
        def drop_physics(mob, alpha):
            y = start_pos[1] - (drop_distance * (alpha ** 2))
            mob.move_to(np.array([start_pos[0], y, 0]))

        # The Drop (Vector fades out concurrently as ball falls in front of it)
        self.play(
            UpdateFromAlphaFunc(ball, drop_physics),
            FadeOut(VGroup(grav_vec_drop, grav_lbl_drop), run_time=0.7), # Fades out during the first half of the drop
            run_time=2,
            rate_func=linear 
        )

        # The Impact Ripple
        ripple = Circle(radius=0.3, color=COLOR_GREY_BALL, stroke_width=4)
        ripple.move_to(ball.get_center())
        self.play(
            ripple.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )
        self.wait()


        # Clear the first ball
        self.play(FadeOut(ball))

        # Create the Second Ball
        ball2_core = Circle(radius=0.3, color=COLOR_BLUE_BALL, fill_opacity=1)
        ball2_glow = Circle(radius=0.4, color=COLOR_BLUE_BALL, fill_opacity=0.15, stroke_width=0)
        ball2 = VGroup(ball2_glow, ball2_core)
        ball2.move_to(start_pos)
        ball2.set_z_index(1) 

        # Fade in
        self.play(FadeIn(ball2, scale=0.5), run_time=1.5)
        self.wait(1.5)


        # --- NEW: Vectors for the Throw (g and vx) ---
        grav_vec_throw = Arrow(
            start=ball2.get_center(), end=ball2.get_center() + DOWN * 1.5,
            color=COLOR_VEC_G, buff=0, stroke_width=6
        ).set_z_index(0) 
        grav_lbl_throw = MathTex("g", color=COLOR_VEC_G).next_to(grav_vec_throw, RIGHT, buff=0.1)

        vx_vec = Arrow(
            start=ball2.get_center(), end=ball2.get_center() + RIGHT * 1.5,
            color=COLOR_VEC_V_X, buff=0, stroke_width=6
        ).set_z_index(0) 
        vx_lbl = MathTex("v_x", color=COLOR_VEC_V_X).next_to(vx_vec, DOWN, buff=0.1)

        # Introduce both vectors while stationary
        self.play(
            GrowArrow(vx_vec), Write(vx_lbl),
            GrowArrow(grav_vec_throw), Write(grav_lbl_throw),
            run_time=1.5
        )
        self.wait(2.5) 

        horizontal_distance = 10.0 

        # TRUE PHYSICS + Dynamic Vector Updates
        def throw_physics(mob, alpha):
            x = start_pos[0] + (horizontal_distance * alpha)
            y = start_pos[1] - (drop_distance * (alpha ** 2))
            current_pos = np.array([x, y, 0])
            mob.move_to(current_pos)

            # Move and update the labels/arrows attached to ball2
            # grav_vec_throw.put_start_and_end_on(current_pos, current_pos + DOWN * 1.5)
            # vx_vec.put_start_and_end_on(current_pos, current_pos + RIGHT * 2.0)
            # grav_lbl_throw.next_to(grav_vec_throw, RIGHT, buff=0.1)
            # vx_lbl.next_to(vx_vec, DOWN, buff=0.1)


        # The Throw 
        self.play(
            UpdateFromAlphaFunc(ball2, throw_physics),
            FadeOut(VGroup(grav_vec_throw, vx_vec, grav_lbl_throw, vx_lbl), run_time=0.1, rate_func=linear),
            run_time=2, 
            rate_func=linear 
        )

        # The Impact Ripple
        ripple2 = Circle(radius=0.3, color=COLOR_BLUE_BALL, stroke_width=4)
        ripple2.move_to(ball2.get_center())
        self.play(
            ripple2.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )
        self.wait()

        self.play(FadeOut(ball2, ground))

        # Text Reveal
        word1 = Text("Which", font="SF Pro Display", font_size=64, weight=BOLD, color="#FFFFFF")
        word2 = Text("lands", font="SF Pro Display", font_size=64, weight=BOLD, color="#FFFFFF")
        word3 = Text("first?", font="SF Pro Display", font_size=64, weight=BOLD, color="#FFFFFF")
        
        question_group = VGroup(word1, word2, word3).arrange(RIGHT, buff=0.3)
        question_group.move_to(ORIGIN)

        self.play(
            AnimationGroup(
                FadeIn(word1, shift=UP * 0.2),
                FadeIn(word2, shift=UP * 0.2),
                FadeIn(word3, shift=UP * 0.2),
                lag_ratio=0.4 
            ),
            run_time=3.5,
            rate_func=rate_functions.ease_out_cubic 
        )

        self.wait(3)

        self.play(FadeOut(question_group), run_time=0.5)
        self.wait(0.5)

class Scene2_TheNaiveAnswer(Scene):
    def construct(self):
        COLOR_BG = "#1C1C1E"
        COLOR_GROUND = "#8E8E93"
        COLOR_GREY_BALL = "#E5E5EA"
        COLOR_BLUE_BALL = "#007AFF"
        COLOR_VEC_G = "#FF3B30"     # Apple Red for gravity
        COLOR_VEC_V_X = "#32ADE6"   # Apple Cyan for initial velocity

        # ==================================================
        # --- 0. THE FADING BACKGROUND GRID ---
        # ==================================================
        grid = VGroup()
        max_x = 12
        max_y = 8
        grid_spacing = 0.5
        
        # Helper function to create a line that fades out at its ends
        def get_fading_line(start, end, peak_opacity):
            line_segments = VGroup()
            segs = 30
            vec = end - start
            for i in range(segs):
                p1 = start + vec * (i / segs)
                p2 = start + vec * ((i + 1) / segs)
                # Parabolic fade along the line length
                t = (i + 0.5) / segs
                op = peak_opacity *0.25* (1 - (2*t - 1)**2)
                line_segments.add(Line(p1, p2, stroke_opacity=op, stroke_width=1, color="#E5E5EA"))
            return line_segments
            
        # Vertical grid lines (fade based on X distance from center)
        for x in np.arange(-max_x, max_x + 0.1, grid_spacing):
            peak = 0.2 * (1 - (abs(x)/max_x)**1.5) # The 0.2 controls maximum grid opacity
            if peak > 0:
                grid.add(get_fading_line(UP*max_y + RIGHT*x, DOWN*max_y + RIGHT*x, peak))
                
        # Horizontal grid lines (fade based on Y distance from center)
        for y in np.arange(-max_y, max_y + 0.1, grid_spacing):
            peak = 0.2 * (1 - (abs(y)/max_y)**1.5)
            if peak > 0:
                grid.add(get_fading_line(LEFT*max_x + UP*y, RIGHT*max_x + UP*y, peak))

        self.add(grid)

        # ==========================================
        # 1. SETUP & CONSTANTS
        # ==========================================
        self.camera.background_color = "#1C1C1E"
        ground = Line(start=LEFT*7, end=RIGHT*7, color="#3A3A3C", stroke_width=2)
        ground.to_edge(DOWN, buff=1)

        start_pos = np.array([-5.0, 2.5, 0.0])

        horizontal_distance = 10.0 

        def create_ball(color):
            core = Circle(radius=0.3, color=color, fill_opacity=1)
            glow = Circle(radius=0.4, color=color, fill_opacity=0.15, stroke_width=0)
            ball = VGroup(glow, core)
            ball.set_z_index(2) # Keep balls on the absolute top layer
            return ball

        self.play(FadeIn(ground, shift=UP*0.5), run_time=1.5, rate_func=smooth)
        self.wait(1)

        dummy_ball = Circle(radius=0.3).move_to(start_pos)

        drop_distance = dummy_ball.get_y() - ground.get_y() - dummy_ball.radius

        def drop_physics(mob, alpha):
            y = start_pos[1] - (drop_distance * (alpha ** 2))
            mob.move_to(np.array([start_pos[0], y, 0]))

        def throw_physics(mob, alpha):
            x = start_pos[0] + (horizontal_distance * alpha)
            y = start_pos[1] - (drop_distance * (alpha ** 2))
            mob.move_to(np.array([x, y, 0]))

        # Master clock
        t_tracker = ValueTracker(0)
        
        # ==========================================
        # 2 & 3. GREY BALL APPEAR & FALL (Trailing Dashes)
        # ==========================================
        ball1 = create_ball("#E5E5EA").move_to(start_pos)
        self.play(FadeIn(ball1, scale=0.5), run_time=1)
        self.wait(0.5)

        # Create the full dashed line, hide all dashes initially
        full_drop_path = DashedLine(
            start_pos, start_pos + DOWN * drop_distance, 
            dashed_ratio=0.5, color="#E5E5EA"
        ).set_z_index(0)

        for dash in full_drop_path.submobjects:
            dash.set_opacity(0)
        self.add(full_drop_path)

        # Updater: Only reveal dashes that are safely behind the ball
        def update_drop_trail(m):
            t = t_tracker.get_value()
            lag_y = 0.8 * (1 - t) # Lag shrinks to 0 as ball hits ground (catches up)
            ball_y = ball1.get_y()
            for dash in m.submobjects:
                # If dash is above the ball + gap, reveal it
                if dash.get_center()[1] >= ball_y + lag_y:
                    dash.set_opacity(1)

        ball1.add_updater(lambda m: drop_physics(m, t_tracker.get_value()))
        full_drop_path.add_updater(update_drop_trail)

        self.play(t_tracker.animate.set_value(1), run_time=2, rate_func=linear)
        
        ball1.clear_updaters()
        full_drop_path.clear_updaters()
        # Force any remaining dashes to appear at t=1
        for dash in full_drop_path.submobjects: dash.set_opacity(1)

        ripple = Circle(radius=0.3, color=COLOR_GREY_BALL, stroke_width=4)
        ripple.move_to(ball1.get_center())
        self.play(
            ripple.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )
        self.wait()


        # ==========================================
        # 4 & 5. BLUE BALL APPEAR & THROW (Trailing Dashes)
        # ==========================================
        
        ball2 = create_ball("#007AFF").move_to(start_pos)
        self.play(FadeIn(ball2, scale=0.5), run_time=1)
        self.wait(0.5)

        t_tracker.set_value(0) # Reset clock

        base_path_throw = ParametricFunction(
            lambda t: np.array([
                start_pos[0] + (horizontal_distance * t),
                start_pos[1] - (drop_distance * (t ** 2)),
                0
            ]),
            t_range=[0, 1]
        )
        
        full_throw_path = DashedVMobject(
            base_path_throw, num_dashes=35
        ).set_color("#FF3B30").set_stroke(width=4).set_z_index(0)

        for dash in full_throw_path.submobjects:
            dash.set_opacity(0)
        self.add(full_throw_path)

        def update_throw_trail(m):
            t = t_tracker.get_value()
            lag_x = 1.2 * (1 - t) # Gap shrinks to 0 at impact
            ball_x = ball2.get_x()
            for dash in m.submobjects:
                # If dash is left of the ball - gap, reveal it
                if dash.get_center()[0] <= ball_x - lag_x:
                    dash.set_opacity(1)

        ball2.add_updater(lambda m: throw_physics(m, t_tracker.get_value()))
        full_throw_path.add_updater(update_throw_trail)

        self.play(t_tracker.animate.set_value(1), run_time=2, rate_func=linear)
        
        ball2.clear_updaters()
        full_throw_path.clear_updaters()
        for dash in full_throw_path.submobjects: dash.set_opacity(1)

        ripple = Circle(radius=0.3, color=COLOR_GREY_BALL, stroke_width=4)
        ripple.move_to(ball2.get_center())
        self.play(
            ripple.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )
        self.wait()
        # ==========================================
        # 6. PERFECT FLATTENING (Solid Swap Technique)
        # ==========================================
        # Create solid versions of the math paths for a clean unbending animation
        solid_drop = Line(start_pos, start_pos + DOWN * drop_distance, color="#E5E5EA", stroke_width=4)
        solid_throw = base_path_throw.copy().set_color("#FF3B30").set_stroke(width=4)

        # Swap dashed for solid seamlessly
        self.play(
            FadeIn(solid_drop), FadeIn(solid_throw),
            FadeOut(full_drop_path), FadeOut(full_throw_path),
            run_time=0.3
        )

        len_drop = solid_drop.get_length()
        len_throw = solid_throw.get_arc_length()

        # The target flat lines
        flat_drop = Line(ORIGIN, RIGHT * len_drop, color="#E5E5EA", stroke_width=4)
        flat_throw = Line(ORIGIN, RIGHT * len_throw, color="#FF3B30", stroke_width=4)

        bars_group = VGroup(flat_drop, flat_throw).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        bars_group.move_to(RIGHT * 0.5 + UP * 0.5)

        # Smooth Unbending Transformation
        self.play(
            Transform(solid_drop, flat_drop),
            Transform(solid_throw, flat_throw),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_cubic
        )
        
        diff_line = DashedLine(
            solid_drop.get_right(), 
            np.array([solid_drop.get_right()[0], solid_throw.get_right()[1], 0]), 
            color="#8E8E93"
        )
        self.play(Create(diff_line))
        self.wait(2)

        # ==========================================
        # 7. RESET FOR SIMULTANEOUS DROP
        # ==========================================
        self.play(FadeOut(solid_drop), FadeOut(solid_throw), FadeOut(diff_line))
        
        self.play(
            ball1.animate.move_to(start_pos),
            ball2.animate.move_to(start_pos),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(2)

        # ==========================================
        # 8. SLOW MOTION DROP (With Synced Timer)
        # ==========================================
        t_tracker.set_value(0)

        # The true physical time of the fall
        total_fall_time = 2.00 
        
        # 1. Create the label (our static anchor)
        timer_label = Text("Time:", font="monospace", font_size=36, color="#E5E5EA")
        
        # 2. DUMMY GROUP TRICK: Set the layout position perfectly in the UR corner
        dummy_number = Text("0.00", font="monospace", font_size=36)
        dummy_unit = Text("s", font="monospace", font_size=36)
        VGroup(timer_label, dummy_number, dummy_unit).arrange(RIGHT, buff=0.15).to_corner(UR, buff=1.0)
        
        # 3. Create the dynamically updating number (Using the anchor)
        timer_number = always_redraw(lambda: Text(
            f"{t_tracker.get_value() * total_fall_time:.2f}",
            font="monospace",
            font_size=36,
            color="#FFFFFF"
        ).next_to(timer_label, RIGHT, buff=0.15, aligned_edge=DOWN))
        
        # 4. Create the dynamically updating unit
        timer_unit = Text("s", font="monospace", font_size=36, color="#E5E5EA")
        timer_unit.add_updater(lambda u: u.next_to(timer_number, RIGHT, buff=0.1, aligned_edge=DOWN))
        
        # Add the visible parts to the scene
        timer_group = VGroup(timer_label, timer_number, timer_unit)
        self.play(FadeIn(timer_group), run_time=0.5)

        ball1.add_updater(lambda m: drop_physics(m, t_tracker.get_value()))
        ball2.add_updater(lambda m: throw_physics(m, t_tracker.get_value()))

        # Normal speed: 0 to 0.90 (which maps to 0.00 to 1.80 seconds on the timer)
        self.play(t_tracker.animate.set_value(0.90), run_time=1.8, rate_func=linear)
        
        # Slow motion: 0.90 to 1.0 (which maps to 1.80 to 2.00 seconds on the timer)
        self.play(t_tracker.animate.set_value(1.0), run_time=2.0, rate_func=linear)

        # Freeze the updaters instantly on impact
        ball1.clear_updaters()
        ball2.clear_updaters()
        timer_number.clear_updaters()
        timer_unit.clear_updaters()

        # The Impact Ripples
        ripple1 = Circle(radius=0.3, color="#E5E5EA", stroke_width=4).move_to(ball1.get_center())
        ripple2 = Circle(radius=0.3, color="#007AFF", stroke_width=4).move_to(ball2.get_center())
        self.play(
            ripple1.animate.scale(2.5).set_opacity(0),
            ripple2.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )

        self.wait()

        # ==========================================
        # 9. APPLE-STYLE TEXT ("Exactly the same")
        # ==========================================
        full_text = Text(
            "Exactly the same", 
            font="SF Pro Display", 
            font_size=64, 
            weight=BOLD,
            t2c={"same": "#34C759"}  # Automatically colors just the word "same" green
        )
        full_text.move_to(UP * 1.5)

        word1 = full_text[0:7]
        word2 = full_text[7:10]
        word3 = full_text[10:14]

        self.play(
            AnimationGroup(
                FadeIn(word1, shift=UP * 0.2),
                FadeIn(word2, shift=UP * 0.2),
                FadeIn(word3, shift=UP * 0.2),
                lag_ratio=0.4 
            ),
            run_time=3, # Adjusted to 3 seconds so the sequence flows a bit faster
            rate_func=rate_functions.ease_out_cubic
        )

        # Wait exactly 1 second before the next text appears
        self.wait(1)

        # ==========================================
        # 10. SURPRISED -> UNDERSTAND TEXT MORPH
        # ==========================================
        text_surprised = Text("surprised by this?", font="SF Pro Display", font_size=40, color="#8E8E93")
        text_understand = Text("truly understand?", font="SF Pro Display", font_size=40, color="#8E8E93")
        
        # Center is the default position, so no .move_to() is needed!
        

        self.play(
                FadeIn(text_surprised, shift=UP * 0.2),            
            run_time=3, # Adjusted to 3 seconds so the sequence flows a bit faster
            rate_func=rate_functions.ease_out_cubic
        )
        
        # Give the viewer a moment to read the first question
        self.wait(1.5)
        
        # 2. Transform the text seamlessly
        self.play(
            TransformMatchingShapes(text_surprised, text_understand), 
            run_time=2, 
            rate_func=rate_functions.ease_in_out_cubic
        )

        # Final pause and fade to black
        self.wait(2)
        
        objects_to_fade = [m for m in self.mobjects if m is not grid]
        self.play(FadeOut(Group(*objects_to_fade)), run_time=1.5)
        
        self.wait()
        
# ─────────────────────────────────────────────
#  BRAND PALETTE
# ─────────────────────────────────────────────
COLOR_BG        = "#1C1C1E"
COLOR_GROUND    = "#8E8E93"
COLOR_GREY_BALL = "#E5E5EA"
COLOR_BLUE_BALL = "#007AFF"
COLOR_VEC_G     = "#FF3B30"
COLOR_VEC_V_X   = "#32ADE6"
COLOR_GREEN     = "#34C759"
COLOR_AMBER     = "#FFCC00" 
COLOR_WHITE     = "#E5E5EA" 

MIN_VEC_LEN = 0.02

# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════

def build_grid():
    grid = VGroup()
    max_x, max_y, spacing = 12, 8, 0.5

    def fading_line(start, end, peak_op):
        segs = VGroup()
        vec = end - start
        N = 30
        for i in range(N):
            p1 = start + vec * (i / N)
            p2 = start + vec * ((i + 1) / N)
            t  = (i + 0.5) / N
            op = peak_op * 0.25 * (1 - (2 * t - 1) ** 2)
            segs.add(Line(p1, p2, stroke_opacity=op,
                          stroke_width=1, color="#E5E5EA"))
        return segs

    for x in np.arange(-max_x, max_x + 0.1, spacing):
        peak = 0.2 * (1 - (abs(x) / max_x) ** 1.5)
        if peak > 0:
            grid.add(fading_line(UP * max_y + RIGHT * x,
                                 DOWN * max_y + RIGHT * x, peak))
    for y in np.arange(-max_y, max_y + 0.1, spacing):
        peak = 0.2 * (1 - (abs(y) / max_y) ** 1.5)
        if peak > 0:
            grid.add(fading_line(LEFT * max_x + UP * y,
                                 RIGHT * max_x + UP * y, peak))
    return grid

def create_ball(color, radius=0.28):
    core = Circle(radius=radius, color=color,
                  fill_opacity=1).set_z_index(3)
    glow = Circle(radius=radius * 1.6, color=color,
                  fill_opacity=0.10, stroke_width=0).set_z_index(2)
    return VGroup(glow, core)

def safe_put(arrow, start, end):
    if np.linalg.norm(end - start) < MIN_VEC_LEN:
        end = start + np.array([0.0, -MIN_VEC_LEN, 0.0])
    arrow.put_start_and_end_on(start, end)

def text_bg(text_mob, fill_color=COLOR_BG, fill_opacity=0.80,
            pad_x=0.22, pad_y=0.18, stroke=False,
            stroke_color=COLOR_WHITE, stroke_opacity=0.3):
    """Solid dark background rect behind text for readability."""
    bg = Rectangle(
        width=text_mob.width + pad_x * 2,
        height=text_mob.height + pad_y * 2,
        fill_color=fill_color, fill_opacity=fill_opacity,
        stroke_width=1 if stroke else 0,
        stroke_color=stroke_color,
        stroke_opacity=stroke_opacity if stroke else 0,
    ).move_to(text_mob.get_center()).set_z_index(text_mob.get_z_index() - 1)
    return VGroup(bg, text_mob)

def make_dashed_connector(get_start, get_end, color):
    """always_redraw DashedLine connector that never crashes on zero length."""
    def draw():
        s = get_start()
        e = get_end()
        if np.linalg.norm(e - s) < MIN_VEC_LEN:
            e = s + np.array([0.0, -MIN_VEC_LEN * 2, 0.0])
        return DashedLine(
            s, e, color=color,
            stroke_width=1.8, dash_length=0.14,
            dashed_ratio=0.5, stroke_opacity=0.65
        )
    return always_redraw(draw)

# ═══════════════════════════════════════════════════════════════════
#  SCENE
# ═══════════════════════════════════════════════════════════════════
class Scene3_TheFrameShift(Scene):

    def construct(self):
        self.camera.background_color = COLOR_BG
        grid = build_grid()
        self.add(grid)

        # ──────────────────────────────────────────────────────────
        # ACT 1 · "Reality Splits"
        # ──────────────────────────────────────────────────────────
        words     = ["Reality", "Splits"] 
        word_mobs = [
            Text(w, font="Segoe UI", font_size=72,
                 weight=BOLD, color=COLOR_WHITE).set_z_index(6)
            for w in words
        ]
        title_group = VGroup(*word_mobs).arrange(RIGHT, buff=0.25).move_to(ORIGIN)

        title_bg = Rectangle(
            width=title_group.width + 0.5,
            height=title_group.height + 0.35,
            fill_color=COLOR_BG, fill_opacity=0.78, stroke_width=0
        ).move_to(title_group).set_z_index(5)
        self.add(title_bg)

        # Simply play the FadeIn; Manim handles the starting opacity/offset automatically
        self.play(
            AnimationGroup(
                FadeIn(word_mobs[0], shift=UP * 0.2),
                FadeIn(word_mobs[1], shift=UP * 0.2),
                lag_ratio=0.4,
            ),
            run_time=1.5
        )
        self.wait()

        self.play(
            title_group.animate.scale(0.52).move_to(UP * 3.25).set_opacity(0.50),
            title_bg.animate.scale(0.52).move_to(UP * 3.25).set_opacity(0.50),
            run_time=1.0,
        )
        self.wait()

        divider = DashedLine(
            UP * 4.2, DOWN * 4.2,
            color=COLOR_GROUND, stroke_width=2,
            dash_length=0.22, dashed_ratio=0.45
        ).set_z_index(0) 
        self.play(Create(divider), run_time=1.4)
        self.wait()

        lbl_vert = Text("Vertical World", font="Segoe UI",
                        font_size=28, weight=BOLD, color=COLOR_VEC_G)
        lbl_vert.move_to(LEFT * 3.5 + UP * 2.25)

        lbl_horiz = Text("Horizontal World", font="Segoe UI",
                         font_size=28, weight=BOLD, color=COLOR_VEC_V_X)
        lbl_horiz.move_to(RIGHT * 3.5 + UP * 2.25)

        self.play(
            FadeIn(lbl_vert,  shift=RIGHT * 0.3),
            FadeIn(lbl_horiz, shift=LEFT  * 0.3),
            run_time=1
        )

        sep_l = Line(LEFT * 6.5 + UP * 2, LEFT * 0.25 + UP * 2,
                     color=COLOR_VEC_G, stroke_width=1, stroke_opacity=0.35)
        sep_r = Line(RIGHT * 0.25 + UP * 2, RIGHT * 6.5 + UP * 2,
                     color=COLOR_VEC_V_X, stroke_width=1, stroke_opacity=0.35)
        self.play(Create(sep_l), Create(sep_r), run_time=0.6)
        self.wait(0.5)

        # ──────────────────────────────────────────────────────────
        # ACT 2 · VERTICAL WORLD
        # ──────────────────────────────────────────────────────────
        q_vert = Text("How far did it fall?",
                      font="Segoe UI", font_size=20,
                      color=COLOR_VEC_G, slant=ITALIC)
        q_vert.move_to(LEFT * 3.5 + UP * 1.75)
        self.play(FadeIn(q_vert, shift=UP * 0.15))
        self.wait()

        BALL_V_START = np.array([-3.5, 1.0, 0.0])
        ball_v = create_ball(COLOR_GREY_BALL).move_to(BALL_V_START)
        self.play(FadeIn(ball_v, scale=0.4), run_time=0.5)
        self.wait(0.5)

        g_arrow_v = Arrow(
            ball_v.get_center(),
            ball_v.get_center() + DOWN * 1.0,
            color=COLOR_VEC_G, buff=0, stroke_width=5
        ).set_z_index(2)

        G_LBL_OFFSET = np.array([-0.50, -0.50, 0.0])
        g_lbl_v = MathTex(r"g", color=COLOR_VEC_G,
                          font_size=34).set_z_index(4)
        g_lbl_v.move_to(ball_v.get_center() + np.array([0.35, -0.5, 0.0]))

        self.play(GrowArrow(g_arrow_v), Write(g_lbl_v), run_time=0.9)
        self.wait(0.8)

        # --- PHYSICS ENGINE ALIGNMENT ---
        GRAVITY = 2.75  # Derived from 5.5 units / 2 sec
        t_final = 1.6   # Time required to fall exactly 3.5 units at this gravity
        
        N_DOTS     = 9
        # Spread the dots nicely across the 1.6 seconds
        dot_t_vals = np.linspace(0.15, 1.45, N_DOTS)
        
        trail_dots_v = VGroup()
        for tv in dot_t_vals:
            # Use real physics formula: y = y_initial - 0.5 * g * t^2
            y_pos = BALL_V_START[1] - 0.5 * GRAVITY * (tv ** 2)
            d = Dot(
                point=np.array([BALL_V_START[0], y_pos, 0.0]),
                radius=0.055, color=COLOR_GREY_BALL, fill_opacity=0.0
            ).set_z_index(1)
            trail_dots_v.add(d)
        self.add(trail_dots_v)

        # Track actual seconds (0 to 1.6)
        t_v = ValueTracker(0)

        def update_v(m):
            t   = t_v.get_value()
            y   = BALL_V_START[1] - 0.5 * GRAVITY * (t ** 2)
            pos = np.array([BALL_V_START[0], y, 0.0])
            m.move_to(pos)
            safe_put(g_arrow_v, pos, pos + DOWN * 1.0)
            g_lbl_v.move_to(pos + np.array([0.35, -0.5, 0.0]))
            for tv, dot in zip(dot_t_vals, trail_dots_v):
                if t >= tv:
                    dot.set_fill(opacity=0.50)

        ball_v.add_updater(update_v)
        
        # run_time matches t_final so simulation speed equals real animation speed
        self.play(t_v.animate.set_value(t_final),
                  run_time=t_final, rate_func=linear) 
        ball_v.clear_updaters()
        self.wait(0.7)

        axes_v_note = Text("Only ↑↓ matters here",
                           font="Segoe UI", font_size=16,
                           color=COLOR_GROUND).set_z_index(6)
        axes_v_note.move_to(LEFT * 3.5 + DOWN * 3.3)
        axes_v_group = text_bg(axes_v_note)
        self.play(FadeIn(axes_v_group), run_time=0.6)
        self.wait(0.8)
        # ──────────────────────────────────────────────────────────
        # ACT 3 · HORIZONTAL WORLD
        # ──────────────────────────────────────────────────────────
        q_horiz = Text("How far did it move sideways?",
                       font="Segoe UI", font_size=20,
                       color=COLOR_VEC_V_X, slant=ITALIC).set_z_index(6)
        q_horiz.move_to(RIGHT * 3.5 + UP * 1.75)
        self.play(FadeIn(q_horiz, shift=UP * 0.15), run_time=0.7)
        self.wait()

        BALL_H_START = np.array([0.8, 1.0, 0.0])
        ball_h = create_ball(COLOR_BLUE_BALL).move_to(BALL_H_START)
        self.play(FadeIn(ball_h, scale=0.4), run_time=0.5)
        self.wait(0.5)

        vx_arrow = Arrow(
            ball_h.get_center(),
            ball_h.get_center() + RIGHT * 1.4,
            color=COLOR_VEC_V_X, buff=0, stroke_width=5
        ).set_z_index(2)
        vx_lbl = MathTex(r"v_x", color=COLOR_VEC_V_X,
                         font_size=32).set_z_index(4)
        vx_lbl.next_to(vx_arrow, UP, buff=0.05)

        self.play(GrowArrow(vx_arrow), Write(vx_lbl))
        self.wait()

        phantom_g = Arrow(
            ball_h.get_center(),
            ball_h.get_center() + DOWN * 1.0,
            color=COLOR_VEC_G, buff=0, stroke_width=4,
            stroke_opacity=0.6
        ).set_z_index(2)
        phantom_lbl = Text("g?",
                           font_size=22, color=COLOR_VEC_G)
        phantom_lbl.next_to(phantom_g, RIGHT, buff=0.05)

        self.play(GrowArrow(phantom_g),
                  FadeIn(phantom_lbl, shift=RIGHT * 0.1))

        self.wait(0.5)
        self.play(
            phantom_g.animate.shift(DOWN * 0.4).set_opacity(0),
            phantom_lbl.animate.shift(DOWN * 0.4).set_opacity(0)
        )
        self.remove(phantom_g, phantom_lbl)

        no_g_text = Text("Gravity does NOT exist here.",
                         font="Segoe UI", font_size=22,
                         weight=BOLD, color=COLOR_VEC_G).set_z_index(7)
        no_g_text.move_to(RIGHT * 3.5 + DOWN * 0.25)
        no_g_bg = RoundedRectangle(
            width=no_g_text.width + 0.30,
            height=no_g_text.height + 0.25,
            corner_radius=0.25,
            fill_color=COLOR_BG, fill_opacity=0.80,
            stroke_color=COLOR_VEC_G, stroke_width=1.2,
            stroke_opacity=0.45
        ).move_to(no_g_text.get_center()).set_z_index(6)
        self.play(FadeIn(VGroup(no_g_bg, no_g_text), scale=0.88),
                  run_time=0.8)
        self.wait(1.5)

        # --- PHYSICS ENGINE ALIGNMENT (Horizontal) ---
        t_final = 1.6  # MUST match the exact fall time from Act 2
        slide_dist = 4.6
        H_VEL = slide_dist / t_final  # Constant velocity (distance / time)
        
        N_DOTS_H = 9
        # Use the exact same time thresholds as the vertical drop
        dot_t_vals_h = np.linspace(0.15, 1.45, N_DOTS_H) 
        
        trail_dots_h = VGroup()
        for tv in dot_t_vals_h:
            # Kinematics for constant velocity: x = x_initial + v * t
            x_pos = BALL_H_START[0] + H_VEL * tv
            d = Dot(
                point=np.array([x_pos, BALL_H_START[1], 0.0]),
                radius=0.055, color=COLOR_BLUE_BALL, fill_opacity=0.0
            ).set_z_index(1)
            trail_dots_h.add(d)
        self.add(trail_dots_h)

        # Track actual seconds (0 to 1.6)
        t_h = ValueTracker(0)

        def update_h(m):
            t = t_h.get_value()
            x = BALL_H_START[0] + H_VEL * t
            m.move_to([x, BALL_H_START[1], 0])
            safe_put(vx_arrow, m.get_center(), m.get_center() + RIGHT * 1.4)
            vx_lbl.next_to(vx_arrow, UP, buff=0.08)
            for tv, dot in zip(dot_t_vals_h, trail_dots_h):
                if t >= tv:
                    dot.set_fill(opacity=0.50)

        ball_h.add_updater(update_h)
        
        # run_time matches t_final so simulation speed equals vertical speed
        self.play(t_h.animate.set_value(t_final),
                  run_time=t_final, rate_func=linear)
        ball_h.clear_updaters()
        self.wait()

        axes_h_note = Text("Only ←→ matters here",
                           font="Segoe UI", font_size=16,
                           color=COLOR_GROUND).set_z_index(6)
        axes_h_note.move_to(RIGHT * 3.5 + DOWN * 3.3)
        axes_h_group = text_bg(axes_h_note)
        self.play(FadeIn(axes_h_group))
        self.wait()

        # ──────────────────────────────────────────────────────────
        # ACT 4 · BLIND TO EACH OTHER
        # ──────────────────────────────────────────────────────────

        blind_text = Text(
            "Same space. Same object. Completely blind to each other.",
            font="Segoe UI", font_size=19, color=COLOR_AMBER
        ).set_z_index(7)
        blind_text.move_to(DOWN * 1.25)
        blind_bg = Rectangle(
            width=blind_text.width + 0.40,
            height=blind_text.height + 0.26,
            fill_color=COLOR_BG, fill_opacity=0.82, stroke_width=0
        ).move_to(blind_text.get_center()).set_z_index(6)
        self.play(FadeIn(blind_bg),
                  Write(blind_text),
                  run_time = 2)
        self.wait(1.5)

        # ──────────────────────────────────────────────────────────
        # ACT 5 · INDEPENDENCE OF MOTION
        # ──────────────────────────────────────────────────────────
        cleanup_group = VGroup(
            lbl_vert, lbl_horiz, sep_l, sep_r, divider,
            title_group, title_bg,
            q_vert, q_horiz,
            g_arrow_v, g_lbl_v,
            vx_arrow, vx_lbl,
            no_g_bg, no_g_text,
            axes_v_group, axes_h_group,
            blind_bg, blind_text,
            trail_dots_v, trail_dots_h,
        )
        ground = Line(start=LEFT*7, end=RIGHT*7, color="#3A3A3C", stroke_width=2)
        ground.to_edge(DOWN, buff=1)

        # 1. Prepare the final title text FIRST
        iom_words = Text("Independence of Motion", font="Segoe UI", font_size=46,
                         weight=BOLD, color=COLOR_GREEN).to_edge(UP, buff=0.25)

        # 2. Morph everything from the cleanup_group into the title
        self.play(
            ReplacementTransform(cleanup_group, iom_words),
            ball_v.animate.set_opacity(0),
            ball_h.animate.set_opacity(0),
            run_time=2
        )
        self.wait()
        
        ORIGIN_PT = np.array([-5.0, 2.5, 0.0])
        ball_v.move_to(ORIGIN_PT)
        ball_h.move_to(ORIGIN_PT)

        self.play(
            ball_v.animate.move_to(ORIGIN_PT).set_opacity(0.35),
            ball_h.animate.move_to(ORIGIN_PT).set_opacity(0.35),
            FadeIn(ground, shift=UP*0.5),
            run_time=1.5
        )

        ball_real = create_ball(COLOR_BLUE_BALL, radius=0.3).move_to(ORIGIN_PT)
        self.play(
            FadeIn(ball_real, scale=0.5),
            ball_v.animate.set_opacity(0.25),
            ball_h.animate.set_opacity(0.25)
        )
        self.wait(0.5)

        proj_v_line = make_dashed_connector(
            lambda: ball_v.get_center(),
            lambda: ball_real.get_center(),
            COLOR_VEC_G
        )
        proj_h_line = make_dashed_connector(
            lambda: ball_h.get_center(),
            lambda: ball_real.get_center(),
            COLOR_AMBER
        )
        self.add(proj_v_line, proj_h_line)

        self.wait(0.5)

        # ─── Physics & Timer Setup ────────────────────────────────
        t_master = ValueTracker(0)
        
        total_fall_time = 2.00 
        
        # Calculate vertical drop: Start Y (2.5) down to Target Y (-3.0)
        vertical_drop_distance = 5.5 - 0.28
        
        H_VEL   = 10.0 / total_fall_time                
        # Calculate acceleration needed to cover 5.5 units in exactly 2 seconds
        V_ACC   = (vertical_drop_distance * 2) / (total_fall_time ** 2)    
        
        # 1. Create the label
        timer_label = Text("Time:", font="monospace", font_size=28, color=LIGHT_GRAY)
        
        # 2. DUMMY GROUP TRICK
        dummy_number = Text("0.00", font="monospace", font_size=28)
        dummy_unit = Text("s", font="monospace", font_size=28)
        VGroup(timer_label, dummy_number, dummy_unit).arrange(RIGHT, buff=0.15).to_edge(DOWN, buff=0.5)
        
        # 3. Create the dynamically updating number
        timer_number = always_redraw(lambda: Text(
            f"{t_master.get_value() * total_fall_time:.2f}",
            font="monospace",
            font_size=28,
            color=LIGHT_GRAY
        ).next_to(timer_label, RIGHT, buff=0.15, aligned_edge=DOWN))
        
        # 4. Create the dynamically updating unit
        timer_unit = Text("s", font="monospace", font_size=28, color=LIGHT_GRAY)
        timer_unit.add_updater(lambda u: u.next_to(timer_number, RIGHT, buff=0.1, aligned_edge=DOWN))
        
        timer_group = VGroup(timer_label, timer_number, timer_unit)
        self.play(FadeIn(timer_group), run_time=0.5)

        # 5. Updaters for balls
        def update_all(mob, dt=0):
            t = t_master.get_value() * total_fall_time
            x = ORIGIN_PT[0] + H_VEL * t
            y = ORIGIN_PT[1] - 0.5 * V_ACC * (t ** 2)
            
            ball_real.move_to([x, y, 0])
            ball_h.move_to([x, ORIGIN_PT[1], 0])
            ball_v.move_to([ORIGIN_PT[0], y, 0])

        t_master.add_updater(update_all)
        self.add(t_master)

        # ─── Animation Execution ──────────────────────────────────
        # Single, real-time drop. 2 seconds of simulation played over 2 seconds of animation.
        self.play(t_master.animate.set_value(1.0), run_time=total_fall_time, rate_func=linear)

        # Freeze the updaters instantly on impact
        t_master.clear_updaters()
        timer_number.clear_updaters()
        timer_unit.clear_updaters()
        ball_real.clear_updaters()
        ball_h.clear_updaters()
        ball_v.clear_updaters()

        # The Impact Ripples (Triggered on the ground-hitting balls)
        ripple_v = Circle(radius=0.3, color=COLOR_GROUND, stroke_width=4).move_to(ball_v.get_center())
        ripple_real = Circle(radius=0.3, color=COLOR_BLUE_BALL, stroke_width=4).move_to(ball_real.get_center())
        
        self.play(
            ripple_v.animate.scale(2.5).set_opacity(0),
            ripple_real.animate.scale(2.5).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_out_quad
        )

        self.wait()

        all_objects = [m for m in self.mobjects if m is not grid]
        self.play(FadeOut(Group(*all_objects)), run_time=1.8)
        self.wait(0.5)
