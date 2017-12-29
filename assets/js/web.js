

function closeOther(ids, current) {
    ids.forEach(function (id) {

        if (id === current) {
            return
        }

        var x = document.getElementById(id);

        x.style.display = "none";
    })
}

function toggleById(ids, id) {
    closeOther(ids, id)

    var x = document.getElementById(id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function useWechat () {
    var wechat = document.getElementById("wechat");
    var alipay = document.getElementById("alipay");
    var qrcode = document.getElementById("donation-qrcode-image");

    wechat.classList.add("active")
    alipay.classList.remove("active")
    qrcode.src = "/assets/images/wechat.png"

} 

function useAlipay () {
    var wechat = document.getElementById("wechat");
    var alipay = document.getElementById("alipay");
    var qrcode = document.getElementById("donation-qrcode-image");

    alipay.classList.add("active")
    wechat.classList.remove("active")

    qrcode.src = "/assets/images/alipay.jpg"
} 