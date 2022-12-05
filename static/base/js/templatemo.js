/*

TemplateMo 559 Zay Shop

https://templatemo.com/tm-559-zay-shop

*/

'use strict';
$(document).ready(function () {

    // Accordion
    var all_panels = $('.templatemo-accordion > li > ul').hide();

    $('.templatemo-accordion > li > a').click(function () {
        console.log('Hello world!');
        var target = $(this).next();
        if (!target.hasClass('active')) {
            all_panels.removeClass('active').slideUp();
            target.addClass('active').slideDown();
        }
        return false;
    });
    // End accordion

});

import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.esm.browser.min.js';

const swiper1 = new Swiper('#swiper-container1', {
    slidesPerView: 'auto',
    paginationClickable: true,
    spaceBetween: 0,
    navigation: {
        nextEl: '.left-slide1',
        prevEl: '.right-slide1',
    },
});
const swiper2 = new Swiper('#swiper-container2', {
    slidesPerView: 'auto',
    paginationClickable: true,
    spaceBetween: 0,
    navigation: {
        nextEl: '.left-slide2',
        prevEl: '.right-slide2',
    },
});
const swiper3 = new Swiper('#swiper-container3', {
    slidesPerView: 'auto',
    paginationClickable: true,
    spaceBetween: 0,
    navigation: {
        nextEl: '.left-slide3',
        prevEl: '.right-slide3',
    },
});
const swiper_detail = new Swiper('#detail-swiper-container', {
    slidesPerView: 'auto',
    paginationClickable: true,
    spaceBetween: 0,
    navigation: {
        nextEl: '.detail-left-slide',
        prevEl: '.detail-right-slide',
    },
});


const one_star = document.getElementById('1star')
const two_star = document.getElementById('2star')
const three_star = document.getElementById('3star')
const four_star = document.getElementById('4star')
const five_star = document.getElementById('5star')

const handleSelect = (selection) => {
    switch (selection) {
        case '1star': {
            one_star.classList.add('text-warning')
            two_star.classList.remove('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '2star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.remove('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '3star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.remove('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '4star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.add('text-warning')
            five_star.classList.remove('text-warning')
            return
        }
        case '5star': {
            one_star.classList.add('text-warning')
            two_star.classList.add('text-warning')
            three_star.classList.add('text-warning')
            four_star.classList.add('text-warning')
            five_star.classList.add('text-warning')
            return
        }
    }
}
const arr = [one_star, two_star, three_star, four_star, five_star]
arr.forEach(item => item.addEventListener('mouseover', (event) => {
    handleSelect(event.target.id)
}))


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
    const percent1 = (sliderOne.value / sliderMaxValue) * 100;
    const percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #bc1f69 ${percent1}% , #bc1f69 ${percent2}%, #dadae5 ${percent2}%)`;
}

