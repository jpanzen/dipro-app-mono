# Systém pro komunikaci a vizualizaci sériové linky

Tato aplikace zobrazuje data měřená ze sériové linky v interaktivní formě v rámci webové aplikace.

Webový server je postaven na frameworku Flask, frontend je obyčejné HTML s JavaScriptem, chart.js, luxon a socketio pro komunikaci mezi serverem a klientem.

Pro využití pro Vás experiment můžete použít bare-bones verzi z main branche, ta však nezahrnuje komunikaci od klient-> server, ale pouze server->klient, protože se styl komunikace může lišit v závislosti na tom, jak chcete data posílat.

Nicméně pro inspiraci, jak komunikaci provést se doporučuji podívat do jednoho z branchů otestované na reálných experimentech, svetelne-prvky či trafo

## Instalace závislostí

1. **Instalace Pythonu:** Pokud ještě nemáte nainstalovaný Python, stáhněte a nainstalujte ho z [Python.org](https://www.python.org/downloads/).
2. **Instalace node.js:** Pokud ještě nemáte nainstalovaný node.js, stáhněte a nainstalujte ho z [Nodejs.org](https://nodejs.org/en/).
3. **Instalace python závislostí pomocí pip:**
Otevřete příkazový řádek/terminál a spusťte následující příkazy:
```
pip install Flask 
pip install python-socketio
```
4. **Instalace python závislostí pomocí npm install:**
Otevřete příkazový řádek/terminál a spusťte následující příkaz:
```
npm install
```
5. **Ujistěte se, že máte správně nastaven COM a baudrate v app.py:**
Máte-li v aplikaci error, že k souboru COM nemáte oprávnění, pravděpodobně máte špatně nastavený komunikační kanál sériové linky.
Čte-li backend data experimentu ve zvláštním formátu, anebo je nečte vůbec, pravděpodobně máte problém se špatnou hodnotou baudRate.
6. **Ujistěte se, že data zasíláte přes sériovou linku ve správném formátu:**
Obecně funkční formát dat je "hodnotax,hodnotay,hodnotaz,hodnota..."
Popřípadě si můžete v app.py nastavit vlastní způsob parsování dat, defaultní je však tento.
7. **Upravte legendu chart.js:**
Přizpůsobte legendu Vašemu use-case
8. **Spusťte aplikaci**
```
py app.py
```
9. **Úprava Tailwindcss tříd:**
Máte-li jakékoliv CSS úpravy neprojevující se v rozhraní aplikace, tak spusťte kontinuální buildování Tailwindu v separátním terminále.
```
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
```
