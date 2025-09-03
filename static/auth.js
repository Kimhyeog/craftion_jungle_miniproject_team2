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
            alert('회원가입에 성공했습니다! 로그인 페이지로 이동합니다.');
            window.location.href = data.redirect_url;
          } else {
            alert(data.msg || '회원가입 중 오류가 발생했습니다.');
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('이미 존재하는 아이디 입니다.');
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
            alert('로그인에 성공했습니다! 메인 페이지로 이동합니다.');
            const destinationUrl = data.redirect_url + '?id=' + data.user_db_id;
            window.location.href = destinationUrl;
          } else {
            alert(data.msg || '로그인에 실패했습니다.');
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('요청 처리 중 오류가 발생했습니다.');
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