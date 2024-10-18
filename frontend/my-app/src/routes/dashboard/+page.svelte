<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { checkToken, checkRole } from '$lib/utils/auth.js';
    import { showNotification } from '$lib/stores/popupStore.js';
    import { Radar, Line } from 'svelte-chartjs';
    import { Chart, RadialLinearScale, PointElement, LineElement, Filler, CategoryScale, LinearScale } from 'chart.js';
  

    Chart.register(RadialLinearScale, PointElement, LineElement, Filler, CategoryScale, LinearScale);

    let isValid = false;
    let errorMessage = '';
    let hasAccess = false;
    let isProcessing = false;

    let total = 0;
    let thisYear = 0;
    let thisMonth = 0;
    let thisWeek = 0;



    const expectedRoles = ['user', 'manager'];

    onMount(async () => {
        isProcessing = true;
        const { isValid: valid, error } = await checkToken(); 
        if (!valid) {
            errorMessage = error;
            if (error === 'Your account is pending approval') {
                showNotification('Your account is pending approval', 'info');
                goto('/pending-approval');
                return;
            } else {
                goto('/login');
                return;
            }
        } 
        if(valid) {
            hasAccess = await checkRole(expectedRoles);
        }
        if (!hasAccess) {
            showNotification('You do not have access to this page', 'error');
            goto('/login')
            return;

        } else {
            await fetchTotalSpendings();
            await fetchYearlySpendings();
            await fetchCategorySpendings();
        }
        isProcessing = false;
    });

    async function fetchTotalSpendings(){
        isProcessing = true;

        try {
            const response = await fetch('http://localhost:8000/api/expenses/statistics/total-spendings', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });
            if(!response.ok){
                const errorData = await response.json();

                if(errorData.status === 403) {
                    showNotification('You do not have access to this page.', 'error');
                    goto('/login');
                } else {
                    showNotification(errorData.detail || 'Failed to fetch total spendings', 'error');
                }
            } else {
                const data = await response.json();
                total = data.total;
                thisYear = data.year;
                thisMonth = data.month;
                thisWeek = data.week;
            }
        } catch (error) {
            console.error("Error fetching data", error);
            showNotification('Failed to fetch data', 'error');
        }
    }

    async function fetchYearlySpendings() {
        isProcessing = true;

        try {
            const response = await fetch('http://localhost:8000/api/expenses/statistics/yearly-comparison', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });

            if(!response.ok){
                const errorData = await response.json();

                if(errorData.status === 403) {
                    showNotification('You do not have access to this page.', 'error');
                    goto('/login');
                } else {
                    showNotification(errorData.detail || 'Failed to fetch total spendings', 'error');
                }
            } else {
                const data = await response.json();
                lineData.datasets[0].data = Object.values(data.current_year);;
                lineData.datasets[1].data = Object.values(data.last_year);;
            }

        } catch (error) {
            console.error("Error fetching data", error);
            showNotification('Failed to fetch data', 'error');
        }
        isProcessing = false;
    }

    async function fetchCategorySpendings() {
        isProcessing = true;

        try {

            const response = await fetch('http://localhost:8000/api/expenses/statistics/category-spendings', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}`
                }
            });

            if(!response.ok){
                const errorData = await response.json();

                if(errorData.status === 403) {
                    showNotification('You do not have access to this page.', 'error');
                    goto('/login');
                } else {
                    showNotification(errorData.detail || 'Failed to fetch total spendings', 'error');
                }
            } else {
                const data = await response.json();
                radarData.labels = Object.keys(data);
                radarData.datasets[0].data = Object.values(data);
            }

        } catch (error) {
            console.error("Error fetching data", error);
            showNotification('Failed to fetch data', 'error');
        }
        isProcessing = false;
    }

    let lineData = {
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
        data: []
      },
      {
        label: 'Expenses',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
        fill: true,
        data: []
      }
    ]
  };

  let lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
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

  let  radarData = {
    labels: [],
    datasets: [{
      data: [],
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }]
  };
</script>

{#if isProcessing}
    <div class="loading-circle"></div>
{:else}
<div class="center-container">
    <div class="card-info-container">
      <div class="card-info">
        <p>Total</p>
        <h1>{total} PLN</h1>
      </div>
  
      <div class="card-info">
        <p>This Year</p>
        <h1>{thisYear} PLN</h1>
      </div>
      <div class="card-info">
        <p>This Month</p>
        <h1>{thisMonth} PLN</h1>
      </div>
      <div class="card-info">
        <p>This Week</p>
        <h1>{thisWeek} PLN</h1>
      </div>
    </div>
</div>

<div class="center-container">
      <Line data={lineData} options={lineOptions} style="width: 50%"/>
</div>
<div class="center-container radar-chart">
  <Radar data={radarData} style="width: 100%"/>
</div>

<style>
  .radar-chart {
    width: 50%;
  }
</style>
{/if}
