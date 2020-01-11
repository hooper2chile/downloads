$(document).ready(function() {

    namespace = '/biocl';

    // Connect to the Socket.IO server.
    var socket = io.connect(location.protocol + '//' +
	    		       document.domain + ':' +
		             location.port + namespace);



    //Se escuchan las mediciones de ph, OD, Temp.
    socket.on('Medidas', function(msg) {
        $('#med1').text('T. Promedio: ' + msg.data[0] + ' º[C]').html();
        $('#med2').text('T. Sombrero: ' + msg.data[1] + ' º[C]').html();
        $('#med3').text('T. Mosto   : ' + msg.data[2] + ' º[C]').html();
    });

    //se emiten los setpoints hacia el servidor
    $('form#setpoints').submit(function(event) {
        socket.emit('Setpoints',
                    { alimentar:     $('#alimentar').val(),
                        mezclar:     $('#mezclar').val(),
                             ph:     $('#ph').val(),
                       descarga:     $('#descargar').val(),
                    temperatura:     $('#temperatura').val(),
                      alimentar_rst: $('#alimentar_rst').is(':checked'),  //rst1
                        mezclar_rst: $('#mezclar_rst').is(':checked'),    //rst2
                             ph_rst: $('#ph_rst').is(':checked'),         //rst3
                       descarga_rst: $('#descargar_rst').is(':checked'),  //rst4
                    temperatura_rst: $('#temperatura_rst').is(':checked'),//rst5
                      alimentar_dir: $('#alimentar_dir').is(':checked'),  //dir1
                             ph_dir: $('#ph_dir').is(':checked'),         //dir2
                    temperatura_dir: $('#temperatura_dir').is(':checked') //dir3
                     });

        //para depurar
        console.log('Emitiendo Valores: alimentar, mezclar, ph, descargar, temperatura:');
        console.log($('#alimentar').val());
        console.log($('#mezclar').val());
        console.log($('#ph').val());
        console.log($('#descargar').val());
        console.log($('#temperatura').val());

        console.log('Emitiendo Chekeds');
        console.log($('#alimentar_rst').is(':checked'));
        console.log($('#mezclar_rst').is(':checked'));
        console.log($('#ph_rst').is(':checked'));
        console.log($('#descargar_rst').is(':checked'));
        console.log($('#temperatura_rst').is(':checked'));
        console.log($('#alimentar_dir').is(':checked'));
        console.log($('#ph_dir').is(':checked'));
        console.log($('#temperatura_dir').is(':checked'));


        socket.emit('producto',
                    { densidad: $('#densidad_input_id').val(),
                           yan: $('#yan_input_id').val(),
                            ph: $('#ph_input_id').val(),
                          brix: $('#brix_input_id').val(),
                        acidez: $('#acidez_input_id').val(),
                         fundo: $('#fundo_input_id').val(),
                          cepa: $('#cepa_input_id').val(),
                          lote: $('#lote_input_id').val(),
                         dosis: $('#dosis_input_id').val()
                    });
        return false;
    });

    //se escuchan desde el servidor los setpoints aplicados
    //para ser desplegados en todos los clientes.
    socket.on('Setpoints', function(msg) {
        document.getElementById('alimentar').value         = msg.set[0];
        document.getElementById('mezclar').value           = msg.set[1];
        document.getElementById('ph').value                = msg.set[2];
        document.getElementById('descargar').value         = msg.set[3];
        document.getElementById('temperatura').value       = msg.set[4];
        document.getElementById('alimentar_rst').checked   = msg.set[5];
        document.getElementById('mezclar_rst').checked     = msg.set[6];
        document.getElementById('ph_rst').checked          = msg.set[7];
        document.getElementById('descargar_rst').checked   = msg.set[8];
        document.getElementById('temperatura_rst').checked = msg.set[9];
        document.getElementById('alimentar_dir').checked   = msg.set[10];
        document.getElementById('ph_dir').checked          = msg.set[11];
        document.getElementById('temperatura_dir').checked = msg.set[12];

        //para depurar
        console.log('Checkeds Recibidos');
        console.log($('#alimentar_rst').is(':checked'));
        console.log($('#mezclar_rst').is(':checked'));
        console.log($('#ph_rst').is(':checked'));
        console.log($('#descargar_rst').is(':checked'));
        console.log($('#temperatura_rst').is(':checked'));
        console.log($('#alimentar_dir').is(':checked'));
        console.log($('#ph_dir').is(':checked'));
        console.log($('#temperatura_dir').is(':checked'));
    });


    //para escuchar datos de ficha de producto
    socket.on('producto', function(msg) {
        document.getElementById('densidad_input_id').value = msg.set[0];
        document.getElementById('yan_input_id').value      = msg.set[1];
        document.getElementById('ph_input_id').value       = msg.set[2];
        document.getElementById('brix_input_id').value     = msg.set[3];
        document.getElementById('acidez_input_id').value   = msg.set[4];
        document.getElementById('fundo_input_id').value    = msg.set[5];
        document.getElementById('cepa_input_id').value     = msg.set[6];
        document.getElementById('lote_input_id').value     = msg.set[7];
        document.getElementById('dosis_input_id').value    = msg.set[8];

        //aca el codigo para insertar los valores guardados
        $('#densidad_div_id').text('Densidad: ' + msg.save[0] ).html();
        $('#yan_div_id'     ).text('Yan     : ' + msg.save[1] ).html();
        $('#ph_div_id'      ).text('pH      : ' + msg.save[2] ).html();
        $('#brix_div_id'    ).text('Brix    : ' + msg.save[3] ).html();
        $('#acidez_div_id'  ).text('Acidez  : ' + msg.save[4] ).html();
        $('#fundo_div_id'   ).text('Fundo   : ' + msg.save[5] ).html();
        $('#cepa_div_id'    ).text('Cepa    : ' + msg.save[6] ).html();
        $('#lote_div_id'    ).text('Lote    : ' + msg.save[7] ).html();
        $('#dosis_div_id'   ).text('Dosis   : ' + msg.save[8] ).html();
    });


    //se emiten señal de reinicio,apagado, grabacion y limpiaza hacia el servidor
    $('form#process').submit(function(event) {
        socket.emit('power',
                    { action  : $('select[name=selection]').val(),
                      checked : $('#confirm').is(':checked')
                   });

        //para depurar
        console.log('Emitiendo Valores de Acción');
        console.log($('select[name=selection]').val())
        console.log($('#confirm').is(':checked'));

        return false;
    });

    //se escuchan desde el servidor señal de reinicio,apagado, grabacion y limpiaza
    //para ser desplegados en todos los clientes.
    socket.on('power', function(msg) {
        document.getElementById("select").value    = msg.set[0]
        document.getElementById('confirm').checked = msg.set[1]

        console.log('Recibiendo Valores de Acción');
        console.log(msg.set[0]);
        console.log(msg.set[1]);
    });

    $('#densidad_div_id' ).css({ 'color': 'white', 'font-size': '110%' });
    $('#yan_div_id'      ).css({ 'color': 'white', 'font-size': '110%' });
    $('#ph_div_id'       ).css({ 'color': 'white', 'font-size': '110%' });
    $('#brix_div_id'     ).css({ 'color': 'white', 'font-size': '110%' });
    $('#acidez_div_id'   ).css({ 'color': 'white', 'font-size': '110%' });
    $('#brix_div_id'     ).css({ 'color': 'white', 'font-size': '110%' });
    $('#fundo_div_id'    ).css({ 'color': 'white', 'font-size': '110%' });
    $('#cepa_div_id'     ).css({ 'color': 'white', 'font-size': '110%' });
    $('#lote_div_id'     ).css({ 'color': 'white', 'font-size': '110%' });
    $('#dosis_div_id'    ).css({ 'color': 'white', 'font-size': '110%' });
});
