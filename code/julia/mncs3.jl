
using DifferentialEquations, ModelingToolkit
using Peaks


@parameters Iapp

@constants gCad=1.0 taud=100 gKCa=1.0 mu=0.01 eps=0.012
@constants THcm=-28.0 Kcm=-3.0 gm=3.5 gnap=0.04 gna=100.0 gkdr=20.0 gl=0.12
@constants gh=0.05 Cm=1 Vna=55.0 Vk=-90 Vl=-70 Vh=-27.4 VCa=120 THm=-28.0
@constants Km=-7.8 THh=-50.0 Kh=7.0 THn=-23.0 Kn=-15.0 THp=-53.0 Kp=-5.0
@constants THz=-28.0 Kz=-3.0 tauz=400.0 THd=12.0 Kd=-12.0

Il(V)=gl*(V-Vl) 
Ina(V,h)=gna*(minf(V)^3)*h*(V-Vna)
minf(V)=1.0/(1.0+exp((V-THm)/Km))
hinf(V)=1.0/(1.0+exp((V-THh)/Kh))
tauh(V)=30.0/(exp((V+50.0)/15.0)+exp(-(V+50.0)/16.0))
#
Ikdr(V,n)=gkdr*(n^4)*(V-Vk)
ninf(V)=1.0/(1.0+exp((V-THn)/Kn))
taun(V)=7.0/(exp((V+40.0)/40.0)+exp(-(V+40.0)/50.0))
#
Inap(V)=gnap*pinf(V)*(V-Vna)
pinf(V)=1.0/(1+exp((V-THp)/Kp))
#
Im(V,z)=gm*z*(V-Vk)
zinf(V)=1.0/(1+exp((V-THz)/Kz))
#
ICad(V,d)=gCad*d*(V-VCa)
dinfe(V)= 1.0/(1.0+exp((V-THd)/Kd))

@variables t V(t) h(t) n(t) z(t) d(t)

D = Differential(t)

eqs = [D(V) ~ (-Il(V)-Ina(V,h)-Ikdr(V,n)-Inap(V)-Im(V,z)-ICad(V,d)+Iapp)/Cm,
D(h) ~ (hinf(V)-h)/tauh(V),
D(n) ~ (ninf(V)-n)/taun(V),
D(z) ~ (zinf(V)-z)/tauz,
D(d) ~ (dinfe(V)-d)/taud ]

@named de = ODESystem(eqs)


using Plots

function burst_freq_cb_vec(iapp)
    prob = ODEProblem(de, [V => -52.0,h => 0.4,n => 0.1, z => 0.1,d => 0.1, Iapp => iapp], (0.0, 6000.0))
    sol = solve(prob,abstol=1e-8,reltol=1e-8)

    zarr = []
    darr = []
    varr = []
    for i in 1:length(sol)
        push!(zarr, sol[i][4])
        push!(darr, sol[i][5])
        push!(varr, sol[i][1])
    end
    return sol.t, varr
end

function burst_freq_cb(iapp)
    t, y = burst_freq_cb_vec(iapp)
    pks_times = []
    for i in eachindex(y)
        if y[i] > 0
            push!(pks_times, t[i])
        end
    end

    pks, vals = findmaxima(y)

    pks_diff = []

    for i in 1:length(pks_times)-1
        push!(pks_diff, pks_times[i+1]-pks_times[i])
    end

    pks_sorted = sort(pks_diff, rev=true)
    println("freq interval cb")
    println(pks_sorted[1:10])

    pks_avg_delta = sum(pks_sorted)/length(pks_sorted)

    burst_period = pks_sorted[2]
    threshold = 20
    if (burst_period - pks_avg_delta) > threshold
        return 1000/burst_period
    end
    return 0 
end

#freq = burst_freq(de, 1.001)
#println(pks)
#println("cb: ", 1.001)
#println(freq)
#plot(t,y)
#plotpeaks(t, y, peaks=pks, prominences=true, widths=true)

function create_burst_freq_array_cb(n)
    freq_arr = []
    iapp_arr = []
    iapp_ret = []
    for i in 1:0.1:n
        push!(iapp_ret, i)
        push!(freq_arr, burst_freq(de, i))
    end
    return iapp_ret, freq_arr
end

