def drawdown_indicator(data):

    info = {
        "max_duration_has_recovered": True
    }

    returns = data.pct_change()
    cumulative_returns = (1 + returns).cumprod()-1
    data = data.iloc[1:]
    data = data.reset_index(drop=True)
    input_length = len(data)
    high_water_mark = [0]
    drawdown = [0]
    drawdown_duration = [0]

    # INFO - Compute drawdown
    for t in range(1, input_length):
        high_water_mark.append(
            max(high_water_mark[t-1], cumulative_returns[t]))
        drawdown.append(-((1+high_water_mark[t])/(1+cumulative_returns[t])-1))
        drawdown_duration.append(
            0 if drawdown[t] == 0 else drawdown_duration[t-1]+1)

    # INFO - Get Duration of Max Drawdown
    max_drawdown_index = drawdown_duration[drawdown.index(min(drawdown))]
    max_drawdown = min(drawdown)

    while max_drawdown != 0:
        if max_drawdown_index < input_length:
            max_drawdown_index += 1
            max_drawdown = drawdown[max_drawdown_index]
        else:
            info["max_duration_has_recovered"] = False
            max_drawdown_index += 1
            max_drawdown = 0

    # INFO - Max drawdown of max duration
    z = max(drawdown_duration)
    pos = drawdown_duration.index(z)
    k = []
    for _ in range(z):
        k.append(drawdown[pos])
        pos -= 1

    max_drawdown = min(drawdown)  # INFO - MAX drawdown
    max_duration = max(drawdown_duration)  # INFO - MAX duration
    # INFO - Duration MAX drawdown
    duration_of_max_drawdown = drawdown_duration[max_drawdown_index-1]
    # INFO - Drawdown of the max duration
    drawdown_of_max_duration = min(k)

    return {
        # "high_water_mark": high_water_mark,
        # "drawdown_duration": drawdown_duration,
        "values": drawdown,
        "max_drawdown": max_drawdown,
        "max_duration": max_duration,
        "drawdown_of_max_duration": drawdown_of_max_duration,
        "duration_of_max_drawdown": duration_of_max_drawdown,
        "info": info
    }


def underwater_indicator(data):
    initial_value = float(data[0])
    data = data.apply(lambda x: initial_value if x > initial_value else x)
    underwater_infos = drawdown_indicator(data)
    return {
        "values": underwater_infos["values"],
        "max_underwater": underwater_infos["max_drawdown"],
        "max_duration": underwater_infos["max_duration"],
        "underwater_of_max_duration": underwater_infos["drawdown_of_max_duration"],
        "duration_of_max_underwater": underwater_infos["duration_of_max_drawdown"],
        "info": underwater_infos["info"]
    }
