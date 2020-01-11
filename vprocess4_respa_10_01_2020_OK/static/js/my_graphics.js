// Connect to the Socket.IO server.
namespace = '/biocl';
var socket = io.connect(location.protocol + '//' +
             document.domain + ':' +
             location.port + namespace);


function my_chart(){

          var N = parseInt($('#real_time').val());

          var time_axis = new Array(N+1);

          var med_ph    = new Array(N+1);
          var med_od    = new Array(N+1);
          var med_temp  = new Array(N+1);

          var set_ph    = new Array(N+1);


          for(i=N;i>=0;i=i-6){
            time_axis[i] = N-i;
          }

          for(i=0;i<=N;i++){
            if(time_axis[i]==undefined){
              time_axis[i] = "  ";
            }
            else {
              time_axis[i]= " '0." + time_axis[i] + "[s] ' " ;
            }
          }

          //mediciones de ph, OD, Temp. Socket regenera el grafico con cada llamada!!!
          socket.on('Medidas', function(msg) {
              $('#med1_g').text('T. Promedio: ' + msg.data[0] + '[C]' ).html();
              $('#med2_g').text('T. Sombrero: ' + msg.data[1] + '[C]' ).html();
              $('#med3_g').text('T. Mosto: ' + msg.data[2] + '[C]' ).html();

              //muestra el setpoint de ph en el grafico real time.
              $('#ph_g').text('Temperatura Set: ' + msg.set[4]         ).html();

              //grafico ph
              set_ph.shift();
              set_ph.push( parseFloat( [msg.set[4] ] ) )

              med_ph.shift();
              med_ph.push( parseFloat( [ msg.data[0] ] ) );

              var ctx = document.getElementById('myChart').getContext('2d')
              var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: time_axis,

                  datasets: [{
                    label: 'T. Promedio',//'TEMP1 Bioreactor',
                    data: med_ph,
                    fill: false,
                    lineTension: 0.5,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "rgba(75,192,192,1)",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 2.5,
                    pointHitRadius: 10,
                  },
                  {
                      label: 'Temp Set',
                      data: set_ph,
                      lineTension: 0.5,
                      borderColor: "rgba(255,0,0,1)",
                      borderJoinStyle: 'miter',
                      pointBackgroundColor: "rgba(255,0,0,1)",
                      fill: false,
                      pointRadius: 2.5,
                  }]
                },

                options: {
                    animation: {
                        duration: 0
                    },
          	        scales: {
                  		  yAxes: [{
                  			     ticks: {
                        			   beginAtZero: true,
                        			   min: 0,
                        			   max: 50,
                  			      }
                  		  }]
                  	}
      	        }
              });


              //grafico oxigeno disuelto
              med_od.shift();
              med_od.push( parseFloat( [ msg.data[1] ] ) );

              var ctx = document.getElementById('myChart2').getContext('2d')
              var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: time_axis,

                  datasets: [{
                    label: 'T. Sombrero',
                    data: med_od,
                    fill: false,
                    lineTension: 0.5,
                    backgroundColor: "rgba(0,0,200,0.4)",
                    borderColor: "blue",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "blue",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 2.5,
                    pointHitRadius: 10,
                  }]
                },

                options: {
                    animation: {
                        duration: 0
                    },
                    scales: {
                        yAxes: [{
                             ticks: {
                                 beginAtZero: true,
                                 min: 0,
                                 max: 50,
                              }
                        }]
                    }
                }
              });


              //Grafico temperatura
              med_temp.shift();
              med_temp.push( parseFloat( [ msg.data[2] ] ) );

              var ctx = document.getElementById('myChart3').getContext('2d')
              var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                  labels: time_axis,

                  datasets: [{
                    label: 'T. Mosto',
                    data: med_temp, //med_temp
                    fill: false,
                    lineTension: 0.5,
                    backgroundColor: "rgba(0,200,0,0.4)",
                    borderColor: "green",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "green",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 2.5,
                    pointHitRadius: 10,
                  }]
                },

                options: {
                    animation: {
                        duration: 0
                    },
                    scales: {
                        yAxes: [{
                             ticks: {
                                 beginAtZero: true,
                                 min: 0,
                                 max: 50,
                              }
                        }]
                    }
                }


              });
      //fin ultimo grafico

  });//fin de la función socket.on


//});//fin de la función document.ready
}
