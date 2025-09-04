document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalMessage = document.getElementById("modal-message");
    const submitBtn = document.getElementById("submit-btn");
    const closeBtn = document.getElementById("close-modal");
    const input = document.querySelector("input[type=text]");

    submitBtn.addEventListener("click", () => {
        const userAnswer = input.value.trim();
        if (userAnswer == correctName)
        { 
            modalTitle.textContent = "🎉 정답입니다!";
            modalMessage.innerHTML = `${correctName}님을 맞추셨습니다!<br>두 분은 식사를 합시다!!`;
            $.get('/user/api/me', function (me) {
                if (me.result !== 'success') 
                    return (location.href = '/auth/login');

                $.post('/quiz/api/quiz_solved', {
                    _targetId: targetId,    
                    _solverId: me.userId
                });
            });
        }
        else
        {
            modalTitle.textContent = "❌ 오답입니다";
            modalMessage.textContent = "다시 시도해 보세요!";
        }
        modal.classList.remove("hidden");
    });

    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden"); 
    });
  });