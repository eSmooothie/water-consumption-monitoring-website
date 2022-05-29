var tr = document.createElement('tr');
tr.classList.add('bg-white', 'border-b');
var th = document.createElement('th');
th.classList.add('px-6', 'py-4', 'font-medium', 'text-gray-900', 'dark:text-white', 'whitespace-nowrap');
var td = document.createElement('td');
td.classList.add('px-6', 'py-4');
var tbody = document.getElementById('consumption_tbody');

$(document).ready(function(){
    // every 3 sec table the table will refresh its data
    setInterval(function(){
        getRequest();
    }, 2500);
});

function getRequest(){
    let base_url = window.location.origin;
    let api_url = "/api/get/consumption";
    let url = base_url + api_url;

    $.ajax(
        url = url,
        method = 'GET'
    ).done(function(data){
        status_code = data['status_code'];
        if(status_code == 200){

            var consumptions = data['consumptions_data'];
            document.getElementById('amount_to_pay').innerHTML = data['total_amount'];

            var latest_data = -1;
            if(tbody.childElementCount > 0){
                latest_data = tbody.children[0];
            }
            

            for (const key in consumptions) {
                if (Object.hasOwnProperty.call(consumptions, key)) {
                    const consumption = consumptions[key];

                    if(consumption['id'] == latest_data.id){
                        break;
                    }

                    if(consumption['id'] != latest_data.id){

                        let clone_tr = tr.cloneNode();
                        clone_tr.setAttribute('id', consumption['id']);

                        let clone_th = th.cloneNode();
                        clone_th.innerHTML = consumption['created_at'];

                        let elapsed_time_td = td.cloneNode();
                        elapsed_time_td.innerHTML = consumption['timelapse_in_min'];

                        let cubic_meter_td = td.cloneNode();
                        cubic_meter_td.innerHTML = consumption['cubic_per_meter'] + " cu. m";

                        let amount_td = td.cloneNode();
                        amount_td.innerHTML = consumption['amount'] + " PHP";

                        let peso_per_cub_td = td.cloneNode();
                        peso_per_cub_td.innerHTML = consumption['peso_per_cu_m'];

                        clone_tr.appendChild(clone_th);
                        clone_tr.appendChild(elapsed_time_td);
                        clone_tr.appendChild(cubic_meter_td);
                        clone_tr.appendChild(peso_per_cub_td);
                        clone_tr.appendChild(amount_td);

                        tbody.prepend(clone_tr);
                    }
                }
            }
        }
    }).fail(function(xhr){
        console.log(xhr);
    });
}