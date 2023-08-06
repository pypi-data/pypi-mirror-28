$(document).ready ->

    #csrftoken for AJAX
    #----------------------------------------------------------------------
    #Ajax setup for use CSRF tokens
    csrftoken = $.cookie("csrftoken")
    csrfSafeMethod = (method) -> (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
    $.ajaxSetup
        beforeSend: (xhr, settings) ->
            if not csrfSafeMethod(settings.type) and not @crossDomain
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
    window.csrftoken = csrftoken
    #----------------------------------------------------------------------

