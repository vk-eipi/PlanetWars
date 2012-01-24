var Visualizer = {
    canvas: null,
    ctx: null,
    frame: 0,
    playing: false,
    haveDrawnBackground: false,
    frameDrawStarted: null,
    frameDrawEnded: null,
    players: ["Player A", "Player B"],
    planets: [],
    moves: [],
    dirtyRegions: [],
    shipCount: [0, 0, 0],
    growthRate: [0, 0, 0],
    config: {
        planet_font: "bold 15px Arial,Helvetica",
        fleet_font: "normal 12px Arial,Helvetica",
        planet_pixels: [10, 13, 18, 21, 23, 29],
        showFleetText: true,
        display_margin: 30,
        turnsPerSecond: 8,
        teamColor: ["#455", "#c00", "#7ac"],
        teamFleetColor: ["#455", "#a00", "#69b"]
    },
    setup: function (a) {
        this.canvas = document.getElementById("display");
        this.ctx = this.canvas.getContext("2d");
        this.ctx.textAlign = "center";
        this.parseData(a);
        this.config.unit_to_pixel = (this.canvas.height - this.config.display_margin * 2) / 34;
        this.drawFrame(0)
    },
    unitToPixel: function (a) {
        return this.config.unit_to_pixel * a
    },
    drawBackground: function () {
        var a = this.ctx;
        a.fillStyle = "#000";
        if (this.haveDrawnBackground == false) {
            a.fillRect(0, 0, this.canvas.width, this.canvas.height);
            this.haveDrawnBackground = true
        }
        for (var b = 0; b < this.dirtyRegions.length; b++) {
            var c = this.dirtyRegions[b];
            a.fillRect(parseInt(c[0]), parseInt(c[1]), parseInt(c[2]), parseInt(c[3]))
        }
        this.dirtyRegions = []
    },
    drawFrame: function (b) {
        var j = 0,
        h = 0;
        var n = this.ctx;
        var l = Math.floor(b);
        var m = this.moves[l].planets;
        var c = this.moves[l].moving;
        this.drawBackground();
        this.shipCount = [0, 0, 0];
        this.growthRate = [0, 0, 0];
        n.font = this.config.planet_font;
        n.textAlign = "center";
        for (var g = 0; g < this.planets.length; g++) {
            var f = this.planets[g];
            f.owner = m[g].owner;
            f.numShips = m[g].numShips;
            this.shipCount[f.owner] += f.numShips;
            this.growthRate[f.owner] += f.growthRate;
            j = this.unitToPixel(f.x) + this.config.display_margin;
            h = this.unitToPixel(f.y) + this.config.display_margin;
            n.beginPath();
            n.arc(j + 0.5, this.canvas.height - h + 0.5, this.config.planet_pixels[f.growthRate] + 1, 0, Math.PI * 2, true);
            n.closePath();
            n.fillStyle = "#000";
            n.fill();
            n.beginPath();
            n.arc(j, this.canvas.height - h, this.config.planet_pixels[f.growthRate], 0, Math.PI * 2, true);
            n.closePath();
            n.fillStyle = this.config.teamColor[f.owner];
            n.fill();
            n.fillStyle = "#fff";
            n.fillText(f.numShips, j, this.canvas.height - h + 5)
        }
        this.ctx.font = this.config.fleet_font;
        for (var g = 0; g < c.length; g++) {
            var k = c[g];
            this.shipCount[k.owner] += k.numShips;
            var a = (k.progress + 1 + (b - l)) / (k.tripLength + 2);
            k.x = k.source.x + (k.destination.x - k.source.x) * a;
            k.y = k.source.y + (k.destination.y - k.source.y) * a;
            j = this.unitToPixel(k.x) + this.config.display_margin;
            h = this.unitToPixel(k.y) + this.config.display_margin;
            n.fillStyle = this.config.teamFleetColor[k.owner];
            n.beginPath();
            n.save();
            n.translate(j, this.canvas.height - h);
            var e = Math.log(Math.max(k.numShips, 4)) * 0.03;
            n.scale(e, e);
            var d = Math.PI / 2 - Math.atan((k.source.y - k.destination.y) / (k.source.x - k.destination.x));
            if (k.source.x - k.destination.x < 0) {
                d = d - Math.PI
            }
            n.rotate(d);
            n.moveTo(0, -10);
            n.lineTo(40, -30);
            n.lineTo(0, 100);
            n.lineTo(- 40, -30);
            n.closePath();
            n.fill();
            n.strokeStyle = "#fff";
            n.stroke();
            n.restore();
            if (this.config.showFleetText == true) {
                d = -1 * (d + Math.PI / 2);
                j += -11 * Math.cos(d);
                h += -11 * Math.sin(d) - 5;
                n.fillText(k.numShips, j, this.canvas.height - h)
            }
            this.dirtyRegions.push([j - 25, this.canvas.height - h - 35, 50, 50])
        }
        $(this.canvas).trigger("drawn")
    },
    drawChart: function () {
        var a = document.getElementById("chart");
        var m = a.getContext("2d");
        m.scale(1, -1);
        m.translate(0, -a.height);
        var k = 100;
        for (var e = 0; e < this.moves.length; e++) {
            var h = this.moves[e];
            h.shipCount = [0, 0, 0];
            for (var c = 0; c < h.moving.length; c++) {
                var l = h.moving[c];
                h.shipCount[l.owner] += l.numShips
            }
            for (var c = 0; c < h.planets.length; c++) {
                var d = h.planets[c];
                h.shipCount[d.owner] += d.numShips
            }
            for (var c = 0; c < h.shipCount.length; c++) {
                k = Math.max(k, h.shipCount[c])
            }
        }
        var b = a.height / k / 1.05;
        var f = a.width / Math.max(200, this.moves.length);
        for (var e = 1; e <= 2; e++) {
            m.strokeStyle = this.config.teamColor[e];
            m.fillStyle = this.config.teamColor[e];
            m.beginPath();
            m.moveTo(0, this.moves[0].shipCount[e] * b);
            for (var c = 1; c < this.moves.length; c++) {
                var g = this.moves[c].shipCount[e];
                m.lineTo(c * f, g * b)
            }
            m.stroke();
            m.beginPath();
            m.arc((c - 1) * f, g * b, 2, 0, Math.PI * 2, true);
            m.fill()
        }
    },
    start: function () {
        this.playing = true;
        setTimeout(function () {
            Visualizer.run.apply(Visualizer)
        },
        1);
        $("#play-button").html("&#9553;")
    },
    stop: function () {
        this.playing = false;
        $("#play-button").html("&#9654;")
    },
    run: function () {
        if (!this.playing) {
            return
        }
        this.frameDrawStarted = new Date().getTime();
        if (this.frame >= Visualizer.moves.length) {
            this.stop();
            return
        }
        this.drawFrame(this.frame);
        var a = (this.frameDrawStarted - this.frameDrawEnded) / (1000 / this.config.turnsPerSecond);
        if (isNaN(a)) {
            a = 0.3
        }
        this.frame += Math.min(1, Math.max(0.0166, a));
        this.frameDrawEnded = new Date().getTime();
        var b = 1;
        setTimeout(function () {
            Visualizer.run.apply(Visualizer)
        },
        b)
    },
    setFrame: function (b, a) {
        if (a === true) {
            b = Math.floor(b)
        }
        this.frame = Math.max(0, Math.min(this.moves.length - 1, b))
    },
    parseData: function (a) {
        a = a.split(/\n/);
        var f;
        if (a.length == 1) {
            f = a[0]
        } else {
            for (var c = 0; c < a.length; c++) {
                var e = a[c].split("=");
                switch (e[0]) {
                case "player_one":
                    this.players[0] = e[1];
                    break;
                case "player_two":
                    this.players[1] = e[1];
                    break;
                case "playback_string":
                    f = e[1];
                    break
                }
            }
        }
        var f = f.split("|");
        this.planets = f[0].split(":").map(ParserUtils.parsePlanet);
        this.moves.push({
            planets: this.planets.map(function (g) {
                return {
                    owner: parseInt(g.owner),
                    numShips: parseInt(g.numShips)
                }
            }),
            moving: []
        });
        if (f.length < 2) {
            return
        }
        var b = f[1].split(":").slice(0, -1);
        for (var c = 0; c < b.length; c++) {
            var d = b[c].split(",");
            this.moves.push({
                planets: d.slice(0, this.planets.length).map(ParserUtils.parsePlanetState),
                moving: d.slice(this.planets.length).map(ParserUtils.parseFleet)
            })
        }
    },
    _eof: true
};
var ParserUtils = {
    parseFleet: function (a) {
        a = a.split(".");
        return {
            owner: parseInt(a[0]),
            numShips: parseInt(a[1]),
            source: Visualizer.planets[a[2]],
            destination: Visualizer.planets[a[3]],
            tripLength: parseInt(a[4]),
            progress: parseInt(a[4] - a[5])
        }
    },
    parsePlanet: function (a) {
        a = a.split(",");
        return {
            x: parseFloat(a[0]),
            y: parseFloat(a[1]),
            owner: parseInt(a[2]),
            numShips: parseInt(a[3]),
            growthRate: parseInt(a[4])
        }
    },
    parsePlanetState: function (a) {
        a = a.split(".");
        return {
            owner: parseInt(a[0]),
            numShips: parseInt(a[1])
        }
    },
    _eof: true
};
(function (c) {
    Visualizer.setup(data);
    var d = function () {
        if (!Visualizer.playing) {
            if (Visualizer.frame > Visualizer.moves.length - 2) {
                Visualizer.setFrame(0)
            }
            Visualizer.start()
        } else {
            Visualizer.stop()
        }
        return false
    };
    c("#play-button").click(d);
    c("#start-button").click(function () {
        Visualizer.setFrame(0);
        Visualizer.drawFrame(Visualizer.frame);
        Visualizer.stop();
        return false
    });
    c("#end-button").click(function () {
        Visualizer.setFrame(Visualizer.moves.length - 1, true);
        Visualizer.drawFrame(Visualizer.frame);
        Visualizer.stop();
        return false
    });
    var b = function () {
        Visualizer.setFrame(Visualizer.frame - 1, true);
        Visualizer.drawFrame(Visualizer.frame);
        Visualizer.stop();
        return false
    };
    c("#prev-frame-button").click(b);
    var a = function () {
        Visualizer.setFrame(Visualizer.frame + 1);
        Visualizer.drawFrame(Visualizer.frame);
        Visualizer.stop();
        return false
    };
    c("#next-frame-button").click(a);
    c(document.documentElement).keydown(function (e) {
        if (e.keyCode == "37") {
            b();
            return false
        } else {
            if (e.keyCode == "39") {
                a();
                return false
            } else {
                if (e.keyCode == "32") {
                    d();
                    return false
                }
            }
        }
    });
    c("#turnCounter").css("font-size", "20px");
    c("#turnCounter").append("<span id='player1score' style='float:left;width:150px;'>test</span>");
    c("#player1score").css("color", Visualizer.config.teamColor[1]);
    c("#turnCounter").append("<span id='player2score' style='float:right;'>test</span>");
    c("#player2score").css("color", Visualizer.config.teamColor[2]);
    c("#turnCounter").append("<span id='turnText' style=''>test</span>");
    c("#display").bind("drawn",
    function () {
        var e = Visualizer.frame;
        c("#turnText").html("Turn: " + Math.floor(Visualizer.frame + 1) + " of " + Visualizer.moves.length);
        c("#player1score").text("(" + Visualizer.shipCount[1] + "/" + Visualizer.growthRate[1] + ")");
        c("#player2score").text("(" + Visualizer.shipCount[2] + "/" + Visualizer.growthRate[2] + ")")
    });
    c(".player1Name").text(Visualizer.players[0]);
    c(".player1Name").css("color", Visualizer.config.teamColor[1]);
    c(".player2Name").text(Visualizer.players[1]);
    c(".player2Name").css("color", Visualizer.config.teamColor[2]);
    c(".playerVs").text("v.s.");
    c("title").text(Visualizer.players[0] + " v.s. " + Visualizer.players[1] + " - Planet Wars");
    Visualizer.start();
    Visualizer.drawChart()
})(window.jQuery);
