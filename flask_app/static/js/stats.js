"use strict";
let show_line = (date_count) =>{
  let dates = Object.keys(date_count);
  let amount = Object.values(date_count);
  graph_line(dates,amount);
} 

let show_pie = (tipo_count) =>{
  graph_pie(tipo_count);
  //graph_line(dates,amount);
} 

let show_bar = (tipo_month_count) =>{
  let gatos=tipo_month_count["gato"];
  let perros=tipo_month_count["perro"];
  let dates = Object.keys(gatos);
  let amount_gatos = Object.values(gatos);
  let amount_perros = Object.values(perros);
  graph_bar(dates,amount_gatos,amount_perros)
  //graph_line(tipo_month_count);
} 


let fetchUrl = (url,function_show) => {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((jsonResponse) => { 
      function_show(jsonResponse["data"]); 
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
};


let get_dates = () => {
  fetchUrl(`/get-fechas/`,show_line);
};

let get_tipos = () => {
  fetchUrl(`/get-tipos/`,show_pie);
};


let get_tipo_month = () => {
  fetchUrl(`/get-tipos-mes/`,show_bar);
};

let graph_line= (dates,amount) =>{
    Highcharts.chart('graph-line', {

        title: {
            text: 'Avisos por día',
            align: 'left'
        },

        subtitle: {
            text: 'Total de avisos subidos cada día.',
            align: 'left'
        },
        xAxis: {
            title: {
                text: 'Año'
            },
            type: 'datetime',
            categories: dates
            },

        yAxis: {
            title: {
                text: 'Numero de avisos por día'
            }
        },

        series: [{
            name: 'avisos',
            data: amount
        }]

        
    });
}

let graph_pie= (tipo_count) =>{
    let cat_count=tipo_count["gato"]
    let dog_count=tipo_count["perro"]
    const colors = Highcharts.getOptions().colors.map((c, i) =>
        Highcharts.color(Highcharts.getOptions().colors[0])
            .brighten((i - 3) / 7)
            .get()
    );


    Highcharts.chart('graph-pie', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Total de avisos por tipo de mascota',
            align: 'left'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
            pointFormatter: function() {
                return `<b>${this.name}</b>: ${this.y} (${this.percentage.toFixed(2)}%)`;
            }
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                colors,
                borderRadius: 5,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b><br>{point.percentage:.1f} %',
                    distance: -50,
                    filter: {
                        property: 'percentage',
                        operator: '>',
                        value: 4
                    }
                }
            }
        },
        series: [{
            name: 'Porcentaje',
            data: [
                { name: 'Gatos', y: cat_count },
                { name: 'Perros', y: dog_count }
            ]
        }]
    });
}

let graph_bar= (dates,amount_gatos,amount_perros) =>{
    Highcharts.chart('graph-bar', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Cantidad de avisos para gatos y perros por mes',
            align: 'left'
        },
        xAxis: {
            categories: dates,
            crosshair: true,
            accessibility: {
                description: 'Tipo'
            },
            type: 'datetime',
            title: {
                text: 'Año-Mes'
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Cantidad de avisos'
            }
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            {
                name: 'Gatos',
                data: amount_gatos
            },
            {
                name: 'Perros',
                data: amount_perros
            }
        ]
    });
}

//show_line()
get_dates()
get_tipos()
get_tipo_month()