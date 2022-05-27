

function load_data_to_chart({labels=[],dataset=[]}){
    // setup
    const label = labels;
    const data = {
        labels: label,
        datasets: dataset
    };

    // [{
    //     label: 'My First dataset',
    //     backgroundColor: 'rgb(255, 99, 132)',
    //     borderColor: 'rgb(255, 99, 132)',
    //     data: [0, 10, 5, 2, 20, 30, 45],
    // }]

    // config
    const config = {
        type: 'line',
        data: data,
        options: {
            'responsive': true,
            'maintainAspectRatio' : false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                      // Luxon format string
                      tooltipFormat: 'DD T'
                    },
                    title: {
                      display: true,
                      text: 'Date and Time'
                    }
                }, y: {
                    title: {
                      display: true,
                      text: ''
                    }
                }
            }
        }
    };
    // render
    const myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
}

$(document).ready(function(){
    let base_url = window.location.origin;
    let api_url = "/api/get/history_consumption";
    let url = base_url + api_url;

    $.ajax(
        url = url,
        method = 'GET',
    ).done(function(data){
        
        var consumption_data = data['consumptions_data'];

        var labels = data['label'].map((elem, i) => {
            return convertTZ(elem, "Asia/Manila");
        });

        var elapsed_time_data = [];
        var cubic_meter_data = [];
        var peso_per_cu_m_data = [];
        var amount_data = [];

        let i = 0;
        for (const key in consumption_data) {
            if (Object.hasOwnProperty.call(consumption_data, key)) {
                const consumption = consumption_data[key];

                const elapsed_time = consumption['timelapse_in_min'];
                const cubic_meter = consumption['cubic_per_meter'];
                const peso_per_cu_m = consumption['peso_per_cu_m'];
                const amount = consumption['amount'];

                const date = labels[i];

                elapsed_time_data.push({x:date,y:elapsed_time});
                cubic_meter_data.push({x:date,y:cubic_meter});
                peso_per_cu_m_data.push({x:date,y:peso_per_cu_m});
                amount_data.push({x:date,y:amount});
                i += 1;
            }
        }
        
        var elapsed_time_dataset = {
            label: 'Elapsed Time',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: elapsed_time_data,
            fill: false,
            hidden: true,
        };

        var cubic_meter_dataset = {
            label: 'Cubic per meter',
            backgroundColor: 'rgb(255, 159, 64)',
            borderColor: 'rgb(255, 159, 64)',
            data: cubic_meter_data,
            fill: false,
            hidden: true,
        };

        var peso_per_cu_m_dataset = {
            label: 'Peso / cu. m',
            backgroundColor: 'rgb(255, 205, 86)',
            borderColor: 'rgb(255, 205, 86)',
            data: peso_per_cu_m_data,
            fill: false,
            hidden: true,
        };

        var amount_dataset = {
            label: 'Amount',
            backgroundColor: 'rgb(75, 192, 192)',
            borderColor: 'rgb(75, 192, 192)',
            data: amount_data,
            fill: false,
            hidden: false,
        };

        var datasets = [
            elapsed_time_dataset,
            cubic_meter_dataset,
            peso_per_cu_m_dataset,
            amount_dataset,
        ];

        load_data_to_chart({
            labels : labels,
            dataset : datasets
        })

    }).fail(function(xhr){
        console.log(xhr);
    });
});

function convertTZ(date, tzString) {
    return new Date((typeof date === "string" ? new Date(date) : date)).toISOString();   
}