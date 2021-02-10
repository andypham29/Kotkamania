function setCookie(name,value,days = 365) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
            c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    function eraseCookie(name) {   
        document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }

    function getProspectsInCookie() {
        var value = getCookie('prospects')
        return (value == "") ? [] : JSON.parse(value).prospects
    }

    function savePlayerInCookie1(id, name, cookie_name) {
        var cookies = getCookie(cookie_name)
        var json = {}

        var inner = {}
        inner["id"] = id
        inner["name"] = name
        
        var newProspects = (cookies == "") ? [] : JSON.parse(cookies).prospects
        var position = newProspects.findIndex(obj => {
            return obj.id === id
        })
        if ( position == -1  ) newProspects.push(inner)

        json[cookie_name] = newProspects
        setCookie(cookie_name, JSON.stringify(json))
    }

    function removePlayerInCookie1(id, cookie_name) {
        var cookies = getCookie(cookie_name)
        var json = {}
        var newProspects = (cookies == "") ? [] : JSON.parse(cookies).prospects
        var position = newProspects.findIndex(obj => {
            return obj.id === id
        })
        if ( position != -1  ) newProspects.splice(position, 1)
        
        json[cookie_name] = newProspects
        setCookie(cookie_name, JSON.stringify(json))
    }