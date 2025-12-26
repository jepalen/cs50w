let counter = 0;
let seconds = localStorage.getItem("seconds") || 0;

async function get_exchange_rate() {
    try {
        event.preventDefault();
        const result = document.querySelector("#exchange_rate");
        const response = await fetch("https://api.exchangerate-api.com/v4/latest/USD")
        const data = await response.json()
        const currency = document.querySelector("#currency").value.toUpperCase();
        console.log('data', data.rates);
        console.log('currency', currency);
        const rate = data.rates[currency];
        if (!rate) {
            result.innerHTML = "Invalid currency";

        } else {
            result.innerHTML = `1 USD = ${rate} ${currency}`;
        }
        return false;
    } catch (error) {
        console.log(error);
    }
}

function updateSeconds() {
    seconds++;
    const heading = document.querySelector("h2");
    heading.innerHTML = seconds;
    localStorage.setItem("seconds", seconds);
}

function count() {
    const heading = document.querySelector("h1");
    if (counter % 2 == 0) {
        heading.style.color = "blue";
    } else {
        heading.style.color = "red";
    }
    counter++;
    if (counter % 10 == 0) {
        alert(counter);
        heading.style.color = "green";

    }

    heading.innerHTML = 'hello world ' + counter;
}

function sayHello() {
    const name = document.querySelector("#name").value;
    alert(`hello ${name}`);
}

function changeColor(color) {
    if (!color) {
        color = "black";
    }
    const heading = document.querySelector("#heading");
    heading.style.color = color;
}

function changeFont() {
    const heading = document.querySelector("#heading");
    heading.style.fontFamily = this.value;
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#get_exchange_rate").onsubmit = get_exchange_rate;
    document.querySelector("#seconds").innerHTML = seconds;
    document.querySelector("button").addEventListener("click", count);
    document.querySelector("form").addEventListener("submit", sayHello);
    document.querySelectorAll("button").forEach(button => {
        button.addEventListener("click", () => changeColor(button.dataset.color));
    })
    document.querySelector("#font").onchange = changeFont;
})

setInterval(updateSeconds, 1000);
