$(document).ready(function() {

var Itemp1 = 0;
var Itemp2 = 0;
var Iod    = 0;

// Connect to the Socket.IO server.
namespace = '/biocl';
var socket = io.connect(location.protocol + '//' +
             document.domain + ':' +
             location.port + namespace);

          //mediciones de ph, OD, Temp.
          socket.on('Medidas', function(msg) {
              $('#med1_c').text('Itemp: '  + msg.data[3] + ' [mA]' ).html();
              $('#med2_c').text('Iod: '    + msg.data[4] + ' [mA]' ).html();
              $('#med3_c').text('Itemp: '  + msg.data[5] + ' [mA]' ).html();

              Itemp1 = msg.data[3];
              Iod    = msg.data[4];
              Itemp2 = msg.data[5];
          });//fin de la función socket.on


          $('#med1_c').css({ 'color': 'white', 'font-size': '120%' });
          $('#med2_c').css({ 'color': 'white', 'font-size': '120%' });
          $('#med3_c').css({ 'color': 'white', 'font-size': '120%' });


          //CALIBRAR PH
          //se emiten la calibración hacia el servidor
          $('form#calibrar_ph').submit(function(event) {
              socket.emit('ph_calibrar',
                          {   ph : $('#ph').val(),
                             iph : Itemp1,
                            medx : $('#medx_ph').val()
                           });

                console.log("en socket.emit TEMP1:");
                console.log( $('#ph').val() );
                console.log(Itemp1);
                return false;
          });

          //se escuchan desde el servidor los valores seteados para calibración.
          socket.on('ph_calibrar', function(msg) {
            $('#ph1_set' ).text('Set Temp1 : ' + msg.set[0]).html();
            $('#iph1_set').text('Set Itemp1: ' + msg.set[1]).html();
            $('#ph2_set' ).text('Set Temp2 : ' + msg.set[2]).html();
            $('#iph2_set').text('Set Itemp2: ' + msg.set[3]).html();
          });



          //CALIBRAR OD
          //se emiten la calibración hacia el servidor
          $('form#calibrar_od').submit(function(event) {
              socket.emit('od_calibrar',
                          {   od : $('#od').val(),
                             iod : Iod,
                            medx : $('#medx_od').val()
                           });

                console.log("en socket.emit OD:");
                console.log( $('#od').val() );
                console.log(Iod);
              return false;
          });

          //se escuchan desde el servidor los valores seteados para calibración.
          socket.on('od_calibrar', function(msg) {
            $('#od1_set' ).text('Set OD1 : ' + msg.set[0]).html();
            $('#iod1_set').text('Set IOd1: ' + msg.set[1]).html();
            $('#od2_set' ).text('Set OD2 : ' + msg.set[2]).html();
            $('#iod2_set').text('Set IOd2: ' + msg.set[3]).html();
          });




          //CALIBRAR TEMP
          //se emiten la calibración hacia el servidor
          $('form#calibrar_temp').submit(function(event) {
              socket.emit('temp_calibrar',
                          {   temp : $('#temp').val(),
                             itemp : Itemp2,
                              medx : $('#medx_temp').val()
                           });

                console.log("en socket.emit TEMP2:");
                console.log( $('#temp').val() );
                console.log(Itemp2);
              return false;
          });

          //se escuchan desde el servidor los valores seteados para calibración.
          socket.on('temp_calibrar', function(msg) {
            $('#temp1_set' ).text('Set Temp1 : ' + msg.set[0]).html();
            $('#itemp1_set').text('Set Itemp1: ' + msg.set[1]).html();
            $('#temp2_set' ).text('Set Temp2 : ' + msg.set[2]).html();
            $('#itemp2_set').text('Set Itemp2: ' + msg.set[3]).html();
          });




          //CALIBRAR ACTUADOR PH
          //se emite la calibración hacia el servidor
          $('form#calibrar_u').submit(function(event) {
              socket.emit('u_calibrar',
                          {   u_acido_max : $('#u_a').val(),
                              u_base_max  : $('#u_b').val()
                           });

                //console.log("en socket.emit actuador:");
                //console.log( $('#u_a').val() );
                //console.log( $('#u_b').val() );
              return false;
          });

          //se escuchan desde el servidor los valores seteados para calibración.
          socket.on('u_calibrar', function(msg) {
            $('#rpm_max_a').text('Set MAX rpm acido: ' + msg.set[0]).html();
            $('#rpm_max_b').text('Set MAX rmp base : ' + msg.set[1]).html();
            //test
            console.log( msg.set[0] );
            console.log( msg.set[1] );

          });


          //CALIBRAR ACTUADOR TEMP
          //se emite la calibración hacia el servidor
          $('form#calibrar_u_temp').submit(function(event) {
              socket.emit('u_calibrar_temp',
                          {   u_temp : $('#u_temp').val()
                          });

                //console.log("en socket.emit actuador temp:");
                //console.log( $('#u_temp').val() );
              return false;
          });

          //se escuchan desde el servidor los valores seteados para calibración.
          socket.on('u_calibrar_temp', function(msg) {
            $('#rpm_max_temp').text('Set MAX rpm Temperatura: ' + msg.set ).html();
            //test
            console.log( msg.set );
          });


});
