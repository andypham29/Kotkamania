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
        responsive: true,
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

function setRadar(radarName, values) {
    console.log(values)
    const data = {
      labels: [
        'scoring',
        'playmaking',
        'defense',
        'powerplay',
        'intangibles'
      ],
      datasets: [{
        data: values,
        label: "Player",
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        pointBackgroundColor: 'rgb(54, 162, 235)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgb(54, 162, 235)'
      }]
    };
    new Chart(radarName, {
      type: 'radar',
      data: data,
      options: {
        responsive: true,
        spanGaps: true,
        scales: {
            r: {
                min: 0,
                max: 11,
                ticks: {
                  beginAtZero: true,
                  stepSize: 2,
                  display: false,
                }
            },
        },
      },
    });
}