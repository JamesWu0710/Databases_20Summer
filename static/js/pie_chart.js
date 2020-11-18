document.addEventListener('DOMContentLoaded', function () {
    var chart1 = Highcharts.chart(chart_id_y, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: chart_type
        },
        title: {
            text: title1
        },
        accessibility: {
            point: {
                valueSuffix: '$'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                }
            }
        },
        series: [{
            name: 'Revenue in last year: View in Quarters',
            colorByPoint: true,
            data: [{
                name: '1st quarter revenue',
                y: quarter1,
            },{
                name: '2nd quarter revenue',
                y: quarter2,

            },{
                name: '3rd quarter revenue',
                y: quarter3,

            },{name: '4th quarter revenue',
                y: quarter4,

            }]
        }]
    });
});
