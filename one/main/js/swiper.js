var swiper = new Swiper(".mySwiper", {
    slidesPerView: 'auto',
    slidesOffsetAfter: 47,
    slidesOffsetBefore: 47,
    spaceBetween: 10,
    clickable: true,
    effect: 'coverflow',
    coverflowEffect: {
        rotate: 0,           // 옆으로 넘어갈 때 회전 각도 (0이면 평평함)
        stretch: 0,         // 슬라이드 간의 간격 (값이 클수록 겹침)
        depth: 0,          // 깊이감 (원근감)
        modifier: 1,         // 효과 배수
        slideShadows: false, // 그림자 끄기 (이미지에 그림자가 이미 있다면 false)
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },

});

var swiper2 = new Swiper(".mySwiper2", {
    navigation: {
        nextEl: ".nav_slider .swiper-button-next",
        prevEl: ".nav_slider .swiper-button-prev",
    },
    slidesPerView: 'auto',
    freeMode: true,
    slidesOffsetAfter: 47,
    slidesOffsetBefore: 47,
    spaceBetween: 10,
});

var swiper3 = new Swiper(".mySwiper3", {
    navigation: {
        nextEl: ".section_slider .swiper-button-next",
        prevEl: ".section_slider .swiper-button-prev",
    },
    pagination: {
        el: ".section_slider .swiper-pagination",
        clickable: true,
    },
    slidesPerView: 'auto',
    freeMode: true,
    slidesOffsetAfter: 47,
    slidesOffsetBefore: 47,
    spaceBetween: 15,
});

var swiper4 = new Swiper(".mySwiper4", {
    navigation: {
        nextEl: ".section_slider .swiper-button-next",
        prevEl: ".section_slider .swiper-button-prev",
    },
    pagination: {
        el: ".section_slider .swiper-pagination",
        clickable: true,
    },
    slidesPerView: 'auto',
    slidesPerGroup: 7,
    slidesOffsetAfter: 47,
    slidesOffsetBefore: 47,
    spaceBetween: 10,
});