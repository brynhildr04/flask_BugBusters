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

function review(id, name, contents, rating, date, items) {
    const reviewsContainer = document.getElementById('reviewsContainer');
    const reviewDiv = document.createElement('div');
    reviewDiv.classList.add('review-item');

    const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);

    reviewDiv.innerHTML = `
        <div class="review-header">
            <div class="reviewer-info">
                <span class="reviewer-name">${name}</span>
                <span class="review-date">${date}</span>
            </div>
            <div class="review-rating">${stars}</div>
        </div>
        <div class="review-purchase-info">
            구매 수량: ${items}개
        </div>
        <div class="review-content">${contents}</div>
    `;
     
    reviewsContainer.appendChild(reviewDiv);
}

function showReviews() {
    const reviewsTab = document.getElementById('reviewsTab');
    const detailsTab = document.getElementById('detailsTab');
    const reviewsContent = document.getElementById('reviewsContent');
    const detailsContent = document.getElementById('detailsContent');
    
    if (reviewsTab && detailsTab && reviewsContent && detailsContent) {
        reviewsTab.classList.add('active');
        detailsTab.classList.remove('active');
        reviewsContent.classList.add('active-content');
        detailsContent.classList.remove('active-content');
        
        if (!reviewsAdded) {
            // 더미 리뷰 데이터 추가
            review("1", "오*원", "향도 너무 좋고, 생각보다 커서 오래 사용할 수 있을 것 같아요. 특히 잠들기 전에 켜두면 좋아요!", 5, "2024.10.19.", 1);
            review("2", "김*아", "친구에게 선물로 주려고 샀다가 저도 쓰고 싶어서 하나 더 샀어요. 포장도 예쁘고 향도 은은해서 좋네요.", 5, "2024.10.18.", 2);
            review("3", "박*하", "가족들에게 선물을 주려고 많이 샀습니다! 다들 너무 좋아하셨어요.", 5, "2024.10.16.", 5);
            reviewsAdded = true;
        }
    }
}

// 페이지 로드 시 기본 탭 설정
window.onload = () => {
    showDetails();
};

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

/********payment js********/
setTimeout(() => {
    document.getElementById('paymentStatus').innerHTML = "결제가 완료되었습니다! <br><button onclick='continueShopping()'>쇼핑 계속하기</button>";
}, 2000);

function continueShopping() {
    window.location.href = "/main_service.html"; // 메인 페이지로 돌아가는 링크
}

window.onload=showDetails(); //첫 화면에서 기본은 상품 상세로 설정

/*******chat js*******/
function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    
    if (message === "") return;

    const chatMessages = document.getElementById("chatMessages");

    // 사용자 메시지 추가
    addMessage(message, "user");

    // 예제 봇 응답
    setTimeout(() => {
        addMessage("안녕하세요! 판매자입니다! 무엇을 도와드릴까요?", "bot");
    }, 500);

    // 입력 필드 초기화
    input.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById("chatMessages");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = text;

    const timestamp = document.createElement("div");
    timestamp.classList.add("timestamp");
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    timestamp.textContent = time;

    messageDiv.appendChild(timestamp);
    chatMessages.appendChild(messageDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}



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

// 슬라이더 기능 (신우림 js)
document.addEventListener('DOMContentLoaded', function() {
    // 슬라이더 1 (인기 상품)
    initializeSlider('slideTrack1', 'prevBtn1', 'nextBtn1');
    // 슬라이더 2 (최신 등록 상품)
    initializeSlider('slideTrack2', 'prevBtn2', 'nextBtn2');
});

function initializeSlider(trackId, prevBtnId, nextBtnId) {
    const slideTrack = document.getElementById(trackId);
    const prevBtn = document.getElementById(prevBtnId);
    const nextBtn = document.getElementById(nextBtnId);
    
    if (!slideTrack || !prevBtn || !nextBtn) return;

    let currentPosition = 0;
    const cards = slideTrack.querySelectorAll('.product-card');
    const cardWidth = cards[0].offsetWidth;
    const gap = 32; // CSS에서 설정한 gap 크기
    const visibleCards = 3; // 한 번에 보여질 카드 수
    const maxPosition = cards.length - visibleCards;

    // 초기 상태 설정
    updateSliderState();

    prevBtn.addEventListener('click', () => {
        if (currentPosition > 0) {
            currentPosition--;
            updateSliderPosition();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentPosition < maxPosition) {
            currentPosition++;
            updateSliderPosition();
        }
    });

    function updateSliderPosition() {
        const translateX = currentPosition * -(cardWidth + gap);
        slideTrack.style.transform = `translateX(${translateX}px)`;
        updateSliderState();
    }

    function updateSliderState() {
        prevBtn.disabled = currentPosition === 0;
        nextBtn.disabled = currentPosition >= maxPosition;
        
        // 버튼 스타일 업데이트
        prevBtn.style.opacity = currentPosition === 0 ? '0.5' : '1';
        nextBtn.style.opacity = currentPosition >= maxPosition ? '0.5' : '1';
    }
}
