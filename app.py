<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mercator Oblique - Minimaliste</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://unpkg.com/topojson@3"></script>
    <style>
        body { margin: 0; background: #020617; color: white; font-family: sans-serif; overflow: hidden; }
        
        /* Fenêtre Globe (Pilote) */
        #globe-container {
            position: absolute; top: 20px; left: 20px;
            width: 200px; height: 200px;
            border: 2px solid #38bdf8; border-radius: 50%;
            background: #000; z-index: 10; overflow: hidden;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }

        /* Aide et Stats */
        #info {
            position: absolute; bottom: 20px; left: 20px;
            background: rgba(15, 23, 42, 0.85); padding: 15px;
            border-radius: 8px; border: 1px solid #1e293b; z-index: 10;
            font-size: 0.8rem; line-height: 1.5;
        }
        .highlight { color: #38bdf8; font-weight: bold; }

        canvas { display: block; }
        #map-canvas { position: absolute; top: 0; right: 0; }
    </style>
</head>
<body>

<div id="globe-container">
    <canvas id="globe-canvas" width="200" height="200"></canvas>
</div>

<div id="info">
    <div id="stats" class="highlight" style="margin-bottom: 10px;">LONG: 0° | LAT: 0° | ROLL: 0°</div>
    <b>CONTRÔLES CLAVIER :</b><br>
    • <kbd>←</kbd> <kbd>→</kbd> : Rotation Axe Polaire (Long.)<br>
    • <kbd>↑</kbd> <kbd>↓</kbd> : Rotation Axe Greenwich (Lat.)<br>
    • <kbd>A</kbd> / <kbd>E</kbd> : Rotation Axe Orthogonal (Roll)<br>
    • <kbd>+</kbd> / <kbd>-</kbd> : Zoom
</div>

<canvas id="map-canvas"></canvas>

<script>
    const gCanvas = d3.select("#globe-canvas");
    const gCtx = gCanvas.node().getContext("2d");
    const mCanvas = d3.select("#map-canvas");
    const mCtx = mCanvas.node().getContext("2d");

    let worldData = null;
    let rotation = [0, 0, 0]; // [λ, φ, γ]
    let scale = 250;

    const projG = d3.geoOrthographic().clipAngle(90).scale(98).translate([100, 100]);
    const projM = d3.geoMercator();

    const pathG = d3.geoPath(projG, gCtx);
    const pathM = d3.geoPath(projM, mCtx);

    // Chargement des données
    d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(data => {
        worldData = topojson.feature(data, data.objects.countries);
        resize();
        render();
    });

    function render() {
        if (!worldData) return;
        const w = window.innerWidth, h = window.innerHeight;

        // 1. Rendu du Globe (Pilote)
        projG.rotate(rotation);
        gCtx.clearRect(0, 0, 200, 200);
        
        // Fond mer
        gCtx.beginPath(); gCtx.arc(100, 100, 98, 0, Math.PI * 2);
        gCtx.fillStyle = "#0f172a"; gCtx.fill();
        
        drawLayers(gCtx, pathG, false);

        // 2. Rendu Mercator (Résultat)
        // La projection est centrée sur le point visualisé par le globe
        projM.scale(scale).translate([w/2, h/2]).rotate(rotation);
        
        mCtx.clearRect(0, 0, w, h);
        mCtx.fillStyle = "#020617"; mCtx.fillRect(0, 0, w, h);
        
        drawLayers(mCtx, pathM, true);

        // Mise à jour stats
        d3.select("#stats").text(`LON: ${(-rotation[0]).toFixed(1)}° | LAT: ${(-rotation[1]).toFixed(1)}° | ROLL: ${rotation[2].toFixed(1)}°`);
    }

    function drawLayers(ctx, pathGen, isMain) {
        // Grille
        ctx.beginPath(); pathGen(d3.geoGraticule()());
        ctx.strokeStyle = "rgba(255,255,255,0.05)"; ctx.lineWidth = 0.5; ctx.stroke();

        // Pays
        ctx.beginPath(); pathGen(worldData);
        ctx.fillStyle = "#1e293b"; ctx.fill();
        ctx.strokeStyle = "#334155"; ctx.lineWidth = isMain ? 1 : 0.5; ctx.stroke();

        // Repères (Équateur et Tropiques)
        ctx.setLineDash([]);
        ctx.beginPath(); ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 2;
        pathGen({type: "LineString", coordinates: [[-180, 0], [180, 0]]}); ctx.stroke(); // Equateur

        ctx.beginPath(); ctx.strokeStyle = "#fb923c"; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
        pathGen({type: "LineString", coordinates: [[-180, 23.4], [180, 23.4]]}); ctx.stroke();
        pathGen({type: "LineString", coordinates: [[-180, -23.4], [180, -23.4]]}); ctx.stroke();
        ctx.setLineDash([]);
    }

    // Gestion du clavier
    window.addEventListener("keydown", e => {
        const step = 5;
        switch(e.key) {
            case "ArrowLeft":  rotation[0] -= step; break;
            case "ArrowRight": rotation[0] += step; break;
            case "ArrowUp":    rotation[1] += step; break;
            case "ArrowDown":  rotation[1] -= step; break;
            case "a": case "A": rotation[2] -= step; break;
            case "e": case "E": rotation[2] += step; break;
            case "+": scale *= 1.1; break;
            case "-": scale *= 0.9; break;
        }
        render();
    });

    function resize() {
        mCanvas.attr("width", window.innerWidth).attr("height", window.innerHeight);
        render();
    }

    window.addEventListener("resize", resize);
</script>
</body>
</html>
