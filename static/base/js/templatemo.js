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


