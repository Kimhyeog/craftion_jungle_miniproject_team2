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

document.addEventListener('DOMContentLoaded', function () {
  
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    let isSubmitting = false;
    
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();
      
      if (isSubmitting) {
        return;
      }
      
      isSubmitting = true;
      
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
          isSubmitting = false;
          
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        });
    });
  }

  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    let isLoggingIn = false;
    
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();
      
      if (isLoggingIn) {
        return;
      }
      
      isLoggingIn = true;
      
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
          isLoggingIn = false;
          
          submitButton.disabled = false;
          submitButton.textContent = originalText;
        });
    });
  }
});