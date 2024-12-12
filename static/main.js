//스위치를 위한 js
function showSwitch() {
    $.ajax({
        type: 'GET',
        url: '/switch',
        data: {},
        success: function (response) {
            let status = response['status'];
            if (status == "product") {
                $("#switch").attr("onclick", "toService()");
            }
            else {
                $("#switch").attr("onclick", "toProduct()");
            }
        }
    });
}
function toService() {
    $.ajax({
        type: 'POST',
        url: '/toService',
        data: {
            status: "service"
        },
        success: function (response) {
            alert(response['msg'])
            window.location.href="/main.html";
        }
    });
}
function toProduct() {
    $.ajax({
        type: 'POST',
        url: '/toProduct',
        data: {
            status: "product"
        },
        success: function (response) {
            alert(response['msg'])
            window.location.href="/main.html";
        }
    });
}
$(document).ready(function () {
    showSwitch();
});

//민하님 js
/*
document.getElementById('quantity').addEventListener('input', function () {
    const quantity = parseInt(this.value, 10) || 0;
    const total = quantity * 10000;
    document.getElementById('result').innerText = `수량: ${quantity}, 총액: ${total.toLocaleString()}원`;
});

if (document.getElementById('quantity')) {
    document.getElementById('quantity').dispatchEvent(new Event('input'));
}*/

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

//소윤님 js
// 카테고리 옵션 업데이트 함수
function updateCategoryOptions(obj) {
    const categories = {
        first: [],
        product: ["식품", "공예", "뷰티", "패션", "기타 제품", "제품 제작 의뢰"],
        service: ["어학", "IT", "취미", "디자인", "첨삭", "생활", "기타"]
    };
    const productType = $(obj).val(); // 제품 유형 선택
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

document.getElementById('images').addEventListener('change', function (event) {
    const previewContainer = document.getElementById('imagePreviewContainer');
    previewContainer.innerHTML = ''; // 이전 미리보기 초기화

    const files = event.target.files;
    Array.from(files).forEach((file) => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.width = '100px'; // 미리보기 이미지 크기
            img.style.margin = '5px';
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
});

//1204 추가
/*const imageInput = document.getElementById("image-input");
const cameraBox = document.getElementById("camera-box");
const previewContainer = document.getElementById("image-preview-container");

// 업로드된 이미지를 추적하기 위한 배열
let uploadedImages = [];

// 카메라 박스를 클릭하면 파일 입력 창 열기
cameraBox.addEventListener("click", () => {
    imageInput.click();
});

// 파일 선택 시 처리
imageInput.addEventListener("change", (event) => {
    const files = Array.from(event.target.files);

    // 이미 5장 이상의 이미지가 업로드된 경우 추가 불가
    if (uploadedImages.length + files.length > 5) {
        alert("최대 5장의 이미지만 업로드할 수 있습니다.");
        return;
    }

    // 파일 읽기 및 미리보기 생성
    files.forEach((file) => {
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.src = e.target.result;
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
            uploadedImages.push(file);
        }
    });

    // 파일 입력 초기화 (같은 파일을 다시 선택할 수 있도록)
    event.target.value = "";
});*/

/*//1206 추가
// 파일 등록 버튼 클릭 시 파일 선택 창 열기
document.getElementById("file-upload-button").addEventListener("click", function () {
    document.getElementById("image-input").click();
});

// 파일 선택 후 미리보기 추가
// 파일 등록 버튼 클릭 시 파일 선택 창 열기
document.getElementById("file-upload-button").addEventListener("click", function (event) {
    event.preventDefault(); // 기본 동작(폼 제출) 방지
    document.getElementById("image-input").click();
});

// 파일 선택 후 미리보기 추가
document.getElementById("image-input").addEventListener("change", function (event) {
    const files = event.target.files; // 선택된 파일들
    const previewContainer = document.getElementById("image-preview-container");

    // 파일 각각에 대해 미리보기 생성
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement("img");
            img.src = e.target.result; // 이미지 소스 설정
            img.className = "image-preview-item"; // 클래스 추가
            previewContainer.appendChild(img); // 컨테이너에 이미지 추가
        };
        reader.readAsDataURL(file); // 파일 읽기
    });

    // 파일 입력 필드 초기화 (같은 파일 선택 가능하도록)
    event.target.value = "";
});*/



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


//장바구니 삭제버튼
function deleteItem(button) {
    // 현재 버튼과 연결된 cart-item을 삭제
    const cartItem = button.closest('.cart-item');
    cartItem.remove();

    // 장바구니 총 금액 업데이트
    updateGrandTotal();
}

function updateGrandTotal() {
    let grandTotal = 0;
    const itemTotals = document.querySelectorAll('.item-total');

    // 모든 아이템의 총 금액 합산
    itemTotals.forEach(item => {
        grandTotal += parseInt(item.textContent.replace(/,/g, ''), 10);
    });

    // 총 금액 업데이트
    document.getElementById('grandTotal').textContent = grandTotal.toLocaleString() + '원';
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

//댓글 등록 js
