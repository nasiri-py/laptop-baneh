
window.onload = function () {
    slideOne();
    slideTwo();
}
let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1").max;
let sliderMinValue = document.getElementById("slider-1").min;

function slideOne() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    fillColor();
}

function slideTwo() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    fillColor();
}

function fillColor() {
    const percent1 = (sliderOne.value / sliderMaxValue) * 100 - (sliderMinValue / sliderMaxValue) * 50;
    const percent2 = (sliderTwo.value / sliderMaxValue) * 100 - (sliderMinValue / sliderMaxValue) * 50;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #bc1f69 ${percent1}% , #bc1f69 ${percent2}%, #dadae5 ${percent2}%)`;
}
