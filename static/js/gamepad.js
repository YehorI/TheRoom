window.onload = function () {
    var up = document.getElementById('gamepadup');
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === 38) { // note camel casing: keyCode, not KeyCode
            up.submit();
        }
    });
    var right = document.getElementById('gamepadright');
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === 39) {
            right.submit();
        }
    });
    var down = document.getElementById('gamepaddown');
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === 40) {
            down.submit();
        }
    });
    var left = document.getElementById('gamepadleft');
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === 37) {
            left.submit();
        }
    });
 };