const client =
  new Ably.Realtime({
    key: ABLY_KEY
  });

const channel =
  client.channels.get("nova");

/* ELEMENTS */
const solarFill =
  document.getElementById("solarFill");

const solarHud =
  document.getElementById("solarHud");

const batteryFill =
  document.getElementById("batteryFill");

const runner =
  document.querySelector(".runner");

/* POLYGON */
const A = { x: 100, y: 115 };
const B = { x: 119, y: 183 };
const C = { x: 550, y: 220 };
const D = { x: 476, y: 156 };

/* UPDATE FILL */
function setSolarFill(solar_pct) {

  const p =
    Math.max(
      0,
      Math.min(100, Number(solar_pct))
    ) / 100;

  const topRight = {
    x: A.x + p * (D.x - A.x),
    y: A.y + p * (D.y - A.y)
  };

  const bottomRight = {
    x: B.x + p * (C.x - B.x),
    y: B.y + p * (C.y - B.y)
  };

  solarFill.style.clipPath =
    `polygon(
      ${A.x}px ${A.y}px,
      ${topRight.x}px ${topRight.y}px,
      ${bottomRight.x}px ${bottomRight.y}px,
      ${B.x}px ${B.y}px
    )`;
}

function setBatteryFill(pct) {

  const p =
    Math.max(
      0,
      Math.min(100, Number(pct))
    ) / 100;

  /*
    coordinates:
    top = 385
    bottom = 446
    height = 61
  */

  const maxHeight = 60;

  const h = maxHeight * p;

  batteryFill.style.height =
    `${h}px`;

  batteryFill.style.top =
    `${439 - h}px`;
}


/* SHOW/HIDE EFFECTS */
function setPowerState(solar) {

  const active =
    Number(solar) > 0;

  solarFill.style.display =
    active ? "block" : "none";

  solarHud.style.display =
    active ? "block" : "none";

  runner.style.display =
    active ? "block" : "none";
}

/* ABLY */
channel.subscribe((msg) => {

  try {

    if (!msg || !msg.data) {

      console.warn(
        "Empty message ignored:",
        msg
      );

      return;
    }

    let data = msg.data;

    /* STRING PAYLOAD */
    if (typeof data === "string") {
      data = JSON.parse(data);
    }

    /* SAFETY WRAPPER */
    if (data.data) {
      data = data.data;
    }

    const solar = Number(data.solar ?? 0);
    const solar_pct = Number(data.solar_pct ?? 0);

    const car = Number(data.car ?? 0);
    const car_pct = Number(data.car_pct ?? 0);

    const battery = Number(data.battery ?? 0);
    const battery_pct = Number(data.battery_pct ?? 0);

    const house = Number(data.house ?? 0);
    const grid = Number(data.grid ?? 0);

    console.log(
      "LIVE:",
      data
    );

    /* MAIN POWER */
    setPowerState(solar_pct);
    
    setEnergy("solar", solar, solar_pct);
    setSolarFill(solar_pct);

    setEnergy("battery", battery, battery_pct);
    setBatteryFill(battery_pct);

    setEnergy("car", car, car_pct);
    setEnergy("house", house);
    setEnergy("grid", grid);

  } catch (err) {

    console.error(
      "Parse error:",
      err
    );

  }

});

const hudMap = {
  solar:   solarHud,
  battery: batteryHud,
  car:     carHud,
  house:   houseHud,
  grid:    gridHud
};

function setEnergy(label, power, pct) {
  const el = hudMap[label];
  if (!el) return;

  const kw = (Number(power) / 1000).toFixed(1);
  const p = pct !== undefined ? ` ${pct}%` : "";

  el.textContent = `${kw} KW${p}`;
}

/* DEFAULT */
setPowerState(true);

setEnergy("solar", 1800, 50);
setSolarFill(45);

setEnergy("battery", 1800, 40);
setBatteryFill(80);

setEnergy("car", 2300, 20);
setEnergy("house", 500);
setEnergy("grid", 100);