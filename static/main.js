//민하님 js
document.getElementById('quantity').addEventListener('input', function () {
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

function addToCart1() {
    alert("장바구니에 담았습니다!");
}


function buy() {
    alert("구매 화면으로 이동합니다!");
}

let reviewsAdded = false; // 리뷰가 추가되었는지 여부를 추적하는 변수

function showReviews() {
    // 탭 활성화
    const reviewsTab = document.getElementById('reviewsTab');
    const detailsTab = document.getElementById('detailsTab');
    const reviewsContent = document.getElementById('reviewsContent');
    const detailsContent = document.getElementById('detailsContent');
    if (reviewsTab && detailsTab && reviewsContent && detailsContent) {
        reviewsTab.classList.add('active');
        detailsTab.classList.remove('active');
        reviewsContent.classList.add('active-content');
        detailsContent.classList.remove('active-content');
    }
}
// 커서 스타일 추가
reviewDiv.style.cursor = 'pointer';
const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);

function showDetails() {
    document.getElementById('detailsTab')?.classList.add('active');
    document.getElementById('reviewsTab')?.classList.remove('active');
    document.getElementById('detailsContent')?.classList.add('active-content');
    document.getElementById('reviewsContent')?.classList.remove('active-content');
}



// 페이지 로드 시 기본 탭 설정
window.onload = () => {
    showDetails();
};

/*******purchase js********/
function updateFinalPrice1(quantityId1, finalPriceId1, price1) {
    const quantity1 = parseInt(document.getElementById(quantityId1).innerText);
    document.getElementById(finalPriceId1).innerText = (price1 * quantity1).toLocaleString() + '원';
}

function increaseQuantity1(quantityId1, price1) {
    const quantityElement1 = document.getElementById(quantityId1);
    let quantity1 = parseInt(quantityElement1.innerText);
    quantityElement1.innerText = ++quantity1;
    updateFinalPrice1(quantityId1, 'finalPrice1', price1);
}

function decreaseQuantity1(quantityId1, price1) {
    const quantityElement1 = document.getElementById(quantityId1);
    let quantity1 = parseInt(quantityElement1.innerText);
    if (quantity1 > 1) {
        quantityElement1.innerText = --quantity1;
        updateFinalPrice1(quantityId1, 'finalPrice1', price1);
    }
}

function removeProduct1(productId1) {
    const productElement1 = document.getElementById(productId1);
    productElement.remove();
    const finalprice2 = document.querySelector('.finalprice1');
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

window.onload = showDetails(); //첫 화면에서 기본은 상품 상세로 설정

/*******chat js*******/
function sendMessage(isButton = false, message = "") {
    const chatMessages = document.getElementById("chatMessages");

    if (!isButton) {
        const input = document.getElementById("userInput");
        message = input.value.trim();
        if (message === "") return;
        addMessage(message, "user");
        input.value = "";
    } else {
        addMessage(message, "user");
    }

    // 자동 응답 봇 처리
    setTimeout(() => {
        if (!isButton) {
            addBotOptions();
        } else {
            handleBotResponse(message);
        }
    }, 500);

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

function addBotOptions() {
    const chatMessages = document.getElementById("chatMessages");

    const optionsDiv = document.createElement("div");
    optionsDiv.classList.add("message", "bot");

    // 안내 멘트 추가
    const guideMessage = document.createElement("p");
    guideMessage.textContent = "안녕하세요! 판매자입니다. 문의사항을 선택해주세요.";
    guideMessage.style.marginBottom = "10px"; // 버튼과 간격
    optionsDiv.appendChild(guideMessage);

    const options = [
        "1. 배송 문의",
        "2. 취소 및 환불 문의",
        "3. 교환 및 반품 문의",
        "4. 기타 문의"
    ];

    options.forEach((option, index) => {
        const button = document.createElement("button");
        button.textContent = option;
        button.onclick = () => sendMessage(true, option);
        button.style.display = "block";
        button.style.margin = "5px 0";
        button.style.padding = "8px";
        button.style.border = "1px solid #00462A";
        button.style.borderRadius = "5px";
        button.style.backgroundColor = "#CDECDB";
        button.style.color = "#00462A";
        button.style.cursor = "pointer";
        optionsDiv.appendChild(button);
    });

    chatMessages.appendChild(optionsDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleBotResponse(userChoice) {
    let response;
    switch (userChoice) {
        case "1. 배송 문의":
            response = "배송은 5~7일 내로 시작될 예정입니다. 배송이 시작되면 문자 드리겠습니다.";
            break;
        case "2. 취소 및 환불 문의":
            response = "주문 취소는 발송 시작 전에 가능합니다. 환불 문의는 판매자와의 상담 후에 해주시기 바랍니다.";
            break;
        case "3. 교환 및 반품 문의":
            response = "교환 및 반품은 상품이 사용되지 않은 상태, 온전하게 보전된 상태에서만 가능합니다.";
            break;
        case "4. 기타 문의":
            response = "기타 문의 사항은 아래의 Q&A 게시판을 이용해주시기 바랍니다.";
            break;
        default:
            response = "죄송합니다. 정확히 선택해주세요.";
    }

    addMessage(response, "bot");

    // 다시 옵션 출력
    setTimeout(() => {
        addBotOptions();
    }, 1000);
}



//소윤님 js
// 카테고리 옵션 목록
const categories = {
    product: ["식품", "공예", "뷰티", "패션", "기타 제품", "제품 제작 의뢰"],
    service: ["어학", "IT", "취미", "디자인", "첨삭", "생활", "기타"]
};

// 카테고리 옵션 업데이트 함수
function updateCategoryOptions() {
    const productType = document.getElementById("product_type").value; // 제품 유형 선택
    const categorySelect = document.getElementById("category"); // 카테고리 드롭다운

    // 기존 옵션 제거
    categorySelect.innerHTML = "";

    // 선택된 유형에 따른 카테고리 옵션 추가
    categories[productType].forEach(function (category) {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;
        categorySelect.appendChild(option);
    });
}

// 페이지가 처음 로드될 때 기본 카테고리 옵션 설정
document.addEventListener("DOMContentLoaded", function () {
    updateCategoryOptions(); // 기본적으로 '제품' 카테고리를 설정
});

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
    reader.onload = function () {
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
function pwSending() {
    var msg = document.getElementById("findPW_msg");
    msg.innerHTML = "*임시 비밀번호가 이메일이 전송되었습니다.";
    msg.style.visibility = "visible";
}
function idSending() {
    var msg = document.getElementById("findId_msg");
    msg.innerHTML = "*아이디가 이메일이 전송되었습니다.";
    msg.style.visibility = "visible";
}

// 슬라이더 기능 (신우림 js)
document.addEventListener('DOMContentLoaded', function () {
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




// 수량 증가 함수
function increaseQuantity(button) {
    const quantitySpan = button.previousElementSibling;
    let quantity = parseInt(quantitySpan.textContent);
    quantity++;
    quantitySpan.textContent = quantity;
    updateItemTotal(button.parentElement.parentElement);
    updateGrandTotal();
}

// 수량 감소 함수
function decreaseQuantity(button) {
    const quantitySpan = button.nextElementSibling;
    let quantity = parseInt(quantitySpan.textContent);
    if (quantity > 1) {
        quantity--;
        quantitySpan.textContent = quantity;
        updateItemTotal(button.parentElement.parentElement);
        updateGrandTotal();
    }
}

// 개별 상품 총액 업데이트
function updateItemTotal(cartItem) {
    const unitPrice = parseInt(cartItem.querySelector('.unit-price').textContent.replace(',', ''));
    const quantity = parseInt(cartItem.querySelector('.quantity').textContent);
    const itemTotalSpan = cartItem.querySelector('.item-total');
    const total = unitPrice * quantity;
    itemTotalSpan.textContent = total.toLocaleString();
}

// 장바구니 총액 업데이트
function updateGrandTotal() {
    const itemTotals = document.querySelectorAll('.item-total');
    let grandTotal = 0;
    itemTotals.forEach(item => {
        grandTotal += parseInt(item.textContent.replace(',', ''));
    });
    document.getElementById('grandTotal').textContent = grandTotal.toLocaleString();
}

// 장바구니에서 상품 제거
function removeItem(cartItem) {
    cartItem.remove();
    updateGrandTotal();

    // 장바구니가 비었는지 확인
    const cartContainer = document.getElementById('cartContainer');
    if (cartContainer.children.length === 0) {
        cartContainer.innerHTML = '<p class="empty-cart">장바구니가 비어있습니다.</p>';
        document.getElementById('purchasebutton').style.backgroundColor = '#ccc';
        document.getElementById('purchasebutton').style.cursor = 'not-allowed';
    }
}

// 장바구니에 상품 추가
function addToCart(productInfo) {
    const cartContainer = document.getElementById('cartContainer');

    // 비어있는 장바구니 메시지 제거
    const emptyCart = cartContainer.querySelector('.empty-cart');
    if (emptyCart) {
        emptyCart.remove();
    }

    const cartItem = document.createElement('div');
    cartItem.className = 'cart-item';
    cartItem.innerHTML = `
        <img src="${productInfo.image}" alt="${productInfo.name}">
        <div class="cart-details">
            <p><strong>${productInfo.name}</strong></p>
            <p>개당 가격: <span class="unit-price">${productInfo.price.toLocaleString()}</span>원</p>
        </div>
        <div class="quantity-control">
            <span class="quantity-btn" onclick="decreaseQuantity(this)">-</span>
            <span class="quantity">1</span>
            <span class="quantity-btn" onclick="increaseQuantity(this)">+</span>
        </div>
        <div class="total-price">
            총 금액: <span class="item-total">${productInfo.price.toLocaleString()}</span>원
        </div>
        <button class="remove-item" onclick="removeItem(this.parentElement)">×</button>
    `;

    cartContainer.appendChild(cartItem);
    updateGrandTotal();

    // 구매하기 버튼 활성화
    document.getElementById('purchasebutton').style.backgroundColor = '#006633';
    document.getElementById('purchasebutton').style.cursor = 'pointer';
}

// 구매하기
function checkout() {
    const cartItems = document.querySelectorAll('.cart-item');
    if (cartItems.length === 0) {
        alert('장바구니가 비어있습니다.');
        return;
    }

    // 장바구니 상품 정보 수집
    const items = [];
    cartItems.forEach(item => {
        items.push({
            name: item.querySelector('.cart-details strong').textContent,
            quantity: parseInt(item.querySelector('.quantity').textContent),
            price: parseInt(item.querySelector('.unit-price').textContent.replace(',', ''))
        });
    });

    // 로컬 스토리지에 장바구니 정보 저장
    localStorage.setItem('cartItems', JSON.stringify(items));

    // 구매 페이지로 이동
    window.location.href = 'purchase_product.html';
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function () {
    // 저장된 장바구니 정보가 있다면 복원
    const savedCart = localStorage.getItem('cartItems');
    if (savedCart) {
        const items = JSON.parse(savedCart);
        items.forEach(item => {
            addToCart({
                name: item.name,
                price: item.price,
                image: 'default-product-image.png' // 기본 이미지 경로
            });
        });
    }

    // 초기 총액 계산
    updateGrandTotal();
});
