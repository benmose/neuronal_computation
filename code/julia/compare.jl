using DifferentialEquations, ModelingToolkit
using Peaks
include("mncs3.jl")
include("mncs3_rate.jl")

#a = rate_burst_freq(de, 3)
#println(a)
# ia, fa = rate.create_burst_freq_array_rate()
# println(fa)
# p = plot(ia, fa)
# title!("Rate model burst frequencies per current")
# xlabel!("Iapp")
# ylabel!("Hz")
# savefig(p, "rate_burst_freq.pdf")


function plot_comparison(start, endpoint, fraction, filename = "cb_rate_comparison.pdf")
    x, y = create_burst_freq_array_cb(start, endpoint)
    xr, yr = create_burst_freq_array_rate(start, endpoint, fraction)

    p = plot(x, y, label="CB")
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
# plot_comparison(10)
fr = burst_freq_rate(1,0.9)
fc = burst_freq_cb(1)
println("rate freq")
println(fr)
println("cb freq")
println(fc)
#plot_freq_graph_rate(3, "")
#plot_freq_graph_cb(3, "")

#plot_comparison(1, 1.1, 0.9)
#plot_comparison(1.1, 2, 0.8)
#plot_comparison(2, 2.2, 0.775)
#plot_comparison(2.2, 2.5, 0.7)
#plot_comparison(2.5, 2.8, 0.55)
#plot_comparison(2.8, 2.9, 0.32)
#plot_comparison(2.9, 3, 0.2)
plot_comparison(1,3,-1, "burst_freq_cb_vs_rate_varying_adaptaion_.pdf")


#create_burst_freq_array_cb()
#burst_freq_cb_vec(1.0)
#burst_freq_cb(1.0)