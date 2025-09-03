// modal 함수 추가 
function  showModal(title, message) 
{
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const modalMessage = document.getElementById("modal-message");
  const closeBtn = document.getElementById("close-modal");

  modalTitle.textContent = title;
  modalMessage.textContent = message;

  modal.classList.remove("hidden");

  closeBtn.onclick = () => {
    modal.classList.add("hidden");
  };

}

// 토큰 만료 시 자동 로그인 페이지 이동 함수
function checkTokenExpiration() {
  // 현재 페이지가 로그인/회원가입 페이지가 아닌 경우에만 토큰 확인
  const currentPath = window.location.pathname;
  if (currentPath.includes('/auth/login') || currentPath.includes('/auth/signup')) {
    return;
  }
  
  fetch('/quiz/api/auth/check')
    .then(response => response.json())
    .then(data => {
      if (data.result === 'fail') {
        // 토큰이 만료되었거나 유효하지 않은 경우
        if (data.msg === '로그인 시간이 만료되었습니다.' || 
            data.msg === '유효하지 않은 토큰입니다.' ||
            data.msg === '존재하지 않는 사용자입니다.' ||
            data.msg === '로그인이 필요합니다.') {
          alert(data.msg);
          window.location.href = '/auth/login';
        }
      }
    })
    .catch(error => {
      console.error('토큰 확인 중 오류:', error);
    });
}

// 인증 실패 시 공통 처리 함수
function handleAuthFailure(data) {
  if (data.result === 'fail' && data.redirect_url) {
    alert(data.msg);
    window.location.href = data.redirect_url;
  }
}

// fetch 요청에 인증 실패 처리 추가
function fetchWithAuth(url, options = {}) {
  return fetch(url, options)
    .then(response => response.json())
    .then(data => {
      if (data.result === 'fail' && data.redirect_url) {
        handleAuthFailure(data);
        return Promise.reject(data);
      }
      return data;
    });
}

// 회원가입과 로그인 폼 처리
document.addEventListener('DOMContentLoaded', function () {
  
  // 페이지 로드 시 토큰 상태 확인
  checkTokenExpiration();
  
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
            showModal("✅ 회원가입 성공", "회원가입에 성공했습니다! 로그인 페이지로 이동합니다.");
            setTimeout(() => {
              window.location.href = data.redirect_url;
            }, 2000)
          } else {
            showModal("❌ 회원가입 실패", data.msg || "회원가입 중 오류가 발생했습니다.");
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          showModal("🚨 오류 발생", "요청 처리 중 심각한 오류가 발생했습니다.");
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
            showModal("🔑 로그인 성공", "로그인에 성공했습니다. 메인 페이지로 이동합니다.");
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