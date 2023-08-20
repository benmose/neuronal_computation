
using DifferentialEquations, ModelingToolkit
using Peaks
using Statistics
include("find_maxima.jl")


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

function remove_transient_values(times, vals)
    ret_times = []
    ret_vals = []
    for i in eachindex(times)
        if times[i] > 500
            ret_times = times[i:1:end]
            ret_vals = vals[i:1:end]
            break
        end
    end
    return ret_times, ret_vals
end

function return_peaks_tuple_array_cb(iapp, remove_transient=false)
    times, vals = burst_freq_cb_vec(iapp)
    if remove_transient
        times, vals = remove_transient_values(times, vals)
    end
    peaks_tuple_array = []
    points_array = find_points_for_maxima(times, vals)
    for i in eachindex(points_array)
        peak_tuple = find_maxima_by_parabola(points_array[i])
        push!(peaks_tuple_array, peak_tuple)
    end
    return peaks_tuple_array
end

function return_peaks_tuple_array_cb_with_transient_remove(iapp)
    return return_peaks_tuple_array_cb(iapp, true)
end

function find_peaks_time_after_zeroes(iapp, threshold=20, remove_transient=false)
    peaks_tuple_array = return_peaks_tuple_array_cb(iapp)
    if remove_transient
        peaks_tuple_array = return_peaks_tuple_array_cb_with_transient_remove(iapp)
    end  
    start_of_burst_peak_times = []
    for i in eachindex(peaks_tuple_array)
        if firstindex(peaks_tuple_array) == i
            continue
        end
        previous_peak_time = peaks_tuple_array[i-1][1]
        current_peak_time = peaks_tuple_array[i][1]
        if (current_peak_time - previous_peak_time) > threshold
            push!(start_of_burst_peak_times, current_peak_time)
        end
    end
    return start_of_burst_peak_times
end

function return_burst_size_in_time(iapp, threshold=100)
    peaks_tuple_array = return_peaks_tuple_array_cb_with_transient_remove(iapp)    
    bursts_size_array = []
    time_between_peaks_array = []
    time_of_first_peak_in_burst = peaks_tuple_array[1][1]
    for i in eachindex(peaks_tuple_array)
        if firstindex(peaks_tuple_array) == i
            continue
        end

        if lastindex(peaks_tuple_array) == i
            continue
        end
        previous_peak_time = peaks_tuple_array[i-1][1]
        current_peak_time = peaks_tuple_array[i][1]
        next_peak_time = peaks_tuple_array[i+1][1]
        if (current_peak_time - previous_peak_time) > threshold
            time_of_first_peak_in_burst = current_peak_time
            time_between_bursts = current_peak_time - previous_peak_time
            push!(time_between_peaks_array, time_between_bursts)
        end

        if (next_peak_time - current_peak_time) > threshold
            burst_size = current_peak_time - time_of_first_peak_in_burst
            push!(bursts_size_array, burst_size)
        end
    end

    if length(bursts_size_array) > 1
        bursts_size_array = bursts_size_array[2:1:end]
    end

    if length(time_between_peaks_array) > 1
        time_between_peaks_array = time_between_peaks_array[2:1:end]
    end

    return mean(bursts_size_array), mean(time_between_peaks_array)
 end

function return_time_between_bursts(iapp, threshold=20)
end


function burst_freq_cb(iapp, threshold = 20, remove_transient=false)
    pks_times = find_peaks_time_after_zeroes(iapp, threshold, remove_transient)
    println("pks times")
    println(pks_times)
    #println(pks_times)
    # pks_times = []
    # for i in eachindex(y)
    #     if y[i] > 0
    #         push!(pks_times, t[i])
    #     end
    # end

    pks_diff = []

    for i in 1:length(pks_times)-1
        diff = pks_times[i+1]-pks_times[i]
        # if diff > threshold
        push!(pks_diff, diff)
        # end
    end

    pks_sorted = sort(pks_diff, rev=true)
    println("freq interval cb")
    println(pks_sorted)

    #pks_avg_delta = sum(pks_sorted)/length(pks_sorted)

    if length(pks_sorted) > 1
        burst_period = pks_sorted[2]
    elseif length(pks_sorted) == 1
            burst_period = pks_sorted[1]
    else
        return 0
    end
    return 1000/burst_period
end

function create_burst_freq_array_cb_with_trasient_removed(start, endpoint, step, threshold)
    return create_burst_freq_array_cb(start, endpoint, step, threshold, true)
end

function create_burst_freq_array_cb(start, endpoint, step, threshold, remove_transient=false)
    freq_arr = []
    iapp_ret = []
    for i in start:step:endpoint
        push!(iapp_ret, i)
        if remove_transient
            push!(freq_arr, burst_freq_cb(i, threshold, true))
        else
            push!(freq_arr, burst_freq_cb(i,threshold))
        end
    end
    return iapp_ret, freq_arr
end

function create_burst_size_array_cb(start, endpoint, step, threshold)
    burst_size_arr = []
    time_between_bursts_arr = []
    iapp_ret = []
    for i in start:step:endpoint
        push!(iapp_ret, i)
        burst_size, time_between_bursts = return_burst_size_in_time(i,threshold)
        push!(burst_size_arr, burst_size)
        push!(time_between_bursts_arr, time_between_bursts)
    end
    return iapp_ret, burst_size_arr, time_between_bursts_arr
end
