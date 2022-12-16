
export class Canvas {
    points = [];
    path = [];
    canvas = HTMLCanvasElement;

    constructor(canvas, points=[], path=[]) {
        this.canvas = canvas;
        this.points = points;
        this.path = path;

        addEventListener("resize", ()=>{this.renderCanvas()});
        this.renderCanvas();
    }

    drawPoint(point) {
        let context = this.canvas.getContext('2d')
        context.beginPath();
        let rect = this.canvas.getBoundingClientRect();
        context.arc(point.x * rect.width, point.y * rect.height, 5, 0, 2 * Math.PI);
        context.fill()
        context.stroke()
    }

    drawPath() {
        if (this.path.length === 0)
            return;

        let context = this.canvas.getContext('2d');
        context.beginPath();
        let rect = this.canvas.getBoundingClientRect();

        context.moveTo(this.path[0].x * rect.width, this.path[0].y * rect.height);

        this.path.forEach(point => {
            context.lineTo(point.x * rect.width, point.y * rect.height);
        });
        context.stroke();

    }
    getRealPoints() {
        let rect = this.canvas.getBoundingClientRect();
        let result = [];
        this.points.forEach(point => {
            result.push({"x": point.x * rect.width, "y": point.y * rect.height});
        });
        console.log(this.points);
        console.log(result);
        return result;
    }

    renderCanvas() {
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;

        if(this.points.length !== 0)
            this.points.forEach(point => {this.drawPoint(point);});
        else if(this.path.length !== 0)
            this.path.forEach(point => {this.drawPoint(point);});

        this.drawPath();
    }
    addPoint(new_point) {
        const rect = this.canvas.getBoundingClientRect();
        const x = new_point.x - rect.left
        const y = new_point.y - rect.top

        const point = {"x": x / rect.width, "y": y / rect.height}
        this.points.push(point)
        this.drawPoint(point);
    }

    addPathPoint(new_point, at_start=false) {
        const rect = this.canvas.getBoundingClientRect();

        const point = {"x": new_point.x / rect.width, "y": new_point.y / rect.height}
        if(at_start)
            this.path = [point, ...this.path];
        else
            this.path.push(point);

        this.renderCanvas();
    }
    setPath(path = []) {
        this.path = path;
        this.renderCanvas();
    }
    clearPath() {
        this.setPath([]);
    }
    clear() {
        this.points = []
        this.path = []
        const context = this.canvas.getContext('2d');
        context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}
