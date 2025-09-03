// 회원가입 버튼 이벤트 핸들러
document.addEventListener('DOMContentLoaded', function () {
  // id가 'signup-form'인 요소를 찾습니다.
  const signupForm = document.getElementById('signup-form');

  // 만약 signupForm이 존재한다면,
  if (signupForm) {
    // 폼에서 'submit' 이벤트가 발생했을 때(버튼 클릭 시) 실행될 함수를 등록합니다.
    signupForm.addEventListener('submit', function (event) {
      // 1. 브라우저의 기본 폼 제출 동작(페이지 새로고침)을 막습니다.
      event.preventDefault();

      // 2. 폼 데이터를 FormData 객체로 쉽게 가져옵니다.
      const formData = new FormData(this);

      // 3. fetch API를 사용해 백그라운드에서 서버로 데이터를 보냅니다.
      fetch(this.action, {
        method: this.method,
        body: formData,
      })
        .then((response) => response.json()) // 4. 서버로부터 받은 응답을 JSON 형태로 파싱합니다.
        .then((data) => {
          // 5. 서버가 보내준 JSON 데이터를 처리합니다.
          if (data.result === 'success') {
            // 성공했다면,
            alert('회원가입에 성공했습니다! 로그인 페이지로 이동합니다.');
            // 'auth.login_page'로 리다이렉트합니다. data.redirect_url을 사용합니다.
            window.location.href = data.redirect_url;
          } else {
            // 실패했다면 (예: 아이디 중복 등),
            alert(data.msg || '회원가입 중 오류가 발생했습니다.');
          }
        })
        .catch((error) => {
          // 6. 네트워크 오류 등 fetch 자체에 문제가 생겼을 때 처리합니다.
          console.error('Error:', error);
          alert('요청 처리 중 심각한 오류가 발생했습니다.');
        });
    });
  }
});

// 로그인 버튼 이벤트 핸들러
document.addEventListener('DOMContentLoaded', function () {
  
  // --- 1. 회원가입 폼 처리 (기존 코드) ---
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const formData = new FormData(this);
      fetch(this.action, {
        method: this.method,
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.result === 'success') {
            alert('회원가입에 성공했습니다! 로그인 페이지로 이동합니다.');

            // [가장 중요한 수정]
            // 서버가 알려준 ID를 URL에 꼬리표로 붙여서 이동합니다.
            // 예: /?id=68b71902c2592ccd641f586b
            // const destinationUrl = data.redirect_url + '?id=' + data.user_db_id;
            // window.location.href = destinationUrl;
            // window.location.href = data.redirect_url;
          } else {
            alert(data.msg || '회원가입 중 오류가 발생했습니다.');
          }
        })
        .catch((error) => console.error('Error:', error));
    });
  }

  // --- 2. 로그인 폼 처리 (새로 추가된 코드) ---
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      // 기본 폼 제출(새로고침) 방지
      event.preventDefault();

      const formData = new FormData(this);

      fetch(this.action, {
        method: this.method,
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // 서버로부터 받은 응답 처리
          if (data.result === 'success') {
            // 성공 시
            alert('로그인에 성공했습니다! 메인 페이지로 이동합니다.');
            // [가장 중요한 수정]
            // 서버가 알려준 ID를 URL에 꼬리표로 붙여서 이동합니다.
            // 예: /?id=68b71902c2592ccd641f586b

          } else {
            // 실패 시
            alert(data.msg); // 서버가 보내준 실패 메시지 보여주기
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('요청 처리 중 오류가 발생했습니다.');
        });
    });
  }
});

