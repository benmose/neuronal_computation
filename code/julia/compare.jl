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


function plot_comparison(n)
    x, y = create_burst_freq_array_cb(n)
    xr, yr = create_burst_freq_array_rate(n)

    plot(x, y, label="CB")
    plot!(xr, yr, label="rate")
    title!("CB model burst frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    plot!(legend=:outerbottom, legendcolumns=3)
    #savefig(p, "cb_burst_freq.pdf")
end

function plot_freq_graph(iapp, filename)
    path = "/Users/rammantzur/work/github_rate_model/media/bursts"
    x,y = burst_freq_rate_vec(iapp)
    plot(x, y, label="rate model")
    #plot!(xr, yr, label="rate")
    title!("rate model frequencies per current")
    xlabel!("Iapp")
    ylabel!("Hz")
    #plot!(legend=:outerbottom, legendcolumns=3)
    #savefig(p, "cb_burst_freq.pdf")

end
burst_freq_rate_vec(3.8)