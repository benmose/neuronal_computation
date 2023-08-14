
function find_maxima_by_parabola(points_tuple)
    x1 = points_tuple[1][1]
    y1 = points_tuple[1][2]
    x2 = points_tuple[2][1]
    y2 = points_tuple[2][2]
    x3 = points_tuple[3][1]
    y3 = points_tuple[3][2]
    denom = (x1 - x2)*(x1 - x3)*(x2 - x3)
    #Avoided the division by denominator since it cancells out in out return
    #values.
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2))
    b = (x3^2 * (y1 - y2) + x2^2 * (y3 - y1) + x1^2 * (y2 - y3))
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3)
    x_maxima = -b / 2a
    y_maxima = (c - b^2 / 4a) / denom
    return (x_maxima, y_maxima)
end

function find_points_for_maxima(times_array, values_array)
    points_for_maxima_array = []
    previous_value = 0
    previous_value_time = 0
    # Assuming both arrays are of the same size
    for i in eachindex(times_array)
        if firstindex(times_array) == i
            previous_value = values_array[i]
            previous_value_time = times_array[i]
            continue
        end
        if lastindex(times_array) == i
            break
        end
        if values_array[i] == previous_value
            continue
        end
        if values_array[i] > values_array[i+1] && 
            previous_value < values_array[i]
            push!(points_for_maxima_array,
             ((previous_value_time, previous_value),
              (times_array[i],values_array[i]),
              (times_array[i+1], values_array[i+1])))
        end
        previous_value = values_array[i]
        previous_value_time = times_array[i]
    end
    return points_for_maxima_array
end