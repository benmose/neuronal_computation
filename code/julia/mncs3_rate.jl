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
    return 0.73484029*sqrt(d-d_biff(z,iapp))-0.30128275*(d-d_biff(z,iapp))
end

function M(z, d, iapp)
    return ifelse(d >= d_biff(z,iapp), Freq(z,d,iapp), 0)
    #println(result)
end

function compute_frequency(z, d, iapp)
    if d >= d_biff(z,iapp)
        return 0.73484029*sqrt(d-d_biff(z,iapp))-0.30128275*(d-d_biff(z,iapp))
    end
    return 0
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
        mval = compute_frequency(sol[i][1], sol[i][2], iapp)
        push!(freq_arr, mval)
        push!(freq_time, sol.t[i])
    end
    return freq_time, freq_arr
end

function find_first_zero_before_maxima(val_arr, max_time_index)
    i = max_time_index
    while i >= 1 && val_arr[i] > 0
        i = i - 1
    end

    if i == 1
        return -1
    end

    while i >= 1 && val_arr[i] == 0
        i = i - 1
    end

    return i
end

function find_first_fractional_value_before_maxima(val_arr, max_time_index, fraction)
    i = max_time_index
    while i >= 1 && val_arr[i] > val_arr[max_time_index]*fraction
        i = i - 1
    end
    return i
end
function zero_times(iapp)
    freq_time, freq_arr = burst_freq_rate_vec(iapp)
    pks_times = []
    pks, vals = findmaxima(freq_arr)
    for i in eachindex(pks)
        push!(pks_times, freq_time[pks[i]])
    end
    
    return pks, pks_times, freq_arr, freq_time
end

function burst_freq_rate(iapp, fraction = 0.7)
    pks, pks_times, vals, times = zero_times(iapp)
    pks_diff = []
    zero_val_arr = Set([])
 
    if length(pks_times) <= 1
        return 0
    end

    for i in 1:length(pks)-1
        zero_val_index = find_first_zero_before_maxima(vals, pks[i])
        push!(zero_val_arr, zero_val_index)
        fractional_val_index = find_first_fractional_value_before_maxima(vals, pks[i], fraction)
        println("zero time")
        println(times[zero_val_index])
        println(fraction, " max time")
        println(times[fractional_val_index])
        push!(pks_diff, times[fractional_val_index] - times[zero_val_index])
    end

    if length(zero_val_arr) <= 2
        println("only one zero interval")
        return 0
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


function create_burst_freq_array_rate(start, endpoint, fraction)
    freq_arr = []
    iapp_ret = []
    frac = 1
    for i in start:0.1:endpoint
        if fraction < 0
            if i >= 1 && i < 1.1 
                frac = 0.9
            elseif i >= 1.1 && i < 2
                frac = 0.8
            elseif i >=2 && i < 2.2
                frac = 0.775
            elseif i >= 2.2 && i < 2.5
                frac = 0.7
            elseif i >= 2.5 && i < 2.8
                frac = 0.55
            elseif i >= 2.8 && i < 2.9
                frac = 0.32
            elseif i >= 2.9 && i < 3
                frac = 0.2
            else
                frac = 0.1
            end
        else
            frac = fraction
        end
        push!(iapp_ret, i)
        push!(freq_arr, burst_freq_rate(i, frac))
    end
    return iapp_ret, freq_arr
end
