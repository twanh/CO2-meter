# CO2 Meter

> Keep track of the values of the CO2 meter that is placed in all the classrooms @ school.

## Requirements:

- Periodicly check the value's of the sensor
- Store the value's of the sensor
- Export the values to an excel sheet
- View graphs about the data (data visualization)

## Installation:

- Install PIP dependencies
  - `pip install -r requirements.txt`
- Download Chrome Webdriver from: https://chromedriver.chromium.org/
  - Note: Make sure the webdriver matches your chrome version
  - Place `chromedriver.exe` in the `webdriver` folder.
- Run with `python main.py`

# Notes:

- Sensor url: https://pulse.strukton.com/comfortsensor/7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a
- Use the xlink:href attribute to get the values
- document.getElementById("idTempValue1") returns the element with the xlink:href on it (for the first value)

## Element IDS:

- Temperature:
  - idTempValue1
  - idTempValue2
- Humidity (luchvochtigheid)
  - idHumValue1
  - idHumValue2
- Air Qualitity (Luch Kwaliteit)
  - idCooValue1
  - idCooValue2
  - idCooValue3
  - idCooValue4

## Iframe Source:

```html
<html lang="nl">
  <head>
    <meta charset="utf-8" />

    <title>Strukton Environment Indicator</title>
    <meta name="description" content="Strukton Environment Indicator" />
    <meta name="author" content="FactoryLab" />
    <meta http-equiv="cache-control" content="no-store" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  </head>
  <body
    style="height:1912px;overflow:scroll;"
    onload="setValues('7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a',4,4,'17',1,'39',1,'503')"
  >
    <object
      type="image/svg+xml"
      id="sei"
      data="./strukt1.svg"
      style="margin:auto;width:100%;height:100%;"
    ></object>
    <script type="text/javascript">
      var svgdoc;
      indicators = [
        "#symb-letterA",
        "#symb-letterB",
        "#symb-letterC",
        "#symb-letterD",
      ];
      values = [
        "#symb-digit0",
        "#symb-digit1",
        "#symb-digit2",
        "#symb-digit3",
        "#symb-digit4",
        "#symb-digit5",
        "#symb-digit6",
        "#symb-digit7",
        "#symb-digit8",
        "#symb-digit9",
      ];
      dvalues = [
        "#symb-ddigit0",
        "#symb-ddigit1",
        "#symb-ddigit2",
        "#symb-ddigit3",
        "#symb-ddigit4",
        "#symb-ddigit5",
        "#symb-ddigit6",
        "#symb-ddigit7",
        "#symb-ddigit8",
        "#symb-ddigit9",
      ];

      function setDateTime(datetimesting) {
        i = 0;
        for (; i < datetimesting.length; i++) {
          digit = datetimesting.substr(i, 1);
          svgdoc
            .getElementById("idDT" + i.toString())
            .setAttribute("xlink:href", dvalues[parseInt(digit)]);
        }
      }

      function setWidget(idIndicator, indicator, value, vids) {
        svgdoc
          .getElementById(idIndicator)
          .setAttribute("xlink:href", indicators[indicator - 1]);

        i = 0;
        for (; i < vids.length; i++) {
          digit = value.substr(i, 1);
          if (digit != "") {
            svgdoc
              .getElementById(vids[i])
              .setAttribute("xlink:href", values[parseInt(digit)]);
          } else {
            svgdoc.getElementById(vids[i]).setAttribute("xlink:href", "");
          }
        }
      }

      function setValues(uuid, atime, itemp, vtemp, ihum, vhum, ico, vco) {
        var svg = document.getElementById("sei");
        svgdoc = svg.contentDocument;
        setWidget("idIndicatorTemp", itemp, vtemp, [
          "idTempValue1",
          "idTempValue2",
        ]);
        setWidget("idIndicatorHum", ihum, vhum, ["idHumValue1", "idHumValue2"]);
        setWidget("idIndicatorCoo", ico, vco, [
          "idCooValue1",
          "idCooValue2",
          "idCooValue3",
          "idCooValue4",
        ]);

        svgdoc
          .getElementById("refreshUrl")
          .addEventListener("click", function () {
            location.reload();
          });
        svgdoc
          .getElementById("refreshUrl")
          .setAttribute(
            "xlink:href",
            "https://pulse.strukton.com/comfortsensor/" + uuid
          );

        var timenow = new Date();
        timenow.setMinutes(timenow.getMinutes() - atime);

        day =
          timenow.getDate() < 10 ? "0" + timenow.getDate() : timenow.getDate();
        month =
          timenow.getMonth() < 9
            ? "0" + (timenow.getMonth() + 1)
            : timenow.getMonth() + 1;
        timehour =
          timenow.getHours() < 10
            ? "0" + timenow.getHours()
            : timenow.getHours();
        timeminutes =
          timenow.getMinutes() < 10
            ? "0" + timenow.getMinutes()
            : timenow.getMinutes();

        setDateTime(
          day.toString() +
            month.toString() +
            timenow.getFullYear().toString() +
            timehour.toString() +
            timeminutes.toString()
        );
      }
    </script>
  </body>
</html>
```

## Window Onload:

```html
<body
  style="height:1912px;overflow:scroll;"
  onload="setValues('7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a',1,4,'17',1,'39',1,'509')"
></body>
```

The `onload` attribute contains the actual values.

THe `setValues` function signature

```javascript
function setValues(uuid,atime,itemp, vtemp, ihum, vhum, ico, vco)
```

### Function arguments:

- `uuid`: The id of the sensor
- `atime`: Unkown?
- `itemp`: Probably the icon to use for the temperature
- `vtemp`: The actual temperature (as string)
- `ihum`: Probably the icon to use for the humidity
- `vhum`: The actual humidity (value --> `v`)
- `ico`: Probably the icon to use for the air quality
- `vco`: The actual air quality value (ppm)

Note: `v` is the prefix for a value and `i` is the prefix for an icon (number)

### Icon Numberings:

```javascript
indicators = [
  "#symb-letterA",
  "#symb-letterB",
  "#symb-letterC",
  "#symb-letterD",
];
```

- A ('Zeer goed'): `symb-letterA` with index `0`
- B ('Goed'): `symb-letterB` with index `1`
- C ('Acceptabel'): `symb-letterC` with index `2`
- D ('Onacceptabel'): `symb-letterD` with index `3`

## SVG Number Paths:

```svg
<svg xmlns="http://www.w3.org/2000/svg">

<!-- 1 id="symb-digit1" -->
<!-- <path fill="#696C7D" d="M 1 26 v -4.76 H 6.52 V 6.56 H 1.76 v -3.64 c 1.387 -0.267 2.56 -0.587 3.52 -0.96 c 0.96 -0.373 1.893 -0.827 2.8 -1.36 H 12.4 V 21.24 h 4.76 v 4.76z"/> -->
<!-- 2 id="symb-digit2" -->
      <!-- <path fill="#696C7D" d="M 0.28 25.88 V 22.52 C 1.907 21 3.387 19.587 4.72 18.28 C 6.08 16.947 7.24 15.707 8.2 14.56 C 9.187 13.387 9.947 12.307 10.48 11.32 C 11.04 10.307 11.32 9.347 11.32 8.44 C 11.32 7.187 11 6.24 10.36 5.6 C 9.72 4.933 8.84 4.6 7.72 4.6 C 6.787 4.6 5.96 4.867 5.24 5.4 C 4.52 5.907 3.84 6.507 3.2 7.2 L 0 4.04 C 1.254 2.707 2.534 1.707 3.84 1.04 C 5.147 0.347 6.707 0 8.52 0 C 9.774 0 10.907 0.2 11.92 0.6 C 12.96 0.973 13.854 1.52 14.6 2.24 C 15.347 2.933 15.92 3.773 16.32 4.76 C 16.72 5.747 16.92 6.853 16.92 8.08 C 16.92 9.147 16.694 10.24 16.24 11.36 C 15.787 12.453 15.174 13.56 14.4 14.68 C 13.654 15.773 12.787 16.88 11.8 18 C 10.84 19.093 9.84 20.173 8.8 21.24 C 9.44 21.16 10.147 21.093 10.92 21.04 C 11.72 20.96 12.427 20.92 13.04 20.92 H 18.16 V 25.88 H 0.28z"/> -->
<!-- 3 id="symb-digit3" -->
<!-- <path fill="#696C7D" d="M 9 26.4 C 6.92 26.4 5.16 26.08 3.72 25.44 C 2.28 24.773 1.093 23.893 0.16 22.8 L 2.88 19.08 C 3.653 19.827 4.493 20.44 5.4 20.92 C 6.333 21.4 7.347 21.64 8.44 21.64 C 9.693 21.64 10.693 21.387 11.44 20.88 C 12.187 20.347 12.56 19.6 12.56 18.64 C 12.56 18.08 12.453 17.573 12.24 17.12 C 12.053 16.667 11.707 16.293 11.2 16 C 10.693 15.68 10 15.44 9.12 15.28 C 8.24 15.093 7.107 15 5.72 15 V 10.84 C 6.867 10.84 7.813 10.76 8.56 10.6 C 9.333 10.44 9.947 10.213 10.4 9.92 C 10.88 9.6 11.213 9.24 11.4 8.84 C 11.613 8.413 11.72 7.947 11.72 7.44 C 11.72 6.56 11.453 5.88 10.92 5.4 C 10.387 4.893 9.613 4.64 8.6 4.64 C 7.693 4.64 6.867 4.84 6.12 5.24 C 5.4 5.64 4.64 6.187 3.84 6.88 L 0.88 3.28 C 2.053 2.267 3.28 1.48 4.56 0.92 C 5.867 0.333 7.307 0.04 8.88 0.04 C 10.187 0.04 11.373 0.2 12.44 0.52 C 13.533 0.813 14.453 1.267 15.2 1.88 C 15.973 2.467 16.573 3.187 17 4.04 C 17.427 4.893 17.64 5.88 17.64 7 C 17.64 8.333 17.267 9.467 16.52 10.4 C 15.8 11.307 14.76 12.053 13.4 12.64 V 12.8 C 14.867 13.227 16.067 13.96 17 15 C 17.96 16.013 18.44 17.347 18.44 19 C 18.44 20.173 18.187 21.227 17.68 22.16 C 17.173 23.067 16.493 23.84 15.64 24.48 C 14.787 25.093 13.787 25.573 12.64 25.92 C 11.493 26.24 10.28 26.4 9 26.4z"/> -->
<!-- 4 id="symb-digit4" -->
<!-- <path fill="#696C7D" d="M 11 26 V 19.92 H 0 V 15.88 L 9.28 0.6 H 16.48 V 15.44 H 19.4 V 19.92 H 16.48 V 26 H 11 z M 5.64 15.44 H 11 V 11.32 C 11 10.493 11.027 9.547 11.08 8.48 C 11.133 7.387 11.187 6.44 11.24 5.64 H 11.08 C 10.76 6.333 10.427 7.04 10.08 7.76 C 9.733 8.48 9.373 9.2 9 9.92 L 5.64 15.44z"/>
 --><!-- 5 id="symb-digit5" -->
<!--  <path fill="#696C7D" d="M 8.96 26 C 6.88 26 5.12 25.667 3.68 25 C 2.24 24.307 1.013 23.453 0 22.44 L 2.64 18.72 C 3.413 19.413 4.24 20.013 5.12 20.52 C 6.027 21 7.027 21.24 8.12 21.24 C 9.427 21.24 10.467 20.907 11.24 20.24 C 12.013 19.573 12.4 18.587 12.4 17.28 C 12.4 16 12.027 15.027 11.28 14.36 C 10.56 13.693 9.6 13.36 8.4 13.36 C 8.027 13.36 7.693 13.387 7.4 13.44 C 7.107 13.467 6.813 13.533 6.52 13.64 C 6.253 13.747 5.96 13.88 5.64 14.04 C 5.347 14.2 5.013 14.4 4.64 14.64 L 2 12.96 L 2.72 0.12 H 17.12 V 5.08 H 7.8 L 7.36 9.84 C 7.84 9.627 8.293 9.48 8.72 9.4 C 9.173 9.293 9.667 9.24 10.2 9.24 C 11.293 9.24 12.32 9.4 13.28 9.72 C 14.267 10.04 15.133 10.52 15.88 11.16 C 16.627 11.8 17.213 12.613 17.64 13.6 C 18.067 14.587 18.28 15.76 18.28 17.12 C 18.28 18.533 18.027 19.787 17.52 20.88 C 17.013 21.973 16.333 22.907 15.48 23.68 C 14.627 24.427 13.627 25 12.48 25.4 C 11.36 25.8 10.187 26 8.96 26z"/>
      -->
<!-- 6 id="symb-digit6"-->
<!-- <path fill="#696C7D" d="M 9.2 26.4 C 7.84 26.4 6.6 26.12 5.48 25.56 C 4.36 24.973 3.4 24.12 2.6 23 C 1.827 21.88 1.213 20.493 0.76 18.84 C 0.333 17.187 0.12 15.28 0.12 13.12 C 0.12 10.96 0.333 9.067 0.76 7.44 C 1.213 5.813 1.827 4.453 2.6 3.36 C 3.4 2.24 4.36 1.413 5.48 0.88 C 6.6 0.32 7.84 0.04 9.2 0.04 C 10.56 0.04 11.8 0.32 12.92 0.88 C 14.04 1.413 14.987 2.24 15.76 3.36 C 16.56 4.453 17.173 5.813 17.6 7.44 C 18.053 9.067 18.28 10.96 18.28 13.12 C 18.28 15.28 18.053 17.187 17.6 18.84 C 17.173 20.493 16.56 21.88 15.76 23 C 14.987 24.12 14.04 24.973 12.92 25.56 C 11.8 26.12 10.56 26.4 9.2 26.4 z M 9.2 21.84 C 9.707 21.84 10.173 21.72 10.6 21.48 C 11.027 21.213 11.4 20.747 11.72 20.08 C 12.04 19.413 12.28 18.52 12.44 17.4 C 12.627 16.28 12.72 14.853 12.72 13.12 C 12.72 11.387 12.627 9.973 12.44 8.88 C 12.28 7.76 12.04 6.893 11.72 6.28 C 11.4 5.64 11.027 5.2 10.6 4.96 C 10.173 4.72 9.707 4.6 9.2 4.6 C 8.72 4.6 8.267 4.72 7.84 4.96 C 7.413 5.2 7.04 5.64 6.72 6.28 C 6.4 6.893 6.147 7.76 5.96 8.88 C 5.773 9.973 5.68 11.387 5.68 13.12 C 5.68 14.853 5.773 16.28 5.96 17.4 C 6.147 18.52 6.4 19.413 6.72 20.08 C 7.04 20.747 7.413 21.213 7.84 21.48 C 8.267 21.72 8.72 21.84 9.2 21.84z"/> -->
<!-- 7 id="symb-digit7"-->
<!-- <path fill="#696C7D" d="M 4.6 26 c 0.107 -2.107 0.293 -4.04 0.56 -5.8 c 0.293 -1.787 0.693 -3.48 1.2 -5.08 c 0.533 -1.627 1.2 -3.213 2 -4.76 C 9.186 8.813 10.2 7.213 11.4 5.56 H 0 V 0.6 H 17.68 V 4.2 c -1.467 1.787 -2.653 3.467 -3.56 5.04 c -0.88 1.547 -1.573 3.16 -2.08 4.84 c -0.48 1.653 -0.827 3.44 -1.04 5.36 c -0.213 1.893 -0.373 4.08 -0.48 6.56z"/> -->
<!-- 8 id="symb-digit8"-->
<!-- <path fill="#696C7D" d="M 8.948 26.179 c -1.28 0 -2.467 -0.16 -3.56 -0.48 c -1.067 -0.347 -2 -0.827 -2.8 -1.44 c -0.773 -0.613 -1.387 -1.347 -1.84 -2.2 c -0.427 -0.853 -0.64 -1.8 -0.64 -2.84 c 0 -1.547 0.413 -2.813 1.24 -3.8 c 0.853 -0.987 1.88 -1.8 3.08 -2.44 v -0.16 c -0.987 -0.747 -1.8 -1.587 -2.44 -2.52 c -0.64 -0.96 -0.96 -2.12 -0.96 -3.48 c 0 -1.067 0.2 -2.027 0.6 -2.88 c 0.4 -0.88 0.96 -1.627 1.68 -2.24 c 0.72 -0.613 1.573 -1.08 2.56 -1.4 c 1.013 -0.32 2.107 -0.48 3.28 -0.48 c 1.147 0 2.2 0.173 3.16 0.52 c 0.96 0.32 1.773 0.787 2.44 1.4 c 0.667 0.587 1.187 1.32 1.56 2.2 c 0.373 0.853 0.56 1.8 0.56 2.84 c 0 1.227 -0.333 2.32 -1 3.28 c -0.667 0.933 -1.44 1.693 -2.32 2.28 v 0.16 c 1.227 0.667 2.267 1.52 3.12 2.56 c 0.853 1.04 1.28 2.4 1.28 4.08 c 0 1.013 -0.213 1.947 -0.64 2.8 c -0.427 0.853 -1.04 1.6 -1.84 2.24 c -0.773 0.613 -1.72 1.107 -2.84 1.48 c -1.093 0.347 -2.32 0.52 -3.68 0.52 z m 1.6 -15.28 c 1.04 -1.2 1.56 -2.44 1.56 -3.72 c 0 -0.987 -0.28 -1.773 -0.84 -2.36 c -0.533 -0.613 -1.28 -0.92 -2.24 -0.92 c -0.773 0 -1.44 0.24 -2 0.72 c -0.56 0.48 -0.84 1.213 -0.84 2.2 c 0 1.04 0.4 1.853 1.2 2.44 c 0.8 0.587 1.853 1.133 3.16 1.64 z m -1.48 11.2 c 0.987 0 1.8 -0.253 2.44 -0.76 c 0.64 -0.533 0.96 -1.333 0.96 -2.4 c 0 -0.56 -0.133 -1.04 -0.4 -1.44 c -0.24 -0.4 -0.6 -0.76 -1.08 -1.08 c -0.48 -0.347 -1.053 -0.667 -1.72 -0.96 c -0.64 -0.293 -1.36 -0.613 -2.16 -0.96 c -0.56 0.533 -1.027 1.147 -1.4 1.84 c -0.373 0.693 -0.56 1.427 -0.56 2.2 c 0 1.12 0.387 2 1.16 2.64 c 0.773 0.613 1.693 0.92 2.76 0.92z"/> -->
<!-- 9 id="symb-digit9"-->
  <!-- <path fill="#696C7D" d="M 8.774 12.019 c 0.667 0 1.333 -0.187 2 -0.56 c 0.693 -0.4 1.293 -1.053 1.8 -1.96 c -0.267 -2 -0.773 -3.373 -1.52 -4.12 c -0.72 -0.773 -1.533 -1.16 -2.44 -1.16 c -0.853 0 -1.6 0.333 -2.24 1 c -0.64 0.64 -0.96 1.68 -0.96 3.12 c 0 1.36 0.32 2.32 0.96 2.88 c 0.64 0.533 1.44 0.8 2.4 0.8 z m -0.92 14.16 c -1.68 0 -3.147 -0.307 -4.4 -0.92 c -1.227 -0.613 -2.24 -1.32 -3.04 -2.12 l 3.12 -3.52 c 0.427 0.48 1 0.907 1.72 1.28 c 0.72 0.347 1.453 0.52 2.2 0.52 c 0.72 0 1.387 -0.133 2 -0.4 c 0.613 -0.267 1.147 -0.707 1.6 -1.32 c 0.48 -0.64 0.853 -1.453 1.12 -2.44 c 0.293 -1.013 0.467 -2.267 0.52 -3.76 c -0.32 0.427 -0.693 0.813 -1.12 1.16 c -0.427 0.32 -0.867 0.6 -1.32 0.84 c -0.453 0.213 -0.907 0.387 -1.36 0.52 c -0.453 0.107 -0.88 0.16 -1.28 0.16 c -1.093 0 -2.107 -0.16 -3.04 -0.48 c -0.907 -0.32 -1.693 -0.8 -2.36 -1.44 c -0.667 -0.64 -1.2 -1.453 -1.6 -2.44 c -0.373 -0.987 -0.56 -2.147 -0.56 -3.48 c 0 -1.307 0.227 -2.48 0.68 -3.52 c 0.453 -1.067 1.053 -1.973 1.8 -2.72 c 0.773 -0.747 1.667 -1.307 2.68 -1.68 c 1.04 -0.4 2.133 -0.6 3.28 -0.6 c 1.227 0 2.413 0.24 3.56 0.72 c 1.173 0.48 2.2 1.227 3.08 2.24 c 0.907 1.013 1.627 2.32 2.16 3.92 c 0.56 1.573 0.84 3.48 0.84 5.72 c 0 2.373 -0.293 4.427 -0.88 6.16 c -0.56 1.733 -1.32 3.16 -2.28 4.28 c -0.933 1.12 -2.027 1.96 -3.28 2.52 c -1.227 0.533 -2.507 0.8 -3.84 0.8z"/> -->
<!-- 0 id="symb-digit0"-->
<path fill="#696C7D" d="M 9.2 26.4 C<!--  7.84 26.4 6.6 26.12 5.48 25.56 C 4.36 24.973 3.4 24.12 2.6 23 C 1.827 21.88 1.213 20.493 0.76 18.84 C 0.333 17.187 0.12 15.28 0.12 13.12 C 0.12 10.96 0.333 9.067 0.76 7.44 C 1.213 5.813 1.827 4.453 2.6 3.36 C 3.4 2.24 4.36 1.413 5.48 0.88 C 6.6 0.32 7.84 0.04 9.2 0.04 C 10.56 0.04 11.8 0.32 12.92 0.88 C 14.04 1.413 14.987 2.24 15.76 3.36 C 16.56 4.453 17.173 5.813 17.6 7.44 C 18.053 9.067 18.28 10.96 18.28 13.12 C 18.28 15.28 18.053 17.187 17.6 18.84 C 17.173 20.493 16.56 21.88 15.76 23 C 14.987 24.12 14.04 24.973 12.92 25.56 C 11.8 26.12 10.56 26.4 9.2 26.4 z M 9.2 21.84 C 9.707 21.84 10.173 21.72 10.6 21.48 C 11.027 21.213 11.4 20.747 11.72 20.08 C 12.04 19.413 12.28 18.52 12.44 17.4 C 12.627 16.28 12.72 14.853 12.72 13.12 C 12.72 11.387 12.627 9.973 12.44 8.88 C 12.28 7.76 12.04 6.893 11.72 6.28 C 11.4 5.64 11.027 5.2 10.6 4.96 C 10.173 4.72 9.707 4.6 9.2 4.6 C 8.72 4.6 8.267 4.72 7.84 4.96 C 7.413 5.2 7.04 5.64 6.72 6.28 C 6.4 6.893 6.147 7.76 5.96 8.88 C 5.773 9.973 5.68 11.387 5.68 13.12 C 5.68 14.853 5.773 16.28 5.96 17.4 C 6.147 18.52 6.4 19.413 6.72 20.08 C 7.04 20.747 7.413 21.213 7.84 21.48 C 8.267 21.72 8.72 21.84 9.2 21.84z"/> -->
</svg>
```
