/*

TemplateMo 559 Zay Shop

https://templatemo.com/tm-559-zay-shop

*/

'use strict';
$(document).ready(function() {

    // Accordion
    var all_panels = $('.templatemo-accordion > li > ul').hide();

    $('.templatemo-accordion > li > a').click(function() {
        console.log('Hello world!');
        var target =  $(this).next();
        if(!target.hasClass('active')){
            all_panels.removeClass('active').slideUp();
            target.addClass('active').slideDown();
        }
      return false;
    });
    // End accordion

    // Product detail
    $('.product-links-wap a').click(function(){
      var this_src = $(this).children('img').attr('src');
      $('#product-detail').attr('src',this_src);
      return false;
    });
    $('#btn-minus').click(function(){
      var val = $("#var-value").html();
      val = (val=='1')?val:val-1;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('#btn-plus').click(function(){
      var val = $("#var-value").html();
      val++;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('.btn-size').click(function(){
      var this_val = $(this).html();
      $("#product-size").val(this_val);
      $(".btn-size").removeClass('btn-secondary');
      $(".btn-size").addClass('btn-success');
      $(this).removeClass('btn-success');
      $(this).addClass('btn-secondary');
      return false;
    });
    // End roduct detail

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


