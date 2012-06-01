/* Author:
    David Francos Cuartero
    GPL 2+
*/

function get_digenpy_url(){
    if ($('#wpa').val()){
        return "/get/Spanish/" + $('#company').val() + "/" + $('#mac').val() + "/" + $('#essid').val()
    }
    return "/get_file/Spanish/" + $('#company').val() + "/" + $('#mac').val() + "/" + $('#essid').val()
}

function do_digenpy(){
    if ($('#wpa').val()){
        
    } else {
        $('#result').attr('src',get_digenpy_url());
    }
}


