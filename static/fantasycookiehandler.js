function getPlayersInCookie(cookie_name) {
        var value = getCookie(cookie_name)
        return (value === "") ? [] : JSON.parse(value)
    }
function savePlayerInCookie(id, cookie_name) {
    var cookies = getCookie(cookie_name)
    var json = {}

    // var inner = {}
    // inner["id"] = id
    // inner["name"] = name

    var newProspects = (cookies == "") ? [] : JSON.parse(cookies)
    var position = newProspects.findIndex(item => {
        return item === id
    })
    if ( position == -1  ) newProspects.push(id)

    json = newProspects
    setCookie(cookie_name, JSON.stringify(json))
}

function removePlayerInCookie(id, cookie_name) {
    var cookies = getCookie(cookie_name)
    var json = {}
    var newProspects = (cookies == "") ? [] : JSON.parse(cookies)
    var position = newProspects.findIndex(item => {
        return item === id
    })
    if ( position != -1  ) newProspects.splice(position, 1)

    json = newProspects
    setCookie(cookie_name, JSON.stringify(json))
}
function addFavoritePlayerById(id) {
    cookie_name = "favorite_fantasy_player"
    console.log(`${id} ${cookie_name}`)

    button = document.getElementById("star_button_" + id.toString())
    if (button.classList.contains('active')) {
        removePlayerInCookie(id, cookie_name)
        // button.classList.remove("active")
    }
    else {
        savePlayerInCookie(id, cookie_name)
        // button.classList.add("active")
    }
}
function addWatchListPlayerById(id) {
    cookie_name = "watchlist_fantasy_player"
    console.log(`${id} ${cookie_name}`)

    button = document.getElementById("glass_button_" + id.toString())
    if (button.classList.contains('active')) {
        removePlayerInCookie(id, cookie_name)
        // button.classList.remove("active")
    }
    else {
        savePlayerInCookie(id, cookie_name)
        // button.classList.add("active")
    }
}

function addDraftBoardListPlayerById (id) {
    cookie_name = "draftboard_fantasy_player"
    console.log(`${id} ${cookie_name}`)

    button = document.getElementById("check_button_" + id.toString())
    if (button.classList.contains('active')) {
        removePlayerInCookie(id, cookie_name)
        // button.classList.remove("active")
    }
    else {
        savePlayerInCookie(id, cookie_name)
        // button.classList.add("active")
    }
}

function moveUpPlayerInCookie(playerId1, playerId2, cookie_name) {

    var cookies = getCookie(cookie_name)
    var json = {}
    var newProspects = (cookies == "") ? [] : JSON.parse(cookies)

    var playerId1_position = newProspects.indexOf(parseInt(playerId1))
    var playerId2_position = newProspects.indexOf(parseInt(playerId2))

    if (playerId2_position >= 0 && playerId2_position >= 0) {
       // remove playerId1
       newProspects.splice(playerId1_position, 1)
       // move playerId1 above playerId2
       newProspects.splice(playerId2_position, 0, parseInt(playerId1));
    }

    json = newProspects
    setCookie(cookie_name, JSON.stringify(json))
}