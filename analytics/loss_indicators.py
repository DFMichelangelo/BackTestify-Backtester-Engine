import numpy as np


def drawdown_indicator(data):
    info = {
        "duration_of_max_drawdown_has_recovered": True
    }
    returns = data.pct_change()
    cumulative_returns = np.cumprod(1 + returns)-1
    cumulative_returns[np.isclose(cumulative_returns, 0)] = 0
    input_length = len(data)

    data = data.iloc[1:].reset_index(drop=True)
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

    max_drawdown = min(drawdown)

    # INFO - Get Duration of Max Drawdown
    index_max_drawdown = drawdown.index(max_drawdown)
    max_drawdown_relative_index = drawdown_duration[index_max_drawdown]

    ind = 0
    # for i in range(index_max_drawdown, input_length):
    #    if drawdown_duration[index_max_drawdown+i] == 0:
    #        break
    #    elif i==input_length-1:
    #        info["duration_of_max_drawdown_has_recovered"] = False
    #        break

    while drawdown_duration[index_max_drawdown+ind] != 0:
        max_drawdown_relative_index += 1
        if index_max_drawdown+ind < input_length-1:
            ind += 1
        else:
            info["duration_of_max_drawdown_has_recovered"] = False
            break

    max_duration = max(drawdown_duration)  # INFO - MAX duration
    # INFO - Max drawdown of max duration
    pos = drawdown_duration.index(max_duration)
    k = []
    for _ in range(max_duration+1):
        k.append(drawdown[pos])
        pos -= 1

    max_drawdown = min(drawdown)  # INFO - MAX drawdown
    # INFO - Duration MAX drawdown
    duration_of_max_drawdown = max_drawdown_relative_index

    # INFO - Drawdown of the max duration
    drawdown_of_max_duration = min(k)  # if len(k) > 0 else 0

    return {
        # "high_water_mark": high_water_mark,
        # "drawdown_duration": drawdown_duration,
        "values": drawdown,
        "mean_drawdown": np.mean(drawdown),
        "max_drawdown": max_drawdown,
        "max_duration": max_duration,
        "duration_of_max_drawdown": duration_of_max_drawdown,
        "drawdown_of_max_duration": drawdown_of_max_duration,
        "info": info
    }


def underwater_indicator(data):
    initial_value = float(data[0])
    data = data.apply(lambda x: initial_value if x > initial_value else x)
    underwater_infos = drawdown_indicator(data)
    return {
        "values": underwater_infos["values"],
        "mean_underwater": underwater_infos["mean_drawdown"],
        "max_underwater": underwater_infos["max_drawdown"],
        "max_duration": underwater_infos["max_duration"],
        "underwater_of_max_duration": underwater_infos["drawdown_of_max_duration"],
        "duration_of_max_underwater": underwater_infos["duration_of_max_drawdown"],
        "info": underwater_infos["info"]
    }
