using DifferentialEquations, ModelingToolkit
using Peaks
#using PlotlyJS
include("mncs3.jl")
include("mncs3_rate.jl")
include("find_maxima.jl")

#a = rate_burst_freq(de, 3)
#println(a)
# ia, fa = rate.create_burst_freq_array_rate()
# println(fa)
# p = plot(ia, fa)
# title!("Rate model burst frequencies per current")
# xlabel!("Iapp")
# ylabel!("Hz")
# savefig(p, "rate_burst_freq.pdf")


function plot_comparison(start, endpoint, fraction, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=100)
    x, y = create_burst_freq_array_cb(start, endpoint, steps, threshold)
    xr, yr = create_burst_freq_array_rate(start, endpoint, fraction, steps)

    p = plot(x, y, seriestype=plottype, label="CB")
    plot!(xr, yr, label="rate")
    title!("CB model vs rate model burst frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)
end

function plot_comparison_without_transient(start, endpoint, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=100)
    x, y = create_burst_freq_array_cb_with_trasient_removed(start, endpoint, steps, threshold)
    xr, yr = create_burst_freq_array_rate_with_transient_removed(start, endpoint, steps)

    p = plot(x, y, seriestype=plottype, label="CB")
    plot!(xr, yr, label="rate")
    title!("CB model vs rate model burst frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)
end

function plot_freq_graph_rate(iapp, filename)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts"
    x,y = burst_freq_rate_vec(iapp)
    plot(x, y, label="rate model")
    #plot!(xr, yr, label="rate")
    title!("rate model frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    #savefig(p, "cb_burst_freq.pdf")

end

function plot_freq_graph_cb(iapp, filename)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts"
    x,y = burst_freq_cb_vec(iapp)
    plot(x, y, label="cb model")
    #plot!(xr, yr, label="rate")
    title!("CB model frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    #savefig(p, "cb_burst_freq.pdf")

end

function burst_size_cb(start, endpoint, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=100)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    x,y,z = create_burst_size_array_cb(start, endpoint, steps, threshold)
    p = plot(x, y, seriestype=plottype, label="CB bursts_size")
    plot!(x, z, seriestype=:line, label="CB time between bursts")
    title!("CB model burst sizes per current")
    xlabel!("Iapp")
    ylabel!("time")
    plot!(legend=:outerbottom, legendcolumns=3)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)
end

function mound_size_rate(start, endpoint, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=100)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    xr,yr,zr = create_freq_mounds_size_array_rate(start, endpoint, steps)
    p = plot(xr, yr, seriestype=plottype, label="Rate freq non-zero size")
    plot!(xr, zr, seriestype=:line, label="Rate time between non-zeroes")

    title!("Rate model non-zero-areas sizes per current")
    xlabel!("Iapp")
    ylabel!("time")
    plot!(legend=:outerbottom, legendcolumns=3)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)
end


function peaks_coordinates_tuples_array_to_spearate_arrays(iapp, func)
    peaks = func(iapp)
    peaks_x = []
    peaks_y = []
    for i in eachindex(peaks)
        push!(peaks_x, peaks[i][1])
        push!(peaks_y, peaks[i][2])
    end
    return peaks_x, peaks_y
end

function plot_side_by_side_freq_graphs(iapp, filename, show_peaks=false)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts"
    x,y = burst_freq_rate_vec(iapp)
    peaks_x, peaks_y = 
        peaks_coordinates_tuples_array_to_spearate_arrays(iapp, return_peaks_tuple_array_rate)
    p1 = plot(x, y, label="rate model")
    plot!(peaks_x, peaks_y, seriestype=:scatter, label="rate peaks")
    #plot!(xr, yr, label="rate")
    title!("rate model frequencies for current " * string(iapp))
    xlabel!("time")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)

    x,y = burst_freq_cb_vec(iapp)
    p2 = plot(x, y, label="cb model")
    if show_peaks
        peaks_x, peaks_y = 
        peaks_coordinates_tuples_array_to_spearate_arrays(iapp, return_peaks_tuple_array_cb)
        plot!(peaks_x, peaks_y, seriestype=:scatter, label="cb peaks")
    end

    #plot!(xr, yr, label="rate")
    title!("CB model frequencies for current " * string(iapp))
    xlabel!("time")
    ylabel!("V")
    plot!(legend=:outerbottom, legendcolumns=3)

    p = plot(p1, p2, layout=(2,1))

    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)

end

# zero_times(1.75)
#t, y = burst_freq_cb_vec(0)
#find_peaks_time_after_zeroes(y, t, 100)#plot_comparison(10)
# fr = burst_freq_rate(0, 1)
# fc = burst_freq_cb(0, 100)
# println("rate freq")
# println(fr)
# println("cb freq")
# println(fc)
#plot_freq_graph_rate(3, "")
#plot_freq_graph_cb(3, "")

#plot_comparison(1, 1.1, 0.9)
#plot_comparison(1.1, 2, 0.8)
#plot_comparison(2, 2.2, 0.775)
#plot_comparison(2.2, 2.5, 0.7)
#plot_comparison(2.5, 2.8, 0.55)
#plot_comparison(2.8, 2.9, 0.32)
#plot_comparison(2.9, 3, 0.2)
#plot_comparison(0,3,1, "0_1_step_0.01_burst_freq_cb_vs_rate_threshold_100.pdf", 0.01, :line, 100)


#create_burst_freq_array_cb()
#burst_freq_cb_vec(1.0)
#burst_freq_cb(1.0)

#plot_side_by_side_freq_graphs(0.1, "both_peaks_cb_vs_rate_bursts_0.1uA.pdf", true)

# t, y = burst_freq_cb_vec(1.75)
# points_array = find_points_for_maxima(t,y)
# find_maxima_by_parabola(points_array[1])

#array_to_print = return_burst_size_in_time(2)
#println(array_to_print)

#mound_size_rate(0,3,"mound_size_comparison.pdf")
#burst_size_cb(0,3,"burst_size_comparison.pdf")
# x, y = return_peaks_time_value_arrays_rate_with_transient_removed(2)
# plot(x,y, seriestype=:scatter)

plot_comparison_without_transient(0,3, "burst_comarison_without_transient.pdf")