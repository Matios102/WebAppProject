<script>
    import { Radar } from 'svelte-chartjs';
    
    const data = {
        labels: [
            'Eating',
            'Drinking',
            'Sleeping',
            'Designing',
            'Coding',
            'Cycling',
            'Running',
        ],
        datasets: [
            {
            label: 'My First dataset',
            backgroundColor: 'rgba(194, 116, 161, 0.5)',
            borderColor: 'rgb(194, 116, 161)',
            data: [65, 59, 90, 81, 56, 55, 40],
            },
            {
            label: 'My Second dataset',
            backgroundColor: 'rgba(71, 225, 167, 0.5)',
            borderColor: 'rgb(71, 225, 167)',
            data: [28, 48, 40, 19, 96, 27, 100],
            },
        ],
    };
  
    import {
      Chart as ChartJS,
      Title,
      Tooltip,
      Legend,
      PointElement,
      RadialLinearScale,
      LineElement,
    } from 'chart.js';
  
    ChartJS.register(
      Title,
      Tooltip,
      Legend,
      PointElement,
      RadialLinearScale,
      LineElement
    );
  </script>

<style>
    canvas {
        max-width: 600px;
        max-height: 600px;
        margin: 0 auto;
    }
</style>
  
  <Radar {data} options={{ responsive: true }} />