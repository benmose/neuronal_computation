using DifferentialEquations, ModelingToolkit
using Peaks
using IfElse
using Plots
include("find_maxima.jl")

@parameters Iapp taud tauz

#@constants


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
    val = first_c(iapp)*(x^2)+second_c(iapp)*x+third_c(iapp)
    return ifelse(val >= 0, val, 0)
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

function burst_freq_rate_vec(iapp, Taud=100, Tauz=400)
    prob = ODEProblem(de_rate, [z => 0.1,d => 0.1, Iapp => iapp, taud => Taud, tauz => Tauz], (0.0, 6000.0))
    sol = solve(prob,abstol=1e-15,reltol=1e-15)
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

function return_peaks_of_rate_values(times, vals)
    peaks_tuple_array = []
    points_array = find_points_for_maxima(times, vals)
    for i in eachindex(points_array)
        peak_tuple = find_maxima_by_parabola(points_array[i])
        push!(peaks_tuple_array, peak_tuple)
    end
    return peaks_tuple_array
end

function return_peaks_tuple_array_rate(iapp, taud, tauz)
    times, vals = burst_freq_rate_vec(iapp, taud, tauz)
    return return_peaks_of_rate_values(times, vals)
end

function burst_freq_rate_vec_with_transient_removed(iapp, taud, tauz)
    times, vals = burst_freq_rate_vec(iapp, taud, tauz)
    for i in eachindex(times)
        if times[i] > 50
            times = times[i:1:end]
            vals = vals[i:1:end]
            break
        end
    end
    return times, vals    
end

function return_peaks_tuple_array_rate_with_transient_removed(iapp, taud, tauz)
    times, vals = burst_freq_rate_vec_with_transient_removed(iapp, taud, tauz)
    return return_peaks_of_rate_values(times, vals)
end

function return_rate_zero_period_size_in_time(iapp, taud, tauz)
    times, vals = burst_freq_rate_vec_with_transient_removed(iapp, taud, tauz)    
    mounds_size_array = []
    time_between_freq_mounds_array = []
    time_of_first_non_zero_val = times[1]
    time_of_last_non_zero_val = times[1]
    for i in eachindex(times)
        if firstindex(times) == i
            continue
        end

        if lastindex(times) == i
            continue
        end
        previous_val_time = times[i-1]
        previous_val = vals[i-1]
        current_val_time = times[i]
        current_val = vals[i]
        next_val_time = times[i+1]
        next_val = vals[i+1]
        if (current_val != 0) && (previous_val == 0)
            time_of_first_non_zero_val = current_val_time
            time_between_mounds = current_val_time - time_of_last_non_zero_val
            push!(time_between_freq_mounds_array, time_between_mounds)
        end

        if (next_val == 0) && (current_val != 0)
            time_of_last_non_zero_val = current_val_time
            mound_size = current_val_time - time_of_first_non_zero_val
            push!(mounds_size_array, mound_size)
        end
    end

    if length(mounds_size_array) > 1
        mounds_size_array = mounds_size_array[2:1:end]
    end

    if length(time_between_freq_mounds_array) > 1
        time_between_freq_mounds_array = time_between_freq_mounds_array[2:1:end]
    end

    return mean(mounds_size_array), mean(time_between_freq_mounds_array)
 end


function peaks_tuple_array_to_peaks_time_value_arrays(peaks)
    peaks_time = []
    peaks_value = []
    for i in eachindex(peaks)
        push!(peaks_time, peaks[i][1])
        push!(peaks_value, peaks[i][2])
    end
    return peaks_time, peaks_value
end

function return_peaks_time_value_arrays_rate(iapp)
    times, vals = burst_freq_rate_vec(iapp)
    peaks = return_peaks_of_rate_values(times, vals)
    return peaks_tuple_array_to_peaks_time_value_arrays(peaks)
end

function return_peaks_time_value_arrays_rate_with_transient_removed(iapp)
    peaks = return_peaks_tuple_array_rate_with_transient_removed(iapp)
    return peaks_tuple_array_to_peaks_time_value_arrays(peaks)
end

function burst_freq_rate_with_transient_removed(iapp, taud, tauz)
    return burst_freq_rate(iapp, taud, tauz, true)
end

function burst_freq_rate(iapp, taud=100, tauz=400, remove_transient=false)
    peaks_tuple_array = return_peaks_tuple_array_rate(iapp, taud, tauz)
    if remove_transient
        peaks_tuple_array = return_peaks_tuple_array_rate_with_transient_removed(iapp, taud, tauz)
    end
    pks_diff = []
    for i in eachindex(peaks_tuple_array)
        if i == 1
            continue
        end
        previous_peak_time = peaks_tuple_array[i-1][1]
        #current_peak_time = times[peak_indices[i]]
        current_peak_time = peaks_tuple_array[i][1]
        #if (current_peak_time - previous_peak_time) > threshold
        push!(pks_diff, current_peak_time - previous_peak_time)
        #end
    end


    pks_sorted = sort(pks_diff, rev=true)
    #println("sorted intervals rate")
    #println(pks_sorted)
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

function create_burst_freq_array_rate_with_transient_removed(start, endpoint, step, taud, tauz)
    return create_burst_freq_array_rate(start, endpoint, step, taud, tauz, true)
end

function create_burst_freq_array_rate(start, endpoint, step, taud=100, tauz=400, remove_transient=false)
    freq_arr = []
    iapp_ret = []
    for i in start:step:endpoint
        push!(iapp_ret, i)
        if remove_transient
            push!(freq_arr, burst_freq_rate_with_transient_removed(i, taud, tauz))
        else
            push!(freq_arr, burst_freq_rate(i, taud, tauz))
        end
    end
    return iapp_ret, freq_arr
end

function create_freq_mounds_size_array_rate(start, endpoint, step)
    mound_size_arr = []
    time_between_mounds_arr = []
    iapp_ret = []
    for i in start:step:endpoint
        push!(iapp_ret, i)
        mound_size, time_between_mounds = return_rate_zero_period_size_in_time(i)
        push!(mound_size_arr, mound_size)
        push!(time_between_mounds_arr, time_between_mounds)
    end
    return iapp_ret, mound_size_arr, time_between_mounds_arr
end
