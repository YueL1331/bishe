cookie_qcc_did: function (){
    var e = (new Date).getTime();
                return window.performance && "function" == typeof window.performance.now && (e += performance.now()),
                "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (function(t) {
                    var n = (e + 16 * Math.random()) % 16 | 0;
                    return e = Math.floor(e / 16),
                    ("x" === t ? n : 3 & n | 8).toString(16)
                }
                ))
}