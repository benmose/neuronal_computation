using Plots;
using DifferentialEquations

f(u,p,t) = 0.98u
u0 = 1.0
tspan = (0.0,1.0)
prob = ODEProblem(f,u0,tspan)
sol = solve(prob)
gr()
# plot(sol)

plot(sol, linewidth=5,
     title="Solution to the linear ODE with a thick line",
     xaxis="Time (t)", yaxis="u(t) (in μm)",
     label="My Thick Line!") # legend=false
     plot!(sol.t, t->1.0*exp(0.98t), lw=3, ls=:dash, label="True Solution!")
sol.t
[t+u for (u,t) in tuples(sol)]
sol
sol(0.45)
sol = solve(prob,abstol=1e-8,reltol=1e-8) 
plot(sol)
plot!(sol.t, t->1.0*exp(0.98t),lw=3,ls=:dash,label="True Solution!")
sol = solve(prob, saveat=0.1)
