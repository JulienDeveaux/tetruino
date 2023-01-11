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
            console.log("Tetris getStatus : perdu !!!");

            this.ctx.strokeText("Perdu!", this.width/2- this.ctx.measureText("Perdu!").width/2, this.height/3);
        }

        this.ctx.strokeRect(0, 0, this.width, this.height);
    }

    #drawBlock(x, y)
    {
        this.ctx.fillRect(this.block_w * x, this.block_h * y, this.block_w - 1, this.block_h - 1);
        this.ctx.strokeRect(this.block_w * x, this.block_h * y, this.block_w - 1, this.block_h - 1);
    }
}