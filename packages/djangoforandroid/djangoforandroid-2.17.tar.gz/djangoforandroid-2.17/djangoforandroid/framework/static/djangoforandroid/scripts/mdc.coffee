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


    ##Open and close grawer from lateral slide
    #drawerEl = document.querySelector(".mdc-temporary-drawer");
    #MDCTemporaryDrawer = mdc.drawer.MDCTemporaryDrawer;
    #drawer = new MDCTemporaryDrawer(drawerEl);

    #MDL_Layout = new Hammer($("body")[0])
    #MDL_Layout.get("pan").set
        #velocity: 100
        #pointers: 1
        #threshold: 2
        #direction: Hammer.DIRECTION_HORIZONTAL
    #MDL_Layout.on "panright", (event) ->
        #if event
            #if event.center.x > 30 or event.center.x is 0
                #return
        #drawer.open = true;


    ##Add show drawer to menu icon
    #$(".mdc-toolbar__menu-icon").on "click", (event) ->
        #drawer.open = true


    ##Automatic tabs change
    #$(".mdc-tab-bar .mdc-tab").on "click", (event) ->
        #$(".mdc-tab-bar .mdc-tab").removeClass("mdc-tab--active")
        #$(@).addClass("mdc-tab--active")
        #panel = $(@).attr("aria-controls")
        #$(".panels .panel").hide()
        #$(".panels ##{panel}").show()
