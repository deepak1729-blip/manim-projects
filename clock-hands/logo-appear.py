from manim import *
import numpy as np
import itertools as it
import random

class Logo(VMobject):
    def __init__(
        self,
        pupil_radius: float = 1.0,
        outer_radius: float = 2.0,
        iris_background_blue: str = "#74C0E3",
        iris_background_brown: str = "#8C6239",
        blue_spike_colors: list = None,
        brown_spike_colors: list = None,
        n_spike_layers: int = 4,
        n_spikes: int = 28,
        **kwargs
    ):
        self.pupil_radius = pupil_radius
        self.outer_radius = outer_radius
        self.iris_background_blue = iris_background_blue
        self.iris_background_brown = iris_background_brown
        self.blue_spike_colors = blue_spike_colors or [
            "#528EA3",
            "#3E6576",
            "#224C5B",
            BLACK,
        ]
        self.brown_spike_colors = brown_spike_colors or [
            "#754C24",
            "#603813",
            "#42210b",
            BLACK,
        ]
        self.n_spike_layers = n_spike_layers
        self.n_spikes = n_spikes
        self.spike_angle = TAU / 28

        super().__init__(**kwargs)
        self.add_iris_back()
        self.add_spikes()
        self.add_pupil()

    def add_iris_back(self):
        blue_iris_back = AnnularSector(
            inner_radius=self.pupil_radius,
            outer_radius=self.outer_radius,
            angle=270 * DEGREES,
            start_angle=180 * DEGREES,
            fill_color=self.iris_background_blue,
            fill_opacity=1,
            stroke_width=0,
        )
        brown_iris_back = AnnularSector(
            inner_radius=self.pupil_radius,
            outer_radius=self.outer_radius,
            angle=90 * DEGREES,
            start_angle=90 * DEGREES,
            fill_color=self.iris_background_brown,
            fill_opacity=1,
            stroke_width=0,
        )
        self.iris_background = VGroup(
            blue_iris_back,
            brown_iris_back,
        )
        self.add(self.iris_background)

    def add_spikes(self):
        layers = VGroup()
        radii = np.linspace(
            self.outer_radius,
            self.pupil_radius,
            self.n_spike_layers,
            endpoint=False,
        )
        radii[:2] = radii[1::-1]  # Swap first two
        if self.n_spike_layers > 2:
            radii[-1] = interpolate(radii[-1], self.pupil_radius, 0.25)

        for radius in radii:
            tip_angle = self.spike_angle
            half_base = radius * np.tan(tip_angle)
            triangle, right_half_triangle = [
                Polygon(
                    radius * UP,
                    half_base * RIGHT,
                    vertex3,
                    fill_opacity=1,
                    stroke_width=0,
                )
                for vertex3 in (half_base * LEFT, ORIGIN,)
            ]
            left_half_triangle = right_half_triangle.copy()
            left_half_triangle.flip(UP, about_point=ORIGIN)

            n_spikes = self.n_spikes
            full_spikes = [
                triangle.copy().rotate(
                    -angle,
                    about_point=ORIGIN
                )
                for angle in np.linspace(
                    0, TAU, n_spikes, endpoint=False
                )
            ]
            index = (3 * n_spikes) // 4
            if radius == radii[0]:
                layer = VGroup(*full_spikes)
                layer.rotate(
                    -TAU / n_spikes / 2,
                    about_point=ORIGIN
                )
                layer.brown_index = index
            else:
                half_spikes = [
                    right_half_triangle.copy(),
                    left_half_triangle.copy().rotate(
                        90 * DEGREES, about_point=ORIGIN,
                    ),
                    right_half_triangle.copy().rotate(
                        90 * DEGREES, about_point=ORIGIN,
                    ),
                    left_half_triangle.copy()
                ]
                layer = VGroup(*it.chain(
                    half_spikes[:1],
                    full_spikes[1:index],
                    half_spikes[1:3],
                    full_spikes[index + 1:],
                    half_spikes[3:],
                ))
                layer.brown_index = index + 1

            layers.add(layer)

        # Color spikes
        blues = self.blue_spike_colors
        browns = self.brown_spike_colors
        for layer, blue, brown in zip(layers, blues, browns):
            index = layer.brown_index
            layer[:index].set_color(blue)
            layer[index:].set_color(brown)

        self.spike_layers = layers
        self.add(layers)

    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)

    def cut_pupil(self):
        pupil = self.pupil
        center = pupil.get_center()
        new_pupil = VGroup(*[
            pupil.copy().pointwise_become_partial(pupil, a, b)
            for (a, b) in [(0.25, 1), (0, 0.25)]
        ])
        for sector in new_pupil:
            sector.add_cubic_bezier_curve_to([
                sector.get_points()[-1],
                *[center] * 3,
                *[sector.get_points()[0]] * 2
            ])
        self.remove(pupil)
        self.add(new_pupil)
        self.pupil = new_pupil

    def get_blue_part_and_brown_part(self):
        if len(self.pupil) == 1:
            self.cut_pupil()
        blue_part = VGroup(
            self.iris_background[0],
            *[
                layer[:layer.brown_index]
                for layer in self.spike_layers
            ],
            self.pupil[0],
        )
        brown_part = VGroup(
            self.iris_background[1],
            *[
                layer[layer.brown_index:]
                for layer in self.spike_layers
            ],
            self.pupil[1],
        )
        return blue_part, brown_part

class LogoScene(Scene):
    def construct(self):
        logo = Logo()
        
        logo.scale(1)
        
        logo.move_to(np.array([0, 0.5, 0]))
        
        self.play(FadeIn(logo), run_time=2)
        self.wait()

        text=Text("3Blue1Brown", font_size=48, font="Times New Roman").move_to([0,-2.5,0])
        self.play(Write(text), run_time=2.5)

        self.wait()
        
        text1=Text("Mathematical Animator Application Video",font_size=32)
        text2=Text("By Deepak Rana",font_size=32)

        g = VGroup(text1,text2)
        g.arrange(DOWN).move_to([0,-2.5,0])

        self.play(TransformMatchingShapes(text,g),run_time=2)
        self.wait(2)

        self.play(FadeOut(g,logo), run_time=2)
        self.wait()
