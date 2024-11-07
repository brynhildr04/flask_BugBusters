/*******purchase js********/
function updateFinalPrice(quantityId, finalPriceId, price) {
    const quantity = parseInt(document.getElementById(quantityId).innerText);
    document.getElementById(finalPriceId).innerText = (price * quantity).toLocaleString() + '원';
}

function increaseQuantity(quantityId, price) {
    const quantityElement = document.getElementById(quantityId);
    let quantity = parseInt(quantityElement.innerText);
    quantityElement.innerText = ++quantity;
    updateFinalPrice(quantityId, 'finalPrice1', price);
}

function decreaseQuantity(quantityId, price) {
    const quantityElement = document.getElementById(quantityId);
    let quantity = parseInt(quantityElement.innerText);
    if (quantity > 1) {
        quantityElement.innerText = --quantity;
        updateFinalPrice(quantityId, 'finalPrice1', price);
    }
}

function removeProduct(productId) {
    const productElement = document.getElementById(productId);
    productElement.remove();
    const finalprice2 = document.querySelector('.finalprice');
    if (finalprice2) {
        finalprice2.remove(); // finalprice 클래스를 가진 요소 삭제
    }
}

function redirectToPayment() {
const productBoxes = document.querySelectorAll('.product-box');
if (productBoxes.length === 0) {
    alert("오류입니다. 결제할 상품이 없습니다."); // 상품이 없을 때 경고창 표시
} else {
    window.location.href = "payment.html"; // 결제 중 페이지로 이동
}
}
