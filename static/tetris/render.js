class TetrisRender
{
    /**
     * @param {CanvasRenderingContext2D} ctx
     * @param rows
     * @param cols
     */
    constructor(ctx, rows = 20, cols = 10)
    {
        this.colors = ['cyan', 'orange', 'blue', 'yellow', 'red', 'green', 'purple'];

        this.width = ctx.canvas.width;
        this.height = ctx.canvas.height;

        this.block_h = this.height / rows;
        this.block_w = this.width / cols;

        this.ctx = ctx;
        this.cols = cols;
        this.rows = rows;

        console.log({
            width: this.width,
            height: this.height,
            block_h: this.block_h,
            block_w: this.block_w,
            cols: this.cols,
            rows: this.rows
        })
    }

    /**
     * @param {{isGameover: boolean, score: number, isPaused: boolean, titles: [], current: {tetromino: [], type: number, rotation: number}, currentCoord: []}} data
     */
    render(data)
    {
        const board = data.titles;

        this.ctx.clearRect(0, 0, this.width, this.height);
        this.ctx.strokeStyle = 'black';

        for (let x = 0; x < this.cols; ++x) {
            for (let y = 0; y < this.rows; ++y) {
                if (board[y][x]) {
                    this.ctx.fillStyle = this.colors[board[y][x] - 1];
                    this.#drawBlock(x, y);
                }
            }
        }

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

        if (data.isGameover === true)
        {
            this.#drawMessage("Perdu !", "red", 30);
        }
        else if(data.isPaused)
        {
            this.#drawMessage("Jeu en pause", "cyan", 30);
        }

        this.ctx.strokeRect(0, 0, this.width, this.height);
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