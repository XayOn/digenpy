/* Author:
    David Francos Cuartero
    GPL 2+
*/

function get_digenpy_url(){
	if($('#WPA').is(':checked')){
		return "/get/Spanish/" + $('#company').val() + "WPA/" + $('#mac').val() + "/" + $('#essid').val();
    }
	return "/get_file/Spanish/" + $('#company').val() + "/" + $('#mac').val() + "/" + $('#essid').val();
}

function do_digenpy(){
    $('#result').attr('src',get_digenpy_url());
}


