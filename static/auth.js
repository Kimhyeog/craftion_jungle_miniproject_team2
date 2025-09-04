// modal 함수 추가 
function  showModal(title, message) 
{
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const modalMessage = document.getElementById("modal-message");
  const closeBtn = document.getElementById("close-modal");

  modalTitle.textContent = title;
  modalMessage.innerHTML = message;

  modal.classList.remove("hidden");

  closeBtn.onclick = () => {
    modal.classList.add("hidden");
  };

}

// 회원가입과 로그인 폼 처리
document.addEventListener('DOMContentLoaded', function () {
  
  // --- 1. 회원가입 폼 처리 ---
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    // 중복 제출 방지를 위한 플래그
    let isSubmitting = false;
    
    signupForm.addEventListener('submit', function (event) {
      // 기본 폼 제출(새로고침) 방지
      event.preventDefault();
      
      // 이미 제출 중이면 중단
      if (isSubmitting) {
        return;
      }
      
      // 제출 상태로 설정
      isSubmitting = true;
      
      // 버튼 비활성화
      const submitButton = this.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = '처리 중...';
      
      const formData = new FormData(this);
      
      fetch(this.action, {
        method: this.method,
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.result === 'success') {
            showModal("✅ 회원가입 성공", "회원가입에 성공했습니다!<br>로그인 페이지로 이동합니다.");
            setTimeout(() => {
              window.location.href = data.redirect_url;
            }, 2000)
          } else {
            showModal("❌ 회원가입 실패", data.msg || "회원가입 중 오류가 발생했습니다.");
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          showModal("🚨 오류 발생", "이미 등록된 아이디입니다.");
        })
        .finally(() => {
          // 제출 상태 초기화
          isSubmitting = false;
          
          // 버튼 다시 활성화
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        });
    });
  }

  // --- 2. 로그인 폼 처리 ---
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    // 중복 제출 방지를 위한 플래그
    let isLoggingIn = false;
    
    loginForm.addEventListener('submit', function (event) {
      // 기본 폼 제출(새로고침) 방지
      event.preventDefault();
      
      // 이미 로그인 중이면 중단
      if (isLoggingIn) {
        return;
      }
      
      // 로그인 상태로 설정
      isLoggingIn = true;
      
      // 버튼 비활성화
      const submitButton = this.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = '로그인 중...';
      
      const formData = new FormData(this);
      
      fetch(this.action, {
        method: this.method,
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.result === 'success') {
            showModal("🔑 로그인 성공", "로그인에 성공했습니다.<br>메인 페이지로 이동합니다.");
            const destinationUrl = data.redirect_url + '?id=' + data.user_db_id;
            setTimeout(() => {
              window.location.href = destinationUrl;
            }, 2000)
          } else {
            showModal("❌ 로그인 실패", data.msg);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          showModal("🚨 오류 발생", "요청 처리 중 오류가 발생했습니다.");
        })
        .finally(() => {
          // 로그인 상태 초기화
          isLoggingIn = false;
          
          // 버튼 다시 활성화
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        });
    });
  }
});