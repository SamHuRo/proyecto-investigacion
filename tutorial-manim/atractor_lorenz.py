from manimlib import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(InteractiveScene):
    def construct(self):
        #Mostrar los ejes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8,
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.frame.reorient(43, 76, 1, IN, 10)
        self.add(axes)

        #Adicionar las ecuadiones
        equations = Tex(
            R"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{~d}t} & = \sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{~d}t} & = x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{~d}t} & = x y - \beta z
            \end{aligned}
            """, 
            t2c={
                "x": RED,
                "y": BLUE,
                "z": GREEN,
            },
            font_size=30
        )

        equations.fix_in_frame()
        equations.to_corner(UL)
        equations.set_backstroke()
        self.play(Write(equations))

        #Mostrar la solucion de Lorenz
        epsilon = 1e-5
        evolution_time = 30
        n_points = 10
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(n_points)
        ]
        colors = color_gradient([BLUE, TEAL], len(states))

        curves = VGroup()

        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve = VMobject().set_points_as_corners(axes.c2p(*points.T))
            curve.set_stroke(color, 2)
            curves.add(curve)

        dots = Group(GlowDot(color=color, radius=0.25) for color in colors)

        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        dots.add_updater(update_dots)

        tail = VGroup(
            TracingTail(dot, time_traced=3).match_color(dot) for dot in dots
        ) 
        
        self.add(dots)
        self.add(tail)
        self.add(equations)
        curves.set_opacity(0)
        self.play(
            *(
            ShowCreation(curve, rate_func=linear)
            for curve in curves    
            ),
            FadeOut(curves),
            self.frame.animate.reorient(270, 71, 0, (0.0, 0.0, -1.0), 10.00),
            run_time=evolution_time,
        )
