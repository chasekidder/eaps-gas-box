function buildChart(ctx, title, labels, axis_label){
    var datasets = []
    labels.forEach(function(label){
        datasets.push({
            label: label,
            fill: false,
            data: []
        });
    });

    var config = {
			type: 'line',
            labels: labels,
            title: title,
            axisLabel: axis_label,
			data: {
				datasets: datasets
			},
			options: {
				title: {
					display: true,
					text: title
				},
				scales: {
					xAxes: [{
						type: 'realtime',
						realtime: {
							duration: 20000,
							refresh: 1000,
							delay: 2000,
							onRefresh: onRefresh
						}
					}],
					yAxes: [{
						scaleLabel: {
							display: true,
							labelString: axis_label
						},
                        ticks: {
                            min: -5,
                            max: 15
                        }
					}]
				},
                plugins: {
                    colorschemes: {
                        scheme: "tableau.Tableau10"
                    }
                },
                
				
				
			}
		};

    return new Chart(ctx, config);
}

function onRefresh(chart) {


    let title = chart.config.title
    chart.config.data.datasets.forEach(function(dataset) {
        chart.config.labels.forEach(function(label) {
            if (dataset.label === label) {
                try {
                    if (title === label){
                        throw "fake error";
                    }
                    let data = live_data[title][label]
                    dataset.data.push({
                                x: Date.now(),
                                y: data
                            });
                }
                catch{
                    dataset.data.push({
                        x: Date.now(),
                        y: live_data[label]
                    });
                }
            }

        });

        chart.update();
    });












}

