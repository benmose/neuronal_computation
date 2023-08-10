using DifferentialEquations, ModelingToolkit
using Peaks
using IfElse
using Plots

@parameters Iapp

@constants tauz=400 taud=100


#
# FUNCTIONS
#
function first_c(x)
    return (-0.03613657*x)+0.86373433
end

function second_c(x)
    return 0.00999634*x+0.71959234
end

function third_c(x)
    return (-0.00659051*x)-0.00090384
end

function d_biff(x, iapp)
    return first_c(iapp)*(x^2)+second_c(iapp)*x+third_c(iapp)
end

function print_values(d,iapp)       
    prinln("d: ")
    println(d)
    println("d_biff")
    println(d_biff(z,iapp))
end

    
function Freq(z,d,iapp)
    # ifelse((d-d_biff(z,iapp) < 0), print_values, println(""))
    println("z: ",z, " d: ", d, " dbiff: ", d_biff(z,iapp))
    return 0.73484029*sqrt(d-d_biff(z,iapp))-0.30128275*(d-d_biff(z,iapp))
end

function M(z, d, iapp)
    return ifelse(d >= d_biff(z,iapp), Freq(z,d,iapp), 0)
    #println(result)
end

dinfavg(M)=0.5*M
zinfavg(M)=0.9*M 


#
# EQUATIONS
#
@variables t z(t) d(t)

D = Differential(t)



eqs_rate = [D(z) ~ (zinfavg(M(z,d,Iapp))-z)/tauz,
       D(d) ~ (dinfavg(M(z,d,Iapp))-d)/taud]

@named de_rate = ODESystem(eqs_rate)

function burst_freq_rate_vec(iapp)
    prob = ODEProblem(de_rate, [z => 0.1,d => 0.1, Iapp => iapp], (0.0, 6000.0))
    sol = solve(prob,abstol=1e-8,reltol=1e-8)
    zarr = []
    darr = []
    freq_arr = []
    freq_time = []
    for i in 1:length(sol)
        push!(zarr, sol[i][1])
        push!(darr, sol[i][2])
        d_b_val = d_biff(sol[i][1], 1)
        # if (sol[i][2] - d_b_val > 0)
            mval = M(sol[i][1], sol[i][2], 1)
        # else
        #     mval = 0
        # end
            push!(freq_arr, mval)
            push!(freq_time, sol.t[i])
    end
    return freq_time, freq_arr
end

function zero_times(iapp)
    freq_time, freq_arr = burst_freq_rate_vec(iapp)
    pks_times = []
    pks, vals = findmaxima(freq_arr)
    println("pks")
    println(pks)
    for i in eachindex(pks)
        push!(pks_times, freq_time[pks[i]])
    end
    
    return pks_times
end

function burst_freq_rate(iapp)
    pks_times = zero_times(iapp)
    pks_diff = []

    if length(pks_times) <= 1
        return 0
    end

    for i in 1:length(pks_times)-1
        push!(pks_diff, pks_times[i+1]-pks_times[i])
    end

    pks_sorted = sort(pks_diff, rev=true)
    println("sorted intervals rate")
    println(pks_sorted)
    #pks_avg_delta = sum(pks_sorted)/length(pks_sorted)
    indx = 2
    if length(pks_sorted) <= 1
        if length(pks_sorted) < 1
            return 0
        end
        indx = 1
    end
    burst_period = pks_sorted[indx]
    threshold = 20
    if burst_period > threshold
    #if pks_avg_delta > 0
        return 1000/burst_period
    end
    return 0 
end


function create_burst_freq_array_rate(n)
    freq_arr = []
    iapp_ret = []
    for i in 1:0.1:n
        push!(iapp_ret, i)
        push!(freq_arr, burst_freq_rate(i))
    end
    return iapp_ret, freq_arr
end
