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


function plot_comparison(start, endpoint, taud=100, tauz=400, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=100)
    x, y = create_burst_freq_array_cb(start, endpoint, steps, threshold, taud, tauz)
    xr, yr = create_burst_freq_array_rate(start, endpoint, steps, taud, tauz)

    p = plot(x, y, seriestype=plottype, label="CB")
    plot!(xr, yr, label="rate")
    title!("taud=" * string(taud) * " tauz=" * string(tauz))
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)
end

function plot_comparison_without_transient(start, endpoint, taud, tauz, filename = "cb_rate_comparison.pdf", steps=0.1, plottype=:line, threshold=50)
    x, y = create_burst_freq_array_cb_with_transient_removed(start, endpoint, steps, taud, tauz, threshold)
    xr, yr = create_burst_freq_array_rate_with_transient_removed(start, endpoint, steps, taud, tauz)

    p = plot(x, y, seriestype=plottype, label="CB")
    plot!(xr, yr, label="rate")
    title!("taud=" * string(taud) * " tauz=" * string(tauz))
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


function peaks_coordinates_tuples_array_to_spearate_arrays(iapp, taud, tauz, func)
    peaks = func(iapp, taud, tauz)
    peaks_x = []
    peaks_y = []
    for i in eachindex(peaks)
        push!(peaks_x, peaks[i][1])
        push!(peaks_y, peaks[i][2])
    end
    return peaks_x, peaks_y
end

function plot_side_by_side_freq_graphs(iapp, taud, tauz, filename, show_peaks=false)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts"
    x,y = burst_freq_rate_vec(iapp, taud, tauz)
    peaks_x, peaks_y = 
        peaks_coordinates_tuples_array_to_spearate_arrays(iapp, taud, tauz, return_peaks_tuple_array_rate)
    p1 = plot(x, y, label="rate model")
    plot!(peaks_x, peaks_y, seriestype=:scatter, label="rate peaks")
    #plot!(xr, yr, label="rate")
    title!("current " * string(iapp) * " taud: " * string(taud) * " tauz: " * string(tauz))
    xlabel!("time")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)

    x,y = burst_freq_cb_vec(iapp, taud, tauz)
    p2 = plot(x, y, label="cb model")
    if show_peaks
        peaks_x, peaks_y = 
        peaks_coordinates_tuples_array_to_spearate_arrays(iapp, taud, tauz, return_peaks_tuple_array_cb)
        plot!(peaks_x, peaks_y, seriestype=:scatter, label="cb peaks")
    end

    #plot!(xr, yr, label="rate")
    title!("current " * string(iapp) * " taud: " * string(taud) * " tauz: " * string(tauz))
    xlabel!("time")
    ylabel!("V")
    plot!(legend=:outerbottom, legendcolumns=3)

    p = plot(p1, p2, layout=(2,1))

    path = "/Users/rammantzur/work/github_rate_model/media/bursts/"
    savefig(p, path * filename)

end

