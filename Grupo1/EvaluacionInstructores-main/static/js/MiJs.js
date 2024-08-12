
    function getFecha(){
        const d = new Date();
        let text = d.toString();
        return text;
    }

    function Ir(cual){
        document.forms['mio'].action="/niveles/"+cual
        document.forms['mio'].submit();
     
     
       }function Ir1(cual){
        location.href=cual
       }
        function Confirmar(que,donde){
            if (confirm(que))
              location.href=donde
        }
       function Va(tipo){
        
        if(tipo=="i")
        document.forms['mio'].action="/niveles/i"
        if(tipo=="u"){
         
         document.forms['mio'].action="/niveles/u"   
        }
        
        document.forms['mio'].submit();    
     
       }
       