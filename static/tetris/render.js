class TetrisRender
{
    /**
     * @param {CanvasRenderingContext2D} ctx
     * @param confettiCanvas
     * @param {number} canvasWidth largeur de dessin du canvas (< taille réelle)
     * @param {number} textWidth largeur pour le dessin du text
     * @param rows
     * @param cols
     */
    constructor(ctx, confettiCanvas, canvasWidth, textWidth, rows = 20, cols = 10)
    {
        this.colors = ['cyan', 'orange', 'blue', 'yellow', 'red', 'green', 'purple'];

        this.width = ctx.canvas.width < canvasWidth ? ctx.canvas.width * 0.9 : canvasWidth;
        this.height = ctx.canvas.height;

        this.block_h = this.height / rows;
        this.block_w = this.width / cols;

        this.ctx = ctx;
        this.cols = cols;
        this.rows = rows;
        this.textWidth = this.width + textWidth < ctx.canvas.width ? textWidth : ctx.canvas.width * 0.1;

        this.jsConfetti = new JSConfetti({ confettiCanvas });
    }

    /**
     * @param {{isGameover: boolean, score: number, isPaused: boolean, titles: [], current: {tetromino: [], type: number, rotation: number}, currentCoord: [], nexts: []}} data
     */
    render(data)
    {
        const board = data.titles;

        this.ctx.clearRect(0, 0, this.width + this.textWidth, this.height);
        this.ctx.strokeStyle = 'black';

        this.ctx.fillStyle = "rgba(255,255,255,0.81)"
        this.ctx.fillRect(this.width, 0, this.textWidth, this.height);

        for (let x = 0; x < this.cols; ++x) {
            for (let y = 0; y < this.rows; ++y) {
                if (board[y][x]) {
                    this.ctx.fillStyle = this.colors[board[y][x] - 1];
                    this.#drawBlock(x, y);
                }
            }
        }

        if(data.current)
        {
            for ( let y = 0; y < 4; ++y )
            {
                for ( let x = 0; x < 4; ++x )
                {
                    if ( data.current.tetromino[ y ][ x ] )
                    {
                        this.ctx.fillStyle = this.colors[ data.current.tetromino[ y ][ x ] - 1 ];
                        this.#drawBlock( data.currentCoord[0] + x, data.currentCoord[1] + y );
                    }
                }
            }
        }

        if (data.isGameover === true)
        {
            this.#drawMessage("Perdu !", "red", 30);
            this.jsConfetti.addConfetti({
                emojis: ['😭', '🪦', '☠️ ', '😢', '🥷', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧', '⚰️', '😱', '🤧',
                    '😭', '🪦', '☠️ ', '😢', '⚰️', '😱', '🤧'],
                confettiNumber: 2,
                confettiRadius: 1
            });
        }
        else if(data.isPaused)
        {
            this.#drawMessage("Jeu en pause", "cyan", 30);
        }

        if(data.score !== undefined)
        {
            const str = "score: " + data.score;
            if(data.boardCleared === true)
                this.jsConfetti.addConfetti();
            this.ctx.font = this.ctx.font.replace(/\d+px/, 12 + "px");

            const textSize = this.ctx.measureText(str);

            this.ctx.fillStyle = "black";
            this.ctx.fillText(str, this.width + (this.textWidth/2-textSize.width/2), this.height - 15);
        }

        if(data.nexts)
        {
            let str = "Prochain:";

            this.ctx.font = this.ctx.font.replace(/\d+px/, 12 + "px");

            const textSize = this.ctx.measureText(str);

            this.ctx.fillStyle = "black";
            this.ctx.fillText(str, this.width + (this.textWidth/2-textSize.width/2), 15);

            for (let i = 0; i < data.nexts.length; i++)
            {
                const next = data.nexts[i].tetromino;

                const widthNext = this.textWidth / next.length - 5;

                for ( let y = 0; y < 4; ++y )
                {
                    for ( let x = 0; x < 4; ++x )
                    {
                        if ( next[ y ][ x ] )
                        {
                            this.ctx.fillStyle = this.colors[ next[ y ][ x ] - 1 ];

                            this.ctx.fillRect((this.width + 5 ) + (widthNext*x), (15 + textSize.actualBoundingBoxDescent + textSize.actualBoundingBoxAscent) + (widthNext* y) + (widthNext*4 + 5) * i, widthNext - 1, widthNext - 1);
                            this.ctx.strokeRect((this.width + 5 ) + (widthNext*x), (15 + textSize.actualBoundingBoxDescent + textSize.actualBoundingBoxAscent) + (widthNext* y) + (widthNext*4 + 5) * i, widthNext, widthNext);
                        }
                    }
                }

                if(i < data.nexts.length-1)
                    this.ctx.setLineDash([7.5]);
                this.ctx.strokeRect(this.width, (15 + textSize.actualBoundingBoxDescent + textSize.actualBoundingBoxAscent) + (widthNext* 4) + (widthNext*4 + 5) * i + 2.5, this.textWidth, 0);
                this.ctx.setLineDash([]);
            }
        }

        this.ctx.strokeRect(0, 0, this.width, this.height);
        this.ctx.strokeRect(0, 0, this.width + this.textWidth, this.height);
    }

    /**
     * @param {number} x
     * @param {number} y
     */
    #drawBlock(x, y)
    {
        this.ctx.fillRect(this.block_w * x, this.block_h * y, this.block_w - 1, this.block_h - 1);
        this.ctx.strokeRect(this.block_w * x, this.block_h * y, this.block_w - 1, this.block_h - 1);
    }

    /**
     * @param {string} txt
     * @param {string | CanvasGradient | CanvasPattern} fillColor
     * @param {number | undefined} size
     */
    #drawMessage(txt, fillColor = "cyan", size= undefined)
    {
        const oldFill = this.ctx.fillStyle;
        const oldSize = this.ctx.font;

        this.ctx.fillStyle = fillColor;

        if(size)
            this.ctx.font = this.ctx.font.replace(/\d+px/, size + "px");

        const txtDim = this.ctx.measureText(txt);
        const x = this.width/2 - txtDim.width/2;
        const y = this.height/3;
        const txtHeigth = (txtDim.actualBoundingBoxDescent + txtDim.actualBoundingBoxAscent);

        this.ctx.fillRect(x - 10, y - txtHeigth - 5, txtDim.width + 15, txtHeigth + 15)
        this.ctx.strokeRect(x - 10, y - txtHeigth - 5, txtDim.width + 15, txtHeigth + 15)
        this.ctx.fillStyle = "black";
        this.ctx.fillText(txt, x, y);
        this.ctx.fillStyle = oldFill;
        this.ctx.font = oldSize;

    }
}