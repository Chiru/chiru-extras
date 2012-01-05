def rk4(x, v, a, dt):
        """Returns final (position, velocity) tuple after
        time dt has passed.

        x: initial position (number-like object)
        v: initial velocity (number-like object)
        a: acceleration function a(x,v,dt) (must be callable)
        dt: timestep (number)"""
        x1 = x
        v1 = v
        a1 = a(x1, v1, 0)

        x2 = x + 0.5*v1*dt
        v2 = v + 0.5*a1*dt
        a2 = a(x2, v2, dt/2.0)

        x3 = x + 0.5*v2*dt
        v3 = v + 0.5*a2*dt
        a3 = a(x3, v3, dt/2.0)

        x4 = x + v3*dt
        v4 = v + a3*dt
        a4 = a(x4, v4, dt)

        xf = x + (dt/6.0)*(v1 + 2*v2 + 2*v3 + v4)
        vf = v + (dt/6.0)*(a1 + 2*a2 + 2*a3 + a4)

        return xf, vf
    
def accel(x, v, dt):
        """Determines acceleration from current position,
        velocity, and timestep. This particular acceleration
        function models a spring."""
        stiffness = 1
        damping = -0.005
        return -stiffness*x - damping*v

    t = 0
    dt = 1.0/40 # Timestep of 1/40 second
    state = 50, 5 # Position, velocity
    euler = 50, 5 # For comparison with Euler integration

    print "Initial    -position: %6.2f, velocity: %6.2f"%state

    # Run for 100 seconds
    while t < 100:
        t += dt
        state = rk4(state[0], state[1], accel, dt)

        # Integrate using Euler's method
        euler = (
            euler[0] + euler[1]*dt,
            euler[1] + accel(euler[0],euler[1],dt)*dt
        )

    print "Final RK4  -position: %6.2f, velocity: %6.2f"%state
    print "Final Euler-position: %6.2f, velocity: %6.2f"%euler
    
