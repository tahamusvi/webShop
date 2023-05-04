let rtlSponsoringProducts = {242700: { title:'قالب HTML مدیریتی زِتا، Zeta',permaLink:'https://www.rtl-theme.com/zeta-html-template/'},232509: { title:'قالب HTML چندمنظوره Polo، پولو',permaLink:'https://www.rtl-theme.com/polo-html-template/'},185436: { title:'قالب Brook، قالب HTML چند منظوره و خلاقانه بروک + 60 دمو',permaLink:'https://www.rtl-theme.com/brook-html-template/'},182359: { title:'قالب Synadmin، قالب HTML مدیریت ساین ادمین',permaLink:'https://www.rtl-theme.com/synadmin-admin-html-template/'},176774: { title:'قالب Foxic، قالب HTML فروشگاهی فاکسیک',permaLink:'https://www.rtl-theme.com/foxic-html-template/'},168802: { title:'قالب Winck، قالب HTML شرکتی وینک',permaLink:'https://www.rtl-theme.com/winck-html-template/'},162415: { title:'قالب Sunny Admin، قالب HTML مدیریت سانی ادمین',permaLink:'https://www.rtl-theme.com/sunny-admin-html-theme/'},158728: { title:'قالب HTML فروشگاهی بیگ دیل، Bigdeal',permaLink:'https://www.rtl-theme.com/bigdeal-html-theme/'},156401: { title:'قالب Portkey، قالب HTML آژانس مسافرتی و رزرو تور',permaLink:'https://www.rtl-theme.com/portkey-html-template/'},153371: { title:'قالب NobleUI، قالب HTML مدیریتی نوبل',permaLink:'https://www.rtl-theme.com/nobleui-admin-html-template/'},151478: { title:'قالب Amira، قالب HTML خلاقانه آمیرا',permaLink:'https://www.rtl-theme.com/amira-html-theme/'},150866: { title:'قالب HTML شرکتی نایت، Knight',permaLink:'https://www.rtl-theme.com/knight-html-template/'},149762: { title:'قالب Gleek، قالب HTML پنل مدیریتی گلیک',permaLink:'https://www.rtl-theme.com/gleek-admin-html-template/'},147340: { title:'قالب Hoscon، قالب HTML هاستینگ و دامنه هاسکون',permaLink:'https://www.rtl-theme.com/hoscon-html-template/'},145525: { title:'قالب Ansta ، قالب HTML مدیریتی آنستا',permaLink:'https://www.rtl-theme.com/ansta-admin-html-template/'},144791: { title:'قالب Molla پوسته HTML چندمنظوره فروشگاهی',permaLink:'https://www.rtl-theme.com/molla-shop-html-template/'},143242: { title:'قالب Medilife | قالب HTML پزشکی مدیلایف',permaLink:'https://www.rtl-theme.com/medilife-html-template/'},143237: { title:'قالب Harborlights | قالب HTML رزرو هتل چراغ بندرگاه',permaLink:'https://www.rtl-theme.com/harborlights-hotel-html-template/'},141882: { title:'قالب Magz | قالب HTML مجله خبری مَگز',permaLink:'https://www.rtl-theme.com/magz-news-html-template/'},141566: { title:'قالب Melody | قالب HTML  مدیریتی ملودی',permaLink:'https://www.rtl-theme.com/melody-admin-html-template/'},140468: { title:'قالب TopMarket | قالب HTML فروشگاهی تاپ مارکت',permaLink:'https://www.rtl-theme.com/topmarket-shop-html-template/'},140189: { title:'قالب Sufee | قالب HTML پنل مدیریتی با بوت استرپ',permaLink:'https://www.rtl-theme.com/sufee-admin-html-template/'}};

const rtlSponsoringDomains = ["filenter.ir"];

    let rtlSponsoringScriptSrc = document.currentScript.src;

    var rtlSponsoringUrl       = new URL(rtlSponsoringScriptSrc);
    var rtlSponsoringAffID     = rtlSponsoringUrl.searchParams.get("aff_id");
    var rtlSponsoringProductID = rtlSponsoringUrl.searchParams.get("pid");

    if (rtlSponsoringDomains.includes(window.location.hostname)) {
        window.addEventListener("scroll", function () {
            var rtlSponsoringScrollPercent = rtlGetAmountScrolled();
            var rtlSponsoringPopupHTML     = `<style>.rtlthemehost{background: rgb(255 255 255 / 100%); box-shadow: 0 0 10px hsl(0deg 0% 75% / 35%); color: #4d535b; border-radius: 4px; padding: 20px 20px; font-size: 14px; position: fixed; bottom: 0; z-index: 99999999999999; width: 400px; right: 0; text-align: right; margin: 10px;}.rtlthemelink1{padding: 8px 12px; border-radius: 4px; color: #fff!important; margin-left: 15px; background-color: #8ed557!important; box-shadow: 0 5px 10px rgb(142 213 87 / 34%);}a.rtlthemelink1{color: white;}.rtlthemelink2{color: #4d535b;}a.rtlthemelink2{color: #4d535b; font-weight: 600;}a.rtlthemelink2:hover{color: #3f51b5;}span.rtlthemesp{border-right: 2px dashed #cfcfcf; padding: 5px 15px 5px 0px;}@media screen and (max-width: 460px){.rtlthemehost{border-radius: 0px; width: 100%; margin: 0px;text-align: center;padding: 20px 0px;font-size: 13px;}}</style> <div class="rtlthemehost"> <a href="[[product_id]]" title="[[title]]" class="rtlthemelink1" target="_blank" rel="follow noopener">خرید از راست چین </a> <span class="rtlthemesp" >میزبانی شده توسط</span> <a href="https://panel.limoo.host/aff.php?aff=994" class="rtlthemelink2" target="_blank" rel="nofollow noopener noreferrer">لیمو هاست</a></div>`;

            /*if (rtlSponsoringAffID == null) {
				rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[aff_id]]', 'aff.php?aff=1340');
			} else {
				rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[aff_id]]', 'aff.php?aff=' + rtlSponsoringAffID);
			}*/

            if (rtlSponsoringProductID == null) {
                rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[product_id]]', 'https://www.rtl-theme.com/');
                rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('title="[[title]]"', ' ');
            } else {
                if (rtlSponsoringProducts.hasOwnProperty(rtlSponsoringProductID)) {
                    rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[product_id]]', rtlSponsoringProducts[rtlSponsoringProductID].permaLink);
                    rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[title]]', rtlSponsoringProducts[rtlSponsoringProductID].title);
                } else {
                    rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('[[product_id]]', 'https://www.rtl-theme.com/?p=' + rtlSponsoringProductID);
                    rtlSponsoringPopupHTML = rtlSponsoringPopupHTML.replace('title="[[title]]"', ' ');
                }
            }

            if (rtlSponsoringScrollPercent >= 70) {
                var rtlSponsoringElement = document.getElementById('rtl-footer-toast-90');

                if (rtlSponsoringElement == null) {
                    let rtlSponsoringPopupDIV       = document.createElement('div');
                    rtlSponsoringPopupDIV.id        = 'rtl-footer-toast-90';
                    rtlSponsoringPopupDIV.innerHTML = rtlSponsoringPopupHTML;

                    document.body.appendChild(rtlSponsoringPopupDIV);
                }
            } else {
                var rtlSponsoringElement = document.getElementById('rtl-footer-toast-90');
                if (typeof (rtlSponsoringElement) != 'undefined' && rtlSponsoringElement != null) {
                    document.getElementById("rtl-footer-toast-90").remove();
                }
            }
        });
    }


    /**
     * Get Document Height
     *
     * @returns {number}
     */
    function rtlGetDocHeight() {
        var rtlSponsoringDocument = document;

        return Math.max(
            rtlSponsoringDocument.body.scrollHeight, rtlSponsoringDocument.documentElement.scrollHeight,
            rtlSponsoringDocument.body.offsetHeight, rtlSponsoringDocument.documentElement.offsetHeight,
            rtlSponsoringDocument.body.clientHeight, rtlSponsoringDocument.documentElement.clientHeight
        )
    }

    /**
     * Get Page Scrolled Amount
     *
     * @returns {number}
     */
    function rtlGetAmountScrolled() {
        var rtlSponsoringWinHeight   = window.innerHeight || (document.documentElement || document.body).clientHeight
        var rtlSponsoringDocHeight   = rtlGetDocHeight()
        var rtlSponsoringScrollTop   = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop
        var rtlSponsoringTrackLength = rtlSponsoringDocHeight - rtlSponsoringWinHeight

        return Math.floor(rtlSponsoringScrollTop / rtlSponsoringTrackLength * 100);
    }