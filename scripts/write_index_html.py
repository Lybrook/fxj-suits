#!/usr/bin/env python3
content = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="FXJ Suits — Modern Law Firm Management System by Fikia × Jenga Tech" />
    <meta name="theme-color" content="#403301" />
    <link rel="icon" type="image/png" href="/pwa-512x512.png" />
    <title>FXJ Suits | Law Firm Management</title>
    <link rel="manifest" href="/manifest.json" />

    <!-- FXJ Suits Fonts: Inter (UI) + Playfair Display (headings) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">

    <style>
      /* Prevent flash of unstyled content */
      body { background-color: #FDF6DC; }
      #root { min-height: 100vh; }
      /* Spinner keyframe for Login */
      @keyframes spin { to { transform: rotate(360deg); } }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
    <script>
      // Unregister stale service workers
      if (\'serviceWorker\' in navigator) {
        navigator.serviceWorker.getRegistrations().then(registrations => {
          registrations.forEach(reg => {
            if (!reg.active?.scriptURL?.includes(\'sw-custom.js\') && !reg.active?.scriptURL?.includes(\'sw.js\')) {
              reg.unregister();
            }
          });
        });
      }
    </script>
  </body>
</html>
'''

with open("/home/ubuntu/fxj-suits/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("index.html written successfully")
