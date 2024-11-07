//민하님 js
document.getElementById('quantity')?.addEventListener('input', function () {
    const quantity = parseInt(this.value, 10) || 0;
    const total = quantity * 10000;
    document.getElementById('result').innerText = `수량: ${quantity}, 총액: ${total.toLocaleString()}원`;
});

if (document.getElementById('quantity')) {
    document.getElementById('quantity').dispatchEvent(new Event('input'));
}

const slides = document.querySelectorAll('.slide');
const prev = document.getElementById('prev');
const next = document.getElementById('next');
let currentSlide = 0;

function showSlide(index) {
    slides.forEach((slide, idx) => {
        slide.style.opacity = idx === index ? '1' : '0';
    });
}

prev?.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
});

next?.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
});

// 초기 슬라이드 표시
showSlide(currentSlide);

function addToCart() {
    alert("장바구니에 담았습니다!");
}

function buy() {
    alert("구매 화면으로 이동합니다!");
}

let reviewsAdded = false; // 리뷰가 추가되었는지 여부를 추적하는 변수

function review(id, name, contents, rating, date, items) {
    var reviewsContainer = document.getElementById('reviewsContainer');
    var reviewDiv = document.createElement('div');
    reviewDiv.classList.add('review');

    reviewDiv.innerHTML = `
        <strong>${name} (${id})</strong><br>
        <div class="rating">${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</div>
        <small>${date} | 수제 캔들, ${items}개</small><br>
        <p>${contents}</p>
    `;
     
    reviewsContainer.appendChild(reviewDiv);
}

function showDetails() {
    document.getElementById('detailsTab')?.classList.add('active');
    document.getElementById('reviewsTab')?.classList.remove('active');
    document.getElementById('detailsContent')?.classList.add('active-content');
    document.getElementById('reviewsContent')?.classList.remove('active-content');
}

function showReviews() {
    document.getElementById('reviewsTab')?.classList.add('active');
    document.getElementById('detailsTab')?.classList.remove('active');
    document.getElementById('reviewsContent')?.classList.add('active-content');
    document.getElementById('detailsContent')?.classList.remove('active-content');
    // 리뷰가 추가되지 않았다면 추가
    if (!reviewsAdded) {
        review("1", "오*원", "향도 너무 좋고, 생각보다 커서 오래 사용할 수 있을 것 같아요...", 5, "2024.10.19.", 1);
        review("2", "김*아", "친구에게 선물로 주려고 샀다가 저도 쓰고 싶어서 하나 더 샀...", 5, "2024.10.18.", 2);
        review("3", "박*하", "가족들에게 선물을 주려고 많이 샀습니다! 사용해본 캔들 중에...", 5, "2024.10.16.", 5);
        reviewsAdded = true; // 리뷰가 추가되었음을 기록
    }
    const reviewsContainer = document.getElementById('reviewsContainer');
    if (reviewsContainer) {
        reviewsContainer.style.display = 'block'; // 리뷰 컨테이너 보이기
    }
}

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

window.onload=showDetails(); //첫 화면에서 기본은 상품 상세로 설정


//은영님 js
function setRating(stars) {
    const starElements = document.querySelectorAll('.star');
    starElements.forEach((star, index) => {
        star.style.color = index < stars ? '#FFC700' : '#ccc';
    });
    document.getElementById('rating').value = stars;
    document.getElementById('starText').innerText = `(${stars})`;
}

function previewImage(event) {
const reader = new FileReader();
reader.onload = function() {
const imagePreviewContainer = document.getElementById('imagePreviewContainer');
imagePreviewContainer.style.backgroundImage = `url(${reader.result})`;
imagePreviewContainer.style.backgroundSize = 'cover';
imagePreviewContainer.style.backgroundPosition = 'center';
}
reader.readAsDataURL(event.target.files[0]);
}


function submitReview() {
    const titleElement = document.getElementById('title');
    const contentElement = document.getElementById('content');
    const ratingElement = document.getElementById('rating');

    if (!titleElement || !contentElement || !ratingElement) {
        alert("필수 입력 요소를 찾을 수 없습니다.");
        return;
    }

    const title = titleElement.value;
    const content = contentElement.value;
    const rating = ratingElement.value;

    localStorage.setItem('reviewTitle', title);
    localStorage.setItem('reviewContent', content);
    localStorage.setItem('reviewRating', rating);

    window.location.href = "review_detail.html";
}

//박수민 js
function pwSending(){
    var msg=document.getElementById("findPW_msg");
    msg.innerHTML="*임시 비밀번호가 이메일이 전송되었습니다."; 
    msg.style.visibility="visible";
}
function idSending(){
    var msg=document.getElementById("findId_msg");
    msg.innerHTML="*아이디가 이메일이 전송되었습니다."; 
    msg.style.visibility="visible";
}