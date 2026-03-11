document.addEventListener("DOMContentLoaded", function () {
    console.log("Charts JS Loaded ✅");

    loadSalesChart();
    loadFilteredChart();
    loadDayWiseChart();
    loadCategoryChart();
    loadYearlyChart();
    loadYearMonthChart();
    loadAOVChart();
    loadRevenueOrdersChart();
    loadTopProductsChart();
    loadPriceRangeChart();
    loadCLVChart();
    loadUserChart();
});

function createChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, config);
}

// ✅ SALES CHART
function loadSalesChart() {

    fetch("/dashboard/api/sales/")
        .then(response => response.json())
        .then(data => {

            const labels = data.labels;
            const values = data.data;

            const ctx = document.getElementById("salesChart").getContext("2d");

            if (window.salesChartInstance) {
                window.salesChartInstance.destroy();
            }

            window.salesChartInstance = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Sales",
                        data: values,
                        borderWidth: 2,
                        fill: false
                    }]
                }
            });

        });
}

// ✅ FILTERED CHART
function loadFilteredChart() {
    const canvas = document.getElementById('filteredSalesChart');
    if (!canvas) return;

    if (!filtered_dates || filtered_dates.length === 0) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: filtered_dates,
            datasets: [{
                label: 'Revenue',
                data: filtered_revenues,
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true
        }
    });
}

let dayChart = null;

function loadDayWiseChart(month=null, year=null) {

    if(!month || !year){
        const monthSelect = document.querySelector("select[name='month']");
        const yearSelect = document.querySelector("select[name='year']");

        month = monthSelect.value;
        year = yearSelect.value;
    }

    fetch(`/dashboard/api/daywise-report/?month=${month}&year=${year}`)
    .then(res => res.json())
    .then(data => {

        const canvas = document.getElementById("dayWiseChart");
        if(!canvas) return;

        const ctx = canvas.getContext("2d");

        if(dayChart){
            dayChart.destroy();
        }

        dayChart = new Chart(ctx,{
            type:"bar",
            data:{
                labels:data.labels,
                datasets:[
                    {
                        label:"Orders",
                        data:data.orders,
                        backgroundColor:"rgba(54,162,235,0.7)",
                        borderRadius:6
                    },
                    {
                        label:"Revenue",
                        data:data.revenues,
                        backgroundColor:"rgba(255,99,132,0.7)",
                        borderRadius:6
                    }
                ]
            },
            options:{
                responsive:true,
                scales:{
                    y:{beginAtZero:true}
                }
            }
        });

    });

}
// 📦 CATEGORY CHART
function loadCategoryChart() {

    fetch("/dashboard/api/category-report/")
    .then(res => res.json())
    .then(data => {

        const canvas = document.getElementById('categoryChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.revenues,
                    backgroundColor: [
                        '#ff6384',
                        '#36a2eb',
                        '#ffcd56',
                        '#4bc0c0',
                        '#9966ff',
                        '#ff9f40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });

    });
}

// 📆 YEARLY CHART
function loadYearlyChart() {
    createChart('yearlySalesChart', {
        type: 'bar',
        data: {
            labels: year_labels,
            datasets: [{
                label: 'Yearly Revenue',
                data: year_revenues
            }]
        }
    });
}
let monthlyChart = null;

function loadYearMonthChart(year=null){

    if(!year){
        const yearSelect = document.getElementById("yearSelect");
        year = yearSelect.value;
    }

    fetch(`/dashboard/api/monthly-sales/?year=${year}`)
    .then(res => res.json())
    .then(data => {

        const canvas = document.getElementById("yearMonthChart");
        if(!canvas) return;

        const ctx = canvas.getContext("2d");

        if(monthlyChart){
            monthlyChart.destroy();
        }

        monthlyChart = new Chart(ctx,{
            type:"bar",
            data:{
                labels:data.labels,
                datasets:[{
                    label:"Monthly Revenue (₹)",
                    data:data.revenues,
                    backgroundColor:"rgba(75,192,192,0.7)",
                    borderRadius:6
                }]
            },
            options:{
                responsive:true,
                scales:{
                    y:{beginAtZero:true}
                }
            }
        });

    });

}
function loadAOVChart() {
    createChart('aovChart', {
        type: 'line',
        data: {
            labels: aov_dates,
            datasets: [{
                label: 'AOV (₹)',
                data: aov_values,
                borderColor: '#ff6384',
                backgroundColor: 'rgba(255,99,132,0.1)',
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function loadRevenueOrdersChart() {
    const canvas = document.getElementById('revenueOrdersChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: revenue_orders_dates,
            datasets: [
                {
                    label: 'Revenue (₹)',
                    data: revenue_orders_revenue,
                    borderColor: '#28a745',
                    tension: 0.3,
                    yAxisID: 'y'
                },
                {
                    label: 'Orders',
                    data: revenue_orders_counts,
                    borderColor: '#007bff',
                    tension: 0.3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

//top selling products
function loadTopProductsChart() {
    const canvas = document.getElementById('topProductsChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top_products_labels,
            datasets: [{
                label: 'Units Sold',
                data: top_products_data,
                backgroundColor: 'rgba(255, 193, 7, 0.7)'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true
        }
    });
}

//clv
function loadCLVChart() {
    createChart('clvChart', {
        type: 'bar',
        data: {
            labels: clv_labels,
            datasets: [{
                label: 'CLV',
                data: clv_values
            }]
        }
    });
}

//user chart
function loadUserChart() {
    const canvas = document.getElementById('userChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: user_labels,
            datasets: [{
                label: 'Total Spent',
                data: user_data
            }]
        },
        options: {
            responsive: true
        }
    });
}

//PRICE RANGE
function loadPriceRangeChart() {
    createChart('priceRangeChart', {
        type: 'doughnut',
        data: {
            labels: price_range_labels,
            datasets: [{
                data: price_range_data
            }]
        }
    });
}

function quickFilter(range){

    fetch(`/dashboard/api/sales-report/?range=${range}`)
    .then(res => res.json())
    .then(data => {

        let chart = Chart.getChart("filteredSalesChart");

        if(chart){
            chart.destroy();
        }

        const ctx = document.getElementById("filteredSalesChart");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Revenue",
                    data: data.revenues,
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true
            }
        });

    });

}

document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("salesFilterForm");

    if(!form) return;

    form.addEventListener("submit", function(e){

        e.preventDefault();   // 🚀 stops page reload

        let from = form.querySelector("input[name='from_date']").value;
        let to = form.querySelector("input[name='to_date']").value;

        fetch(`/dashboard/api/sales-report/?from_date=${from}&to_date=${to}`)
        .then(res => res.json())
        .then(data => {

            let chart = Chart.getChart("filteredSalesChart");

            if(chart){
                chart.destroy();
            }

            const ctx = document.getElementById("filteredSalesChart");

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: "Revenue",
                        data: data.revenues,
                        borderWidth: 2,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true
                }
            });

        });

    });

});

document.addEventListener("DOMContentLoaded",function(){

    const form = document.getElementById("daywiseForm");

    if(!form) return;

    form.addEventListener("submit",function(e){

        e.preventDefault();

        const month = form.querySelector("select[name='month']").value;
        const year = form.querySelector("select[name='year']").value;

        loadDayWiseChart(month,year);

    });

});

document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("monthlySalesForm");

    if(!form) return;

    form.addEventListener("change", function(){

        const year = document.getElementById("yearSelect").value;

        loadYearMonthChart(year);

    });

});