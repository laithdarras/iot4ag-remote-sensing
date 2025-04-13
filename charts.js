function drawCustomGraph(canvasID) {
    const ctx = document.getElementById(canvasID).getContext('2d');
  
    const initialLabels = [];
    const initialData = [];
  
    const chartData = {
      labels: initialLabels,
      datasets: [{
        label: 'Sensor Reading',
        backgroundColor: 'rgba(75, 192, 192, 0.4)', 
        borderColor: 'rgba(75, 192, 192, 1)',         
        borderWidth: 2,
        data: initialData,
        fill: true
      }]
    };
  
    const config = {
      type: 'line',  
      data: chartData,
      options: {
        responsive: true,
        
        plugins: {
          title: {
            display: true,
            text: 'CO2 Sensor Graph'
          }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    return 'Value: ' + context.parsed.y
                }
            }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 5
            }
          }
        }
      }
    };
  
    const myChart = new Chart(ctx, config);
  
    function addData(label, data) {
      myChart.data.labels.push(label);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
  
      const maxDataPoints = 20;
      if (myChart.data.labels.length > maxDataPoints) {
        myChart.data.labels.shift();
        myChart.data.datasets.forEach((dataset) => {
          dataset.data.shift();
        });
      }

      myChart.update();
    }
  
    setInterval(() => {
      const now = new Date();
      const newLabel = now.toLocaleTimeString();
      if(canvasID == 'co2-graph'){
        const newValue = Math.floor(Math.random() * 60);
        addData(newLabel, newValue);
      } else if(canvasID == 'temp-graph'){
        const newValue = Math.floor(Math.random() * 80);
        addData(newLabel, newValue);
      } else if(canvasID == 'alt-graph'){
        const newValue = Math.floor(Math.random() * 20);
        addData(newLabel, newValue);
      }
    }, 1000); //updates every second
}