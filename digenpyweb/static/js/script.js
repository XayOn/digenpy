window.do_digenpy = () ->
    if ($ 'input[name=WPA]').is(':checked')
        jQuery.ajax "/get/Spanish/" + ($ '#company').val() + "WPA/" + ($ '#mac').val() + "/" + ($ '#essid').val(),
            type: 'GET',
            success: (data, textStatus, jqXHR) ->
                ($ '#wpa_pass').text(data)
                ($ '#wpamodal').modal('show')
    else
        window.location.href = "/get_file/Spanish/" + $('#company').val() + "/" + $('#mac').val() + "/" + $('#essid').val()
