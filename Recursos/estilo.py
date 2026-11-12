backgroundColor = "#aadee9"
buttonColor = "#2726ff"
OkButtonColor =  "#2bff00"
CancelButtonColor = "#ff0000"

buttonstyle = {
"background":buttonColor, 
"foreground":"White", 
"font":("Arial", 12)
}

buttonmap = {
"background":[("active",buttonColor),("disabled","#1d1d28")],
"foreground":[("active","yellow")],
"bordercolor":[("!active",buttonColor),("active","yellow")],
"relief" : [('pressed', 'sunken'),('!pressed', 'raised')]
}

buttonstyle_aceptar = {
"background":OkButtonColor, 
"foreground":"White", 
"font":("Arial", 12)
}

buttonmap_aceptar = {
"background":[("active",OkButtonColor),("disabled","#202024")],
"foreground":[("active","yellow")],
"bordercolor":[("!active",OkButtonColor),("active","yellow")],
"relief" : [('pressed', 'sunken'),('!pressed', 'raised')]
}

buttonstyle_rechazar = {
"background":"#ff0000", 
"foreground":"White", 
"font":("Arial", 12)
}

buttonmap_rechazar = {
"background":[("active","#ff0000"),("disabled","#202024")],
"foreground":[("active","yellow")],
"bordercolor":[("!active","#ff0000"),("active","yellow")],
"relief" : [('pressed', 'sunken'),('!pressed', 'raised')]
}