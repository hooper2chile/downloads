$(document).ready(function() {

  namespace = '/biocl';
  // Connect to the Socket.IO server.
  var socket = io.connect(location.protocol + '//' +
    		          document.domain + ':' +
	                  location.port + namespace);

//se emiten los detalles de la selección hacia el servidor
  $('form#form_db"').submit(function(event) {
      socket.emit('my_json',
                  { var: $('#variable').val(),
                    dt:  $('#dt').val()
                  });
      return false;
  });

  socket.on('my_json', function(msg) {
          N = msg.No
        //  console.log(N)
        //  console.log("'"+msg.data[1][0]+"'")
        //  console.log(msg.data[1][1])

          var time_ax = new Array(N)
          var temp    = new Array(N)
          for(i=1;i<=N;i++){
            time_ax[i] = msg.data[i][0]
            temp[i]    = msg.data[i][1]
          }

          if(msg.var=='T_PROMEDIO'){
            var var_options = {animation: {duration: 0}, scales: {yAxes: [{ticks: {beginAtZero: true, min: 0, max:  50,}}]}}
            var data_set     = {      labels: time_ax,
                                      datasets: [{
                                                    label: msg.var,
                                                    data: temp,
                                                    backgroundColor: "rgba(75,192,192,0.4)",
                                                    borderColor: "rgba(75,192,192,1)",
                                                  //pointRadius: 2.5,
                                                    lineTension: 0.5,
                                                    pointBackgroundColor: "#fff",
                                                    fill: false
                                                }]
                              }
          }

          if(msg.var=='T_SOMBRERO'){
            var var_options = {animation: {duration: 0}, scales: {yAxes: [{ticks: {beginAtZero: true, min: 0, max: 50,}}]}}
            var data_set     = {      labels: time_ax,
                                      datasets: [{
                                                    label: msg.var,
                                                    data: temp,
                                                    backgroundColor: "rgba(0,0,200,0.4)",
                                                    borderColor: "blue",
                                                    pointRadius: 2.5,
                                                    lineTension: 0.5,
                                                    pointBackgroundColor: "#fff",
                                                    fill: false
                                                }]
                              }
          }

          if(msg.var=='T_MOSTO'){
            var var_options = {animation: {duration: 0}, scales: {yAxes: [{ticks: {beginAtZero: true, min: 0, max:  50,}}]}}
            var data_set     = {      labels: time_ax,
                                      datasets: [{
                                                    label: msg.var,
                                                    data: temp,
                                                    backgroundColor: "rgba(200,0,0,0.4)",
                                                    borderColor: "red",
                                                    pointRadius: 2.5,
                                                    lineTension: 0.5,
                                                    pointBackgroundColor: "#fff",
                                                    fill: false
                                                }]
                              }
          }

          //Grafico
          var ctx = document.getElementById('myChart').getContext('2d');
          var myChart = new Chart(ctx, {
            type: 'line',
            data: data_set,
            options: var_options
          });

  });//fin de la función socket
});//fin de la función document.ready
