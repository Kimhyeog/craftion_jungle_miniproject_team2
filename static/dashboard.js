document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalMessage = document.getElementById("modal-message");
    const submitBtn = document.getElementById("submit-btn");
    const closeBtn = document.getElementById("close-modal");
    const input = document.querySelector("input[type=text]"); // input 태그 중에서 type="text"인 거 하나 가져오기

    submitBtn.addEventListener("click", () => {
        const userAnswer = input.value.trim(); // trim ->공백 잘라냄
        if (userAnswer == correctName)
        { // 맞추면 이제 안보이게 해야하는데 이걸 어떻게 할지 
            modalTitle.textContent = "🎉 정답입니다!";
            modalMessage.innerHTML = `${correctName}님을 맞추셨습니다!<br>두 분은 식사를 합시다!!`;
            $.get('/user/api/me', function (me) {
                if (me.result !== 'success') 
                    return (location.href = '/auth/login');

                // 2) 정답 기록
                $.post('/quiz/api/quiz_solved', {
                    _targetId: targetId,     // 전역에서 주입되어 있어야 함
                    _solverId: me.userId
                });
            });
        }
        else
        {
            modalTitle.textContent = "❌ 오답입니다";
            modalMessage.textContent = "다시 시도해 보세요!";
        }
        modal.classList.remove("hidden"); // 모달 보이기
    });

    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden"); // 모달 숨기기
    });
  });