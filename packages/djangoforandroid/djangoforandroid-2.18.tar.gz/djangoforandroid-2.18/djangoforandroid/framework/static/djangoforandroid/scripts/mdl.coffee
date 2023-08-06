


########################################################################
class MDLTouchDrawer

    #----------------------------------------------------------------------
    constructor: () ->
        @DEBUG = false
        @TIMEOUT = true
        @TIME_ANIMATION = "0.3s"
        #@MIN_TIME_ANIMATION = "0s"
        @WIDTH_DRAWER = $(".mdl-layout__drawer").width() + parseInt($(".mdl-layout__drawer").css("border-right-width")) + parseInt($(".mdl-layout__drawer").css("border-left-width"))


    #----------------------------------------------------------------------
    hide_drawer: (event) =>
        cls = @
        fn=()->
            $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
            $(".mdl-layout__drawer").css({"-webkit-transition-duration": "#{cls.TIME_ANIMATION}"})
            $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{cls.WIDTH_DRAWER}px)"})
        setTimeout(fn, cls.TIMEOUT)


    #----------------------------------------------------------------------
    show_drawer: (event) =>
        cls = @

        if event
            if event.center.x > 30 or event.center.x is 0
                return

        fn=()->
            $(".mdl-layout__drawer, .mdl-layout__obfuscator").addClass("is-visible")
            $(".mdl-layout__drawer").css({"-webkit-transition-duration": "#{cls.TIME_ANIMATION}"})
            $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(#{0}px)"})
        setTimeout(fn, cls.TIMEOUT)


    #----------------------------------------------------------------------
    toggle_drawer: (event) =>
        cls = @
        #fn=()->
        if $(".mdl-layout__drawer").hasClass("is-visible")
            cls.hide_drawer()
        else
            cls.show_drawer()
        #setTimeout(fn, cls.TIMEOUT)


$(document).ready ->


    MDLTouchDrawer = new MDLTouchDrawer()
    document.MDLTouchDrawer = MDLTouchDrawer


#Contructor
#----------------------------------------------------------------------

    #var myElement = document.getElementById('myElement');
    MDL_Layout = new Hammer($("body")[0])
    MDL_Layout.get("pan").set
        velocity: 100
        pointers: 1
        threshold: 2
        direction: Hammer.DIRECTION_HORIZONTAL
    #MDL_Layout.on "panleft", MDLTouchDrawer.hide_drawer
    #MDL_Layout.on "panstart", MDLTouchDrawer.show_drawer
    MDL_Layout.on "panright", MDLTouchDrawer.show_drawer

    MDL_Layout2 = new Hammer($("body")[0])
    MDL_Layout2.get("pan").set
        velocity: 100
        pointers: 1
        threshold: 100
        direction: Hammer.DIRECTION_HORIZONTAL
    MDL_Layout2.on "panleft", MDLTouchDrawer.hide_drawer
    #MDL_Layout2.on "panstart", MDLTouchDrawer.show_drawer





    #MDL_Layout_ofuscator = new Hammer($(".mdl-layout__obfuscator")[0])
    #MDL_Layout_ofuscator.on "tap", MDLTouchDrawer.hide_drawer

    $(document).on "click", ".mdl-layout__obfuscator, .mdl-hide-drawer", (event) ->
        MDLTouchDrawer.hide_drawer()

    $(document).on "click", ".mdl-layout__drawer-button", (event) ->
        #fn=()->
        if MDLTouchDrawer.DEBUG
            console.log("Click drawer button")

        if $(".mdl-layout__drawer").hasClass("is-visible")
            MDLTouchDrawer.show_drawer()
        else
            MDLTouchDrawer.hide_drawer()
        #setTimeout(fn, cls.TIMEOUT)



    $(document).on "click", ".d4a-hide_drawer", (event) ->
        MDLTouchDrawer.hide_drawer()

    $(document).on "click", ".d4a-show_drawer", (event) ->
        MDLTouchDrawer.show_drawer()

    $(document).on "click", ".d4a-toggle_drawer", (event) ->
        MDLTouchDrawer.toggle_drawer()