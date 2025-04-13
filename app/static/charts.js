function drawCustomGraph(canvasID) {
    const id = canvasID;
    const ctx = document.getElementById(canvasID).getContext('2d');
  
    let titleText;
    if (id === 'co2-graph') {
      titleText = 'CO2 Sensor Graph';
    } else if (id === 'temp-graph') {
      titleText = 'Temperature Graph';
    } else if (id === 'alt-graph') {
      titleText = 'Altitude Graph';
    }
  
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
            text: titleText
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return 'Value: ' + context.parsed.y;
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
  
    function getDataValue() {
      const dataArr = myChart.data.datasets[0].data;
      return dataArr[dataArr.length - 1];
    }
  
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
      fetch('/api/data')
        .then(response => response.json())
        .then(data => {
          const now = new Date().toLocaleTimeString();

          let value;
          if (id === 'co2-graph') {
            value = data.co2;
          } else if (id === 'temp-graph') {
            value = data.bme_temperature;
          } else if (id === 'alt-graph') {
            value = data.bme_altitude;
          }

          if (value !== undefined) {
            addData(now, value);
            const displayId = id.replace('-graph', '');
            document.getElementById(displayId).textContent = value.toFixed(2);
          }
        })
        .catch(err => console.error('Failed to fetch sensor data:', err));
    }, 1000);
  }
  