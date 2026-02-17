from manim import *
import numpy as np
import random


class PuzzleStatement(Scene):
    def construct(self):
        a = Text("Puzzle:", font_size=24,font="Times New Roman")
        b = Text("The minute hand on a watch is 10 mm long and the hour hand is 5 mm long.",font_size=24, font="Times New Roman")
        c = Text("How fast is the distance between the tips of the hands changing at one o'clock?", font_size=24, font="Times New Roman")

        text_group = VGroup(a, b, c)
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        text_group.align_to([-6, 3.5, 0], UL)

        self.play(Write(text_group), run_time=5)
        self.wait(0.5)

        watch_center = [0, -1, 0]
        watchI=Circle(radius=2, color=GOLD).move_to([0,-1,0])
        watchO=Circle(radius=2.1, color=GOLD).move_to([0,-1,0])
    

        # Create numbers and tick marks
        numbers = VGroup()
        tick_marks = VGroup()
        
        for i in range(1, 13):
            # Calculate angle (12 is at top, so start at 90 degrees)
            angle = np.radians(90 - i * 30)  # 30 degrees per hour
            
            # Position for number (slightly inside the circle)
            number_radius = 1.65
            num_x = watchI.get_center()[0] + number_radius * np.cos(angle)
            num_y = watchI.get_center()[1] + number_radius * np.sin(angle)
            
            # Create number
            num = Text(str(i), font_size=18)
            num.move_to([num_x, num_y, 0])
            numbers.add(num)
            
            # Create tick mark (line from circumference toward center)
            outer_radius = 2
            inner_radius = 1.8
            outer_x = watchI.get_center()[0] + outer_radius * np.cos(angle)
            outer_y = watchI.get_center()[1] + outer_radius * np.sin(angle)
            inner_x = watchI.get_center()[0] + inner_radius * np.cos(angle)
            inner_y = watchI.get_center()[1] + inner_radius * np.sin(angle)
            
            tick = Line(start=[outer_x, outer_y, 0],
                        end=[inner_x, inner_y, 0],
                        color=GOLD)
            tick_marks.add(tick)

        watch_face = VGroup(watchO,watchI, tick_marks, numbers)

        minute_hand_len = 1.5
        minute_hand_end = np.array(watch_center) + np.array([0, minute_hand_len, 0])
        minute_hand = Line(start=watch_center, end=minute_hand_end, color=BLUE, stroke_width=4)

        hour_hand_len = 0.75
        hour_angle = np.radians(60)
        hour_hand_end = np.array(watch_center) + np.array([hour_hand_len * np.cos(hour_angle),hour_hand_len * np.sin(hour_angle),0])
        hour_hand = Line(start=watch_center, end=hour_hand_end, color=RED, stroke_width=4)

        minute_word = b[3:13]
        hour_word = b[37:45]
        watch_word = b[16:21]
        distance_word = c[12:34]

        self.play(watch_word.animate.set_color(GOLD),
                  minute_word.animate.set_color(BLUE),
                  hour_word.animate.set_color(RED))

        self.play(ReplacementTransform(watch_word.copy(), watch_face),
                  ReplacementTransform(minute_word.copy(), minute_hand),
                  ReplacementTransform(hour_word.copy(), hour_hand),
                  run_time=2)
        
        self.wait(0.5)

        distance_line = DashedLine(start=minute_hand_end,
                                   end=hour_hand_end,
                                   color=YELLOW)
        
        self.play(distance_word.animate.set_color(YELLOW))

        self.play(ReplacementTransform(distance_word.copy(), distance_line))

        self.wait()
        
        label_m = MathTex("m", color=BLUE, font_size=32)
        label_m.move_to(minute_hand.get_center() + LEFT * 0.2)

        label_h = MathTex("h", color=RED, font_size=32)
        label_h.move_to(hour_hand.get_center() + np.array([0.14, -0.14, 0]))

        label_d = MathTex("d", color=YELLOW, font_size=32)
        label_d.move_to(distance_line.get_center() + np.array([0.14, 0.14, 0]))

        self.play(Write(label_m),
                  Write(label_h),
                  Write(label_d),
                  run_time=1)
        
        line1 = Tex(r"Change in $d$ w.r.t $t$", font_size=36)
        line2 = MathTex(r"\frac{dd}{dt}", r"\text{ at one o'clock} = ?", font_size=36)

        line2[0].scale(0.8)

        rate_label = VGroup(line1, line2).arrange(DOWN).move_to([-4.5, -1, 0])

        self.play(Write(rate_label))
        self.wait()

        box = SurroundingRectangle(line2[0], color=YELLOW, buff=0.1)
        
        self.play(Create(box))

        self.wait()

        geo_group = VGroup(minute_hand, hour_hand, distance_line)
        geo_group.generate_target()
        geo_group.target.scale(4).move_to([-3.5, 0, 0])

        label_m.generate_target()
        label_m.target.scale(1.5)
        label_m.target.move_to(geo_group.target[0].get_center() + LEFT * 0.4)

        label_h.generate_target()
        label_h.target.scale(1.5)
        label_h.target.move_to(geo_group.target[1].get_center() + np.array([0.25, -0.25, 0]))
        
        label_d.generate_target()
        label_d.target.scale(1.5)
        label_d.target.move_to(geo_group.target[2].get_center() + np.array([0.3, 0.3, 0]))

        fade_out_group = VGroup(text_group, watch_face, line1, box)

        self.play(FadeOut(fade_out_group),
                  MoveToTarget(geo_group),
                  MoveToTarget(label_m),
                  MoveToTarget(label_h),
                  MoveToTarget(label_d),
                  line2.animate.move_to(UP * 3.5),
                  run_time=2)

        self.wait(2)

class EquationWriting(Scene):
    def construct(self):
        # Recreate last frame
        watch_center = np.array([0, -1, 0])
        
        minute_hand_len = 1.5
        minute_hand_end = watch_center + np.array([0, minute_hand_len, 0])
        minute_hand = Line(start=watch_center,
                           end=minute_hand_end,
                           color=BLUE,
                           stroke_width=4)

        hour_hand_len = 0.75
        hour_angle = np.radians(60)
        hour_hand_end = watch_center + np.array([hour_hand_len * np.cos(hour_angle),hour_hand_len * np.sin(hour_angle),0])
        hour_hand = Line(start=watch_center,
                         end=hour_hand_end,
                         color=RED,
                         stroke_width=4)

        distance_line = DashedLine(start=minute_hand_end,
                                   end=hour_hand_end,
                                   color=YELLOW)

        geo_group = VGroup(minute_hand, hour_hand, distance_line).scale(4).move_to([-3.5, 0, 0])

        label_m = MathTex("m", color=BLUE, font_size=32).scale(1.5).move_to(geo_group[0].get_center() + LEFT * 0.4)
        
        label_h = MathTex("h", color=RED, font_size=32).scale(1.5).move_to(geo_group[1].get_center() + np.array([0.25, -0.25, 0]))
        
        label_d = MathTex("d", color=YELLOW, font_size=32).scale(1.5).move_to(geo_group[2].get_center() + np.array([0.3, 0.3, 0]))

        line2 = MathTex(r"\frac{dd}{dt}", r"\text{ at one o'clock} = ?", font_size=36)
        line2[0].scale(0.8)
        line2.move_to(UP * 3.5)

        self.add(geo_group, label_m, label_h, label_d, line2)
        
        self.wait()

        # Now its only a problem of triangle        
        text = Text("Problem of Triangles", font_size=36).move_to([1, 2.5, 0], aligned_edge=LEFT)
        self.play(Write(text))
        self.wait(0.5)
        
        # Highlight Big triangle
        center_point = geo_group[0].get_start() #minute hand
        minute_tip = geo_group[0].get_end() #minute hand
        hour_tip = geo_group[1].get_end() #hour hand

        triangle_fill = Polygon(center_point,
                                minute_tip,
                                hour_tip,
                                color=YELLOW,
                                fill_opacity=0.2,
                                stroke_width=0)

        self.play(Circumscribe(text, color=YELLOW, buff=0.1),FadeIn(triangle_fill), run_time=1.5)
        self.play(FadeOut(triangle_fill))

        # Theta label
        angle_arc = Angle(geo_group[0],
                          geo_group[1],
                          radius=0.8,
                          other_angle=True,
                          color=WHITE)
        
        theta_label = MathTex(r"\theta", font_size=36)

        theta_label.move_to(Angle(geo_group[0],
                                  geo_group[1],
                                  radius=1.1,
                                  other_angle=True).point_from_proportion(0.5))

        self.play(Create(angle_arc),Write(theta_label))
        self.wait()

        # Cosine rule equation form and rearrange

        cosine_rule = Tex("Cosine rule:", font_size=32).move_to([1, 1.5, 0], aligned_edge=LEFT)

        self.play(FadeIn(cosine_rule))

        eq1 = MathTex(r"\cos(\theta)",      # [0]
                      r"=",                 # [1]
                      r"{{m^2 + h^2 - d^2", # [2]
                      r"\over",             # [3]
                      r"2mh}}",             # [4]
                      font_size=48).move_to([3.5, 0, 0])

        self.play(Write(eq1))
        self.wait()

        eq2 = MathTex(r"2mh",                # [0]
                      r"\cos(\theta)",       # [1]
                      r"=",                  # [2]
                      r"m^2 + h^2",          # [3]
                      r"-",                  # [4]
                      r"d^2",                # [5]
                      font_size=48).move_to([3.5, 0, 0])
        
        self.play(FadeOut(eq1[3], shift=DOWN*0.5, scale=0.5),
                  ReplacementTransform(eq1[4], eq2[0], path_arc=-120*DEGREES),
                  ReplacementTransform(eq1[0], eq2[1]),
                  ReplacementTransform(eq1[1], eq2[2]),
                  TransformMatchingShapes(eq1[2], eq2[3:]))
        
        self.wait()

        eq3 = MathTex(r"d^2",               # [0]
                      r"=",                  # [1]
                      r"m^2 + h^2",          # [2]
                      r"-",                  # [3]
                      r"2mh",                # [4]
                      r"\cos(\theta)",       # [5]
                      font_size=48).move_to([3.5, 0, 0])

        self.play(ReplacementTransform(eq2[5], eq3[0], path_arc=90*DEGREES),
                  ReplacementTransform(eq2[2], eq3[1]),
                  ReplacementTransform(eq2[3], eq3[2]),
                  ReplacementTransform(eq2[4], eq3[3]),
                  ReplacementTransform(eq2[0], eq3[4], path_arc=-90*DEGREES),
                  ReplacementTransform(eq2[1], eq3[5], path_arc=-90*DEGREES),)
        self.wait()

        eq_vars = MathTex(r"d^2 =",r"m", r"^2", r"+", r"h", r"^2",r"-", r"2", r"m", r"h", r"\cos(\theta)",
                          font_size=48).move_to([3.5, 0, 0])

        self.remove(eq2)
        self.add(eq_vars)
        self.wait(0.5)

        # Value substitution
        eq_sub = MathTex(r"d^2 =",
                         r"10", r"^2", r"+", r"5", r"^2",
                         r"-", r"2", r"(10)", r"(5)", r"\cos(\theta)",
                         font_size=48).move_to([3.5, 0, 0])
        
        eq_sub[1].set_color(BLUE)    # 10
        eq_sub[4].set_color(RED)    # 5
        eq_sub[8].set_color(BLUE)    # 10
        eq_sub[9].set_color(RED)    # 5

        fly_10_sq = MathTex("10", color=BLUE).move_to(geo_group[0].get_center()).scale(0.1)
        fly_10_mul = MathTex("(10)", color=BLUE).move_to(geo_group[0].get_center()).scale(0.1)

        fly_5_sq = MathTex("5", color=RED).move_to(geo_group[1].get_center()).scale(0.1)
        fly_5_mul = MathTex("(5)", color=RED).move_to(geo_group[1].get_center()).scale(0.1)

        self.play(Indicate(geo_group[0], color=ORANGE),
                  Indicate(geo_group[1], color=ORANGE),
                  fly_10_sq.animate.scale(10),
                  fly_10_mul.animate.scale(10),
                  fly_5_sq.animate.scale(10),
                  fly_5_mul.animate.scale(10))
        
        self.wait(0.5)

        self.play(ReplacementTransform(eq_vars[0], eq_sub[0]),
                  ReplacementTransform(eq_vars[2], eq_sub[2]),
                  ReplacementTransform(eq_vars[3], eq_sub[3]),
                  ReplacementTransform(eq_vars[5], eq_sub[5]),
                  ReplacementTransform(eq_vars[6], eq_sub[6]),
                  ReplacementTransform(eq_vars[7], eq_sub[7]),
                  ReplacementTransform(eq_vars[10], eq_sub[10]),
                  FadeOut(eq_vars[1]),
                  FadeOut(eq_vars[4]),
                  FadeOut(eq_vars[8]),
                  FadeOut(eq_vars[9]),
                  ReplacementTransform(fly_10_sq, eq_sub[1]),
                  ReplacementTransform(fly_5_sq, eq_sub[4]),
                  ReplacementTransform(fly_10_mul, eq_sub[8]),
                  ReplacementTransform(fly_5_mul, eq_sub[9]),
                  FadeOut(eq3),
                  run_time=2)

        self.wait()

        eq_calc = MathTex(r"d^2 =", r"125", r"-", r"100", r"\cos(\theta)",
                          font_size=48).move_to([3.5, 0, 0])

        self.play(ReplacementTransform(VGroup(eq_sub[1], eq_sub[2], eq_sub[3], eq_sub[4], eq_sub[5]),eq_calc[1]),
                  ReplacementTransform( VGroup(eq_sub[7], eq_sub[8], eq_sub[9]),eq_calc[3]),
                  ReplacementTransform(eq_sub[0], eq_calc[0]),
                  ReplacementTransform(eq_sub[6], eq_calc[2]),
                  ReplacementTransform(eq_sub[10], eq_calc[4]),
                  run_time=1.5)

        self.wait()

        self.play(FocusOn(line2[0]))
        self.wait()

        # DIFFERENTIATION

        # Add a label to explain what we are doing
        diff_label = Tex("Differentiating w.r.t time:", font_size=32).move_to([1, 1.5, 0], aligned_edge=LEFT)
        self.play(TransformMatchingShapes(cosine_rule,diff_label))
        self.wait(0.5)

        # Define the differentiated equation       
        eq_diff = MathTex(r"2", r"d", r"\frac{dd}{dt}",  # [0], [1], [2]
                           r"=",                          # [3]
                           r"100",                        # [4]
                           r"\sin(\theta)",               # [5]
                           r"\frac{d\theta}{dt}",         # [6]
                           font_size=48).move_to([3.5, 0, 0])

        # Apply Colors
        eq_diff[1].set_color(YELLOW)       # d
        eq_diff[2][1].set_color(YELLOW)    # d in numerator (dd/dt)

        # Animate derivative
        self.play(ReplacementTransform(eq_calc[0], VGroup(eq_diff[0], eq_diff[1], eq_diff[2], eq_diff[3])),
                  FadeOut(eq_calc[1], shift=UP),
                  FadeOut(eq_calc[2]),
                  ReplacementTransform(eq_calc[3], eq_diff[4]),
                  ReplacementTransform(eq_calc[4], VGroup(eq_diff[5], eq_diff[6])),
                  run_time=2.5)

        self.wait(1.5)

        #CALCULATE d(theta)/dt

        # Declutter
        eq_diff_corner = eq_diff.copy().scale(0.7).to_corner(UL)
        
        self.play(Transform(eq_diff, eq_diff_corner),
                  FadeOut(diff_label),
                  FadeOut(geo_group, label_m, label_h, label_d, theta_label, angle_arc,text),
                  run_time=1.5)

        # visual clock for relative velocity
        clock_center = np.array([2, 0, 0])
        clock_circle = Circle(radius=1.8, color=GOLD).move_to(clock_center)
        
        # Create hands starting at 12:00
        hand_m = Line(clock_center, clock_center + UP * 1.5, color=BLUE, stroke_width=4)
        hand_h = Line(clock_center, clock_center + UP * 0.75, color=RED, stroke_width=4)
        
        clock_group = VGroup(clock_circle, hand_m, hand_h)
        
        self.play(FadeIn(clock_group))
        self.wait(0.5)

        # Create Arcs
        # Minute Hand Arc:
        arc_minute = Arc(radius=1.8,
                         start_angle=90*DEGREES,
                         angle=-2*PI + 0.01,
                         color=BLUE,
                         arc_center=clock_center,
                         stroke_width=6)

        # Hour Hand Arc: 1/12th circle
        arc_hour = Arc(radius=1.8,
                       start_angle=90*DEGREES,
                       angle=-30*DEGREES,
                       color=RED,
                       arc_center=clock_center,
                       stroke_width=6)

        label_2pi = MathTex(r"2\pi", color=BLUE).next_to(clock_circle, DOWN, buff=0.2)

        one_oclock_point = clock_center + np.array([1.8 * np.sin(15*DEGREES),1.8 * np.cos(15*DEGREES),0])
        label_2pi_12 = MathTex(r"\frac{2\pi}{12}", color=RED).next_to(one_oclock_point, UR, buff=0.1)


        self.play(Rotate(hand_m, angle=-2*PI, about_point=clock_center),
                  Create(arc_minute),
                  Rotate(hand_h, angle=-30*DEGREES, about_point=clock_center),
                  Create(arc_hour), run_time=2)
        
        arc_30 = Angle(hand_m, hand_h, radius=0.5, other_angle=True, color=YELLOW)
        label_30 = MathTex(r"\frac{\pi}{6}", font_size=30, color=YELLOW).move_to(Angle(hand_m,hand_h,radius=0.75,other_angle=True).point_from_proportion(0.6))
        
        self.play(Write(label_2pi),
                  Write(label_2pi_12),
                  Create(arc_30),
                  Write(label_30),
                  run_time=1.5,rate_func=linear)
        
        self.wait()

        # Form the Equation
        # "d(theta)/dt = "
        omega_eq = MathTex(r"\frac{d\theta}{dt} =", font_size=42).move_to([-3, 0.5, 0])
        minus_sign = MathTex("-", font_size=42).next_to(omega_eq, RIGHT, buff=0.8)

        self.play(Write(omega_eq), Write(minus_sign))

        self.wait()

        # Fly the values from the clock to the equation
        self.play(label_2pi.animate.next_to(omega_eq, RIGHT, buff=0.2),
                  label_2pi_12.animate.next_to(minus_sign, RIGHT, buff=0.2),
                  FadeOut(arc_minute),
                  FadeOut(arc_hour),
                  run_time=1.5)

        # Simplify Result (11pi/6)
        result_text = MathTex(r"\frac{11\pi}{6} \text{ rad/hr}", color=YELLOW, font_size=42).next_to(label_2pi, DOWN, aligned_edge=LEFT, buff=0.5)
        
        self.play(Write(result_text))
        self.wait()

        eq_final_substituted = MathTex(r"2", r"d", r"\frac{dd}{dt}", r"=", r"100", r"\sin\left(\frac{\pi}{6}\right)", r"\frac{11\pi}{6}",
                                       font_size=48).scale(0.7).move_to(eq_diff.get_center())
        
        eq_final_substituted[1].set_color(YELLOW)    # d
        eq_final_substituted[2][1].set_color(YELLOW) # d
        eq_final_substituted[5].set_color(YELLOW)    # sin(30)
        eq_final_substituted[6].set_color(YELLOW)    # 11pi/6

        # Substitute back into Main Equation
        self.play(Transform(eq_diff[0:5], eq_final_substituted[0:5]),
                  Transform(label_30, eq_final_substituted[5]),
                  Transform(result_text, eq_final_substituted[6]),
                  FadeOut(eq_diff[5], shift=UP * 0.2),
                  FadeOut(eq_diff[6], shift=UP * 0.2),
                  run_time=1.5)

        # Cleanup
        self.play(FadeOut(clock_group),
                  FadeOut(omega_eq),
                  FadeOut(minus_sign),
                  FadeOut(label_2pi),
                  FadeOut(label_2pi_12),
                  FadeOut(arc_30))

        # Bring Main Equation back to center
        final_group = VGroup(eq_diff[0:5], label_30, result_text)

        self.play(final_group.animate.scale(1 / 0.7).move_to(ORIGIN),run_time=1.5)
        
        self.wait()

class FinalSolving(Scene):
    def construct(self):

        #Recreate last frame
        final_eq = MathTex( r"2", r"d", r"\frac{dd}{dt}",    # [0], [1], [2]
                           r"=",                             # [3]
                           r"100",                           # [4]
                           r"\sin\left(\frac{\pi}{6}\right)",# [5]
                           r"\frac{11\pi}{6}",               # [6]
                           font_size=48)
        
        # Apply Colors
        final_eq[1].set_color(YELLOW)
        final_eq[2][1].set_color(YELLOW)
        final_eq[5].set_color(YELLOW)
        final_eq[6].set_color(YELLOW)

        self.add(final_eq)

        line2 = MathTex(r"\frac{dd}{dt}", r"\text{ at one o'clock} = ?", font_size=36)
        line2[0].scale(0.8)
        line2.move_to(UP * 3.5)

        self.add(line2)

        
        #Evaluate sin(30) -> 1/2
        
        tex_half = MathTex(r"\frac{1}{2}", font_size=48, color=YELLOW)
        tex_half.move_to(final_eq[5].get_center())

        self.play(
            Transform(final_eq[5], tex_half))
        self.wait(0.5)

        # Define the new equation
        step2_eq = MathTex(
            r"2", r"d", r"\frac{dd}{dt}",  # [0], [1], [2]
            r"=",                          # [3]
            r"50",                         # [4]
            r"\frac{11\pi}{6}",            # [5]
            font_size=48
        )

        step2_eq[1].set_color(YELLOW)
        step2_eq[2][1].set_color(YELLOW)

        step2_eq.move_to(final_eq.get_center())

        self.play(Transform(final_eq[0:4], step2_eq[0:4]),
                  ReplacementTransform(VGroup(final_eq[4], final_eq[5]), step2_eq[4]),
                  Transform(final_eq[6], step2_eq[5]))

        self.wait()

        complete_eq = VGroup(final_eq[0:4], step2_eq[4], final_eq[6])

        target_eq = MathTex(
            r"\frac{dd}{dt}",     # [0]
            r"=",                 # [1]
            r"50",                # [2]
            r"\frac{11\pi}{6}",   # [3]
            r"\frac{1}{2d}",      # [4]
            font_size=48
        )

        target_eq[0][1].set_color(YELLOW)
        target_eq[4][3].set_color(YELLOW)

        self.play(ReplacementTransform(complete_eq[0][2], target_eq[0]),
                  ReplacementTransform(complete_eq[0][3], target_eq[1]),
                  ReplacementTransform(complete_eq[1], target_eq[2]),
                  ReplacementTransform(complete_eq[2], target_eq[3]),
                  ReplacementTransform(complete_eq[0][0], target_eq[4][2]),
                  ReplacementTransform(complete_eq[0][1], target_eq[4][3]),
                  Write(target_eq[4][0]),
                  Write(target_eq[4][1]),)
        
        self.wait()

        #CALCULATE 'd'        
        d_calc = MathTex(r"d^2 &= 125 - 100 \cos(\frac{\pi}{6}) \\",
                         r"d^2 &= 125 - 100(0.866) \\",
                         r"d^2 &\approx 38.4 \\",
                         r"d &\approx 6.2",
                         font_size=32, color=YELLOW).move_to([-4, 0, 0])
        
        self.play(Write(d_calc))
        self.wait(2)

        subbed_eq = MathTex(r"\frac{dd}{dt}",
                            r"=",
                            r"50",
                            r"\frac{11\pi}{6}",
                            r"\frac{1}{2(6.2)}",
                            font_size=48)

        subbed_eq[0][1].set_color(YELLOW)
        subbed_eq[4][4:7].set_color(YELLOW)

        value_source = d_calc[3][2:]

        self.play(FadeOut(d_calc[0:3]),
                  FadeOut(d_calc[3][:2]),
                  Transform(target_eq[0:4], subbed_eq[0:4]),
                  Transform(target_eq[4], subbed_eq[4]),
                  ReplacementTransform(value_source, subbed_eq[4][4:7]))

        self.wait()

        result_eq = MathTex(r"\frac{dd}{dt}", # [0]
                            r"\approx",       # [1]
                            r"23.21 mm/hr",   # [2]
                            font_size=48)
        
        result_eq[0][1].set_color(YELLOW)
        result_eq[2].set_color(YELLOW)

        rhs_group = VGroup(target_eq[2:], subbed_eq[4][4:7])  


        self.play(ReplacementTransform(target_eq[0], result_eq[0]),
                  ReplacementTransform(target_eq[1], result_eq[1]),
                  ReplacementTransform(rhs_group, result_eq[2]))
        
        self.wait(0.5)

        box = SurroundingRectangle(result_eq, color=YELLOW, buff=0.2)
        self.play(Create(box))
        
        self.wait(2)

        animations = []
        for mob in self.mobjects:
            if isinstance(mob, VMobject):
                animations.append(Unwrite(mob))
            else:
                animations.append(FadeOut(mob))
        
        self.play(*animations)
        self.wait()

class GraphingMethod_Act1(Scene):
    def construct(self):
        #Method2
        method2 = Text("Method 2: Slope of the Graph", font="Times New Roman")
        subtitle = Text("Plotting distance vs. time to find the slope", font_size=28, color=GRAY)
        subtitle.next_to(method2, DOWN)
        
        self.play(FadeIn(method2), run_time=2)
        self.play(Write(subtitle))
        self.wait()

        # Setup watch
        watch_center = [-4, -0.5, 0]
        watchI = Circle(radius=2, color=GOLD).move_to(watch_center)
        watchO = Circle(radius=2.1, color=GOLD).move_to(watch_center)

        # Numbers and ticks
        numbers = VGroup()
        tick_marks = VGroup()
        for i in range(1, 13):
            angle = np.radians(90 - i * 30)
            
            # Numbers
            num_x = watchI.get_center()[0] + 1.65 * np.cos(angle)
            num_y = watchI.get_center()[1] + 1.65 * np.sin(angle)
            num = Text(str(i), font_size=18).move_to([num_x, num_y, 0])
            numbers.add(num)
            
            # Ticks
            outer_x = watchI.get_center()[0] + 2.0 * np.cos(angle)
            outer_y = watchI.get_center()[1] + 2.0 * np.sin(angle)
            inner_x = watchI.get_center()[0] + 1.8 * np.cos(angle)
            inner_y = watchI.get_center()[1] + 1.8 * np.sin(angle)
            tick = Line([outer_x, outer_y, 0], [inner_x, inner_y, 0], color=GOLD)
            tick_marks.add(tick)

        watch_face = VGroup(watchO, watchI, tick_marks, numbers)

        # Hands (Initialize at 12:00)
        minute_hand = Line(watch_center, np.array(watch_center) + UP*1.5, color=BLUE, stroke_width=4)
        hour_hand = Line(watch_center, np.array(watch_center) + UP*0.75, color=RED, stroke_width=4)
        distance_line = DashedLine(minute_hand.get_end(), hour_hand.get_end(), color=YELLOW)

        clock_group = VGroup(watch_face, minute_hand, hour_hand, distance_line)

        # SETUP GRAPH
        axes = Axes(x_range=[0, 80, 15],
                    y_range=[0, 16, 5],
                    x_length=6, y_length=4,
                    color= GREY,tips=False).to_edge(RIGHT, buff=0.5).add_coordinates()

        x_label = axes.get_x_axis_label("Time (min)", edge=DOWN, direction=DOWN).scale(0.75)
        y_label = axes.get_y_axis_label("Distance (d)", edge=LEFT, direction=LEFT, buff=-0.9).scale(0.75).rotate(90*DEGREES)
                
        # Metric Box
        metric_box = Rectangle(height=1.3, width=4, color=WHITE, stroke_width=1).move_to([0, 3.5, 0])
        time_label = Text("Time: 12:00", font="monospace", font_size=24).move_to(metric_box.get_center() + UP*0.3)
        dist_label = Text("Dist: 5.00", font="monospace", font_size=24, color=YELLOW).move_to(metric_box.get_center() + DOWN*0.3)
        
        # Show everything
        self.play(FadeIn(clock_group, axes, x_label, y_label, metric_box, time_label, dist_label),
                  FadeOut(method2, subtitle),
                  run_time=2)


        # ANIMATION
        
        t_tracker = ValueTracker(0)

        # Define Updaters for Clock and Text ONLY
        def update_clock_visuals(mob):
            t = t_tracker.get_value() #t represents time in hours
            
            # Hands
            min_angle = PI/2 - 2*PI*t
            minute_hand.put_start_and_end_on(watch_center, watch_center + np.array([np.cos(min_angle), np.sin(min_angle), 0])*1.5)
            
            hour_angle = PI/2 - 2*PI*t/12
            hour_hand.put_start_and_end_on(watch_center, watch_center + np.array([np.cos(hour_angle), np.sin(hour_angle), 0])*0.75)
            
            # Distance Line
            distance_line.put_start_and_end_on(minute_hand.get_end(), hour_hand.get_end())
            
            # Text Labels 
            t_min_total = int(t * 60)
            current_hour = 12 + (t_min_total // 60)
            if current_hour > 12: current_hour -= 12
            current_min = t_min_total % 60
            
            time_label.become(Text(f"Time: {current_hour}:{current_min:02d}", font="monospace", font_size=24).move_to(metric_box.get_center() + UP*0.3))
            
            # Distance calc
            theta = 2*PI * t * (11/12)
            d_val = np.sqrt(125 - 100 * np.cos(theta))
            dist_label.become(Text(f"Dist: {d_val:.2f}", font="monospace", font_size=24, color=YELLOW).move_to(metric_box.get_center() + DOWN*0.3))

        # Attach updaters to clock elements
        minute_hand.add_updater(update_clock_visuals)
        
        # Generate random time points (in hours) 0 - 1.25
        start_time = 0
        end_time = 1.25
        
        # Create 10 random intermediate points and sort them so time moves forward
        random_times = sorted([random.uniform(0.1, 1.2) for _ in range(10)])
        all_times = [start_time] + random_times + [end_time]
        
        graph_dots = VGroup() # Group to hold our plotted dots

        for t_val in all_times:
            # Move clock to the specific time
            self.play(t_tracker.animate.set_value(t_val), run_time=0.5)
            
            # Measure and Plot
            t_min = t_val * 60
            theta = 2*PI * t_val * (11/12)
            d_val = np.sqrt(125 - 100 * np.cos(theta))
            
            # Create the dot
            new_dot = Dot(axes.c2p(t_min, d_val), color=YELLOW, radius=0.08)
            
            # plotting
            self.play(
                Indicate(distance_line, color=WHITE, scale_factor=1.2),
                FadeIn(new_dot, scale=0.5),
                run_time=0.4)
            graph_dots.add(new_dot)
            
            self.wait(0.1)

        self.wait(0.5)

        # SMOOTH CURVE
        
        explanation = Text("Connecting the points...", font_size=24, color=YELLOW).next_to(axes, UP)
        self.play(Write(explanation))

        # We plot the exact mathematical function
        graph_curve = axes.plot(lambda m: np.sqrt(125 - 100 * np.cos(2*PI * (m/60) * (11/12))),
                                x_range=[0, 75],
                                color=YELLOW,
                                stroke_width=4)

        self.play(Create(graph_curve), run_time=2)
        self.play(FadeOut(explanation))
        
        self.wait()

        # Setup a "Tracking Dot" for the rewind
        current_dot = Dot(color=YELLOW)
        
        # Updater to lock it to the graph based on t_tracker
        def update_dot_pos(mob):
            t_hr = t_tracker.get_value()
            t_min = t_hr * 60
            d_val = np.sqrt(125 - 100 * np.cos(2*PI * t_hr * 11/12))
            mob.move_to(axes.c2p(t_min, d_val))
            
        current_dot.add_updater(update_dot_pos)
        self.play(FadeOut(graph_dots),
                  FadeIn(current_dot),
                  run_time=1.5)
        
        # Draw a focus line from the x-axis (60 min)
        focus_point = axes.c2p(60, 0)
        focus_line = DashedLine(start=focus_point,
                                end=axes.c2p(60, 6.19656837464),
                                color=RED,
                                stroke_width=2)

        # Animate Rewind to 1:00 (t=1.0)
        self.play(t_tracker.animate.set_value(1.0),
                  Create(focus_line),
                  run_time=2,
                  rate_func=smooth)
        
        # Remove updaters now that movement is done to save resources
        current_dot.remove_updater(update_dot_pos)
        minute_hand.clear_updaters() 

        # Highlight the dot at 1:00
        self.play(Indicate(current_dot, color=WHITE, scale_factor=2),
                  Flash(current_dot, color=YELLOW, line_length=0.2, num_lines=8),
                  run_time=1)
        
        self.wait()

        #ZOOM IN        
        zoom_center = current_dot.get_center()
        zoom_factor = 10

        # Group the elements that should be scaled
        graph_elements = VGroup(axes, x_label, y_label, graph_curve)
        
        self.play(graph_elements.animate.scale(zoom_factor, about_point=zoom_center).shift(ORIGIN - zoom_center),
                  current_dot.animate.move_to(ORIGIN),
                  FadeOut(clock_group),
                  FadeOut(minute_hand),
                  FadeOut(hour_hand),
                  FadeOut(distance_line),
                  FadeOut(metric_box),
                  FadeOut(time_label),
                  FadeOut(dist_label),
                  FadeOut(focus_line),
                  run_time=2.5)

        # Create new rulers for the zoomed view to provide scale
        # Calculate the exact values at the focus point (t=60 min)
        focus_t = 60
        # Distance d at t=1 hour (theta = 11pi/6)
        focus_d = np.sqrt(125 - 100 * np.cos(11*PI/6)) 

        # Create a horizontal ruler for Time at the bottom
        x_ruler = NumberLine(x_range=[focus_t - 0.4, focus_t + 0.4, 0.2],
                             length=7, # Span most of the screen width
                             color=GREY,
                             include_numbers=True,
                             font_size=20,
                             decimal_number_config={"num_decimal_places": 1}).to_edge(DOWN, buff=0.5)

        x_ruler_label = Text("Time (min)", font_size=20, color=GREY).next_to(x_ruler, UP)

        # Create a vertical ruler for Distance on the left
        y_ruler = NumberLine(x_range=[focus_d - 0.3, focus_d + 0.3, 0.15],
                             length=5,
                             color=GREY,
                             include_numbers=True,
                             font_size=20,
                             decimal_number_config={"num_decimal_places": 2},
                             rotation=90*DEGREES).to_edge(LEFT, buff=0.5)

        y_ruler_label = Text("Distance (d)", font_size=20, color=GREY).next_to(y_ruler, RIGHT).rotate(90*DEGREES)

        self.play(FadeIn(x_ruler), Write(x_ruler_label),
                  FadeIn(y_ruler), Write(y_ruler_label))
        self.wait()
        
        # Explanation Text
        secant_text = Text("Average Rate over interval Δt", font_size=24, color=BLUE).to_corner(UR)
        tangent_text = Text("Instantaneous Rate at 1:00", font_size=24, color=YELLOW).to_corner(UR)

        self.play(Write(secant_text))

        def d_func(m):
            return np.sqrt(125 - 100 * np.cos(2*PI * (m/60) * (11/12)))

        h_tracker = ValueTracker(3) # Start with wide interval

        # Dots and Lines (using always_redraw to stay attached to the curve)
        left_dot = always_redraw(lambda: Dot(axes.c2p(60 - h_tracker.get_value(), d_func(60 - h_tracker.get_value())),color=BLUE))
        
        right_dot = always_redraw(lambda: Dot(axes.c2p(60 + h_tracker.get_value(), d_func(60 + h_tracker.get_value())),color=BLUE))

        secant_line = always_redraw(lambda: Line(left_dot.get_center(), right_dot.get_center(), color=BLUE, stroke_width=3))

        # Rise/Run Triangle
        run_line = always_redraw(lambda: DashedLine(start=left_dot.get_center(),
                                                    end=[right_dot.get_center()[0], left_dot.get_center()[1], 0],color=GREEN))
        
        rise_line = always_redraw(lambda: DashedLine(start=[right_dot.get_center()[0], left_dot.get_center()[1], 0],
                                                     end=right_dot.get_center(),color=ORANGE))

        # Labels
        delta_t_label = always_redraw(lambda: Text("Δt", font_size=20, color=GREEN).next_to(run_line, DOWN, buff=0.1))
        delta_d_label = always_redraw(lambda: Text("Δd", font_size=20, color=ORANGE).next_to(rise_line, RIGHT, buff=0.1))

        slope_label_text = MathTex(r"\text{Slope} \approx", font_size=36)
        
        slope_val_display = DecimalNumber(0,num_decimal_places=2,include_sign=True,font_size=36,color=YELLOW)
        
        unit_text = MathTex(r"\text{ mm/min}", font_size=36, color=YELLOW)
        
        # Group them
        slope_group = VGroup(slope_label_text, slope_val_display, unit_text)
        slope_group.arrange(RIGHT, buff=0.1).to_corner(UR).shift(DOWN*0.5)

        # Updater to calculate slope
        def update_slope_display(mob):
            h = h_tracker.get_value()
            
            #Calculate Slope
            rise_mm = d_func(60 + h) - d_func(60 - h)
            run_min = (60 + h) - (60 - h)
            slope_mm_min = rise_mm / run_min
            
            mob.set_value(slope_mm_min)
            
            slope_group.arrange(RIGHT, buff=0.1).to_corner(UR).shift(DOWN*0.5)

        slope_val_display.add_updater(update_slope_display)

        self.play(FadeIn(left_dot, right_dot),
                  Create(secant_line),
                  Create(run_line), Create(rise_line),
                  Write(delta_t_label), Write(delta_d_label),
                  Write(slope_group),run_time=2)
        
        self.wait()

        # The "Squeeze"
        squeeze_text = Text("Shrinking Δt → 0", font_size=20, color=WHITE).next_to(slope_group, DOWN, buff=0.5)
        self.play(Write(squeeze_text))

        # Animate h getting smaller
        self.play(h_tracker.animate.set_value(2), run_time=2)
        self.play(h_tracker.animate.set_value(1), run_time=2)
        self.play(h_tracker.animate.set_value(0.5), run_time=2)
        
        # Transform to Tangent
        self.play(Transform(secant_text, tangent_text),
                  h_tracker.animate.set_value(0.01),
                  FadeOut(delta_t_label),
                  FadeOut(delta_d_label),run_time=2)
        
        self.wait()
   
        # Stop the updater so we can use the final value statically
        slope_val_display.clear_updaters()
        
        # Get final values
        final_mm_min = slope_val_display.get_value()        
        final_mm_hr = (final_mm_min * 60)
        
        # Display the math       
        conversion_text = MathTex(f"{final_mm_min:.2f}" + r"\text{ mm/min}",
                                  r"\times 60 \text{ min/hr}",
                                  r"\approx " + f"{final_mm_hr:.1f}" + r"\text{ mm/hr}",
                                  r"\approx " + f"{final_mm_hr:.1f}"+ r"\text{ mm/hr}",
                                  font_size=32, color=YELLOW)
        
        # Position
        line1 = VGroup(conversion_text[0], conversion_text[1]).arrange(RIGHT).next_to(slope_group, DOWN, buff=0.5, aligned_edge=RIGHT)
        line2 = conversion_text[3].next_to(line1, DOWN, aligned_edge=RIGHT)

        self.play(FadeOut(squeeze_text),
                  Write(line1))
        self.wait(0.5)
        self.play(Write(line2))
        
        # Box the result
        box = SurroundingRectangle(line2, color=GREEN, buff=0.1)
        check_mark = Text("✔ Matches Method 1", font_size=24, color=GREEN).next_to(box, LEFT)
        
        self.play(Create(box), Write(check_mark))
        
        self.wait()

        # CLEAR THE SCENE
        all_objects = Group(*self.mobjects)

        self.play(FadeOut(all_objects),run_time=2)
        
        self.wait()
