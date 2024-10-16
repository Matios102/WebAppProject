<script>
  import { Radar, Line } from 'svelte-chartjs';
  import { Chart, RadialLinearScale, PointElement, LineElement, Filler, CategoryScale, LinearScale } from 'chart.js';
  

  // Register required components
  Chart.register(RadialLinearScale, PointElement, LineElement, Filler, CategoryScale, LinearScale);

  // Data for Line chart (with labels)
  const linedata = {
    labels: [
      'January', 'February', 'March', 'April', 'May', 'June', 'July',
      'August', 'September', 'October', 'November', 'December'
    ],
    datasets: [
      {
        label: 'Sales',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        fill: true,
        data: [65, 59, 80, 81, 56, 55, 40, 70, 60, 75, 85, 90]
      },
      {
        label: 'Expenses',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: true,
        data: [45, 49, 60, 71, 46, 35, 30, 50, 40, 55, 65, 70]
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      datalabels: {
        display: true,
        color: 'black',
        align: 'top',
        anchor: 'end',
        font: {
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        display: true, 
      },
      x: {
        ticks: {
          display: true,
        }
      }
    },
  };

  // Data for Radar chart
  const data = {
    labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
    datasets: [{
      label: 'My First Dataset',
      data: [65, 59, 90, 81, 56, 55, 40],
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }]
  };

  let totalSpendings = 100;
  let totalThisMonth = 20;
  let totalLastMonth = 30;
  let totalCat1 = 10;
</script>

<!-- Spendings Info Cards -->
<div class="center-container">
  <div class="card-container">
    <div class="card-info">
      <p>Total</p>
      <h1>{totalSpendings}</h1>
    </div>

    <div class="card-info">
      <p>This Year</p>
      <h1>{totalLastMonth}</h1>
    </div>
    <div class="card-info">
      <p>This Month</p>
      <h1>{totalThisMonth}</h1>
    </div>
    <div class="card-info">
      <p>This Week</p>
      <h1>{totalCat1}</h1>
    </div>
  </div>
</div>

<div class="center-container">
  <div style="width: 50%">
    <Radar data={data} />
  </div>
</div>

<div class="center-container">
  <div style="width: 100%">
    <Line data={linedata} {options} />
  </div>
</div>


