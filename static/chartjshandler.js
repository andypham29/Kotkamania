function setGraph(chartName, xValues, yValues, playerType) {
    var title, yLabel;

    if(playerType == "P") {
        title = "Graph Points Per Game Played"
        yLabel = "points"
    }
    else {
        title = "Graph Wins Per Game Played"
        yLabel = "wins"
    }

    new Chart(chartName, {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.1)",
          data: yValues
        }]
      },
      options: {
        legend: {display: false},
        title: {
            display: true,
            text: title,
            fontSize: 20
        },
        scales: {
            yAxes: [
                {
                  ticks: {
                    precision: 0,
                    beginAtZero: true,
                  },
                  scaleLabel: {
                    display: true,
                    labelString: yLabel
                  },
                },
              ],
            xAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: 'games'
                  },
                },
              ],
        },
      }
    });
}