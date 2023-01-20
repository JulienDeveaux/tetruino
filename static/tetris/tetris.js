document.addEventListener("DOMContentLoaded", () =>
{
    const canvas = document.createElement("canvas");

    const screenHeight = window.innerHeight - 28*2;

    canvas.setAttribute("width", (screenHeight)+"px");
    canvas.setAttribute("height", screenHeight + "px");

    document.getElementById("tetrisDiv").appendChild(canvas);
    const ctx  = canvas.getContext('2d');

    const tetrisRender = new TetrisRender(ctx, screenHeight * 0.6, screenHeight * 0.4);

    const socket = new WebSocket('ws://' + location.host + '/ws-game');

    socket.addEventListener('message', ev => {
        const data = JSON.parse(ev.data);

        tetrisRender.render(data);
    });

    /* for test in dev */
    if(isDev)
    {
        document.body.addEventListener("keypress", (e) =>
        {
            console.log(e.key);
           if(e.key == "q")
                fetch("/commande/" + 2);
           else if(e.key == "z")
                fetch("/commande/" + 0);
           else if(e.key == "s")
                fetch("/commande/" + 1);
           else if(e.key == "d")
                fetch("/commande/" + 3);
           else if (e.key == "r")
               fetch("/commande/" + 5);
           else if (e.key == "p")
               fetch("/commande/" + 4);
        });
    }
}, false);